---
name: inventory-data-access
description: Query the Enable the Disabled account/asset inventory sheets.
version: 0.1.0
author: fitness-strategist
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: enable-the-disabled
    tags: [google-sheets, inventory, account-lookup, security-posture, shau kehoe]
    related_skills: [productivity/google-workspace, drive-structure-navigation]
---

# Inventory Data Access Skill — Enable the Disabled

## When to Use
- You need to check whether an online account has MFA enabled.
- You need to find what password manager stores a particular login.
- You need to verify whether a backup exists for a specific asset.
- You need to look up the recovery method for an email or platform account.
- You need to list all physical assets assigned to a specific person.
- You need to audit security posture across all accounts (e.g., "which accounts have no MFA?").

## Prerequisites
- Google Sheets API auth for the `fitness-strategist` profile (same token as `google-workspace` skill).
- The inventory Sheet ID: `1H5VapzupQpUiXrviu1cmrukEnNWCFJu84VptwMRqolQ`
- Reference: `documents/security-inventory/drive-structure.md` for folder context.
- Reference: `documents/security-inventory/README.md` for column definitions.

## Inventory Sheet Structure

The master Google Sheet has 3 tabs. Template CSVs mirror these in the repo:

| Tab Name | CSV Mirror | Purpose |
|----------|------------|---------|
| `Account Security Inventory` | `account-security-inventory.csv` | Online accounts (emails, logins) |
| `Application Platforms` | `application-platforms-inventory.csv` | Software platforms/tools the business uses |
| `Physical Assets` | `physical-assets-inventory.csv` | Hardware, equipment, physical items |

## Quick Reference

### Read all rows from a tab
```python
values = sheets.spreadsheets().values().get(
    spreadsheetId=INVENTORY_SHEET_ID,
    range='Account Security Inventory!A2:L'  # A2 = header row is row 1
).execute()
rows = values.get('values', [])
```

### Query by column value (e.g., "all accounts without MFA")
```python
# Get all rows, then filter in Python
rows = get_all_rows('Account Security Inventory')
unsecured = [r for r in rows if r[7].lower() != 'yes']  # Column H = "MFA Enabled"
```

## Procedure

### 1. Identify which tab(s) to query
| Need | Tab |
|------|-----|
| Email accounts or online logins | `Account Security Inventory` |
| Software tools (CRM, scheduling, payment processors) | `Application Platforms` |
| Physical items (equipment, laptops, phones) | `Physical Assets` |
| Security posture audit (MFA, backups, password manager) | `Account Security Inventory` + `Application Platforms` |

### 2. Use the column index map to write precise queries
The columns differ slightly between Tab 1 and Tab 2:

**Tab 1 — Account Security Inventory** (`account-security-inventory.csv`):
| Index | Column |
|-------|--------|
| 0 | Service Name |
| 1 | Login URL |
| 2 | Email/User ID |
| 3 | Why (Purpose) |
| 4 | When (Use Case) |
| 5 | Backup Available? |
| 6 | Backup Details |
| 7 | MFA Enabled |
| 8 | MFA Method |
| 9 | Password Manager |
| 10 | Owner |
| 11 | Notes |

**Tab 2 — Application Platforms** (`application-platforms-inventory.csv`):
| Index | Column |
|-------|--------|
| 0 | Platform Name |
| 1 | Description |
| 2 | Purpose |
| 3 | Access URL |
| 4 | Who Has Access |
| 5 | Login URL |
| 6 | Backup Available? |
| 7 | Backup Details |
| 8 | MFA Enabled |
| 9 | MFA Method |
| 10 | Owner |
| 11 | Notes |

**Tab 3 — Physical Assets** (`physical-assets-inventory.csv`):
| Index | Column |
|-------|--------|
| 0 | Item |
| 1 | Description |
| 2 | Purpose/Benefit |
| 3 | Value |

### 3. Run the query via the Google Sheets API
Use the Python helper script at `documents/security-inventory/scripts/inventory_query.py`:

```bash
# List all accounts without MFA
python3 documents/security-inventory/scripts/inventory_query.py --tab accounts --no-mfa

# Find all accounts using a specific password manager
python3 documents/security-inventory/scripts/inventory_query.py --tab accounts --password-manager "1Password"

# Find an account by service name
python3 documents/security-inventory/scripts/inventory_query.py --tab accounts --search "QuickBooks"

# List all physical assets
python3 documents/security-inventory/scripts/inventory_query.py --tab assets --list

# Security posture audit (prints accounts without MFA or backup)
python3 documents/security-inventory/scripts/inventory_query.py --audit
```

### 4. Query the CSV mirrors (offline / no auth needed)
If you only need to reference the template structure (not live data), read the CSV files directly:
```bash
read_file documents/security-inventory/account-security-inventory.csv
read_file documents/security-inventory/application-platforms-inventory.csv
read_file documents/security-inventory/physical-assets-inventory.csv
```

### 5. Update a cell (requires Eric approval for production changes)
```python
# After getting user approval, update a single cell
sheets.spreadsheets().values().update(
    spreadsheetId=INVENTORY_SHEET_ID,
    range=f'{tab_name}!H{row_number}',  # e.g., 'Account Security Inventory!H5'
    valueInputOption='RAW',
    body={'values': [['Yes']]}
).execute()
```

## Security Posture Queries (Common Patterns)

| What you need | How to query |
|---------------|-------------|
| All accounts without MFA | Filter Tab 1 + Tab 2 where "MFA Enabled" is not "Yes" |
| All accounts with no backup | Filter where "Backup Available?" is not "Yes" |
| Which password manager each account uses | Column 9 (Password Manager) across both tabs |
| All accounts owned by a specific person | Filter Column 10 (Owner) = person's name |
| All assets with no backup | Tab 1 + Tab 2, filter "Backup Available?" |
| MFA methods in use | Tab 1 + Tab 2, Column 8 (MFA Method) — distinct values |

## Pitfalls
- **Row 1 is always headers** — data starts at row 2. If the sheet was manually edited and row 1 got cleared, re-apply headers from the CSV templates.
- **Empty rows** — Google Sheets returns `[]` for completely empty rows. Filter them out before processing.
- **Tab names matter** — the API requires exact tab names: `Account Security Inventory`, `Application Platforms`, `Physical Assets`.
- **CSV mirrors are templates only** — they contain the header row and empty data rows. Live data is in the Google Sheet.
- **Shaun may enter "Yes"/"No" or "yes"/"no"** — queries should be case-insensitive.
- **Do not update live inventory cells without Eric's approval** — these are Shaun's records.

## Verification
- After creating a query script, run it against the live sheet and confirm at least the header row matches.
- After any update, re-read the cell to confirm the value was written correctly.
- When adding a new account/platform, verify it appears in the audit query results.
