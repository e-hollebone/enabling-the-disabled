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
| Admin root | Yes | Yes | ✅ Complete |
| Admin > Corporate | Yes | Yes | ✅ Complete |
| Admin > Corporate > 08_Security | Partial (inventory README) | Yes | ✅ Complete |
| Shared root | Yes | Yes | ✅ Complete |
| Shared > Corporate | Yes | Yes | ✅ Complete |
| Shared > Corporate > Fact-finding | Yes | Yes | ✅ Complete |
| Shared > Corporate > Incorporation (×2) | Yes | Yes | ✅ Complete (two separate READMEs) |
| Shared > Corporate > Trademark | Yes | Yes | ✅ Complete |
| Shared > Operations | Yes | Yes | ✅ Complete |
| Shared > Operations > 01_Clients | Yes | Yes | ✅ Complete |
| Shared > Operations > 02_HR-Workforce | Yes | Yes | ✅ Complete |
| Shared > Operations > 03_Operations | Yes | Yes | ✅ Complete |
| Shared > Operations > 04_IT-Infrastructure | Yes | Yes | ✅ Complete |
| Shared > Operations > 08_Security | Yes | Yes | ✅ Complete |
| Shared > Operations > 09_Other | Yes | Yes | ✅ Complete |
| Shared > name search | Yes | Yes | ✅ Complete |
| Shared > _archive | Yes | Yes | ✅ Complete |
| Incorporation Checklist | Yes | Yes | ✅ Complete |

## Pitfalls

- **Two "Incorporation" folders** in `Shared > Corporate/` — each needs its own README to disambiguate.
- **Shortcuts** in Drive appear as files but are not real files — document them as shortcuts in the README.
- **The root-level `Trainer_Contractor_Agreement.docx`** in the Shared folder is an orphan — reference it in the Shared root README.
- **Never cross-link Admin↔Shared** — each tree's README links only within its own tree.

## Conversion Workflow (Markdown → Google Docs)

### Key Technique: HTML Import via Drive API `files().update()`

**Do NOT** use the Docs API `batchUpdate` to rewrite doc content — it is complex (requires index tracking, two-phase insert-then-style, and is prone to offset bugs). Instead:

1. Convert markdown → HTML using Python's `markdown` library (with `tables`, `fenced_code`, `sane_lists`, `nl2br` extensions).
2. Wrap the HTML in a `<!DOCTYPE html>` document with embedded CSS for styling (headings, code blocks, tables, links, blockquotes).
3. Import HTML to Google Docs via **Drive API `files().update(fileId=..., media_body=media)`** — this replaces the entire doc content in-place, **preserving the doc ID, permissions, comments, and folder location**. Use `MediaIoBaseUpload` with `mimetype="text/html"`.
4. For NEW docs, use `files().create(body={"name": title, "mimeType": "application/vnd.google-apps.document", "parents": [parent_id]}, media_body=media)`.

**Critical pitfall:** Drive API `files().update()` with `media_body` will silently fail if the `fileId` doesn't exist or is in trash. Wrap in try/except and fall through to create new if update fails. But the create-new path will produce duplicate docs with new IDs — always verify the doc exists first with `drive.files().get(fileId=doc_id)`.

### Internal Link Replacement

Internal links in markdown use backtick-wrapped names like `` `Enable the Disabled - Shaun Kehoe` `` or file IDs like `` `17Sav0cJmDafe8DDvHKKq0OT1awzQ0ik8` ``.

The conversion script's `replace_internal_links()` function:
1. Iterates over a REGISTRY mapping (name → (file_id, type)) in order of longest name first.
2. Replaces backtick-wrapped names/IDs with a sentinel marker containing the name and the Google Drive URL.
3. Converts sentinels to markdown links `[name](url)` at the end.
4. The markdown→HTML converter renders these as `<a href="url">` tags, which Google Docs HTML import renders as clickable hyperlinks.

**REGISTRY must be kept in sync with actual Drive IDs.** After any doc recreation or ID change, update the REGISTRY immediately. Use a lookup dict that maps doc names to IDs, and verify against Drive before processing.

### Token Management

The script reads credentials from `/home/hermes/.hermes/profiles/fitness-strategist/google_token.json` (profile-scoped token path). The `get_creds()` function should **save the refreshed token** back to disk so future runs start with a valid token:

```python
creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    with open(TOKEN_PATH, 'w') as f:
        f.write(creds.to_json())
```

**Never copy tokens between profiles** — the profile token is user-scoped but copying another profile's token (e.g., herschel) can overwrite the correct token with one that has wrong scopes.

## Verification
- After creating a README, verify the Doc exists in the target folder via `drive search "README - [Folder Name]"`.
- After updating a README, verify the repo version is committed and pushed.
- Every folder should have exactly one README Doc — if there are duplicates, clean them up.
