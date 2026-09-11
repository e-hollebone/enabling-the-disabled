# Calendar & Appointment Scheduling Software Research
**For: Enable the Disabled**  
**Prepared by: Eric Hollebone / Hermes Agent**  
**Date: September 10, 2026**  
**Status: Complete — research phase**  
**Workflow Context:** Booking + Google Workspace recording → batch billing in QB (no real-time QB sync required)  

---

## Executive Summary

This document compiles research on calendar and appointment scheduling solutions suitable for small-to-medium businesses. Given the **refined requirement** — appointments recorded in Google Workspace, then batch-billed in QuickBooks via "draw down or invoicing on accounts" — the **QuickBooks real-time sync requirement is DOWNGRADED** from critical to optional. The primary requirement is now:

1. **Appointment booking** with notifications to all parties (client, trainer, Shaun)
2. **Native Google Calendar / Workspace integration** (two-way sync, inventory consumption)
3. **QB integration** as a secondary convenience (batch export or manual)

The standout observation: **the QuickBooks synchronization requirement is no longer the gating factor**. Tools with excellent Google Workspace integration and client self-booking now become viable even if QB sync is via middleware or batch export.

---

## Refined Evaluation Criteria

| Priority | Requirement | Weight Impact |
|----------|-------------|---------------|
| **P1** | Native Google Calendar / Workspace two-way sync | R2 weight: 30% |
| **P1** | Appointment booking with notifications to all parties | R1 weight: 25% |
| **P2** | Client self-booking portal | R5 weight: 15% |
| **P2** | Multi-trainer coordination + substitution | R4 weight: 15% |
| **P3** | QB integration (batch/middleware acceptable) | R1 weight: 10% |
| **P3** | Fitness/disability-specific features | R3 weight: 5% |
| **P3** | Cost at scale | R6 weight: 5% |

---

## Research Sources

All findings below are grounded in the following sources (verified at time of research):

| Source | URL | Scope |
|--------|-----|-------|
| G2: Scheduling Software that Integrates with QuickBooks | `learn.g2.com/scheduling-software-that-integrates-with-quickbooks` | 11 tools, QB + appointment focus |
| Shopify: Fitness Studio Scheduling | `www.shopify.com/blog/fitness-studio-scheduling-software` | 11 fitness-specific apps |
| Ruby: 20 Integrable Scheduling Tools | `www.ruby.com/blog/20-of-the-best-small-business-appointment-scheduling-tools-and-apps/` | 20 general SMB tools |
| Zapier: Appointment Scheduling Apps | `zapier.com/blog/best-appointment-scheduling-apps/` | 5 top tools, QB via Zapier |
| Integrately: Google Calendar + QB | `integrately.com/integrations/google-calendar/quickbooks-online` | Middleware for both |
| Calendly: Google Integration | `calendly.com/integration/google` | Google Workspace deep integration |
| Setmore: QuickBooks Integration | `www.setmore.com/integrations/quickbooks` | QB-native, Google native |
| Vagaro: Google Calendar Sync | `www.vagaro.com/pro/updates/google-sync` | Fitness-specific, Google native |

---

## Tier 1: Native Google Calendar + Strong Booking (Primary Focus)

These tools excel at Google Workspace integration and appointment booking with notifications — the primary requirements now.

### 1. Calendly — Best Google Workspace Integration

**Category:** Meeting/appointment scheduling  
**Google Calendar:** Native two-way sync (up to 6 calendars)  
**QB Integration:** Via Zapier (optional)  
**Pricing:** Free tier; Pro $8–$12/user/month  
**G2 Rating:** 4.7★ (Leaders category, 8.7/10 ease of use)  

**Key Strengths:**
- **Best-in-class Google Calendar integration** — syncs across multiple calendars, prevents double-booking
- **Google Workspace deep integration** — Gmail extension, Google Meet links, Chrome extension
- **Automated notifications** — email and SMS confirmations, reminders, follow-ups via Workflows
- **Client self-booking** — branded booking pages, real-time availability
- **Google Meet integration** — auto-generates video meeting links
- **Simple, clean UI** — 9.4/10 on G2 ease-of-use scale

**Key Weaknesses:**
- **No native QB integration** — requires Zapier ($20–$100/mo)
- **Limited client database** — not a CRM
- **Payment processing** only on Pro/Business tiers (via Stripe)
- **No trainer substitution/management features**

**Google Workspace Integration Details:**
- Two-way sync with primary + 5 additional Google Calendars
- Gmail extension for one-click time slot offers
- Google Meet video conferencing integration
- Chrome extension for scheduling from any webpage
- Booking page embeds via Google Sites integration

**QB Integration Path (if needed later):**
- Zapier automation: New Calendly booking → Create Google Calendar event → Export to QB via Integrately/Zapier
- Or: End of month → Export Google Calendar events → Import to QB as invoices

**Fit for Enable the Disabled (Refined Workflow):**
- ✅ **Native Google Calendar two-way sync** (primary requirement)
- ✅ **Notifications to all parties** (email/SMS automations)
- ✅ **Client self-booking** reduces manual coordination
- ✅ **Inventory consumption** via calendar blocking (each booking occupies a time slot)
- ⚠️ QB via middleware (acceptable under new workflow — QB is batch-processed, not real-time)
- ❌ No fitness-specific features or accessibility compliance

---

### 2. SuperSaaS — Best Budget Fitness-Friendly Option

**Category:** General scheduling (fitness-friendly)  
**Google Calendar:** Native two-way sync  
**QB Integration:** Via Zapier only  
**Pricing:** From $9/month (no per-seat fees)  
**G2 Rating:** 4.6★ (82 reviews)  

**Key Strengths:**
- **Very affordable** — starting at $9/month
- **No per-seat fees** — all features included at paid tiers
- **Native Google Calendar sync** — two-way
- **Custom intake forms** — can collect accessibility needs, emergency contacts, special instructions
- **Waiting list functionality** — useful for popular slots
- **Credit system** — clients buy credits to book sessions
- **Works for fitness classes + personal training**

**Key Weaknesses:**
- QB via Zapier only (acceptable under refined workflow)
- Interface looks dated (not modern UI)
- Not fitness-specific (general purpose)

**Google Calendar Integration:** Two-way sync with Google Calendar

**QB Integration Path:** Zapier automation for batch export of appointments → QB invoices

**Fit for Enable the Disabled:**
- ✅ **Native Google Calendar sync**
- ✅ **Affordable at scale** ($9–$49/month regardless of client count)
- ✅ **Custom fields** for accessibility needs, emergency contacts
- ✅ **Waiting lists** for popular time slots
- ⚠️ QB via middleware (acceptable)
- ⚠️ Interface is dated but functional

---

### 3. Setmore — Native QB + Google, Affordable

**Category:** Appointment scheduling (SMB general)  
**Google Calendar:** Native two-way sync  
**QB Integration:** Native QB Online (one-way, add-on)  
**Pricing:** Free tier; Pro $12/month  

**Key Strengths:**
- **Native Google Calendar two-way sync**
- **Native QuickBooks Online integration** (one-way export)
- **Free tier** with basic features
- **Built-in payment processing** (credit/debit, cash)
- **Auto digital receipts** for bookings
- **Mobile apps** for iOS/Android

**Key Weaknesses:**
- QB sync is one-way (Setmore → QB)
- QB data does NOT flow back to Setmore
- Limited customization of booking page

**Google Workspace Integration:** Native two-way Google Calendar sync, booking page widgets

**QB Integration Path:** Native one-way export of appointment/payment data to QB

**Fit for Enable the Disabled:**
- ✅ **Native Google Calendar sync** (primary requirement)
- ✅ **Native QB Online export** (bonus, not critical)
- ✅ **Payment processing** for session fees
- ✅ **Affordable** ($12/month)
- ✅ **Auto receipts** — reduces manual follow-up
- ⚠️ QB Desktop not supported
- ⚠️ No fitness-specific features

---

### 4. Vagaro — Best Fitness-Specific with Google Sync

**Category:** Fitness, salon, spa business management  
**Google Calendar:** Native two-way sync (enhanced Dec 2024)  
**QB Integration:** Premium add-on (QB Online only)  
**Pricing:** $23.99–$83.99/month + QB add-on fee  
**G2 Rating:** 4.6★ (98.8% small business reviewers)  

**Key Strengths:**
- **Built for fitness studios** — class scheduling, personal training
- **Native two-way Google Calendar sync** — appointments, classes, personal tasks
- **HIPAA and EMR compliant** — relevant for health data
- **Consumer app** — 5M+ users can discover your business
- **Built-in POS and payment processing**

**Key Weaknesses:**
- QB integration is paid add-on (mixed reviews)
- Pricier than general-purpose tools ($24+/month base)
- QB sync described as "a management nightmare" by some users
- Daily export (not real-time)

**Google Workspace Integration:** Native two-way sync across appointments, classes, personal tasks per staff member

**QB Integration Path:** Premium add-on, daily export to QB Online

**Fit for Enable the Disabled:**
- ✅ **Fitness-specific** (classes, personal training, equipment booking)
- ✅ **Native Google Calendar sync** (primary requirement)
- ✅ **HIPAA/EMR compliance** (relevant for disability clients' health data)
- ⚠️ QB add-on costs extra and has mixed reviews
- ❌ Pricier ($24+/month)
- ⚠️ May be overkill for 30-client scale

---

## Tier 2: Google-First Tools with Middleware QB Path

### 5. SavvyCal — Calendly Alternative

**Category:** Meeting scheduling  
**Google Calendar:** Native (Google, Exchange, iCloud)  
**QB Integration:** Via Zapier only  
**Pricing:** $12–$20/user/month  

**Key Strengths:**
- Checks conflicts across multiple calendars
- Better UX than Calendly for some users
- Native Google, Exchange, and iCloud sync

**Key Weaknesses:**
- QB requires Zapier
- No client management features
- Not fitness-specific

**Fit for Enable the Disabled:**
- ✅ Excellent Google Calendar integration
- ⚠️ QB via middleware (acceptable under refined workflow)
- ❌ No client database or special needs tracking

---

### 6. YouCanBookMe — Budget Google Sync

**Category:** Appointment scheduling  
**Google Calendar:** Native (Google, Office 365, iCloud, CalDAV)  
**QB Integration:** Via Zapier only  
**Pricing:** Free tier; Pro $10/month  

**Fit for Enable the Disabled:**
- ⚠️ Google Calendar excellent
- ⚠️ QB via middleware (acceptable)
- ⚠️ Limited fitness features

---

## Middleware Options for QB Integration

Since the refined workflow treats QB as **batch-processed** (not real-time), these middleware tools handle the "appointments → QB invoices" handoff:

| Tool | Description | QB Integration | Google Calendar Triggers | Cost |
|------|-------------|---------------|-------------------------|------|
| **Zapier** | 5,000+ app automation platform | Create invoices, payments, customers from scheduling data | New/updated/cancelled events | $20–$100/mo |
| **Integrately** | AI-powered one-click automations | Create invoices, estimates, customers | New/updated/cancelled events | $20–$100/mo |
| **Make (Integromat)** | Visual automation platform | Full QB data sync | Calendar event triggers | $9–$99/mo |

**Workflow path:** Google Calendar events (completed appointments) → Zapier/Make → QB Online invoices (batch monthly)

---

## Comparison Matrix (Refined)

| Tool | Google Calendar | QB Path | Fitness-Specific | Notifications | Client Self-Book | Starting Price |
|------|----------------|---------|------------------|---------------|-----------------|----------------|
| **Calendly** | ✅ Native 2-way | ⚠️ Zapier | ❌ General | ✅ Built-in | ✅ Yes | $8/mo |
| **SuperSaaS** | ✅ Native 2-way | ⚠️ Zapier | ⚠️ Fitness-friendly | ✅ Email/SMS | ✅ Yes | $9/mo |
| **Setmore** | ✅ Native 2-way | ✅ Native QB | ❌ General | ✅ Built-in | ✅ Yes | $12/mo |
| **Vagaro** | ✅ Native 2-way | ⚠️ Add-on | ✅ Fitness | ✅ Built-in | ✅ Yes | $24/mo |
| **SavvyCal** | ✅ Native 2-way | ⚠️ Zapier | ❌ General | ✅ Built-in | ✅ Yes | $12/mo |
| **YouCanBookMe** | ✅ Native 2-way | ⚠️ Zapier | ❌ General | ✅ Email | ✅ Yes | $10/mo |

---

## Key Findings (Refined)

### 1. QB Real-Time Sync Is No Longer the Gating Factor
With the refined workflow (Google Workspace recording → batch QB billing), the QB integration requirement drops to secondary. This opens up 4 additional viable tools that were previously deprioritized due to QB-via-middleware.

### 2. Calendly Has the Best Google Workspace Integration
Calendly's Google integration is the most mature in the market:
- Native two-way sync across up to 6 calendars
- Gmail extension for one-click scheduling
- Google Meet integration
- Chrome extension for scheduling from any webpage
- Workflows for automated email/SMS notifications

### 3. Vagaro Is the Only Fitness-Specific Tool with Native Google Sync
Vagaro's Dec 2024 Google Calendar sync enhancement makes it the strongest fitness-specific option — it syncs appointments, classes, and personal tasks two-way with each staff member's Google Calendar.

### 4. SuperSaaS Offers Best Value for Fitness-Friendly Booking
At $9/month with no per-seat fees, SuperSaaS is the most affordable option that supports fitness classes, personal training, custom intake forms (for accessibility needs), and native Google Calendar sync.

### 5. QB Desktop Compatibility Remains a Concern
If the business uses QuickBooks Desktop (not Online), most tools will require middleware or batch export for QB integration. QB Desktop is being deprecated by Intuit in favor of QBO.

---

## Recommendations (Refined)

### Shortlist (Test in Order)

1. **Calendly (Pro)** — Best overall Google Workspace integration + client self-booking
   - ✅ Best Google Calendar integration in the market
   - ✅ Automated notifications to all parties
   - ✅ Client self-booking reduces coordination burden
   - ✅ Simple, proven UI
   - ✅ $8/month (budget-friendly)
   - ⚠️ QB via Zapier (acceptable — batch billing workflow)
   - ⚠️ 14-day Pro trial

2. **Vagaro** — Best fitness-specific tool with native Google sync
   - ✅ Fitness-specific (classes, PT, equipment booking)
   - ✅ Native Google Calendar two-way sync
   - ✅ HIPAA/EMR compliance for health data
   - ✅ Consumer app discovery (5M+ users)
   - ⚠️ $24+/month + QB add-on
   - ⚠️ QB add-on has mixed reviews (acceptable — batch workflow)
   - 30-day free trial

3. **SuperSaaS** — Best budget fitness-friendly option
   - ✅ Native Google Calendar sync
   - ✅ Very affordable ($9/month, no per-seat fees)
   - ✅ Custom intake forms (accessibility needs, emergency contacts)
   - ✅ Waiting lists for popular slots
   - ✅ Credit system for session packages
   - ⚠️ QB via Zapier (acceptable)
   - ⚠️ Interface is dated
   - Free tier available

4. **Setmore** — Best if native QB export is valuable
   - ✅ Native Google Calendar two-way sync
   - ✅ Native QB Online integration (one-way export)
   - ✅ Built-in payment processing
   - ✅ Auto digital receipts
   - ⚠️ QB is one-way only (acceptable for batch workflow)
   - $12/month

---

## Open Questions for Shaun

Based on the requirements document (`enable-the-disabled-scheduling-requirements-questions.md`):

1. **Google Workspace usage:** Is the business currently using Google Workspace (Gmail, Calendar, Drive)? If not, this needs to be set up first.

2. **QB edition:** QuickBooks Online or Desktop? If Desktop, most native QB integrations are unsupported — batch export may be the only path.

3. **Client self-booking:** Should clients be able to self-book online, or does all booking go through Shaun? (Affects whether Calendly/Vagaro's self-booking is needed.)

4. **Trainer calendar sync:** How critical is it that each trainer's schedule auto-syncs to their personal Google Calendar? (Vagaro and Calendly both do this natively.)

5. **Batch QB billing frequency:** How often is QuickBooks billing generated — weekly, monthly, or per-campaign? (This determines the QB export workflow complexity.)

6. **Accessibility features:** Are there WCAG/ADA requirements for the booking page? If so, Vagaro's HIPAA compliance is closest, but general tools may need a WordPress plugin like SimplyBook.

7. **Current manual coordination:** How much time is currently spent on scheduling coordination (texts, calls back and forth)? A quantified estimate helps justify the tool investment.

---

## Next Steps

1. **Answer the 7 questions** above
2. **Select 1–2 shortlist tools** based on answers
3. **Sign up for free trials** of the top candidates
4. **Test Google Calendar sync** with 2–3 appointments
5. **Test notification workflow** (client booking → trainer notified → Shaun notified)
6. **Test QB export path** (if batch QB billing is the workflow)
7. **Evaluate the full cycle** with a real client + trainer + Shaun scenario

---

*Sources archived to `/home/hermes/.hermes/profiles/fitness-strategist/cache/web/` for reference. Full-page extracts available for deep review.*
