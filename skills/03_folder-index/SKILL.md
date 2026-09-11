---
name: drive-folder-index
description: Create and maintain README.md index at each Drive folder level.
version: 0.1.0
author: fitness-strategist
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: enable-the-disabled
    tags: [google-drive, folder-index, readme, documentation, navigation]
    related_skills: [drive-structure-navigation, productivity/google-workspace]
---

# Drive Folder Index Skill — Enable the Disabled

## When to Use
- You've created a new folder in Google Drive and need a README documenting its purpose.
- You need to update a folder's README after adding/removing files.
- You need to verify that every Drive folder has a descriptive index document.
- You need to understand what a folder contains before writing into it.
- You need to cross-link between related folders across the Admin and Shared trees.

## Key Constraint
- **Admin and Shared folders are completely separate.** Never cross-link between them. Each tree maintains its own index chain.
- **README documents live in the repo first** as Markdown, then get uploaded to Drive as Google Docs when the folder requires an external-facing index.

## Prerequisites
- The Drive structure reference: `documents/security-inventory/drive-structure.md`
- Google Drive API auth for reading folder contents.
- Google Docs API auth for creating Doc files (if uploading READMEs).

## Folder Index Document Convention

Every Google Drive folder should have a companion **`README.md`** (repo-side) that is also uploaded as a **Google Doc** named `README - [Folder Name]` in that folder. The Doc contains:

1. **Folder purpose** — one sentence explaining why this folder exists.
2. **Contents listing** — child folders and files with brief descriptions.
3. **Parent/sibling navigation** — links to parent and sibling folders (same tree only).
4. **Next actions / TODOs** — any pending work in this folder.
5. **Repo mirror** — where this folder's contents are mirrored (or "not mirrored").

## Procedure

### 1. Determine if a folder needs a README
Check if a Google Doc named `README - [Folder Name]` already exists in the folder:
```python
results = drive.files().list(
    q=f"'{folder_id}' in parents and name contains 'README'",
    fields='files(id, name)'
).execute()
```
If no README Doc exists, or if the folder contents have changed since the last update, create or refresh the README.

### 2. Generate the README content
The README template (stored at `documents/security-inventory/templates/FOLDER_README_TEMPLATE.md` in the repo):

```markdown
# [Folder Name] — README

**Parent:** [Parent Folder Name] ([parent_folder_id])
**Purpose:** [One sentence: why this folder exists]
**Share target:** [Who has access — same tree only, never cross-link Admin↔Shared]

## Contents

### Subfolders
| Name | ID | Purpose |
|------|----|---------|
| [Folder 1 Name] | [ID] | [Brief description] |

### Files
| Name | Type | Description |
|------|------|-------------|
| [File 1] | [Google Doc / Sheet / PDF / etc.] | [Brief description] |

## Repo Mirror
[Where this folder's content is mirrored in the repo, or "Not mirrored"]

## Navigation
- **Parent:** [Parent Folder Name] → `README - [Parent Name]`
- **Siblings:** [List of sibling folder READMEs]

## Next Actions / TODOs
- [ ] [Pending work item]

---
*Index maintained by fitness-strategist profile. Last updated: [date]*
```

### 3. Write the README to the repo
Save the README as a Markdown file in the repo under a folder index structure:
```
documents/security-inventory/folder-index/
├── README-Enable-the-Disabled-Admin.md (Admin root)
├── README-Corporate-Admin.md (Admin > Corporate)
├── README-08-Security-Admin.md (Admin > Corporate > 08_Security)
├── README-Enable-the-Disabled-Shaun-Kehoe.md (Shared root)
├── README-Corporate-Shared.md (Shared > Corporate)
├── README-Fact-Finding.md (Shared > Corporate > Fact-finding)
├── README-Incorporation-Shared.md (Shared > Corporate > Incorporation)
├── README-Trademark.md (Shared > Corporate > Trademark)
├── README-Operations-Shared.md (Shared > Operations)
├── README-01-Clients.md (Shared > Operations > 01_Clients)
├── README-02-HR-Workforce.md (Shared > Operations > 02_HR-Workforce)
├── README-08-Security-Shared.md (Shared > Operations > 08_Security)
└── README-09-Other.md (Shared > Operations > 09_Other)
```

### 4. Upload the README to Google Drive as a Doc
```bash
python3 -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('~/.hermes/profiles/fitness-strategist/google_token.json')
docs = build('docs', 'v1', credentials=creds)
drive = build('drive', 'v3', credentials=creds)

# Create the Google Doc
doc = docs.documents().create(documentTitle='README - [Folder Name]').execute()
# Insert the markdown content (convert to plain text for now — Docs API supports HTML import)
# ...content insertion logic...

# Move the doc to the target folder
drive.files().update(
    fileId=doc['documentId'],
    addParents='[FOLDER_ID]',
    fields='id'
).execute()
"
```

### 5. Cross-link between READMEs
Within each README, link to:
- **Parent:** the parent folder's README Doc
- **Children:** each child folder's README Doc
- **Siblings:** adjacent folders at the same level

Links use Google Docs share URLs (extract `webViewLink` from Drive API responses).

### 6. Keep READMEs current
**When you add or remove files/folders:**
1. Update the corresponding repo-side `documents/security-inventory/folder-index/README-*.md`
2. Push to git
3. Re-upload the Doc to Drive (or ask Eric if the folder is shared)
4. Update the `drive-structure.md` reference file if folder IDs or structure changed

## Current Folder README Status

| Folder | README in Repo? | README as Google Doc in Drive? | Status |
|--------|----------------|-------------------------------|--------|
| Admin root | Not yet | No | Needs creation |
| Admin > Corporate | Not yet | No | Needs creation |
| Admin > Corporate > 08_Security | Partial (inventory README) | No | Needs completion |
| Shared root | Not yet | No | Needs creation |
| Shared > Corporate | Not yet | No | Needs creation |
| Shared > Corporate > Fact-finding | Not yet | No | Needs creation |
| Shared > Corporate > Incorporation | Not yet | No | Needs creation (note: two Incorporation folders) |
| Shared > Corporate > Trademark | Not yet | No | Needs creation |
| Shared > Operations | Not yet | No | Needs creation |
| Shared > Operations > 01_Clients | Not yet | No | Needs creation |
| Shared > Operations > 02_HR-Workforce | Not yet | No | Needs creation |
| Shared > Operations > 08_Security | No | Yes (Comms Sheet only) | Needs README |
| Shared > Operations > 09_Other | Not yet | No | Needs creation |

## Pitfalls
- **Two "Incorporation" folders** in `Shared > Corporate/` — each needs its own README to disambiguate.
- **Shortcuts** in Drive appear as files but are not real files — document them as shortcuts in the README.
- **The root-level `Trainer_Contractor_Agreement.docx`** in the Shared folder is an orphan — reference it in the Shared root README.
- **Never cross-link Admin↔Shared** — each tree's README links only within its own tree.

## Verification
- After creating a README, verify the Doc exists in the target folder via `drive search "README - [Folder Name]"`.
- After updating a README, verify the repo version is committed and pushed.
- Every folder should have exactly one README Doc — if there are duplicates, clean them up.
