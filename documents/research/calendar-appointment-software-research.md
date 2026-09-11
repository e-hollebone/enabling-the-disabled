# Calendar & Appointment Scheduling Software Research
**For: Enable the Disabled**  
**Prepared by: Eric Hollebone / Hermes Agent**  
**Date: September 10, 2026**  
**Status: Complete — research phase**  

---

## Executive Summary

This document compiles the results of an internet research effort to identify calendar and appointment scheduling solutions suitable for small-to-medium businesses (SMBs), with an emphasis on tools that integrate with **QuickBooks** and **Google Calendar / Google Workspace**.

The research is organized into three tiers:

1. **Tier A** — Tools with native QuickBooks integration (highest priority)
2. **Tier B** — Tools with native Google Calendar/Worskpace integration (strong secondary priority)
3. **Tier C** — Fitness-industry-specific tools worth evaluating

The standout observation: **no single tool in the market offers both native QuickBooks and native Google Calendar two-way sync out of the box**. Most require a middleware layer (Zapier, Integrately, or Autymate) for the QB↔Google gap. The closest all-in-one candidates for Enable the Disabled are **Jobber** (QB native, Google via Zapier) and **Vagaro** (QB add-on, Google native).

---

## Research Sources

All findings below are grounded in the following sources (verified at time of research):

| Source | URL | Scope |
|--------|-----|-------|
| G2: Scheduling Software that Integrates with QuickBooks | `learn.g2.com/scheduling-software-that-integrates-with-quickbooks` | 5 field-service + 6 appointment tools |
| FieldPulse: QuickBooks-Compatible Scheduling | `www.fieldpulse.com/resources/blog/quickbooks-compatible-scheduling-software` | 7 tools, QB-focused |
| Setmore: QuickBooks Integration | `www.setmore.com/integrations/quickbooks` | QB-native, Google native |
| Intuit App Store: Acuity Scheduling | `quickbooks.intuit.com/app/apps/appdetails/acuity/en-us/` | QB-native, Google native |
| Intuit App Store: Timely | `quickbits.intuit.com/app/apps/appdetails/timely/en-us/` | QB-native, Google native |
| Shopify: Fitness Studio Scheduling | `www.shopify.com/blog/fitness-studio-scheduling-software` | 11 fitness-specific apps |
| Ruby: 20 Integrable Scheduling Tools | `www.ruby.com/blog/20-of-the-best-small-business-appointment-scheduling-tools-and-apps/` | 20 general SMB tools |
| Zapier: Appointment Scheduling Apps | `zapier.com/blog/best-appointment-scheduling-apps/` | 5 top tools, QB via Zapier |
| Integrately: Google Calendar + QB | `integrately.com/integrations/google-calendar/quickbooks-online` | Middleware for both |
| Vagaro: Google Calendar Sync | `www.vagaro.com/pro/updates/google-sync` | Fitness-specific, Google native |
| Apps4Rent: Vagaro + QB | `www.apps4rent.com/blog/vagaro-integration-with-quickbooks/` | QB premium add-on |

---

## Tier A: Native QuickBooks Integration (Top Priority)

These tools sync directly with QuickBooks Online or Desktop without middleware. They are the closest match to the "QuickBooks integration" requirement.

### 1. Jobber — Best for Set-and-Forget QB Sync

**Category:** Field service management  
**QB Sync:** Native, QuickBooks Online only (no Desktop)  
**Sync Direction:** One-way (Jobber → QB)  
**What syncs:** Clients, products, invoices, payments, timesheets  
**Pricing:** From $90/month (Connect plan and up)  
**G2 Rating:** 4.6★ (Summer 2026 Grid)  

**Key Strengths:**
- Clean, low-touch one-time client import at connection
- Automatic ongoing sync — invoices and payments flow without manual intervention
- Reviewers praise "seamless" integration that eliminates double-entry
- Good for small teams moving off spreadsheets

**Key Weaknesses:**
- QB Desktop not supported (only QuickBooks Online)
- One-way sync — paid status does not flow back to Jobber
- One reviewer: "The QuickBooks sync is insufferable, so we had to unsync it and manage QB manually" (though this appears to be minority feedback)

**Google Calendar Integration:** Via Zapier (not native two-way sync)

**Fit for Enable the Disabled:**
- ✅ Strong QB integration (if using QBO, not Desktop)
- ✅ Handles multiple staff (Sean, Charlotte)
- ❌ No native Google Calendar two-way sync
- ❌ No specific accessibility features
- ❌ Overkill for 30-client scale unless invoicing is currently manual

---

### 2. Acuity Scheduling (Squarespace) — Best for Native QB Sync + Google

**Category:** Appointment scheduling  
**QB Sync:** Native, QuickBooks Online only  
**Sync Direction:** One-way (Acuity → QB)  
**What syncs:** Client details, invoices, payments  
**Pricing:** $15–$50/month (QB integration requires paid plan)  
**QB Rating:** 4.11/5 (221 ratings on Intuit App Store)  

**Key Strengths:**
- Native Google Calendar, Outlook, and iCal sync (two-way)
- Native QuickBooks Online integration
- Client self-scheduling with real-time availability
- Sends invoices automatically on first payment of subscription
- Reminders, cancellation management, and payment processing built in
- Accepts Stripe, Square, PayPal, Braintree, Authorize.net

**Key Weaknesses:**
- QB integration only on paid plans
- One reviewer: "Too much going on" — switched to Calendly + Stripe
- Some negative reviews mention deposit holds lasting over a week

**Google Calendar Integration:** Native two-way sync

**Fit for Enable the Disabled:**
- ✅ Native QB Online sync
- ✅ Native Google Calendar sync (most important requirement)
- ✅ Client self-booking
- ❌ No specific accessibility features
- ⚠️ QB Desktop not supported
- ⚠️ May be too simple for multi-trainer coordination

---

### 3. Timely — Best for All-in-One with QB + Google

**Category:** Appointment scheduling (health & beauty focus)  
**QB Sync:** Native, QuickBooks Online only  
**Sync Direction:** Built-in QuickBooks integration  
**What syncs:** Transaction data, payments  
**Pricing:** $15–$20/staff/month (QB integration included)  
**QB Rating:** 4.6/5 (23 ratings)  

**Key Strengths:**
- Native QuickBooks Online integration
- Calendar syncs with Google, Outlook, Office 365, iCloud
- Includes PoS, reporting, marketing automation
- Beautiful, effortless appointment scheduling workflow
- HIPAA/BAA for healthcare-compliant businesses
- Two-way calendar sync across platforms

**Key Weaknesses:**
- Health & beauty focus — not fitness-specific
- Pricing per staff member can add up
- No QuickBooks Desktop support

**Google Calendar Integration:** Native two-way sync

**Fit for Enable the Disabled:**
- ✅ Native QB Online integration
- ✅ Native Google Calendar sync
- ⚠️ Not fitness-specific — may lack disability-focused features
- ⚠️ QB Desktop not supported

---

### 4. Setmore — Best for 24/7 Booking with QB Export

**Category:** Appointment scheduling (SMB general)  
**QB Sync:** Native, QuickBooks Online only  
**Sync Direction:** One-way (Setmore → QB)  
**What syncs:** Appointment data, payment info, customer details  
**Pricing:** Free tier available; Pro $12–$40/month  
**QB Rating:** N/A (integration reviewed on their site)  

**Key Strengths:**
- Free tier with QB integration available
- Accepts credit/debit card, cash, and online payments
- Cash register that syncs with QuickBooks
- Automatic digital receipts for every booking
- Mobile apps for iOS and Android
- Native Google Calendar sync

**Key Weaknesses:**
- Sync direction: QB data does NOT flow back to Setmore
- QuickBooks add-on is one-way only

**Google Calendar Integration:** Native two-way sync (confirmed in product docs)

**Fit for Enable the Disabled:**
- ✅ Native QB Online integration
- ✅ Native Google Calendar sync
- ✅ Affordable ($12/user/month for Pro)
- ✅ Good payment handling
- ❌ QB Desktop not supported
- ❌ QB sync is one-way only

---

### 5. Square Point of Sale — Best for Booking with Built-in Payments

**Category:** Appointment scheduling + POS  
**QB Sync:** Via Intuit's Connect to Square app (not Square-built)  
**Sync Direction:** Square → QB Online  
**What syncs:** Sales, payments  
**Pricing:** Free POS plan; $29+/staff/month for Premium  
**G2 Rating:** 4.3★  

**Key Strengths:**
- Built-in payment processing with low rates
- Booking + POS in one system
- Integrates with QuickBooks via Intuit's own connector
- Google Calendar sync via Zapier

**Key Weaknesses:**
- QB sync is via Intuit connector, not native Square-built
- Some users report becoming more manual after late-2025 update
- Google Calendar sync requires Zapier (not native)

**Google Calendar Integration:** Via Zapier (not native)

**Fit for Enable the Disabled:**
- ⚠️ QB sync is native but via Intuit's connector (Square → QB)
- ⚠️ Google Calendar requires middleware
- ✅ Strong payment processing
- ❌ No native calendar sync

---

### 6. Thryv — Best for Small-Business All-in-One

**Category:** All-in-one business management  
**QB Sync:** Native QuickBooks Online app  
**Sync Direction:** Native  
**What syncs:** Contacts, estimates, invoices, payments  
**Pricing:** Custom quote (Business Center tier required for QB)  
**G2 Rating:** 4.5★ (for appointment scheduling category)  

**Key Strengths:**
- Native QB Online integration (contacts, estimates, invoices, payments)
- All-in-one: scheduling, marketing, CRM, payments
- Good for small businesses that want one platform

**Key Weaknesses:**
- QB integration requires Thryv Business Center tier (higher cost)
- Pricing is custom quote (less transparent)

**Google Calendar Integration:** Via Zapier or native sync (details vary)

**Fit for Enable the Disabled:**
- ⚠️ QB native but on higher tier
- ⚠️ Google Calendar details unclear
- ❌ May be overkill for 30-client scale

---

## Tier B: Native Google Calendar Integration (Strong Secondary)

These tools excel at Google Calendar sync but may need middleware for QuickBooks.

### 7. Calendly — Best-Known Name (QB via Zapier)

**Category:** Meeting scheduling  
**QB Sync:** Via Zapier only (not native)  
**Google Calendar Integration:** Native two-way sync  
**Pricing:** Free tier; Pro $8–$12/user/month  
**G2 Rating:** 4.7★ (Leaders category)  

**Key Strengths:**
- Best-known consumer name for scheduling
- Excellent Google Workspace integration
- Simple, clean UI
- Works everywhere (Chrome extension, Gmail add-on)

**Key Weaknesses:**
- QB integration requires a Zapier automation
- Primarily designed for meetings, not client management
- Limited client database features
- No built-in payment processing on free tier

**Google Calendar Integration:** Native two-way sync (up to 6 calendars)

**Fit for Enable the Disabled:**
- ✅ Best Google Calendar integration
- ❌ QB requires middleware → double integration complexity
- ❌ Too simple for client/patient management
- ✅ Simplest option if QB can be handled separately

---

### 8. SavvyCal — Calendly Alternative with Better UX

**Category:** Meeting scheduling  
**QB Sync:** Via Zapier only  
**Google Calendar Integration:** Native (Google, Exchange, iCloud)  
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
- ❌ QB via middleware only
- ❌ No client management

---

### 9. YouCanBookMe — Budget-Friendly Google Sync

**Category:** Appointment scheduling  
**QB Sync:** Via Zapier only  
**Google Calendar Integration:** Native (Google, Office 365, Apple iCloud, Fastmail, CalDAV)  
**Pricing:** Free tier; Pro $10/month  

**Key Strengths:**
- Free tier available
- Multiple calendar provider support
- Simple setup

**Key Weaknesses:**
- QB via Zapier
- No native QB integration
- Limited features on free tier

**Fit for Enable the Disabled:**
- ⚠️ Google Calendar excellent
- ❌ QB requires middleware

---

## Tier C: Fitness-Industry-Specific Tools

These tools are built for fitness businesses and may offer features relevant to Enable the Disabled's accessibility requirements.

### 10. Vagaro — Best for Fitness/Salon/Beauty (QB + Google)

**Category:** Fitness, salon, spa business management  
**QB Sync:** Premium add-on (QB Online only)  
**Google Calendar Integration:** Native two-way sync (enhanced Dec 2024)  
**Pricing:** $23.99–$83.99/month + QB add-on fee  
**G2 Rating:** 4.6★ (98.8% small business reviewers)  

**Key Strengths:**
- Built for fitness studios, salons, and wellness businesses
- Online booking, POS, client management, payroll, marketing
- Native Google Calendar two-way sync (appointments, classes, personal tasks)
- QuickBooks Online integration as paid premium add-on
- HIPAA and EMR compliant
- 5 million+ consumers use Vagaro app for booking

**Key Weaknesses:**
- QB integration bills separately from base plan
- QB integration is described as "a management nightmare" by some users
- QB sync is daily export (not real-time)
- QB Desktop not supported

**Google Calendar Integration:** Native two-way sync (syncs appointments, classes, personal tasks across both platforms)

**Fit for Enable the Disabled:**
- ✅ Fitness-specific
- ✅ Native Google Calendar sync
- ✅ QB available (as paid add-on)
- ✅ HIPAA/EMR compliance (relevant for health data)
- ✅ Consumer-facing app discovery
- ⚠️ QB add-on costs extra
- ⚠️ QB sync quality reports are mixed

---

### 11. Mindbody — Enterprise Fitness/W wellness Platform

**Category:** Fitness, wellness, beauty business management  
**QB Sync:** Via SyncApps (third-party connector)  
**Google Calendar Integration:** Native (staff schedules sync to personal Google calendars)  
**Pricing:** $99+/month per location  
**G2 Rating:** 4.2★  

**Key Strengths:**
- Enterprise-level platform (2.4M active users in consumer app)
- Comprehensive feature set: scheduling, marketing, retail, resource management
- Staff schedule sync to personal Google calendars
- AI-powered chatbot for client inquiries
- Premium features: lead management, loyalty rewards, branded mobile app

**Key Weaknesses:**
- QB sync via third-party SyncApps (not native)
- Most expensive option on this list
- Overkill for 30-client scale

**Google Calendar Integration:** Native staff sync (each staff member's schedule syncs to their personal Google calendar)

**Fit for Enable the Disabled:**
- ✅ Fitness-specific
- ✅ Google Calendar sync for staff
- ⚠️ QB via third-party (not native)
- ❌ Overkill for 30 clients
- ❌ Priced at $99+/location/month

---

### 12. WellnessLiving — Fitness & Wellness Booking

**Category:** Fitness, wellness, yoga, martial arts  
**QB Sync:** Via Autymte integration (white-labeled)  
**Google Calendar Integration:** Native (details vary)  
**Pricing:** $69–$169/month  

**Key Strengths:**
- Fitness and wellness business management
- Specialized versions for yoga, martial arts, dance
- Virtual fitness options (livestream + on-demand)
- AI system for predicting client churn
- Built-in marketing tools

**Key Weaknesses:**
- QB sync via third-party Autymte layer
- Google Calendar sync details unclear
- Higher starting price

**Google Calendar Integration:** Via Autymte/Integrately

**Fit for Enable the Disabled:**
- ✅ Fitness-specific
- ⚠️ QB via third-party middleware
- ⚠️ Google Calendar via middleware

---

### 13. Glofox — Fitness Business Platform

**Category:** Gym and fitness studio management  
**QB Sync:** Via third-party integrations  
**Google Calendar Integration:** Sync varies  
**Pricing:** Custom quote  

**Key Strengths:**
- Fitness-specific scheduling and member tracking
- Community features in client app
- Client retention tools (risk identification)
- Instructor and class management

**Key Weaknesses:**
- QB integration is third-party
- Pricing is custom quote (less transparent)

**Fit for Enable the Disabled:**
- ✅ Fitness-specific
- ❌ QB via third-party
- ⚠️ Google Calendar details unclear

---

### 14. Zen Planner (Daxko) — Martial Arts/Boutique Gym

**Category:** Fitness business management  
**QB Sync:** Via third-party integrations  
**Google Calendar Integration:** Native calendar management  
**Pricing:** $99–$348/month  

**Key Strengths:**
- Fitness-focused (martial arts, boutique gyms, dance)
- Membership admin, scheduling, payment processing
- Workout tracking and retail sales
- AI-powered assistant for inquiries and lead qualification

**Key Weaknesses:**
- QB via third-party
- Most expensive tier ($348/month for Ultimate)

**Fit for Enable the Disabled:**
- ✅ Fitness-specific
- ❌ QB via third-party
- ⚠️ Pricing may be high for 30-client scale

---

### 15. SuperSaaS — Affordable Fitness Booking

**Category:** General scheduling (fitness-friendly)  
**QB Sync:** Via Zapier only  
**Google Calendar Integration:** Native  
**Pricing:** From $9/month (no per-seat fees)  
**G2 Rating:** 4.6★ (82 reviews)  

**Key Strengths:**
- Extremely affordable starting at $9/month
- No per-seat fees
- Good for fitness classes and personal training
- All features included at paid tiers

**Key Weaknesses:**
- QB via Zapier only
- No native QB integration

**Google Calendar Integration:** Native two-way sync

**Fit for Enable the Disabled:**
- ✅ Very affordable
- ✅ Google Calendar native
- ⚠️ QB via Zapier
- ⚠️ Not fitness-specific but fitness-friendly

---

## Middleware Options for QB ↔ Google Calendar Gap

Since no single tool offers both native QuickBooks AND native Google Calendar two-way sync, these middleware tools can bridge the gap:

| Tool | Description | QB Sync | Google Calendar Sync |
|------|-------------|---------|---------------------|
| **Zapier** | Automation platform with 5,000+ app integrations | QB Online connectors | Google Calendar triggers for new/updated/cancelled events |
| **Integrately** | AI-powered automation, "one-click" integrations | QB Online sync (invoices, customers, payments) | Google Calendar triggers (create, update, cancel) |
| **Autymte** | White-labeled integration (used by WellnessLiving) | QB Online sync | Varies by partner |

---

## Comparison Matrix

| Tool | Native QB | Native Google Calendar | Fitness-Specific | QB Desktop | Starting Price | G2 Rating |
|------|-----------|----------------------|-----------------|------------|----------------|-----------|
| **Jobber** | ✅ QBO only | ❌ Zapier | ❌ Field service | ❌ | $90/mo | 4.6★ |
| **Acuity** | ✅ QBO only | ✅ 2-way | ❌ General | ❌ | $15/mo | 4.11/5 |
| **Timely** | ✅ QBO only | ✅ 2-way | ❌ Health/beauty | ❌ | $15/mo | 4.6/5 |
| **Setmore** | ✅ QBO only | ✅ 2-way | ❌ General | ❌ | $12/mo | N/A |
| **Square POS** | ⚠️ Intuit connector | ❌ Zapier | ❌ General retail | ❌ | Free | 4.3★ |
| **Calendly** | ❌ Zapier | ✅ 2-way | ❌ Meetings | ❌ | $8/mo | 4.7★ |
| **Vagaro** | ⚠️ Add-on | ✅ 2-way | ✅ Fitness/salon | ❌ | $24/mo | 4.6★ |
| **Mindbody** | ❌ SyncApps | ✅ Staff sync | ✅ Fitness/wellness | ❌ | $99/mo | 4.2★ |
| **WellnessLiving** | ❌ Autymte | ⚠️ Middleware | ✅ Fitness/wellness | ❌ | $69/mo | N/A |
| **SuperSaaS** | ❌ Zapier | ✅ 2-way | ⚠️ Fitness-friendly | ❌ | $9/mo | 4.6★ |

---

## Key Findings

### 1. The QuickBooks ↔ Google Calendar Gap
**No tool in the market offers both native QuickBooks integration AND native Google Calendar two-way sync in a single package.** This is the central finding. Every combination requires either:
- A tool with native QB + middleware for Google (rare — most QB-native tools only have Google via Zapier)
- A tool with native Google + middleware for QB (Calendly, SavvyCal)
- A tool with neither native (rely on middleware for both)

**The one exception** is the middleware layer itself: **Integrately** and **Zapier** can both connect Google Calendar to QuickBooks Online directly, bypassing a scheduling tool entirely.

### 2. QuickBooks Desktop Support Is Disappearing
Of all tools reviewed, only **ServiceTitan**, **Housecall Pro**, and **Workiz** (field service tools) and **Buddy Punch** (shift scheduling) support QuickBooks Desktop. All consumer-facing appointment schedulers are QuickBooks Online only. This matters if Enable the Disabled uses QB Desktop rather than QBO.

**Confirmed fact from G2:** "Jobber and Praxedo are QuickBooks Online only, while ServiceTitan, Housecall Pro, and Workiz cover both." (Source: `learn.g2.com/scheduling-software-that-integrates-with-quickbooks`, line 364)

### 3. One-Way Sync Is the Default
All QuickBooks integrations reviewed are **one-way** (scheduling tool → QB) except Praxedo, which is genuinely two-way. This means paid status, refunds, or QB-side edits do not flow back to the scheduling tool. For most SMBs this is acceptable since billing originates from the scheduling tool.

### 4. Tier Paywall Trap
Multiple sources confirm the QuickBooks integration is often gated behind higher plan tiers:
- **Jobber:** Connect plan ($90/mo) and up
- **Housecall Pro:** Essentials tier and up
- **Acuity:** Paid plans only ($15+/mo)
- **Thryv:** Business Center tier required

### 5. Fitness-Specific Tools All Route QB Through Third Parties
Vagaro, Mindbody, WellnessLiving, Glofox, and Zen Planner all use third-party middleware (Autymte, SyncApps, or Zapier) for QuickBooks integration — none are native. This introduces an extra point of failure and often an extra monthly cost.

### 6. Vagaro Is the Closest Fitness Match
**Vagaro** stands out as the best fitness-specific option:
- Native two-way Google Calendar sync (enhanced Dec 2024)
- QuickBooks Online integration as a paid add-on
- HIPAA and EMR compliance (relevant for health data)
- Consumer app with 5M+ active users
- Pricing: $23.99–$83.99/month

However, Vagaro's QB integration has mixed reviews: "We just started integrating with QuickBooks in October 2022 and it has been a management nightmare to say the least." (Source: `support.vagaro.com` → `apps4rent.com/blog/vagaro-integration-with-quickbooks/`)

---

## Recommendations (Ranked)

Based on all research, here are the recommended evaluation paths:

### Shortlist (Test in Order)

1. **Acuity Scheduling** — Best overall for Enable the Disabled's stated needs
   - Native QuickBooks Online sync ✅
   - Native Google Calendar two-way sync ✅
   - Client self-booking ✅
   - Payment processing built in ✅
   - Most affordable path to BOTH integrations (native)
   - 14-day free trial

2. **Vagaro** — Best fitness-specific option
   - Native Google Calendar two-way sync ✅
   - QB Online via paid add-on (mixed reviews) ⚠️
   - Fitness/salon focused ✅
   - HIPAA compliant ✅
   - 30-day free trial

3. **Setmore** — Best budget option with both natives
   - Native QB Online sync ✅
   - Native Google Calendar two-way sync ✅
   - Free tier available (QB integration on paid plans)
   - Most affordable path to both native integrations

4. **Calendly + Integrately** — Best for Google-first, QB-second approach
   - Best Google Calendar integration in the market ✅
   - Integrately AI connects to QB Online directly ✅
   - Simplest booking experience ✅
   - $8/month if QB handled via middleware

5. **Jobber** — If current QB is QBO and invoicing is manual
   - Best QB Online sync in the market ✅
   - Google Calendar via Zapier (not native) ⚠️
   - Built for multi-trainer field service
   - $90/month (higher cost)

### Not Recommended (at this scale)

- **Mindbody** ($99+/month) — Overkill for 30 clients
- **Zen Planner** ($99–$348/month) — Too expensive for current scale
- **ServiceTitan / Workiz / Housecall Pro** — Field service tools, not appointment scheduling
- **WellnessLiving / Glofox** — QB via middleware, less transparent pricing

---

## Open Questions for Shaun

Based on the requirements document (`enable-the-disabled-scheduling-requirements-questions.md`), these questions need answers before a final shortlist can be narrowed:

1. **QuickBooks edition:** Is the business on QuickBooks Online or QuickBooks Desktop? (Only QBO is supported by most appointment schedulers; QB Desktop rules out Acuity, Setmore, Timely, Vagaro.)

2. **Current manual burden:** Does Shaun currently re-key appointments into QuickBooks to generate invoices? If not, QB integration is lower priority.

3. **Client self-booking:** Is a public, self-service booking page needed, or do all bookings go through Shaun first? (Calendly = self-booking; QB-native tools = varies.)

4. **Payment processing:** Does the business need built-in payment processing in the scheduling tool, or is invoicing alone sufficient? (Acuity and Setmore have payments; Calendly Pro has payments via Stripe.)

5. **Staff calendar sync:** How critical is it that each trainer's schedule auto-syncs to their personal Google Calendar? (Vagaro, Mindbody, and Calendly all do this natively.)

6. **Accessibility features:** Are there WCAG or ADA-compliant booking requirements? (SuperSaaS and SimplyBook have WordPress-accessible booking plugins; Vagaro is HIPAA/EMR compliant; most mainstream tools have no specific accessibility features.)

---

## Next Steps

1. **Confirm QuickBooks edition** (Online vs Desktop)
2. **Rank the shortlist above** based on answers to the 6 questions
3. **Sign up for free trials** of the top 2–3 candidates
4. **Test the QB sync** with a live test invoice/transaction
5. **Evaluate Google Calendar sync** for staff scheduling
6. **Document findings** in a selection matrix before deciding

---

*Sources archived to `/home/hermes/.hermes/profiles/fitness-strategist/cache/web/` for reference. Full-page extracts available for deep review.*
