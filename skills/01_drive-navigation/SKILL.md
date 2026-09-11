---
name: drive-structure-navigation
description: Navigate the Enable the Disabled Drive/Repo folder structure.
version: 0.1.0
author: fitness-strategist
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: enable-the-disabled
    tags: [google-drive, folder-structure, repo-mirror, navigation, shau kehoe]
    related_skills: [productivity/google-workspace]
---

# Drive Structure Navigation Skill — Enable the Disabled

## When to Use
- You need to find a file in Google Drive or the local repo and don't remember which folder it lives in.
- You need the Drive folder ID for uploading a new file.
- You need to cross-reference a Drive path with the local repo path.
- You need to understand the `NN_Name` numbering convention used in the Operations folders.

## Key Constraint: Admin vs Shared
- **`Enabling the Disabled - Admin`** (ID `1_YpciYU1uRS53ol74oqojUKlUKSQF4BJ`) — **Private**. Eric only. Working drafts, private invoicing, internal collaboration. Never referenced from the shared folder.
- **`Enable the Disabled - Shaun Kehoe`** (ID `17Sav0cJmDafe8DDvHKKq0OT1awzQ0ik8`) — **Shared output**. Read-only unless Eric explicitly directs otherwise. External-facing deliverables for Shaun Kehoe. These two trees are completely separate — no cross-referencing.

## Prerequisites
- Google Workspace auth for the `fitness-strategist` profile.
- Reference: `documents/security-inventory/drive-structure.md` (this document's companion reference).

## Quick Reference
```bash
# Check auth
python3 setup.py --check

# Search Drive for a folder
python3 google_api.py drive search "folder name" --max 10

# Search Drive for a file
python3 google_api.py drive search "file name" --max 10

# Load the full structure reference
read_file documents/security-inventory/drive-structure.md
```

## Procedure

### 1. Look up a folder ID or path
Reference the **`documents/security-inventory/drive-structure.md`** file. It contains:
- A full tree map of both Drive trees (Admin + Shared)
- A repo mirror mapping table
- A key folder IDs table
- The `NN_Name` numbering convention

### 2. If a folder isn't in the reference
Search Drive directly via `python3 google_api.py drive search "name"` — prefer exact folder name fragments. Always filter by `mimeType='application/vnd.google-apps.folder'` when looking for folders.

### 3. List contents of a known folder ID
```python
# One-liner to list all children of a folder
python3 -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
creds = Credentials.from_authorized_user_file('~/.hermes/profiles/fitness-strategist/google_token.json')
drive = build('drive', 'v3', credentials=creds)
results = drive.files().list(q=\"'FOLDER_ID' in parents\", fields='files(id,name,mimeType)', pageSize=100).execute()
for f in results.get('files', []):
    print(f'{f[\"name\"]} | {f[\"id\"]} | {f[\"mimeType\"]}')
"
```

### 4. Cross-reference with the local repo
Check the **Repo Mirror Mapping** table in `documents/security-inventory/drive-structure.md`. Columns:
- **Drive Path** — full path within either Admin or Shared
- **Repo Path** — corresponding path in `/home/hermes/enabling-the-disabled`
- **Notes** — sync relationship, e.g., "master copy = Google Sheet; CSV mirrors in repo"

### 5. Understanding the numbered folders
Both Drive trees (and their repo mirrors) use a `NN_Name` prefix convention in operational folders:
- `01_Clients` — Client-facing documents
- `02_HR-Workforce` — Employee/contractor docs
- `04_IT-Infrastructure` — IT docs
- `08_Security` — Security inventory
- `09_Other` — Catch-all

**Rule:** New folders follow the `NN_Name` pattern. Observe gaps (03–07 skipped) — they are intentional. Don't renumber.

## File Creation Policy
| Where to create drafts | Rule |
|------------------------|------|
| Local repo `documents/` | **Always start here** — Markdown only |
| `Enabling the Disabled - Admin` | Safe for internal working copies, mirrors, backups |
| `Enable the Disabled - Shaun Kehoe` | **Never write without Eric's explicit approval** — this is the read-only shared output folder |

## Pitfalls
- **Two "Incorporation" folders** exist in `Shared > Corporate/` (IDs `1w2On6DibxG5z0REfgLoBYUEkERwkgSAU` and `1TxWJJfsh1rm0lFzBTxpyHA56eLp5ncm5`). Check contents before writing — they may serve different sub-purposes.
- **Root-level orphan files**: The Shared folder has a standalone `Trainer_Contractor_Agreement.docx` at root that duplicates content in `Operations > 02_HR-Workforce`.
- **Shortcuts in Drive** (`application/vnd.google-apps.shortcut` MIME) are often invisible to the file-listing API. If something seems missing, search by name.
- **Admin and Shared are completely separate** — never reference one from the other in documentation or cross-links.

## Verification
- After writing a file to Drive, confirm it appears via `drive search "filename"`.
- After mirroring a Drive file to the repo, confirm both paths are listed in the reference.
- If creating a new numbered folder, verify no existing folder already claims that number.
