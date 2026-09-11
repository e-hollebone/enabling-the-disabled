# Repo Conventions

*Auto-generated reference — last updated by fitness-strategist*

## File Formats

| Location | Format | Notes |
|----------|--------|-------|
| `enabling-the-disabled/` (Git repo) | Markdown (`.md`) | Source of truth for all internal documentation |
| Google Drive (Enable the Disabled folders) | Google Docs / Sheets / Slides / PDFs | Published deliverables for Shaun; never `.md` |

## Drive Policy (Updated)

> **No `.md` files in Google Drive for this project.** All documents must be native Google Drive file types (Google Docs, Sheets, Slides) or binary (PDF, PNG). Markdown lives only in the repo. When a `.md` file appears in Drive, it must be converted to a Google Doc and the `.md` deleted.

### Rationale
Team members (including Shaun Kehoe) have no Markdown viewer. `.md` files render as plain, unformatted text — unreadble and unactionable.

## Directory Structure (Enable the Disabled)

### Shared Output Tree
```
Enable the Disabled - Shaun Kehoe (17Sav0cJmDafe8DDvHKKq0OT1awzQ0ik8)
├── README - Enable the Disabled - Shaun Kehoe (doc)
├── Brand (1A45rdYzyLYudsjQEBEm5FcXUDf6198ys)
│   ├── README - Brand (doc)
│   └── [logo, banner, trademark PDFs]
├── Corporate (1dRr76f_xiGQvmnaAAMmSf1IjYhlNeT-O)
│   ├── README - Corporate (doc)
│   ├── 00_Fact-finding (1reMboKf5TezQWDZ9E55H7v3LyxelA5oH)
│   │   ├── README - Fact-finding (doc)
│   │   └── [scheduling Qs, business profile, direction doc]
│   ├── 07_Incorporation (1w2On6DibxG5z0REfgLoBYUEkERwkgSAU)
│   │   ├── README - Incorporation (doc)
│   │   ├── Incorporation Checklist (doc)
│   │   └── name search (1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G)
│   │       ├── README - name search (doc)
│   │       └── [name research docs — Google Docs only]
│   ├── 08_Trademark (1omvZoaW1v63lMHFEgrNcxI4e8xtpaTR8)
│   │   └── README - Trademark (doc)
│   └── Incorporation (1TxWJJfsh1rm0lFzBTxpyHA56eLp5ncm5) [second — investigate]
│       └── README - Incorporation (second) (doc)
├── Operations (1wgqw4-IReNIMFov73r5DCEpvt7Mm9q1y)
│   ├── README - Operations (doc)
│   ├── 01_Clients (1H0dGCPgf3tT8bYDCp9prGWJT9ub9fgIt)
│   ├── 02_HR-Workforce (1Y-mz3Dqsd1rBcY6lohx4cTNYefETcqW3)
│   ├── 04_IT-Infrastructure (1gNcp_RPinZ2ofaSnf5cE2URko-Q3AR1z)
│   ├── 08_Security (1oTb65y2-xWLmNGa5nZoMYqHqOdiZY_uB)
│   │   └── README - 08_Security (Shared) (doc) [needs creation]
│   ├── 09_Other (1WagBxHIuwam9jXlUTN5Ejm0TxSktkFaz)
│   └── 03_Operations (1PV6qMwgnj9ATjhWA9p9Tb0S9x4Bg1Hyb)
└── _archive (1cezQT8LdBg8Z_YTLdSH1Sgsc2gKdmZHO)
    ├── README - _archive (doc)
    ├── originals (1sqNlbb-cUM1noX_a__SZAsmcSnytz679)
    └── word-versions (1tT3kL3jv6Fa4sNwcsA7sYmmi8_luQYAh)
```

### Admin Tree (Private)
```
Enable the Disabled - Admin (1_YpciYU1uRS53ol74oqojUKlUKSQF4BJ)
├── README - Enabling the Disabled - Admin (doc)
├── Corporate (1tH7rTwRGkjaj8KrZheNAkyLBSEkCdM4x)
│   └── 08_Security (14Ek0zgqHHpXuuBtoe7EJDRUwjpTRu_Iy)
│       ├── README - 08_Security (Admin) (doc)
│       └── [Account & Asset Inventory (sheet)]
└── [Effort Log (sheet), Journal (doc), Opp notes (doc)]
```

## Internal Linking Convention

All internal references to folders and files in Google Drive must be **clickable links** in Google Docs, not plain text. The format is:

- **Folders:** `[Folder Name](https://drive.google.com/drive/folders/FOLDER_ID)`
- **Files:** `[File Name](https://docs.google.com/document/d/DOC_ID/edit)` (or appropriate Google Docs/Sheets URLs)

When a README references a child document, subfolder, or sibling, it must link directly to that item — not just display its name or ID.

## Markdown in Google Docs

Google Docs store body text via the Docs API as structured elements (paragraphs, text runs with styling). Markdown source in the repo is converted to Google Docs formatting (headings, bold, tables, lists, checkboxes) using the Docs API `batchUpdate` method. The conversion is handled by the `google_api.py` script's docs commands.

## Repo Mirror Convention

README files in Drive document where they are mirrored in the repo:
- `legal-finance/` ← name research docs
- `documents/security-inventory/` ← security inventory sheets/templates
- `documents/needs-documents/` ← fact-finding documents
- `documents/journal.md` ← Journal doc (two-way mirror)
- `documents/effort-log.csv` ← Effort Log sheet (two-way mirror)
