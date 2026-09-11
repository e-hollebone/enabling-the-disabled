#!/usr/bin/env python3
"""
md_to_gdoc.py — Convert markdown to properly formatted Google Docs.

Approach: Convert markdown → HTML (with CSS styling), then import HTML
into Google Docs via Drive API. For existing docs, update content in-place
preserving the doc ID and location. For new docs, create in the correct folder.

Usage:
  python3 md_to_gdoc.py --convert            # Convert .md files from Drive
  python3 md_to_gdoc.py --update-readmes     # Reformat README docs from repo markdown
  python3 md_to_gdoc.py --convert --delete-md  # Convert then delete original .md files
  python3 md_to_gdoc.py --dry-run --update-readmes  # Preview without changes
"""

import os
import re
import markdown
import argparse
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


# ─── Configuration ───────────────────────────────────────────────────────────

TOKEN_PATH = "/home/hermes/.hermes/profiles/fitness-strategist/google_token.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]
REPO_ROOT = "/home/hermes/enabling-the-disabled"

# Folder IDs (from Drive folder structure)
FOLDER_SHAUN = "17Sav0cJmDafe8DDvHKKq0OT1awzQ0ik8"
FOLDER_ADMIN = "1_YpciYU1uRS53ol74oqojUKlUKSQF4BJ"
FOLDER_NAME_SEARCH = "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G"
FOLDER_INC = "1w2On6DibxG5z0REfgLoBYUEkERwkgSAU"
FOLDER_BRAND = "1A45rdYzyLYudsjQEBEm5FcXUDf6198ys"
FOLDER_CORP_SHARED = "1dRr76f_xiGQvmnaAAMmSf1IjYhlNeT-O"
FOLDER_CORP_ADMIN = "1tH7rTwRGkjaj8KrZheNAkyLBSEkCdM4x"
FOLDER_OPS = "1wgqw4-IReNIMFov73r5DCEpvt7Mm9q1y"
FOLDER_ARCHIVE = "1cezQT8LdBg8Z_YTLdSH1Sgsc2gKdmZHO"
FOLDER_TRADEMARK = "1omvZoaW1v63lMHFEgrNcxI4e8xtpaTR8"
FOLDER_FACTFINDING = "1reMboKf5TezQWDZ9E55H7v3LyxelA5oH"
FOLDER_CLIENTS = "1H0dGCPgf3tT8bYDCp9prGWJT9ub9fgIt"
FOLDER_HR = "1Y-mz3Dqsd1rBcY6lohx4cTNYefETcqW3"
FOLDER_IT = "1gNcp_RPinZ2ofaSnf5cE2URko-Q3AR1z"
FOLDER_SEC = "1oTb65y2-xWLmNGa5nZoMYqHqOdiZY_uB"
FOLDER_OTHER = "1WagBxHIuwam9jXlUTN5Ejm0TxSktkFaz"

# REGISTRY: maps human-readable names to (file_id, type) tuples
# type is "doc", "sheet", or "folder"
REGISTRY = {
    # ── Folders ──
    "Enable the Disabled - Shaun Kehoe": (FOLDER_SHAUN, "folder"),
    "Enable the Disabled - Admin": (FOLDER_ADMIN, "folder"),
    "Brand": (FOLDER_BRAND, "folder"),
    "Corporate": (FOLDER_CORP_SHARED, "folder"),
    "Corporate (Admin)": (FOLDER_CORP_ADMIN, "folder"),
    "Operations": (FOLDER_OPS, "folder"),
    "00_Fact-finding": (FOLDER_FACTFINDING, "folder"),
    "07_Incorporation": (FOLDER_INC, "folder"),
    "08_Trademark": (FOLDER_TRADEMARK, "folder"),
    "name search": (FOLDER_NAME_SEARCH, "folder"),
    "01_Clients": (FOLDER_CLIENTS, "folder"),
    "02_HR-Workforce": (FOLDER_HR, "folder"),
    "03_Operations": ("1PV6qMwgnj9ATjhWA9p9Tb0S9x4Bg1Hyb", "folder"),
    "04_IT-Infrastructure": (FOLDER_IT, "folder"),
    "08_Security (Shared)": (FOLDER_SEC, "folder"),
    "09_Other": (FOLDER_OTHER, "folder"),
    "_archive": (FOLDER_ARCHIVE, "folder"),
    # ── Docs ──
    "README - Enable the Disabled - Shaun Kehoe": ("1BaOpqPfrtpuVpLSqMA8-1ddFOWhKKBnTGzujw-nR5Ic", "doc"),
    "README - Brand": ("12b8To0UXajY1KcXlwcAsKMCsDEglkXfjS_MSUHCDtgk", "doc"),
    "README - Corporate (Shared)": ("1OLSXR8-OeudvLml7T864IZgFJf70NbJmW7qcDid5nig", "doc"),
    "README - Corporate (Admin)": ("1TNTy1BR1uqN_hrUqxhBl_eu8Py4GnUhvzccrnt0dHog", "doc"),
    "README - Operations": ("1jDIciLSh-JJneMl-jNcXeLwPsLk3X-U-LKCMWuuToOU", "doc"),
    "README - _archive": ("14QSII4ScsI86uVX1p96062VaE9kt4jLDnG4jSRtGVI0", "doc"),
    "README - 01_Clients": ("1zY4QxK2pgH5MxtUvVuAf122aCsX0Xn-B27c7I9kPak4", "doc"),
    "README - 02_HR-Workforce": ("1yu8DjUFxSQA_Ot3ekoVe_UavlV1flJRDb0JWJVPjbUI", "doc"),
    "README - 04_IT-Infrastructure": ("1cwQOSxEVWGMebSbyVs7rzHDlFD9A0_Wi2zSs_xvP70k", "doc"),
    "README - 08_Security (Admin)": ("1NBJAe5cyLBXcGiBkbzEuS-HHluagDOgg--CXyTMEcOg", "doc"),
    "README - 09_Other": ("1BLPl8ApzzCPnyfxdYKLfX4Ur-JKEjhijiyCnJ5GjKss", "doc"),
    "README - name search": ("1x7eV4FH5CN3AJ85j5gyJgYuz8Q8ZwSipdgoRrH-5RU0", "doc"),
    "README - Incorporation #1": ("1AQ4RGD4cwQlLL7GuYNJc1gNj417rzQETzKGbxEj9sUY", "doc"),
    "README - Incorporation #2": ("1K9RkjgeeXom1W-UohuSXE7RsKr0OWVSxekbrDhn60as", "doc"),
    "README - Trademark": ("1bQjhimpt5eWKn842tsGDFaPXVL2Hrl-D8kxA551lnBo", "doc"),
    "README - Enabling the Disabled - Admin": ("1jW2WRZCCawPC_unlYhnORZi2A2iLcPs4LztwP4LoP1o", "doc"),
    "README - Fact-finding": ("11dySxk8DaYA_NP0ss8RNsE0LWc3IwTvUj1hLIPnkZoo", "doc"),
    "Incorporation Checklist": ("1slb7W3DF-Tskrn_-QJMch0OKt8o27RUnmGAJZ5ntRlE", "doc"),
    # ── Sister Co Name Research docs ──
    "Sister Co Name Research - batch 01 (Doc)": ("18gze3n3KFKZdQb3DaYQpaph2nZ5N0_Pnb0aaaCqogrY", "doc"),
    "Sister Co Name Research - batch 02 (Doc)": ("10CzD5AEZsBeyjqE8xL2PQ3NGVKVugZN3B5sBL8djO2g", "doc"),
    "Sister Co Name Research - batch 03 (Doc)": ("1Iw6xUJ5ssXcXpNdF57xwyNYAtbCmXVTm70eEYlFQbKo", "doc"),
    "Sister Co Name Research - combined (Doc 1)": ("1Ia2KYJdhsEeJGaILJ6A6suM3cLDMMjyfIvkyVOsQgcU", "doc"),
    "Sister Co Name Research - combined (Doc 2)": ("1S-e72gT6v-Iv5FMgOb7xyWM_FwUkSE879o-mJivl7IA", "doc"),
    "README - 08_Security": ("1QDRTLVSB2haKrFbHCGpMvm3X316b2vyKhi41YPPLics", "doc"),
    # ── Sheets ──
    "Enable the Disabled - Account & Asset Inventory": ("1H5VapzupQpUiXrviu1cmrukEnNWCFJu84VptwMRqolQ", "sheet"),
}

# Repo source files for README docs: maps doc_id → repo file path
README_SOURCES = {
    "1BaOpqPfrtpuVpLSqMA8-1ddFOWhKKBnTGzujw-nR5Ic": "documents/security-inventory/folder-index/README-Shared-root.md",
    "1zY4QxK2pgH5MxtUvVuAf122aCsX0Xn-B27c7I9kPak4": "documents/security-inventory/folder-index/README-01-Clients.md",
    "1yu8DjUFxSQA_Ot3ekoVe_UavlV1flJRDb0JWJVPjbUI": "documents/security-inventory/folder-index/README-02-HR-Workforce.md",
    "1cwQOSxEVWGMebSbyVs7rzHDlFD9A0_Wi2zSs_xvP70k": "documents/security-inventory/folder-index/README-04-IT-Infrastructure.md",
    "12b8To0UXajY1KcXlwcAsKMCsDEglkXfjS_MSUHCDtgk": "documents/security-inventory/folder-index/README-Brand-Shared.md",
    "1OLSXR8-OeudvLml7T864IZgFJf70NbJmW7qcDid5nig": "documents/security-inventory/folder-index/README-Corporate-Shared.md",
    "1TNTy1BR1uqN_hrUqxhBl_eu8Py4GnUhvzccrnt0dHog": "documents/security-inventory/folder-index/README-Corporate-Admin.md",
    "11dySxk8DaYA_NP0ss8RNsE0LWc3IwTvUj1hLIPnkZoo": "documents/security-inventory/folder-index/README-Fact-Finding.md",
    "1jDIciLSh-JJneMl-jNcXeLwPsLk3X-U-LKCMWuuToOU": "documents/security-inventory/folder-index/README-Operations-Shared.md",
    "1x7eV4FH5CN3AJ85j5gyJgYuz8Q8ZwSipdgoRrH-5RU0": "documents/security-inventory/folder-index/README-Name-Search-Shared.md",
    "1QDRTLVSB2haKrFbHCGpMvm3X316b2vyKhi41YPPLics": "documents/security-inventory/folder-index/README-08-Security-Shared.md",
    "1NBJAe5cyLBXcGiBkbzEuS-HHluagDOgg--CXyTMEcOg": "documents/security-inventory/folder-index/README-08-Security-Admin.md",
    "1bQjhimpt5eWKn842tsGDFaPXVL2Hrl-D8kxA551lnBo": "documents/security-inventory/folder-index/README-Trademark-Shared.md",
    "14QSII4ScsI86uVX1p96062VaE9kt4jLDnG4jSRtGVI0": "documents/security-inventory/folder-index/README-Archive-Shared.md",
    "1AQ4RGD4cwQlLL7GuYNJc1gNj417rzQETzKGbxEj9sUY": "documents/security-inventory/folder-index/README-Incorporation-Shared-1.md",
    "1K9RkjgeeXom1W-UohuSXE7RsKr0OWVSxekbrDhn60as": "documents/security-inventory/folder-index/README-Incorporation-Shared-2.md",
    "1jW2WRZCCawPC_unlYhnORZi2A2iLcPs4LztwP4LoP1o": "documents/security-inventory/folder-index/README-Admin-root.md",
    "1slb7W3DF-Tskrn_-QJMch0OKt8o27RUnmGAJZ5ntRlE": "documents/security-inventory/folder-index/Incorporation_Checklist.md",
    "1BLPl8ApzzCPnyfxdYKLfX4Ur-JKEjhijiyCnJ5GjKss": "documents/security-inventory/folder-index/README-09-Other.md",
}

# Repo source files for combined/sister docs
MD_FILES = [
    {
        "name": "Sister Company Name Research - combined (Doc 1)",
        "parent_id": FOLDER_INC,
        "target_doc_id": "1Ia2KYJdhsEeJGaILJ6A6suM3cLDMMjyfIvkyVOsQgcU",
        "repo_path": "documents/security-inventory/folder-index/Sister_Company_Name_Research_combined_Doc1.md",
    },
    {
        "name": "Sister Co Name Research - combined (Doc 2)",
        "parent_id": FOLDER_NAME_SEARCH,
        "target_doc_id": "1S-e72gT6v-Iv5FMgOb7xyWM_FwUkSE879o-mJivl7IA",
        "repo_path": "documents/security-inventory/folder-index/Sister_Company_Name_Research_combined_Doc2.md",
    },
]

# Batch doc info: (name, parent_id, tmp_path, target_doc_id)
BATCH_DOCS = [
    ("Sister Co Name Research - batch 01", FOLDER_NAME_SEARCH, "/tmp/sister_batch01.md", "18gze3n3KFKZdQb3DaYQpaph2nZ5N0_Pnb0aaaCqogrY"),
    ("Sister Co Name Research - batch 02", FOLDER_NAME_SEARCH, "/tmp/sister_batch02.md", "10CzD5AEZsBeyjqE8xL2PQ3NGVKVugZN3B5sBL8djO2g"),
    ("Sister Co Name Research - batch 03", FOLDER_NAME_SEARCH, "/tmp/sister_batch03.md", "1Iw6xUJ5ssXcXpNdF57xwyNYAtbCmXVTm70eEYlFQbKo"),
]


# ─── Auth ────────────────────────────────────────────────────────────────────

def get_creds():
    """Load and refresh Google API credentials."""
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token
        with open(TOKEN_PATH, 'w') as f:
            f.write(creds.to_json())
    return creds


def get_services():
    """Build Drive service object."""
    creds = get_creds()
    return build("drive", "v3", credentials=creds)


# ─── Markdown → HTML ─────────────────────────────────────────────────────────

def md_to_html(md_text):
    """Convert markdown text to styled HTML for Google Docs import."""
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "nl2br"]
    )
    body_html = md.convert(md_text)

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
h1 {{ font-size: 24pt; font-weight: bold; margin: 12pt 0 6pt 0; }}
h2 {{ font-size: 18pt; font-weight: bold; margin: 10pt 0 5pt 0; }}
h3 {{ font-size: 14pt; font-weight: bold; margin: 8pt 0 4pt 0; }}
code {{ font-family: 'Courier New', monospace; font-size: 10pt; background-color: #f0f0f0; padding: 1px 3px; }}
pre {{ font-family: 'Courier New', monospace; font-size: 10pt; background-color: #f0f0f0; padding: 8px; }}
a {{ color: #1155cc; text-decoration: underline; }}
table {{ border-collapse: collapse; width: 100%; margin: 8pt 0; }}
th, td {{ border: 1px solid #ddd; padding: 4px 8px; }}
th {{ background-color: #f0f0f0; font-weight: bold; }}
ul, ol {{ margin: 4pt 0; padding-left: 24px; }}
p {{ margin: 6pt 0; }}
blockquote {{ border-left: 3px solid #ccc; padding-left: 12px; margin: 8pt 0; font-style: italic; }}
hr {{ border: 0; border-top: 1px solid #ccc; margin: 12pt 0; }}
</style>
</head>
<body>
{body_html}
</body>
</html>"""
    return html


# ─── Internal Link Replacement ───────────────────────────────────────────────

def replace_internal_links(md_text):
    """
    Replace backtick-wrapped names and file IDs in markdown text with
    markdown links pointing to the corresponding Google Drive files.

    Handles:
      - `Enable the Disabled - Shaun Kehoe` → [name](folder URL)
      - `17Sav0cJmDafe8DDvHKKq0OT1awzQ0ik8` → [ID](folder URL)

    The resulting markdown links are converted to HTML <a> tags by md_to_html,
    which Google Docs HTML import renders as clickable hyperlinks.
    """
    sorted_names = sorted(REGISTRY.keys(), key=len, reverse=True)
    for name in sorted_names:
        item_id, item_type = REGISTRY[name]
        if item_id is None or not isinstance(item_id, str):
            continue
        if item_type == "folder":
            url = f"https://drive.google.com/drive/folders/{item_id}"
        elif item_type == "doc":
            url = f"https://docs.google.com/document/d/{item_id}/edit"
        elif item_type == "sheet":
            url = f"https://docs.google.com/spreadsheets/d/{item_id}/edit"
        else:
            url = f"https://drive.google.com/file/d/{item_id}/view"

        # Use a sentinel to mark replaced links so file ID replacements
        # don't interfere with each other
        link_text = name if name else item_id
        replacement = f"__LINK_START__{name}__LINK_SEP__{url}__LINK_END__"

        # Replace backtick-wrapped file ID first (IDs are unique and
        # won't appear in URL strings)
        escaped_id = re.escape(item_id)
        md_text = re.sub(
            rf"\`({escaped_id})\`",
            replacement,
            md_text,
        )

        # Replace backtick-wrapped name (only if name differs from ID)
        if name and name != item_id:
            escaped_name = re.escape(name)
            md_text = re.sub(
                rf"\`({escaped_name})\`",
                replacement,
                md_text,
            )

    # Convert sentinel markers to markdown links
    md_text = re.sub(
        r"__LINK_START__(.+?)__LINK_SEP__(.+?)__LINK_END__",
        r"[\1](\2)",
        md_text,
    )

    return md_text


# ─── Doc Creation / Update ───────────────────────────────────────────────────

def import_html_to_doc(drive, html, title, parent_id=None, doc_id=None):
    """
    Import HTML content into a Google Doc.

    If doc_id is given: update the existing doc in-place (preserves ID
    and folder location). If doc_id is None or the doc doesn't exist,
    create a new doc in parent_id.
    """
    media = MediaIoBaseUpload(
        io.BytesIO(html.encode("utf-8")),
        mimetype="text/html",
    )

    if doc_id:
        try:
            drive.files().update(
                fileId=doc_id,
                media_body=media,
                fields="id",
            ).execute()
            return doc_id
        except Exception:
            pass  # Doc doesn't exist, fall through to create new

    body = {"name": title, "mimeType": "application/vnd.google-apps.document"}
    if parent_id:
        body["parents"] = [parent_id]
    result = drive.files().create(
        body=body, media_body=media, fields="id"
    ).execute()
    return result["id"]


def get_file_title(drive, file_id):
    """Get the title of a file."""
    try:
        meta = drive.files().get(fileId=file_id, fields="name").execute()
        return meta.get("name", "Untitled")
    except Exception:
        return None


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Convert markdown to Google Docs")
    parser.add_argument("--convert", action="store_true",
                        help="Convert .md files (batch docs from /tmp)")
    parser.add_argument("--update-readmes", action="store_true",
                        help="Reformat existing README Google Docs from repo markdown")
    parser.add_argument("--delete-md", action="store_true",
                        help="Delete original .md files after conversion (not used - .md files already deleted)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be converted without making changes")
    args = parser.parse_args()

    if not args.convert and not args.update_readmes:
        parser.print_help()
        return

    drive = get_services()

    # ── Step 1: Convert batch/sister docs ──
    if args.convert:
        print("=" * 60)
        print("STEP 1: Converting batch/sister docs")
        print("=" * 60)

        for name, parent_id, tmp_path, target_doc_id in BATCH_DOCS:
            print(f"\nProcessing: {name}")
            with open(tmp_path, "r") as f:
                md_text = f.read()
            print(f"  Source: {len(md_text)} chars from {tmp_path}")

            # Replace internal links
            md_text = replace_internal_links(md_text)
            # Convert to HTML
            html = md_to_html(md_text)
            print(f"  HTML: {len(html)} chars")

            if args.dry_run:
                print(f"  [DRY RUN] Would import as Google Doc")
                continue

            # Use target_doc_id from BATCH_DOCS for in-place update
            doc_id = import_html_to_doc(drive, html, name, parent_id, doc_id=target_doc_id)
            print(f"  Done: {doc_id}")

        # Also process combined docs (from repo markdown)
        for entry in MD_FILES:
            name = entry["name"]
            parent_id = entry["parent_id"]
            repo_path = entry["repo_path"]
            target_doc_id = entry.get("target_doc_id")

            print(f"\nProcessing: {name}")
            full_path = os.path.join(REPO_ROOT, repo_path)
            with open(full_path, "r") as f:
                md_text = f.read()
            print(f"  Source: {len(md_text)} chars from {repo_path}")

            md_text = replace_internal_links(md_text)
            html = md_to_html(md_text)
            print(f"  HTML: {len(html)} chars")

            if args.dry_run:
                print(f"  [DRY RUN] Would import as Google Doc")
                continue

            doc_id = import_html_to_doc(drive, html, name, parent_id, doc_id=target_doc_id)
            print(f"  Done: {doc_id}")

    # ── Step 2: Reformat README docs from repo markdown sources ──
    if args.update_readmes:
        print("\n" + "=" * 60)
        print("STEP 2: Reformatting README docs from repo markdown sources")
        print("=" * 60)

        for doc_id, repo_path in README_SOURCES.items():
            title = get_file_title(drive, doc_id)

            # Find the repo source file
            full_path = os.path.join(REPO_ROOT, repo_path)
            if not os.path.exists(full_path):
                print(f"\n  Skipping (no repo source): {title or doc_id}")
                continue

            with open(full_path, "r") as f:
                md_text = f.read()

            # If doc doesn't exist, find by name from REGISTRY
            if title is None:
                for reg_name, (rid, rtype) in REGISTRY.items():
                    if rid == doc_id:
                        title = reg_name
                        break
                if title is None:
                    title = "Untitled"

            print(f"\n  Processing: {title}")
            print(f"    Source: {len(md_text)} chars from {repo_path}")

            # Replace internal links in the markdown
            md_text = replace_internal_links(md_text)

            # Convert to HTML
            html = md_to_html(md_text)
            print(f"    HTML: {len(html)} chars")

            if args.dry_run:
                print(f"    [DRY RUN] Would reformat doc")
                continue

            # Update doc in-place with new HTML content
            new_id = import_html_to_doc(drive, html, title, doc_id=doc_id)
            print(f"    Reformatted: {title} → {new_id}")

            # Update REGISTRY with new doc ID (in case it was recreated)
            if title in REGISTRY:
                REGISTRY[title] = (new_id, "doc")

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
