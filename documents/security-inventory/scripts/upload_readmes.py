#!/usr/bin/env python3
"""
Upload folder README files as Google Docs to their corresponding Drive folders.
"""

import json
import os
import sys

TOKEN_PATH = os.path.expanduser("~/.hermes/profiles/fitness-strategist/google_token.json")

# Mapping: (repo_markdown_file, target_folder_id, doc_title)
UPLOADS = [
    # Admin tree
    ("documents/security-inventory/folder-index/README-Admin-root.md",
     "1_YpciYU1uRS53ol74oqojUKlUKSQF4BJ",  # Enable the Disabled - Admin
     "README - Enabling the Disabled - Admin"),

    ("documents/security-inventory/folder-index/README-Corporate-Admin.md",
     "1tH7rTwRGkjaj8KrZheNAkyLBSEkCdM4x",  # Admin > Corporate
     "README - Corporate"),

    ("documents/security-inventory/folder-index/README-08-Security-Admin.md",
     "14Ek0zgqHHpXuuBtoe7EJDRUwjpTRu_Iy",  # Admin > Corporate > 08_Security
     "README - 08_Security"),

    # Shared tree
    ("documents/security-inventory/folder-index/README-Shared-root.md",
     "17Sav0cJmDafe8DDvHKKq0OT1awzQ0ik8",  # Enable the Disabled - Shaun Kehoe
     "README - Enable the Disabled - Shaun Kehoe"),

    ("documents/security-inventory/folder-index/README-Corporate-Shared.md",
     "1dRr76f_xiGQvmnaAAMmSf1IjYhlNeT-O",  # Shared > Corporate
     "README - Corporate"),

    ("documents/security-inventory/folder-index/README-Fact-Finding.md",
     "1reMboKf5TezQWDZ9E55H7v3LyxelA5oH",  # Shared > Corporate > Fact-finding
     "README - Fact-finding"),

    ("documents/security-inventory/folder-index/README-Incorporation-Shared-1.md",
     "1w2On6DibxG5z0REfgLoBYUEkERwkgSAU",  # Shared > Corporate > Incorporation #1
     "README - Incorporation"),

    ("documents/security-inventory/folder-index/README-Incorporation-Shared-2.md",
     "1TxWJJfsh1rm0lFzBTxpyHA56eLp5ncm5",  # Shared > Corporate > Incorporation #2
     "README - Incorporation (second)"),

    ("documents/security-inventory/folder-index/README-Trademark-Shared.md",
     "1omvZoaW1v63lMHFEgrNcxI4e8xtpaTR8",  # Shared > Corporate > Trademark
     "README - Trademark"),

    ("documents/security-inventory/folder-index/README-Name-Search-Shared.md",
     "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",  # Shared > Corporate > Incorporation > name search
     "README - name search"),

    ("documents/security-inventory/folder-index/README-Operations-Shared.md",
     "1wgqw4-IReNIMFov73r5DCEpvt7Mm9q1y",  # Shared > Operations
     "README - Operations"),

    ("documents/security-inventory/folder-index/README-01-Clients.md",
     "1H0dGCPgf3tT8bYDCp9prGWJT9ub9fgIt",  # Shared > Operations > 01_Clients
     "README - 01_Clients"),

    ("documents/security-inventory/folder-index/README-02-HR-Workforce.md",
     "1Y-mz3Dqsd1rBcY6lohx4cTNYefETcqW3",  # Shared > Operations > 02_HR-Workforce
     "README - 02_HR-Workforce"),

    ("documents/security-inventory/folder-index/README-04-IT-Infrastructure.md",
     "1gNcp_RPinZ2ofaSnf5cE2URko-Q3AR1z",  # Shared > Operations > 04_IT-Infrastructure
     "README - 04_IT-Infrastructure"),

    ("documents/security-inventory/folder-index/README-08-Security-Shared.md",
     "1oTb65y2-xWLmNGa5nZoMYqHqOdiZY_uB",  # Shared > Operations > 08_Security
     "README - 08_Security"),

    ("documents/security-inventory/folder-index/README-09-Other.md",
     "1WagBxHIuwam9jXlUTN5Ejm0TxSktkFaz",  # Shared > Operations > 09_Other
     "README - 09_Other"),

    ("documents/security-inventory/folder-index/README-Archive-Shared.md",
     "1cezQT8LdBg8Z_YTLdSH1Sgsc2gKdmZHO",  # Shared > _archive
     "README - _archive"),

    ("documents/security-inventory/folder-index/README-Brand-Shared.md",
     "1A45rdYzyLYudsjQEBEm5FcXUDf6198ys",  # Shared > Brand
     "README - Brand"),
]


def upload_readme(md_path, folder_id, doc_title):
    """Upload a markdown file as a Google Doc to the specified folder."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload
    import io

    # Read the markdown content
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Convert markdown to plain text for Google Docs (Docs API accepts plain text)
    # For richer formatting, we could convert to HTML, but plain text is simpler
    # and scannable — which is the priority for Shaun.
    text_content = content

    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    drive = build("drive", "v3", credentials=creds)
    docs = build("docs", "v1", credentials=creds)

    # Create the Google Doc
    doc_body = {"title": doc_title}
    doc_create = docs.documents().create(body=doc_body).execute()
    doc_id = doc_create["documentId"]

    # Insert content into the doc
    # Clear default empty document and insert our text
    requests = [
        {
            "insertText": {
                "location": {"index": 1},  # Insert at the beginning (after the empty paragraph at index 0)
                "text": text_content,
            }
        }
    ]
    docs.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

    # Move the doc to the target folder
    drive.files().update(
        fileId=doc_id,
        addParents=folder_id,
        fields="id"
    ).execute()

    # Get the webViewLink
    file_meta = drive.files().get(fileId=doc_id, fields="webViewLink, name").execute()
    return file_meta


def main():
    base = os.path.expanduser("/home/hermes/enabling-the-disabled")
    results = []
    for md_rel, folder_id, title in UPLOADS:
        md_path = os.path.join(base, md_rel)
        try:
            meta = upload_readme(md_path, folder_id, title)
            results.append((title, folder_id, meta["webViewLink"]))
            print(f"✅ {title} → {meta['webViewLink']}")
        except Exception as e:
            results.append((title, folder_id, f"ERROR: {e}"))
            print(f"❌ {title} → ERROR: {e}")

    # Save results to JSON for reference
    results_path = os.path.join(base, "documents/security-inventory", "upload-results.json")
    with open(results_path, "w") as f:
        json.dump([
            {"title": t, "folder_id": f, "link": l}
            for t, f, l in results
        ], f, indent=2)
    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
