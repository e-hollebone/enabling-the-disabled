# Handoff — fitness-strategist Profile & Enabling-the-Disabled Repo

**Prepared:** 2026-08-27  
**Purpose:** Stand up the `fitness-strategist` Hermes profile and hand it the `enabling-the-disabled` repo as its working directory, so the next agent session can pick up exactly where this one left off.

---

## 1. What this is

A small fitness business combining **personal training** with **gym delivery** — bringing equipment and setup to clients rather than requiring them to come to a fixed location. Owner: **Eric**. Timezone: **America/Toronto (EDT, UTC-04:00)**.

The business is in the **collection phase** — we're gathering what exists, what documents are already in place, and where the business actually stands, before doing a formal assessment and producing forward-moving documents.

The `fitness-strategist` Hermes profile is the authoring agent for all business documents in this repo.

---

## 2. The Hermes profile — `fitness-strategist`

**Location:** `~/.hermes/profiles/fitness-strategist/`

**Wrapper script:** `/home/hermes/.local/bin/fitness-strategist`

```sh
#!/bin/sh
exec /home/hermes/.local/bin/hermes -p fitness-strategist "$@"
```

Invoke as `fitness-strategist` from anywhere — it routes to Hermes with the profile flag.

**Model:** Inherits the default model from the Hermes config. No model override has been set on this profile. When launched, check `hermes -p fitness-strategist config get model` to confirm.

**Personality:** Set to `creative` via profile config (`agent.personalities.default = creative`). This was configured with `hermes -p fitness-strategist config set agent.personalities.default creative`. Confirm current state if needed.

**Config file:** There is **no `config.yaml`** in the profile directory yet. Behavioral settings (model, personality, tools, etc.) are inherited from the default Hermes config and from profile-level overrides set via `hermes config set`. If you need to set anything, use `hermes -p fitness-strategist config set KEY VAL` — do **not** hand-edit `config.yaml`.

**Secrets file:** `~/.hermes/profiles/fitness-strategist/.env` exists (165 bytes). Contents:

```
# Per-profile secrets for this Hermes profile.
# API keys and tokens set here override the shell environment.
# Behavioral settings belong in config.yaml, not here.
```

No API keys or tokens are set in it yet. The profile inherits whatever is in the shell environment.

**Identity files:**

### SOUL.md (`~/.hermes/profiles/fitness-strategist/SOUL.md`, 1331 bytes)

```
You are a creative writer and business operations strategist helping a small fitness
business that combines personal training with gym delivery.

## Voice
- Clear, readable, professional-but-warm prose. You write like someone who understands
  both storytelling and spreadsheets.
- Adapt tone to the document: a needs assessment is direct and structured; a brand narrative
  has pulse.
- No jargon without purpose. No filler. No sycophancy.

## Operating posture
- Start by understanding the business: what exists, what's needed, what's blocking forward
  motion.
- Turn ambiguity into structure: needs lists, prioritized next steps, document outlines,
  ownership assignments.
- Write documents that are actually usable — headers that navigate, action items that are
  assignable, language a non-expert can act on.
- When drafting, produce a complete first pass, not an outline that stalls. When reviewing,
  be specific about what to change and why.
- Admit uncertainty. If you don't know a fitness-industry norm, say so and suggest how to
  find out.

## Boundaries
- This profile's job is creative writing and business operations — document authorship,
  needs analysis, operational planning.
- Commit everything you create to the `enabling-the-disabled` repo.
- Do not hand-edit `config.yaml`. Use `hermes config set KEY VAL`.
```

### USER.md (`~/.hermes/profiles/fitness-strategist/memories/USER.md`, 1068 bytes)

```
Eric runs a small fitness business combining personal training with gym delivery — bringing
equipment and setup to clients rather than requiring them to come to a fixed location.

## Preferences
- Documents that are structurally sound and actually usable — navigation, action items,
  clear owners.
- Creative quality in brand-facing copy; plain, direct language in operational documents.
- Next-step thinking: always drive toward what needs to happen next, not just what exists.
- Timezone: America/Toronto (EDT, UTC-04:00).

## Current phase
We are collecting information about the business — what exists, what documents are already
in place, where the business actually stands — before doing a formal assessment and producing
forward-moving documents.

## How to work with me
- Ask direct questions when you need a fact. Don't pad with synonyms.
- When you produce a document, deliver the full draft — not an outline waiting for me to
  fill in the blanks.
- If you don't know something about the fitness industry, say so rather than inventing it.
```

**Profile identity canonical reference:** `documents/profile-identity.md` in the repo is the tracked, versioned copy of the profile identity (SOUL). The runtime copy is SOUL.md in the profile directory. If the profile identity ever needs to change, update the repo copy and propagate to the profile dir — or decide which is authoritative and make it consistent.

**Bundled skills:** 14 skill directories are present under `~/.hermes/profiles/fitness-strategist/skills/`:

```
apple | autonomous-ai-agents | creative | devops | email | github | media |
mlops | note-taking | productivity | research | smart-home | social-media | software-development
```

These are the synced/bundled skills available to this profile. They cover the full Hermes skill set as of profile creation. No custom business-ops skills have been added yet.

---

## 3. The GitHub repo — `enabling-the-disabled`

**URL:** `https://github.com/e-hollebone/enabling-the-disabled`  
**Clone URL (SSH):** `git@github.com:e-hollebone/enabling-the-disabled.git`  
**Visibility:** Public  
**Description:** "Business documentation and operations for a personal training + gym delivery fitness business"  
**Default branch:** `main`

**Local clone location:** `/home/hermes/enabling-the-disabled`

**Git auth:** `gh` CLI is authenticated as `e-hollebone` with full repo admin scopes. Pushes and pulls work over SSH. If `gh` auth is ever lost, re-authenticate with `gh auth login`.

**Repo structure:**

```
enabling-the-disabled/
├── README.md                          # Repo overview, layout, phases
├── AGENTS.md                          # Project conventions for the authoring profile
├── branding/                          # Brand voice, naming, positioning, creative copy
├── documents/
│   └── needs-documents/
│       ├── business-needs-inventory.md        # Living needs table (template)
│       ├── business-context-collection.md     # Structured questionnaire (collection phase)
│       └── current-state-assessment.md        # Assessment template (post-collection)
├── legal-finance/                     # Pricing, contracts, legal, finance
├── marketing/                        # Marketing plans, content, outreach
└── operations/                       # Operational processes, workflows, delivery logistics
```

Empty folders (`branding/`, `legal-finance/`, `marketing/`, `operations/`) are scaffolded and ready for content when the time comes.

---

## 4. Documents in the repo — what exists and what it is

### README.md (890 bytes)

Repo overview. States the layout, the three phases (Collect → Assess → Build), identifies the authoring profile, and notes the license (private, all rights reserved).

### AGENTS.md (747 bytes)

Project conventions for anyone (any profile) authoring in this repo. Key points:

- Write complete documents, not stubs.
- Every document has a clear owner or next step when it's not final.
- Navigation matters: headers, action items, and summary lines so a reader can use the doc without reading it cover to cover.
- When something is uncertain, say so and mark it for follow-up — don't paper over gaps.
- Do not invent fitness-industry facts. If you don't know, flag it.
- Brand-facing copy gets creative care; operational documents get clarity and actionability.

### documents/needs-documents/business-needs-inventory.md (1,136 bytes)

A living needs table template. Categories: Operations, Branding, Marketing, Legal/Finance, Systems/Tools. Columns: #, Category, Need, Priority (High/Medium/Low), Status (Identified/Researching/Documenting/Resolved), Notes. This is filled in as needs surface — it's a working document, not a final assessment.

### documents/needs-documents/business-context-collection.md (2,354 bytes)

The primary collection-phase document. Structured questionnaire organized into six sections:

1. **The business** — what it does, typical client, how gym delivery works in practice, how personal training fits with delivery.
2. **Current state** — what exists today (clients, equipment, brand, website, social, contracts), what's already documented, what's working, what's not working or missing.
3. **Constraints** — location/geography, time/availability, budget/resources, legal/regulatory.
4. **Goals** — what "moving forward" looks like (next 6 months), near-term priority.
5. **Assets** — equipment (have/need), brand assets, digital presence, relationships.
6. **Open questions** — table for questions that come up during collection; these become research items or decisions to make.

This document is **not yet filled in** — it's waiting for Eric's answers. The collection phase starts here.

### documents/needs-documents/current-state-assessment.md (1,215 bytes)

The formal assessment document, waiting for the business context collection to complete. Structure:

1. **What exists today** — honest picture of the business as it stands.
2. **What's missing** — gaps between where the business is and where it needs to be.
3. **What's working** — strengths and assets to build on.
4. **Priorities** — ranked next steps with reasoning.
5. **Risks / constraints** — anything that limits what can be done or how fast.

The assessment feeds every document that follows. If a document contradicts the assessment, the assessment wins until it's updated.

### documents/profile-identity.md (1,637 bytes)

Canonical, tracked source of truth for the `fitness-strategist` profile identity (mirrors SOUL.md). States that the runtime copy lives at `~/.hermes/profiles/fitness-strategist/SOUL.md` and that this file is the tracked reference. Contains the full soul definition (voice, operating posture, boundaries). This exists so the profile identity is versioned in the repo, not just sitting in the profile directory.

---

## 5. The three-phase plan

### Phase 1 — Collect (current)

Gather everything that exists about the business. The primary tool is `business-context-collection.md` — work through it section by section, get Eric's answers, fill them in directly. Secondary: `business-needs-inventory.md` captures needs as they surface. The goal of this phase is a complete picture of the business as it stands.

**What you need from Eric to start:** Sit down with `business-context-collection.md` and answer the questions. Don't worry about perfect answers — flag anything you're unsure about. The document is written to accept partial answers and mark open items.

### Phase 2 — Assess

Once collection has enough material, fill in `current-state-assessment.md`. This is the honest, structured picture of where the business stands: what exists, what's missing, what's working, what the priorities are, what the constraints are. This becomes the source of truth that every subsequent document defers to.

### Phase 3 — Build

Produce the documents that move the business forward. Which documents those are depends on what the assessment surfaces, but the folders are ready:

- `branding/` — brand voice, naming, positioning, creative copy
- `marketing/` — marketing plans, content, outreach
- `operations/` — operational processes, workflows, delivery logistics
- `legal-finance/` — pricing, contracts, legal, finance

---

## 6. Conventions and boundaries for working in this repo

These are captured in `AGENTS.md` in the repo and in the profile's SOUL.md. The most important ones:

**Document quality bar:**
- Complete documents, not stubs. A draft that's ready to use beats an outline waiting to be filled.
- Every document that isn't final has a clear owner or next step.
- Navigation matters: headers, action items, summary lines. A reader should be able to use the doc without reading it cover to cover.
- When something is uncertain, say so and mark it for follow-up. Don't paper over gaps.

**Source discipline:**
- Do not invent fitness-industry facts. If you don't know something, say so and suggest how to find out.
- Brand-facing copy gets creative care. Operational documents get clarity and actionability.

**Commit discipline:**
- Everything you create goes into the `enabling-the-disabled` repo on the `main` branch.
- Commit with clear messages. The repo follows the convention of atomic, descriptive commits.

**Profile discipline:**
- This profile authors documents. It is not a general-purpose agent — its job is creative writing + business operations for this business.
- Do not hand-edit `config.yaml`. Use `hermes config set KEY VAL`.
- The profile's working directory is `/home/hermes/enabling-the-disabled`.

**Hermes discipline (apply to any agent working here):**
- Diagnose own tooling failures first.
- Own mistakes.
- Prefer local over network.
- Corrections → SKILL (if a correction reveals a workflow gap, capture it as a skill, not just a one-off fix).
- No sycophancy.
- Never implement until told "go" — ask before acting when the action isn't mechanical.
- Lint all code and shell scripts before running or committing (ruff, yamllint, shellcheck, jq, py_compile, bash -n available on the host).
- Do not use IP addresses — always use FQDN (e.g., `renfrew-ai.ts.hollebone.ca`).

---

## 7. Where to start

**If you're picking up in the collection phase (most likely):**

1. Confirm the profile is working: launch `fitness-strategist` and verify the model, personality, and skills load.
2. Read `documents/needs-documents/business-context-collection.md` in full.
3. Reach out to Eric and start walking through the sections. Fill in answers directly into the doc as you go.
4. As needs surface during the conversation, add rows to `business-needs-inventory.md`.
5. Commit as you go — don't batch everything at the end. Each answer or clarification is a commit.

**If collection is already complete when you start:**

1. Read `business-context-collection.md` to see what we know.
2. Fill in `current-state-assessment.md` from that material.
3. Move to Phase 3 and start producing documents based on the assessment.

---

## 8. What's NOT done yet

- **No business answers collected.** `business-context-collection.md` is still a blank template. Eric hasn't answered any of the questions yet.
- **No current-state assessment.** `current-state-assessment.md` is a template waiting for collection to complete.
- **No needs rows filled in.** `business-needs-inventory.md` is an empty table.
- **No business documents produced.** The `branding/`, `marketing/`, `operations/`, and `legal-finance/` folders are empty.
- **No custom skills added.** The profile has the bundled 14 skills but no business-ops-specific skills have been authored yet.
- **No API keys configured.** The `.env` is empty. If the business needs API access (e.g., social platforms, scheduling tools, anything), that's a later concern.

---

## 9. Contacts and access

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
| Profile model | Inherits default (check `hermes -p fitness-strategist config get model`) |
| Profile personality | `creative` (set via `hermes -p fitness-strategist config set agent.personalities.default creative`) |

---

## 10. If something is broken or missing

- **Profile won't launch:** Check that `~/.hermes/profiles/fitness-strategist/` exists with SOUL.md and memories/USER.md. Check that the wrapper `/home/hermes/.local/bin/fitness-strategist` is executable. Run `hermes -p fitness-strategist config get model` to confirm the model resolves.
- **Git push fails:** Check `gh auth status`. Re-authenticate if needed.
- **Profile identity drifts between SOUL.md and profile-identity.md:** Decide which is authoritative. The repo copy (`documents/profile-identity.md`) is the tracked reference; the profile copy (`SOUL.md`) is the runtime load. Make them consistent.
- **`config.yaml` is missing:** That's expected. There is no profile-level config file yet. Use `hermes config set` for overrides.
