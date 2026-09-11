# Calendar & Appointment Software Evaluation Model

**For:** Enable the Disabled scheduling tool selection  
**Prepared by:** Eric Hollebone / Hermes Agent  
**Date:** September 10, 2026  
**Status:** Draft — ready for Shaun answers  

---

## Purpose

This document defines the evaluation criteria and scoring model for comparing calendar/appointment scheduling solutions. It translates the business requirements (from `enable-the-disabled-scheduling-requirements-questions.md`) into a structured fit-assessment framework.

The model is designed to be **scored by you (Shaun)** once you've reviewed the [research document](calendar-appointment-software-research.md) and tested free trials.

---

## How to Use

1. **Read the research document** first (`calendar-appointment-software-research.md`)
2. **Answer Questions 1–6** below
3. **Score each candidate tool** against the criteria (1–5 scale)
4. **Weighted score** is calculated automatically in the comparison matrix
5. The tool with the highest weighted score is the recommended choice

---

## Requirement Categories

### R1. QuickBooks Integration (Weight: 25%)

**Why it matters:** The business uses QuickBooks for accounting. Any scheduling tool that requires manual re-entry of appointments → invoices is a non-starter for efficiency gains.

| Score | Meaning |
|-------|---------|
| 5 | Native QuickBooks Online sync (automatic, ongoing) |
| 4 | Native QuickBooks Desktop sync (automatic, ongoing) |
| 3 | QuickBooks sync via middleware (Zapier/Integrately), reliable |
| 2 | QuickBooks sync via middleware, but with known reliability issues |
| 1 | No QB sync possible |

**Sub-criteria (tie-breaker):**
- Sync direction (two-way preferred but one-way acceptable)
- Data synced (customers, invoices, payments, taxes, timesheets)
- Tier requirement (QB sync on entry tier vs. higher tier)

---

### R2. Google Calendar / Workspace Integration (Weight: 20%)

**Why it matters:** The business uses Google Workspace (Gmail, Calendar, Drive). Two-way calendar sync prevents double-booking and gives each trainer visibility into their schedule on their personal calendar.

| Score | Meaning |
|-------|---------|
| 5 | Native two-way Google Calendar sync across all calendars |
| 4 | Native one-way sync (tool → Google Calendar) |
| 3 | Google Calendar sync via middleware (Zapier/Integrately) |
| 2 | Limited Google Calendar sync (manual export/import) |
| 1 | No Google Calendar integration |

**Sub-criteria (tie-breaker):**
- Staff calendar sync (each trainer's schedule syncs to personal Google Calendar)
- Booking page calendar embedding
- Event detail sync depth (appointment notes, client info, location)

---

### R3. Fitness / Disability-Specific Fit (Weight: 20%)

**Why it matters:** Enable the Disabled serves clients with disabilities requiring wheelchair access, noise sensitivity accommodations, special instructions, and guardian contact info. The tool must support these requirements.

| Score | Meaning |
|-------|---------|
| 5 | Built for fitness/disability services; native accessibility support |
| 4 | Fitness-specific with good customization for special requirements |
| 3 | General-purpose tool with adequate customization (notes, intake forms) |
| 2 | General-purpose tool with limited customization |
| 1 | No accommodation for special needs |

**Sub-criteria (tie-breaker):**
- Custom intake forms / client notes fields
- Emergency contact storage
- Booking page with accessibility features (WCAG/ADA compliance)
- HIPAA/EMR compliance for health data

---

### R4. Multi-Trainer Coordination (Weight: 15%)

**Why it matters:** The business currently has Sean + Charlotte as trainers, with potential for growth. The tool must handle trainer assignments, substitutions, and individual calendar visibility.

| Score | Meaning |
|-------|---------|
| 5 | Native multi-trainer support; trainer-specific calendars, substitution flow |
| 4 | Good multi-trainer support; some manual coordination for substitutions |
| 3 | Basic multi-trainer support (calendar sharing only) |
| 2 | Single-trainer design; workarounds needed |
| 1 | No multi-trainer support |

**Sub-criteria (tie-breaker):**
- Trainer assignment to clients (fixed vs. floating)
- Substitution / handoff workflow
- Staff portal for schedule viewing
- Per-trainer availability management

---

### R5. Client Self-Booking & Payment Processing (Weight: 10%)

**Why it matters:** Reducing manual booking coordination is a goal. Payment processing in the tool reduces invoicing overhead.

| Score | Meaning |
|-------|---------|
| 5 | Native client self-booking portal + built-in payment processing |
| 4 | Self-booking + payment processing via integration |
| 3 | Self-booking only; payments handled separately (QB invoices) |
| 2 | No self-booking; manual booking required |
| 1 | No booking portal at all |

**Sub-criteria (tie-breaker):**
- Deposit acceptance for bookings
- Cancellation policy enforcement
- Refund handling
- Payment method options (card, cash, PayPal, etc.)

---

### R6. Cost at Scale (Weight: 10%)

**Why it matters:** Current revenue ~$204K/yr from 30 clients. The tool must be affordable at current scale and projectable for growth to 40–50 clients.

| Score | Meaning |
|-------|---------|
| 5 | Under $25/month at 30-client scale; scales affordably |
| 4 | $25–$50/month at 30-client scale; reasonable scaling |
| 3 | $50–$100/month at 30-client scale; acceptable |
| 2 | $100–$200/month at 30-client scale; expensive but justified |
| 1 | Over $200/month at 30-client scale; cost-prohibitive |

**Sub-criteria (tie-breaker):**
- Per-user fees (some tools charge per staff member)
- Per-booking fees
- Setup/onboarding fees
- Hidden costs (QB add-on fees, middleware subscriptions)

---

## Questions That Shape the Model

These answers determine how you should weight the criteria above and whether certain tools are disqualified:

### Q1: QuickBooks Edition
- [ ] **QuickBooks Online (QBO)** — Most appointment tools supported. Keep R1 as-is.
- [ ] **QuickBooks Desktop** — Disqualifies Acuity, Setmore, Timely, Vagaro, Calendly-native. Only ServiceTitan, Housecall Pro, Workiz qualify. May need to reconsider.
- [ ] **Not sure** — Test with a QBO account first.

### Q2: Current Manual QB Re-entry
- [ ] **Yes, we re-key everything** — R1 (QB Integration) weight should increase to 30%
- [ ] **No, we don't use scheduling→QB** — R1 weight stays at 25%, but QB integration is still valuable
- [ ] **We don't use QuickBooks at all** — R1 is irrelevant; remove or set to 0%

### Q3: Public Self-Booking Needed?
- [ ] **Yes, clients should self-book online** — R5 weight stays at 10%
- [ ] **No, all booking goes through me** — R5 weight drops to 5%; focus shifts to internal coordination
- [ ] **Hybrid (some self, some manual)** — R5 stays at 10%

### Q4: Payment Processing Needed In-Tool?
- [ ] **Yes, we need payments in the scheduling tool** — R5 weight stays at 10%
- [ ] **No, we invoice via QB only** — R5 drops to 5%; tools without payments are fine
- [ ] **We accept payments separately (Square, etc.)** — R5 stays at 10% but sub-criteria shift

### Q5: Per-Trainer Google Calendar Sync Critical?
- [ ] **Very — each trainer needs their schedule on their personal calendar** — R2 weight stays at 20%
- [ ] **Less critical — we share one business calendar** — R2 weight drops to 15%
- [ ] **Not needed — we don't use personal calendars** — R2 is irrelevant

### Q6: ADA/WCAG Accessibility Required?
- [ ] **Yes — booking page must be screen-reader compatible** — Eliminates tools without accessibility compliance
- [ ] **No formal requirements, but want something in place** — R3 sub-criteria matter
- [ ] **No requirements** — R3 stays general (special needs accommodation only)

---

## Candidate Tools to Score

Score each on R1–R6 (1–5), then the weighted total is calculated:

### Tier A Candidates (Native QB)

| Tool | R1 (QB) | R2 (Google) | R3 (Fitness) | R4 (Multi-trainer) | R5 (Booking/Pay) | R6 (Cost) | Weighted Score |
|------|---------|-------------|--------------|--------------------|-------------------|-----------|-----------------|
| Acuity Scheduling |  |  |  |  |  |  |  |
| Setmore |  |  |  |  |  |  |  |
| Timely |  |  |  |  |  |  |  |
| Jobber |  |  |  |  |  |  |  |

### Tier C Candidates (Fitness-Specific)

| Tool | R1 (QB) | R2 (Google) | R3 (Fitness) | R4 (Multi-trainer) | R5 (Booking/Pay) | R6 (Cost) | Weighted Score |
|------|---------|-------------|--------------|--------------------|-------------------|-----------|-----------------|
| Vagaro |  |  |  |  |  |  |  |

### Tier B Candidates (Native Google, QB via middleware)

| Tool | R1 (QB) | R2 (Google) | R3 (Fitness) | R4 (Multi-trainer) | R5 (Booking/Pay) | R6 (Cost) | Weighted Score |
|------|---------|-------------|--------------|--------------------|-------------------|-----------|-----------------|
| Calendly |  |  |  |  |  |  |  |
| SavvyCal |  |  |  |  |  |  |  |

---

## Disqualifying Criteria

**Do NOT score a tool if any of these apply:**

| Criterion | Disqualified Tools |
|-----------|-------------------|
| **Q1 = QuickBooks Desktop** | Acuity, Setmore, Timely, Vagaro, Calendly, SavvyCal, WellnessLiving, Mindbody, Zen Planner, Glofox, SuperSaaS |
| **Q6 = ADA/WCAG Required** | Any tool without confirmed accessibility compliance (most general-purpose tools) |
| **Q3 = No public booking needed + tool is consumer-facing only** | Calendly, SavvyCal (no client database) |

---

## Scoring Instructions

1. **Fill in the raw scores (1–5) for each tool** in the tables above based on your requirements and trial testing.
2. **The weighted score** = (R1 × 0.25) + (R2 × 0.20) + (R3 × 0.20) + (R4 × 0.15) + (R5 × 0.10) + (R6 × 0.10)
3. **Adjust weights** if your Q1–Q6 answers indicate shifts (e.g., if you re-key QB, bump R1 to 30%).
4. **The highest weighted score wins.** Use sub-criteria as tie-breakers.

---

## Recommendation Template (to be filled after scoring)

```
RECOMMENDED TOOL: _______

Rationale: [Why this tool scored highest]

Trial Testing Notes:
- QB sync: [Tested? Result?]
- Google Calendar sync: [Tested? Result?]
- Client booking experience: [Tested? Result?]
- Trainer substitution flow: [Tested? Result?]
- Payment processing: [Tested? Result?]
- Accessibility: [Tested? Result?]

Estimated Monthly Cost at 30 Clients: $_____
```

---

## Next Steps

1. **Answer Questions Q1–Q6** above
2. **Sign up for free trials** of the top 2–3 tools that pass disqualifying criteria
3. **Score each on R1–R6** using the tables
4. **Calculate weighted scores** and select the winner
5. **Update this document** with the final scores and recommendation
6. **Share the result** with Shaun for final approval
