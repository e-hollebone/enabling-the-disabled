#!/usr/bin/env python3
"""
Inventory query tool for Enable the Disabled's Account & Asset Inventory Google Sheet.

Usage:
  python3 inventory_query.py --tab accounts --no-mfa
  python3 inventory_query.py --tab accounts --password-manager "1Password"
  python3 inventory_query.py --tab accounts --search "QuickBooks"
  python3 inventory_query.py --tab assets --list
  python3 inventory_query.py --audit
  python3 inventory_query.py --tab platforms --no-mfa
"""

import argparse
import json
import sys
import os

SHEET_ID = "1H5VapzupQpUiXrviu1cmrukEnNWCFJu84VptwMRqolQ"
TOKEN_PATH = os.path.expanduser("~/.hermes/profiles/fitness-strategist/google_token.json")

# Tab name → (range, column_indices)
# Column indices correspond to 0-based position in the header row
ACCOUNT_COLS = {
    "Service Name": 0, "Login URL": 1, "Email/User ID": 2,
    "Why (Purpose)": 3, "When (Use Case)": 4, "Backup Available?": 5,
    "Backup Details": 6, "MFA Enabled": 7, "MFA Method": 8,
    "Password Manager": 9, "Owner": 10, "Notes": 11,
}
PLATFORM_COLS = {
    "Platform Name": 0, "Description": 1, "Purpose": 2, "Access URL": 3,
    "Who Has Access": 4, "Login URL": 5, "Backup Available?": 6, "Backup Details": 7,
    "MFA Enabled": 8, "MFA Method": 9, "Owner": 10, "Notes": 11,
}
ASSET_COLS = {
    "Item": 0, "Description": 1, "Purpose/Benefit": 2, "Value": 3,
}

TAB_MAP = {
    "accounts": ("Account Security Inventory", ACCOUNT_COLS),
    "platforms": ("Application Platforms", PLATFORM_COLS),
    "assets": ("Physical Assets", ASSET_COLS),
}


def load_creds():
    if not os.path.exists(TOKEN_PATH):
        print(f"ERROR: No token at {TOKEN_PATH}")
        print("Run the Google Workspace setup first.")
        sys.exit(1)
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds


def get_sheet_data(creds, tab_name, max_cols=12):
    from googleapiclient.discovery import build
    sheets = build("sheets", "v4", credentials=creds)
    # Read all data rows (skip header at row 1)
    result = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"{tab_name}!A2:{chr(65+max_cols)}",
    ).execute()
    return result.get("values", [])


def pad_row(row, n):
    """Pad or truncate a row to exactly n columns."""
    row = list(row)
    while len(row) < n:
        row.append("")
    return row[:n]


def query_no_mfa(rows, cols):
    """Find rows where MFA Enabled is not 'Yes'."""
    mfa_idx = cols["MFA Enabled"]
    results = []
    for row in rows:
        if len(row) <= mfa_idx:
            results.append(row)
            continue
        if row[mfa_idx].strip().lower() != "yes":
            results.append(row)
    return results


def query_password_manager(rows, cols, pm_value):
    """Find rows where Password Manager matches."""
    pm_idx = cols["Password Manager"]
    target = pm_value.lower().strip()
    results = []
    for row in rows:
        if len(row) > pm_idx and row[pm_idx].strip().lower() == target:
            results.append(row)
    return results


def query_search(rows, cols, search_term):
    """Find rows where any cell contains the search term."""
    target = search_term.lower().strip()
    results = []
    for row in rows:
        if any(target in cell.lower() for cell in row):
            results.append(row)
    return results


def query_asset_list(rows, cols):
    """List all physical assets."""
    return rows


def format_account(row, cols):
    name = pad_row(row, 12)[cols["Service Name"]]
    email = pad_row(row, 12)[cols["Email/User ID"]]
    mfa = pad_row(row, 12)[cols["MFA Enabled"]]
    backup = pad_row(row, 12)[cols["Backup Available?"]]
    pm = pad_row(row, 12)[cols["Password Manager"]]
    owner = pad_row(row, 12)[cols["Owner"]]
    return f"  {name} | email: {email} | MFA: {mfa} | Backup: {backup} | PM: {pm} | Owner: {owner}"


def format_platform(row, cols):
    name = pad_row(row, 12)[cols["Platform Name"]]
    access = pad_row(row, 12)[cols["Who Has Access"]]
    mfa = pad_row(row, 12)[cols["MFA Enabled"]]
    backup = pad_row(row, 12)[cols["Backup Available?"]]
    owner = pad_row(row, 12)[cols["Owner"]]
    return f"  {name} | Access: {access} | MFA: {mfa} | Backup: {backup} | Owner: {owner}"


def format_asset(row, cols):
    item = pad_row(row, 4)[cols["Item"]]
    desc = pad_row(row, 4)[cols["Description"]]
    purpose = pad_row(row, 4)[cols["Purpose/Benefit"]]
    value = pad_row(row, 4)[cols["Value"]]
    return f"  {item} | {desc} | {purpose} | Value: {value}"


def main():
    parser = argparse.ArgumentParser(description="Query the Enable the Disabled inventory sheet.")
    parser.add_argument("--tab", choices=["accounts", "platforms", "assets"], required=False, default="accounts")
    parser.add_argument("--no-mfa", action="store_true", help="Show entries without MFA")
    parser.add_argument("--password-manager", metavar="PM", help="Filter by password manager (accounts only)")
    parser.add_argument("--search", metavar="TERM", help="Search for term in any cell")
    parser.add_argument("--list", action="store_true", help="List all rows (assets, or use --tab)")
    parser.add_argument("--audit", action="store_true", help="Full security posture audit across accounts + platforms")
    args = parser.parse_args()

    if args.audit:
        run_audit()
    else:
        tab_name, cols = TAB_MAP[args.tab]
        creds = load_creds()
        rows = get_sheet_data(creds, tab_name, max_cols=len(cols))

        if args.no_mfa:
            rows = query_no_mfa(rows, cols)
            print(f"=== {tab_name}: Entries WITHOUT MFA ({len(rows)} found) ===")
            if args.tab == "accounts":
                for r in rows:
                    print(format_account(r, cols))
            elif args.tab == "platforms":
                for r in rows:
                    print(format_platform(r, cols))
            else:
                print("  (N/A for assets tab)")
        elif args.password_manager:
            rows = query_password_manager(rows, cols, args.password_manager)
            print(f"=== {tab_name}: Password Manager = '{args.password_manager}' ({len(rows)} found) ===")
            if args.tab == "accounts":
                for r in rows:
                    print(format_account(r, cols))
            elif args.tab == "platforms":
                for r in rows:
                    print(format_platform(r, cols))
        elif args.search:
            rows = query_search(rows, cols, args.search)
            print(f"=== {tab_name}: Search '{args.search}' ({len(rows)} found) ===")
            if args.tab == "accounts":
                for r in rows:
                    print(format_account(r, cols))
            elif args.tab == "platforms":
                for r in rows:
                    print(format_platform(r, cols))
            elif args.tab == "assets":
                for r in rows:
                    print(format_asset(r, cols))
        elif args.list or True:
            if args.tab == "assets":
                rows = query_asset_list(rows, cols)
                print(f"=== Physical Assets ({len(rows)} found) ===")
                for r in rows:
                    if r:
                        print(format_asset(r, cols))
            else:
                print(f"=== {tab_name}: {len(rows)} entries ===")
                if args.tab == "accounts":
                    for r in rows:
                        if r:
                            print(format_account(r, cols))
                elif args.tab == "platforms":
                    for r in rows:
                        if r:
                            print(format_platform(r, cols))


def run_audit():
    """Audit all accounts + platforms for missing MFA, backups, or password manager."""
    creds = load_creds()
    account_tab, acc_cols = TAB_MAP["accounts"]
    platform_tab, plat_cols = TAB_MAP["platforms"]

    acc_rows = get_sheet_data(creds, account_tab, max_cols=len(acc_cols))
    plat_rows = get_sheet_data(creds, platform_tab, max_cols=len(plat_cols))

    print("=" * 60)
    print("SECURITY POSTURE AUDIT — Enable the Disabled")
    print("=" * 60)

    # --- Accounts without MFA ---
    no_mfa_acc = [r for r in acc_rows if len(r) <= acc_cols["MFA Enabled"] or r[acc_cols["MFA Enabled"]].strip().lower() != "yes"]
    print(f"\n[1] Online Accounts WITHOUT MFA: {len(no_mfa_acc)}")
    for r in no_mfa_acc:
        if r:
            row = pad_row(r, 12)
            print(f"  • {row[acc_cols['Service Name']]} ({row[acc_cols['Email/User ID']]})")

    # --- Platforms without MFA ---
    no_mfa_plat = [r for r in plat_rows if len(r) <= plat_cols["MFA Enabled"] or r[plat_cols["MFA Enabled"]].strip().lower() != "yes"]
    print(f"\n[2] Application Platforms WITHOUT MFA: {len(no_mfa_plat)}")
    for r in no_mfa_plat:
        if r:
            row = pad_row(r, 12)
            print(f"  • {row[plat_cols['Platform Name']]} (Access: {row[plat_cols['Who Has Access']]})")

    # --- Accounts without backup ---
    no_backup_acc = [r for r in acc_rows if len(r) <= acc_cols["Backup Available?"] or r[acc_cols["Backup Available?"]].strip().lower() != "yes"]
    print(f"\n[3] Online Accounts WITHOUT Backup: {len(no_backup_acc)}")
    for r in no_backup_acc:
        if r:
            row = pad_row(r, 12)
            print(f"  • {row[acc_cols['Service Name']]} ({row[acc_cols['Email/User ID']]})")

    # --- Platforms without backup ---
    no_backup_plat = [r for r in plat_rows if len(r) <= plat_cols["Backup Available?"] or r[plat_cols["Backup Available?"]].strip().lower() != "yes"]
    print(f"\n[4] Application Platforms WITHOUT Backup: {len(no_backup_plat)}")
    for r in no_backup_plat:
        if r:
            row = pad_row(r, 12)
            print(f"  • {row[plat_cols['Platform Name']]} (Access: {row[plat_cols['Who Has Access']]})")

    # --- Password managers in use ---
    pms = set()
    for r in acc_rows:
        if r:
            row = pad_row(r, 12)
            pm = row[acc_cols["Password Manager"]].strip()
            if pm:
                pms.add(pm)
    for r in plat_rows:
        if r:
            row = pad_row(r, 12)
            pm = row[plat_cols["Password Manager"]].strip()
            if pm:
                pms.add(pm)
    print(f"\n[5] Password Managers in use: {len(pms)}")
    for pm in sorted(pms):
        print(f"  • {pm}")

    # --- MFA methods in use ---
    methods = set()
    for r in acc_rows:
        if r:
            row = pad_row(r, 12)
            mfa = row[acc_cols["MFA Method"]].strip()
            if mfa:
                methods.add(f"Accounts: {mfa}")
    for r in plat_rows:
        if r:
            row = pad_row(r, 12)
            mfa = row[plat_cols["MFA Method"]].strip()
            if mfa:
                methods.add(f"Platforms: {mfa}")
    print(f"\n[6] MFA Methods in use: {len(methods)}")
    for m in sorted(methods):
        print(f"  • {m}")

    print("\n" + "=" * 60)
    print("Audit complete.")


if __name__ == "__main__":
    main()
