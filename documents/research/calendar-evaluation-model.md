# Calendar & Appointment Software Evaluation Model

**For:** Enable the Disabled scheduling tool selection  
**Prepared by:** Eric Hollebone / Hermes Agent  
**Date:** September 10, 2026  
**Status:** Draft — ready for Shaun to fill in  
**Workflow:** Booking + native phone calendar → notifications → batch billing in QB  
**QuickBooks Edition:** Online (QBO) — confirmed by user  

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

> **Weights auto-adjust based on your Q1–Q7 answers.** Default weights assume native mobile phone calendar is the primary requirement.

| # | Category | Default Weight | What It Measures |
|---|----------|----------------|-----------------|
| **R1** | Native Mobile Phone Calendar Sync | **35%** | Syncs appointments to iOS Calendar (iPhone), Android Calendar, or Google Calendar app on mobile |
| **R2** | Booking + Notifications | **25%** | Client self-booking, automated notifications to client + trainer + admin |
| **R3** | QB Integration Path | **10%** | QB Online export/sync path (batch/middleware acceptable) |
| **R4** | Multi-Trainer Coordination | **15%** | Trainer assignments, substitutions, per-trainer calendar access |
| **R5** | Client Self-Booking | **10%** | Public booking page with real-time availability |
| **R6** | Fitness/Disability Fit | **5%** | Accessibility features, custom intake forms, health data compliance |
| **R7** | Cost at Scale | **5%** | Monthly cost at 30–50 client scale |

---

## Scoring Rubrics

### R1: Native Mobile Phone Calendar Sync (35%) — PRIMARY REQUIREMENT

**This is the most critical criteria.** The tool must sync appointments to the actual calendar app on trainers' phones.

| Score | Meaning |
|-------|---------|
| 5 | Two-way sync to iOS Calendar AND Android Calendar natively (not via Google Calendar app) |
| 4 | Sync to iOS Calendar OR Android Calendar natively (one platform only) |
| 3 | Sync to Google Calendar app on mobile (requires Google Calendar app installed, not native iOS/Android calendar) |
| 2 | Sync via iCal URL subscription (1-way, manual setup) |
| 1 | No mobile calendar sync |

**Sub-criteria (tie-breaker):** Two-way vs 1-way, iOS + Android both supported, offline access

---

### R2: Booking + Notifications (25%)

| Score | Meaning |
|-------|---------|
| 5 | Client books → trainer notified → Shaun notified; confirmations, reminders, follow-ups automated |
| 4 | Client books → trainer + Shaun notified; confirmations + reminders; no follow-ups |
| 3 | Client books → trainer notified; basic email confirmation |
| 2 | Booking request sent to admin; manual notification to others |
| 1 | No automated notifications |

**Sub-criteria (tie-breaker):** SMS option, timezone handling, cancellation notifications, custom templates

---

### R3: QuickBooks Integration Path (10%)

> **Under the batch billing workflow, this is a convenience, not a requirement.** Any path that gets appointment data into QB is acceptable.

| Score | Meaning |
|-------|---------|
| 5 | Native QB Online sync (automatic) |
| 4 | Native QB Online export (one-way, can be batched) |
| 3 | QB via reliable middleware (Zapier/Make, well-tested) |
| 2 | QB via middleware, but with known issues |
| 1 | No QB integration path |

**Sub-criteria (tie-breaker):** Data synced (customers, invoices, payments), export frequency, sync direction

---

### R4: Multi-Trainer Coordination (15%)

| Score | Meaning |
|-------|---------|
| 5 | Trainer assignments, substitution workflow, per-trainer calendar sync, staff portal |
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

**Sub-criteria (tie-breaker):** Custom URL, embed code, branding options, mobile responsiveness

---

### R6: Fitness / Disability Fit (5%)

| Score | Meaning |
|-------|---------|
| 5 | Built for fitness with accessibility features (custom intake, emergency contacts, HIPAA) |
| 4 | General-purpose tool with good custom fields for special needs |
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
| 2 | $80–$150/month at 30-client scale; high but justifiable |
| 1 | Over $150/month at 30-client scale; cost-prohibitive |

**Sub-criteria (tie-breaker):** Per-user fees, per-booking fees, setup fees, hidden costs (QB add-on, middleware)

---

## Questions That Shape the Model

These answers determine weight adjustments and disqualifying criteria:

### Q1: Phone Calendar Preference
- [ ] **Native iOS Calendar app on iPhone** — Must sync to iOS Calendar natively. Rules out Calendly, SuperSaaS, SimplyBook.
- [ ] **Native Android Calendar app** — Must sync to Android Calendar natively.
- [ ] **Google Calendar app on both iOS and Android** — Calendly, SuperSaaS, and SimplyBook become viable.

### Q2: Current Manual QB Re-entry
- [ ] **Yes, we re-key everything** — R3 increases to 15%
- [ ] **No, we don't re-key** — R3 stays at 10%
- [ ] **We don't use QB for billing yet** — R3 drops to 0%

### Q3: Client Self-Booking Needed?
- [ ] **Yes, clients should self-book online** — R5 stays at 10%
- [ ] **No, all booking goes through me** — R5 drops to 5%
- [ ] **Hybrid** — R5 stays at 10%

### Q4: Trainer Substitution Frequency
- [ ] **Frequent (weekly or more)** — R4 stays at 15%
- [ ] **Occasional (monthly)** — R4 drops to 10%
- [ ] **Rare (less than monthly)** — R4 drops to 5%

### Q5: ADA/WCAG Accessibility Required?
- [ ] **Yes — booking page must be ADA-compliant** — R6 increases to 10%; disqualifies non-compliant tools
- [ ] **No formal requirements, but want something in place** — R6 stays at 5%
- [ ] **No requirements** — R6 stays at 5%

### Q6: Current Weekly Scheduling Coordination Time?
- [ ] **5+ hours/week** — R2 increases to 30%; R4 increases to 20%
- [ ] **2–5 hours/week** — Weights stay as default
- [ ] **Under 2 hours/week** — R2 drops to 20%

### Q7: Batch QB Billing Frequency?
- [ ] **Weekly** — QB export needs to be fast/reliable (R3 weight +5%)
- [ ] **Monthly** — QB export can be batch/manual (R3 stays at 10%)
- [ ] **Per-campaign/event** — QB export needs to be event-triggered (R3 weight +5%)

---

## Candidate Tools to Score

> **Disqualified based on Q1 (phone calendar preference):**
> - If Q1 = Native iOS Calendar: Calendly, SuperSaaS, SavvyCal, YouCanBookMe, SimplyBook are DISQUALIFIED (no native iOS Calendar sync)
> - If Q1 = Native Android Calendar: Calendly, SuperSaaS, SavvyCal, YouCanBookMe, SimplyBook are DISQUALIFIED (sync is via Google Calendar app, not native Android Calendar)
> - If Q1 = Google Calendar app: All tools are eligible (Calendly, SuperSaaS, etc. work if Google Calendar app is used on phone)
>
> **No QB Desktop disqualification** — QuickBooks Online confirmed. All tools supporting QBO export are eligible.

### Tier 1 Candidates (Native Mobile Calendar Support)

| Tool | R1 (Calendar) | R2 (Booking/Notify) | R3 (QB Path) | R4 (Multi-trainer) | R5 (Self-Book) | R6 (Fitness) | R7 (Cost) | Weighted Score |
|------|---------------|---------------------|---------------|---------------------|----------------|--------------|-----------|-----------------|
| **Vagaro** |  |  |  |  |  |  |  |  |
| **Jobber** |  |  |  |  |  |  |  |  |
| **Trafft** |  |  |  |  |  |  |  |  |
| **HoneyBook** |  |  |  |  |  |  |  |  |
| **Setmore** |  |  |  |  |  |  |  |  |

### Tier 2 Candidates (Google Calendar App Only — valid if Q1 = Google Calendar app)

| Tool | R1 (Calendar) | R2 (Booking/Notify) | R3 (QB Path) | R4 (Multi-trainer) | R5 (Self-Book) | R6 (Fitness) | R7 (Cost) | Weighted Score |
|------|---------------|---------------------|---------------|---------------------|----------------|--------------|-----------|-----------------|
| **Calendly** |  |  |  |  |  |  |  |  |
| **SuperSaaS** |  |  |  |  |  |  |  |  |

---

## Scoring Instructions

1. **Fill in the raw scores (1–5) for each tool** in the tables above based on your requirements and trial testing.
2. **The weighted score** = (R1 × 0.35) + (R2 × 0.25) + (R3 × 0.10) + (R4 × 0.15) + (R5 × 0.10) + (R6 × 0.05) + (R7 × 0.05)
3. **Adjust weights** if your Q1–Q7 answers indicate shifts.
4. **The highest weighted score wins.** Use sub-criteria as tie-breakers.

---

## Recommendation Template (fill after scoring)

```
RECOMMENDED TOOL: _______

Rationale: [Why this tool scored highest]

Trial Testing Notes:
- Mobile calendar sync: [Tested on which phone OS? Result?]
- Trainer notification: [Tested? Result?]
- Client booking experience: [Tested? Result?]
- Trainer substitution flow: [Tested? Result?]
- QB export path: [Tested? Result?]
- Accessibility: [Tested? Result?]

Estimated Monthly Cost at 30 Clients: $_____

Selected QB Export Path:
- [ ] Native QB sync (R3=5)
- [ ] Native QB one-way export (R3=4)
- [ ] Middleware: Zapier ($__/mo) + QB
- [ ] Batch monthly export (manual CSV import)
- [ ] No QB integration needed
```

---

## Next Steps

1. **Answer Questions Q1–Q7** above
2. **Eliminate disqualified tools** based on Q1 answer
3. **Sign up for free trials** of remaining Tier 1 candidates
4. **Test mobile calendar sync** on actual iOS/Android device(s) used by the team
5. **Score each tool** using the tables above
6. **Calculate weighted scores** and select the winner
7. **Fill in the recommendation template**
8. **Share the completed model** with Eric for final approval
