# Repository Conventions & Document Organization

**Last updated:** 2026-08-27  
**Purpose:** How documents are organized across systems, what goes where, and why.

---

## GitHub Repository — `enabling-the-disabled`

**URL:** https://github.com/e-hollebone/enabling-the-disabled  
**Visibility:** Public  
**Default branch:** `main`  
**Authoring profile:** `fitness-strategist` (Hermes)

### Folder structure

```
enabling-the-disabled/
├── README.md                          # Repo overview, layout, phases
├── AGENTS.md                          # Project conventions for authoring profile
├── branding/                          # Brand voice, naming, positioning, creative copy
├── documents/
│   ├── journal.md                     # Time-based record of major interactions
│   ├── effort-log.csv                 # Effort tracking (date, hours, subject, category, notes)
│   ├── key-facts.md                   # Key facts about the business (initial draft)
│   ├── profile-identity.md            # Canonical source of truth for fitness-strategist profile
│   ├── needs-documents/
│   │   ├── business-context-collection.md   # Filled-in business profile
│   │   ├── business-needs-inventory.md      # Living needs table (template)
│   │   ├── current-state-assessment.md      # Assessment template (post-collection)
│   │   └── shaun-questions-round-1.md       # Question batches for Shaun
│   └── analysis/
│       └── social-media-website-analysis.md # Strengths & weaknesses (point-in-time)
├── legal-finance/                     # Pricing, contracts, legal, finance
├── marketing/                         # Marketing plans, content, outreach
└── operations/                        # Operational processes, workflows, delivery logistics
```

### What lives here

- All business documents (drafts, templates, assessments)
- Journal of major interactions
- Effort log
- Question lists for Shaun
- Analysis documents
- Brand, marketing, operations, legal/finance documents (as they're produced)

### Commit conventions

- Atomic, descriptive commits
- Each answer or clarification is a commit
- Clear messages describing what changed and why

---

## Google Drive

### Shared Output Folder — `My Drive > Clients > Enable the Disabled - Shaun Kehoe/`

**Purpose:** External-facing materials only  
**Access:** Shared with external parties  
**Rule:** Read-only unless Eric explicitly directs otherwise  
**Contents:**
- `Enable-the-disabled-banner.png`
- 5 Google Docs (contracts, waivers, agreements)
- `originals/` — original contract documents
- `word-versions/` — Word format versions

### Admin Working Folder — `My Drive > Clients > Enabling the Disabled - Admin/`

**Purpose:** Internal working documents  
**Access:** Eric and fitness-strategist only  
**Contents:**
- `Effort Log` (Google Sheet) — mirror of repo effort-log.csv
- `Journal` (Google Doc) — mirror of repo journal.md

---

## Document Flow

1. **Collect** — gather facts from Eric and Shaun → store in `documents/`
2. **Assess** — analyze and structure → store in `documents/analysis/`
3. **Build** — produce forward-moving documents → store in `branding/`, `marketing/`, `operations/`, `legal-finance/`
4. **Share** — when a document is ready for external eyes → move to shared output folder (with Eric's approval only)

---

## Key Contacts

| Resource | Value |
|----------|-------|
| Business owner | Eric |
| Business timezone | America/Toronto (EDT, UTC-04:00) |
| Profile wrapper | `/home/hermes/.local/bin/fitness-strategist` |
| Profile directory | `~/.hermes/profiles/fitness-strategist/` |
| Repo (local) | `/home/hermes/enabling-the-disabled` |
| Repo (web) | `https://github.com/e-hollebone/enabling-the-disabled` |
| Repo (SSH) | `git@github.com:e-hollebone/enabling-the-disabled.git` |
| Git auth | `gh` CLI, user `e-hollebone`, full repo admin |
