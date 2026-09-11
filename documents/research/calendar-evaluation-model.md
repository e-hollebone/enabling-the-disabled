# Calendar & Appointment Software Evaluation Model

**For:** Enable the Disabled scheduling tool selection  
**Prepared by:** Eric Hollebone / Hermes Agent  
**Date:** September 10, 2026  
**Status:** Draft — ready for Shaun to fill in  
**Workflow:** Booking + Google Workspace recording → batch billing in QB (no real-time QB sync required)

---

## Purpose

This document defines the evaluation criteria and scoring model for comparing calendar/appointment scheduling solutions. It translates the business requirements into a structured fit-assessment framework.

The model is designed to be **scored by you (Shaun)** once you've reviewed the [research document](calendar-appointment-software-research.md) and tested free trials.

---

## How to Use

1. **Read the research document** first (`calendar-appointment-software-research.md`)
2. **Answer Questions Q1–Q7** below
3. **Score each candidate tool** against the criteria (1–5 scale)
4. **Weighted score** is calculated automatically in the comparison matrix
5. The tool with the highest weighted score is the recommended choice

---

## Requirement Categories & Weights

> **Weights auto-adjust based on your Q1–Q7 answers.** Default weights assume Google Workspace is primary and QB is secondary (batch workflow).

| # | Category | Default Weight | What It Measures |
|---|----------|----------------|-----------------|
| **R1** | Google Calendar / Workspace Sync | **30%** | Two-way calendar sync, Google Meet, Gmail, Drive integration |
| **R2** | Booking + Notifications | **25%** | Client self-booking, automated notifications to all parties |
| **R3** | QB Integration (Path) | **10%** | QB Online or Desktop sync/export path (middleware acceptable) |
| **R4** | Multi-Trainer Coordination | **15%** | Trainer assignments, substitutions, per-trainer calendar sync |
| **R5** | Client Self-Booking | **10%** | Public booking page, real-time availability |
| **R6** | Fitness/Disability Fit | **5%** | Accessibility features, custom intake forms, health data compliance |
| **R7** | Cost at Scale | **5%** | Monthly cost at 30–50 client scale |

---

## Scoring Rubrics

### R1: Google Calendar / Workspace Sync (30%)

| Score | Meaning |
|-------|---------|
| 5 | Native two-way sync with Google Calendar; integrates with Gmail, Google Meet, Drive |
| 4 | Native two-way sync with Google Calendar; limited Workspace integration |
| 3 | Google Calendar sync via middleware; reliable |
| 2 | Google Calendar sync via middleware; known reliability issues |
| 1 | No Google Calendar integration |

**Sub-criteria (tie-breaker):** Staff calendar sync (per-trainer Google Calendar), Google Meet integration, Gmail extension, booking page embedding

---

### R2: Booking + Notifications (25%)

| Score | Meaning |
|-------|---------|
| 5 | Automated notifications to client + trainer + admin; confirmation, reminder, follow-up |
| 4 | Client + trainer notifications; missing follow-up or admin copy |
| 3 | Client + trainer basic email notifications |
| 2 | Manual notification process required |
| 1 | No automated notifications |

**Sub-criteria (tie-breaker):** SMS option, timezone handling, cancellation notifications, custom notification templates

---

### R3: QuickBooks Integration Path (10%)

> **Note:** Under the refined workflow, QB integration is a convenience, not a requirement. Batch export or middleware is acceptable.

| Score | Meaning |
|-------|---------|
| 5 | Native QB Online or Desktop sync (automatic) |
| 4 | Native QB Online sync (one-way export, acceptable for batch) |
| 3 | QB via reliable middleware (Zapier/Make, well-tested path) |
| 2 | QB via middleware, but with known issues |
| 1 | No QB integration path |

**Sub-criteria (tie-breaker):** Sync direction, data synced (customers, invoices, payments), QB Desktop support

---

### R4: Multi-Trainer Coordination (15%)

| Score | Meaning |
|-------|---------|
| 5 | Trainer assignments, substitution workflow, per-trainer calendars, staff portal |
| 4 | Trainer assignments with calendar sync; limited substitution support |
| 3 | Calendar sharing between trainers; basic assignment |
| 2 | Single shared calendar; no trainer distinction |
| 1 | Single-trainer only |

**Sub-criteria (tie-breaker):** Trainer availability management, substitution handoff notes, staff mobile app access

---

### R5: Client Self-Booking (10%)

| Score | Meaning |
|-------|---------|
| 5 | Public booking page with real-time availability, branded, embeddable |
| 4 | Public booking page with real-time availability |
| 3 | Public booking page with delayed availability update |
| 2 | Booking request form (not real-time) |
| 1 | No client-facing booking |

**Sub-criteria (tie-breaker):** Custom booking page URL, embed code, branding options, mobile responsiveness

---

### R6: Fitness / Disability Fit (5%)

| Score | Meaning |
|-------|---------|
| 5 | Built for fitness with accessibility features (custom intake, emergency contacts, HIPAA) |
| 4 | General-purpose tool with good custom fields for accessibility needs |
| 3 | Basic custom fields; can collect some disability-related info |
| 2 | Limited custom fields |
| 1 | No way to capture special needs or emergency info |

**Sub-criteria (tie-breaker):** HIPAA/EMR compliance, custom intake forms, emergency contact storage, wheelchair accessibility notes

---

### R7: Cost at Scale (5%)

| Score | Meaning |
|-------|---------|
| 5 | Under $20/month at 30-client scale; scales affordably |
| 4 | $20–$40/month at 30-client scale; reasonable |
| 3 | $40–$80/month at 30-client scale; acceptable |
| 4 | $80–$150/month at 30-client scale; high but justifiable |
| 1 | Over $150/month at 30-client scale; cost-prohibitive |

**Sub-criteria (tie-breaker):** Per-user fees, per-booking fees, setup fees, hidden costs (QB add-on, middleware)

---

## Questions That Shape the Model

These answers determine weight adjustments and disqualifying criteria:

### Q1: QuickBooks Edition
- [ ] **QuickBooks Online (QBO)** — Most tools supported. R3 weight stays at 10%.
- [ ] **QuickBooks Desktop** — Rules out most native QB tools. Batch export preferred. R3 drops to 5%.
- [ ] **Not sure / Not using QB yet** — R3 drops to 5%.

### Q2: Current Manual QB Re-entry
- [ ] **Yes, we re-key everything** — R3 weight increases to 15%
- [ ] **No, we don't re-key** — R3 stays at 10%
- [ ] **We don't use QB for billing yet** — R3 drops to 5%

### Q3: Client Self-Booking Needed?
- [ ] **Yes, clients should self-book online** — R5 stays at 10%
- [ ] **No, all booking goes through me** — R5 drops to 5%; focus shifts to internal coordination
- [ ] **Hybrid** — R5 stays at 10%

### Q4: Payment Processing Needed In-Tool?
- [ ] **Yes, we need payments in the scheduling tool** — R2 sub-criteria shift to include payment
- [ ] **No, we invoice via QB batch only** — Payments handled outside scheduling tool
- [ ] **We accept payments separately (Square, etc.)** — No payment requirement in scheduling tool

### Q5: Per-Trainer Google Calendar Sync Critical?
- [ ] **Very — each trainer needs their schedule on their personal calendar** — R1 stays at 30%
- [ ] **Less critical — we share one business calendar** — R1 drops to 25%
- [ ] **Not needed — we use the tool's calendar only** — R1 drops to 20%

### Q6: ADA/WCAG Accessibility Required?
- [ ] **Yes — booking page must be ADA-compliant** — Disqualifies tools without accessibility compliance; R6 increases to 10%
- [ ] **No formal requirements, but want something in place** — R6 stays at 5%
- [ ] **No requirements** — R6 stays at 5%

### Q7: Current Scheduling Coordination Time?
- [ ] **Hours per week (5+)** — R2 increases to 30%; R5 increases to 15%
- [ ] **Moderate (2–5 hours/week)** — Weights stay as default
- [ ] **Minimal (under 2 hours/week)** — R2 drops to 20%

---

## Candidate Tools to Score

### Tier 1: Google Workspace + Booking Focus

| Tool | R1 (Google) | R2 (Booking/Notify) | R3 (QB Path) | R4 (Multi-trainer) | R5 (Self-Book) | R6 (Fitness) | R7 (Cost) | Weighted Score |
|------|-------------|---------------------|---------------|---------------------|----------------|--------------|-----------|-----------------|
| Calendly Pro |  |  |  |  |  |  |  |  |
| SuperSaaS |  |  |  |  |  |  |  |  |
| Setmore Pro |  |  |  |  |  |  |  |  |
| Vagaro |  |  |  |  |  |  |  |  |

### Tier 2: Google-First with QB Middleware

| Tool | R1 (Google) | R2 (Booking/Notify) | R3 (QB Path) | R4 (Multi-trainer) | R5 (Self-Book) | R6 (Fitness) | R7 (Cost) | Weighted Score |
|------|-------------|---------------------|---------------|---------------------|----------------|--------------|-----------|-----------------|
| SavvyCal |  |  |  |  |  |  |  |  |
| YouCanBookMe |  |  |  |  |  |  |  |  |

---

## Disqualifying Criteria

**Do NOT score a tool if any of these apply:**

| Criterion | Disqualified Tools |
|-----------|-------------------|
| Q1 = QuickBooks Desktop AND tool claims native QB Desktop support | Most appointment schedulers (Acuity, Setmore, Timely, Vagaro, Calendly) |
| Q6 = ADA/WCAG Required AND tool has no accessibility compliance | General-purpose tools without verified ADA compliance |

---

## Scoring Instructions

1. **Fill in the raw scores (1–5) for each tool** in the tables above based on your requirements and trial testing.
2. **The weighted score** = (R1 × 0.30) + (R2 × 0.25) + (R3 × 0.10) + (R4 × 0.15) + (R5 × 0.10) + (R6 × 0.05) + (R7 × 0.05)
3. **Adjust weights** if your Q1–Q7 answers indicate shifts (e.g., if you re-key QB, bump R3 to 15%).
4. **The highest weighted score wins.** Use sub-criteria as tie-breakers.

---

## Recommendation Template (fill after scoring)

```
RECOMMENDED TOOL: _______

Rationale: [Why this tool scored highest]

Trial Testing Notes:
- Google Calendar sync: [Tested? Result?]
- Trainer notification: [Tested? Result?]
- Client booking experience: [Tested? Result?]
- Trainer substitution flow: [Tested? Result?]
- QB export path: [Tested? Result?]
- Accessibility: [Tested? Result?]

Estimated Monthly Cost at 30 Clients: $_____

Selected QB Integration Path:
- [ ] Native sync (R3=5)
- [ ] Middleware: Zapier ($__/mo) + Make ($__/mo)
- [ ] Batch monthly export (manual)
- [ ] No QB integration needed
```

---

## Next Steps

1. **Answer Questions Q1–Q7** above
2. **Sign up for free trials** of the top 2–3 tools from the research document
3. **Score each tool** using the tables above
4. **Calculate weighted scores** and select the winner
5. **Fill in the recommendation template**
6. **Share the completed model** with Eric for final approval
