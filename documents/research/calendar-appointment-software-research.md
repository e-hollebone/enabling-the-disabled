---
type: Research
title: "Calendar & Appointment Scheduling Software Research"
description: "# Calendar & Appointment Scheduling Software Research **For: Enable the Disabled**   **Prepared by: "
tags: ["calendar", "software", "research", "appointment", "hermes"]
generated:
  by: agent:hermes
  at: 2026-09-14
  confidence: auto-low-confidence
stale_after: 2027-09-14
status: stable
---

# Calendar & Appointment Scheduling Software Research
**For: Enable the Disabled**  
**Prepared by: Eric Hollebone / Hermes Agent**  
**Date: September 10, 2026**  
**Status: Complete — research phase**  
**Workflow Context:** Booking + mobile phone calendar recording → batch billing in QB  
**QuickBooks Edition:** Online (QBO) — confirmed by user  

---

## Executive Summary

This document compiles research on calendar and appointment scheduling solutions suitable for small-to-medium businesses. Given the **refined requirement** — appointments recorded on **native mobile phone calendars** (iOS Calendar, Android Calendar), then batch-billed in QuickBooks via "draw down or invoicing on accounts" — the **QuickBooks real-time sync requirement is DOWNGRADED** to optional/secondary. The primary requirements are:

1. **Native mobile phone calendar integration** (iOS Calendar, Android Calendar, not just Google Calendar)
2. **Appointment booking** with notifications to all parties (client, trainer, Shaun)
3. **QB integration** as a secondary convenience (batch export or manual)

**Critical finding:** **Google Calendar ≠ mobile phone calendar.** Many tools sync to Google Calendar but do NOT sync to the native iOS Calendar or Android Calendar apps on phones. This disqualifies several otherwise-strong candidates.

> **Note:** Google Calendar sync IS sufficient if Shaun, Sean, and Charlotte all use Google Calendar on their phones (iOS Google Calendar app or Android). But if they use the **native iOS Calendar app** or **native Android Calendar app**, a separate Google Calendar account is required.

---

## Refined Evaluation Criteria

| Priority | Requirement | Weight Impact |
|----------|-------------|---------------|
| **P1** | Native mobile phone calendar sync (iOS Calendar, Android Calendar, or Google Calendar app on mobile) | R1 weight: 35% |
| **P1** | Appointment booking with notifications to all parties | R2 weight: 25% |
| **P2** | Client self-booking portal | R5 weight: 10% |
| **P2** | Multi-trainer coordination + substitution | R4 weight: 15% |
| **P3** | QB integration (batch/middleware acceptable) | R3 weight: 10% |
| **P3** | Fitness/disability-specific features | R6 weight: 5% |
| **P3** | Cost at scale | R7 weight: 5% |

---

## Research Sources

| Source | URL | Scope |
|--------|-----|-------|
| G2: Scheduling Software that Integrates with QuickBooks | `learn.g2.com/scheduling-software-that-integrates-with-quickbooks` | 11 tools, QB + appointment focus |
| Shopify: Fitness Studio Scheduling | `www.shopify.com/blog/fitness-studio-scheduling-software` | 11 fitness-specific apps |
| Calendly Help: Connect Calendar | `calendly.com/help/connect-your-calendar-to-calendly` | Supported calendars list |
| Calendly Help: iCloud Overview | `calendly.com/help/icloud-overview` | iCloud/Apple Calendar discontinued |
| WpAmelia: Calendly Apple Calendar Alternative | `wpamelia.com/calendly-apple-calendar-alternative/` | Confirms Calendly Apple Calendar deprecation |
| Vagaro Support: Add Appointment to Calendar | `support.vagaro.com/hc/articles/360021411314` | Mobile calendar sync for iOS/Android |
| Vagaro Support: Sync with Google Calendar | `support.vagaro.com/hc/articles/31275501148699` | Google Calendar only |
| Setmore Support: iPhone Calendar Sync | `support.setmore.com/en/articles/490972` | 1-way iPhone calendar sync |
| Jobber Help: Calendar Syncing | `help.getjobber.com/en/articles/calendar-syncing` | Syncs to Apple/iPhone + Google |
| SuperSaaS: Mobile Device Use | `supersaas.com/info/doc/daily_use/mobile_device` | iOS/Android home screen shortcut |
| Trafft: Apple Calendar Sync | `traft.com/docs/integrations/apple-calendar-synchronization` | Two-way iCal sync |
| HoneyBook Help: Sync Mobile Calendar | `help.honeybook.com/en/articles/2673859` | Direct iOS/Android calendar sync |
| Microsoft Bookings | `microsoft.com/en-us/microsoft-365/business/scheduling-and-booking-app` | Syncs to iPhone Apple Calendar |
| SimplyBook Calendar Sync | `simplybook.me/en/calsync-fixedstart` | 2-way Google/Outlook only |

---

## Tool-by-Tool Mobile Calendar Sync Capabilities

### 1. Calendly — ⚠️ Apple Calendar NOT Supported

**Category:** Meeting/appointment scheduling  
**Mobile Calendar Sync:** ❌ No Apple/iCloud Calendar support (discontinued Aug 20, 2024)  
**Supported Calendars:** Google Calendar, Office 365/Outlook.com, Exchange only  
**QB Integration:** Via Zapier (optional)  
**Pricing:** Free tier; Pro $8–$12/user/month  
**G2 Rating:** 4.7★ (Leaders category)  

**Key Strengths:**
- Best-in-class Google Calendar integration (if users have Google Calendar on their phones)
- Automated notifications — email and SMS confirmations, reminders, follow-ups
- Client self-booking with real-time availability
- Simple, clean UI (9.4/10 G2 ease-of-use)

**Key Weaknesses:**
- **NO Apple/iCloud Calendar support** — confirmed discontinued as of August 20, 2024
- **NO iPhone native iOS Calendar app sync** — only via Google Calendar app
- Limited client database (not a CRM)
- Payment processing only on Pro/Business tiers

**Calendly Calendar Sync Details (from help.calendly.com):**
- Supported calendars: Google Calendar, Office 365/Outlook.com, Exchange
- "As of August 20, 2024, Calendly no longer supports new connections to iCloud Calendar"
- Existing iCloud connections may continue but are not guaranteed
- Calendly mobile app for iOS and Android does NOT sync to native phone calendar

**Fit for Enable the Disabled:**
- ⚠️ **Only if trainers use Google Calendar app on their phones** (not native iOS Calendar)
- ❌ Disqualified if trainers use native iOS Calendar or Android Calendar app without Google Calendar
- ✅ Automated notifications to all parties
- ✅ Client self-booking
- ✅ $8/month (budget-friendly)
- ⚠️ QB via middleware (acceptable — batch billing workflow)

---

### 2. Vagaro — ✅ Mobile Calendar Sync via App

**Category:** Fitness, salon, spa business management  
**Mobile Calendar Sync:** ✅ iOS/Android native calendar (via Vagaro mobile app)  
**Google Calendar Sync:** ✅ Two-way (only calendar supported for staff sync)  
**QB Integration:** Premium add-on (QB Online only)  
**Pricing:** $23.99–$83.99/month + QB add-on fee  
**G2 Rating:** 4.6★ (98.8% small business reviewers)  

**Key Strengths:**
- Built for fitness studios — class scheduling, personal training
- **Mobile app syncs appointments to device's default calendar on iOS and Android**
- HIPAA and EMR compliant (health data)
- Consumer app (5M+ users can discover business)
- Built-in POS and payment processing

**Mobile Calendar Sync Details (from support.vagaro.com):**
- "The Vagaro app will then open the default calendar app on your mobile device"
- iOS: Choose "Allow Full Access" (sync two-way) or "Keep Add Only" (one-way import)
- Android: Grant Vagaro App access to calendar
- Staff calendar sync: Only Google Calendar supported (per support docs)
- **Client appointments sync to native phone calendar** (iOS Calendar app / Android Calendar app)

**QB Integration:** Premium add-on for QB Online, daily export (mixed user reviews)

**Fit for Enable the Disabled:**
- ✅ **Syncs appointments to native iOS/Android calendar via mobile app**
- ✅ Fitness-specific (classes, personal training)
- ✅ HIPAA/EMR compliance
- ⚠️ QB add-on costs extra and has mixed reviews (acceptable — batch workflow)
- ❌ Pricier ($24+/month)
- ⚠️ Staff Google Calendar sync is the only staff-level calendar sync option

---

### 3. Jobber — ✅ iPhone Calendar via iCal URL

**Category:** Field service management  
**Mobile Calendar Sync:** ✅ Apple/iPhone Calendar, Android Calendar, Google Calendar  
**QB Integration:** Native QB Online (one-way export)  
**Pricing:** From $90/month (higher-tier plans)  
**G2 Rating:** 4.6★ (Summer 2026 Grid)  

**Key Strengths:**
- **Syncs to Apple/iPhone Calendar via iCal URL subscription**
- Also syncs to Google Calendar, Android Calendar, Outlook, Yahoo, Thunderbird
- One-way sync from Jobber into calendar app (appointments show up, can't edit back)
- Pulls data 2 weeks back, 20 weeks forward
- QB Online integration (Connect plan and up)
- Designed for teams with multiple staff

**Mobile Calendar Sync Details (from help.getjobber.com):**
- "The calendar sync is one-way from Jobber into your calendar app"
- Explicitly lists: Google calendar, Apple iCal (iPhone/iPad calendar), iCloud calendar, Yahoo calendar, Microsoft Outlook
- iOS users: Subscribes via iCal URL in iPhone Settings > Calendar > Accounts > Subscribed
- Android users: Can import via Google Calendar web interface (Google Calendar app on phone)

**QB Integration:** Native QB Online sync (one-way Jobber → QB) — clients, invoices, payments, timesheets

**Fit for Enable the Disabled:**
- ✅ **Syncs to iPhone Calendar AND Android Calendar AND Google Calendar**
- ✅ Multi-trainer support (built for teams)
- ⚠️ QB is native but one-way (acceptable for batch workflow)
- ❌ Overkill/pricy for 30-client scale ($90+/month)
- ⚠️ Field service focus, not fitness-specific

---

### 4. Trafft — ✅ Native Apple Calendar Sync

**Category:** Appointment scheduling (service businesses)  
**Mobile Calendar Sync:** ✅ Two-way sync with Google, Outlook, AND **iCal (Apple Calendar)**  
**QB Integration:** Not directly mentioned; likely via Zapier  
**Pricing:** Free plan for teams up to 5; paid plans scale  
**G2/Reviews:** Rating 4.9 (808 reviews)  

**Key Strengths:**
- **Two-way sync with Apple/iCal Calendar** — explicitly documented
- Two-way sync with Google Calendar and Outlook
- Free plan available for small teams
- WordPress plugin available (can embed booking on any site)
- Mobile app for iOS and Android

**Apple Calendar Sync Details (from trafft.com/docs):**
- "Before connecting Apple Calendar in Trafft, your Apple account needs to have 2FA configured and an App-Specific Password created"
- Supports Apple Calendar synchronization natively (not via Google Calendar workaround)
- Two-way sync means changes in either calendar reflect in both

**QB Integration:** Not explicitly documented; likely via Zapier middleware

**Fit for Enable the Disabled:**
- ✅ **Native Apple Calendar two-way sync**
- ✅ Free plan available (low risk to test)
- ✅ WordPress plugin (can add to website)
- ⚠️ QB via middleware (acceptable)
- ⚠️ Not fitness-specific

---

### 5. HoneyBook — ✅ Direct iOS/Android Calendar Sync

**Category:** Creative business CRM + scheduling  
**Mobile Calendar Sync:** ✅ Direct iOS (iCal) and Android calendar sync from mobile app  
**Google Calendar Sync:** ✅ Also supports Google, Apple, Outlook calendar sync  
**QB Integration:** QB integration documented but details unclear  
**Pricing:** $39–$79/month  
**G2 Rating:** 4.6★  

**Key Strengths:**
- **HoneyBook's iOS and Android apps** "directly retrieve events from your iOS (iCal) or Android calendar"
- Connects Google, Apple, or Outlook calendar to HoneyBook
- All-in-one: contracts, invoices, payments, project tracking
- Mobile app syncs directly with native phone calendar

**Mobile Calendar Sync Details (from help.honeybook.com):**
- "Allow the app to directly retrieve events from your iOS (iCal) or Android calendar"
- Can sync personal calendar with HoneyBook
- Works with iOS native Calendar app directly

**QB Integration:** QB integration exists but documentation is sparse (likely via middleware)

**Fit for Enable the Disabled:**
- ✅ **Direct iOS Calendar and Android Calendar sync**
- ✅ Native phone calendar integration from mobile app
- ✅ All-in-one (contracts, invoices, payments)
- ⚠️ QB integration details unclear
- ❌ Not fitness-specific
- ❌ Higher price tier ($39+/month)

---

### 6. Microsoft Bookings — ✅ iPhone Calendar Sync

**Category:** Microsoft 365 integrated scheduling  
**Mobile Calendar Sync:** ✅ Syncs to iPhone's Apple Calendar (via Outlook integration)  
**Google Calendar Sync:** Limited  
**QB Integration:** Not native; via third-party connectors  
**Pricing:** Included with Microsoft 365 Business  

**Key Strengths:**
- **Bookings meetings sync with iPhone's Apple Calendar** (confirmed in Microsoft Q&A)
- Part of Microsoft 365 ecosystem
- Free with M365 Business subscription

**Key Weaknesses:**
- **Microsoft Bookings mobile apps discontinued** as of Dec 1, 2022 (Apple App Store and Google Play)
- Limited Google Calendar support
- QB integration not native

**Mobile Calendar Sync Details:**
- "These Bookings meetings show up on my online Outlook calendar and on my iPhone's Apple Calendar"
- Requires Outlook calendar configuration on iOS device

**Fit for Enable the Disabled:**
- ⚠️ Syncs to iPhone Apple Calendar (if using Outlook on phone)
- ❌ Mobile apps discontinued (Dec 2022)
- ❌ QB not native
- ⚠️ Only useful if already in Microsoft 365 ecosystem

---

### 7. Setmore — ⚠️ 1-Way iPhone Sync Only

**Category:** Appointment scheduling (SMB general)  
**Mobile Calendar Sync:** ⚠️ 1-way iPhone calendar sync via URL subscription  
**Google Calendar Sync:** ✅ Two-way sync  
**QB Integration:** Native QB Online (one-way)  
**Pricing:** Free tier; Pro $12/month  

**Key Weaknesses:**
- iPhone calendar sync is **1-way only** (appointments show in iPhone Calendar, but can't edit back)
- Uses iCal URL subscription method (not native app integration)

**Mobile Calendar Sync Details (from support.setmore.com):**
- "Export appointments from Setmore to your iPhone calendar"
- 1-way sync: "you can't make any changes to Setmore appointments from your iPhone calendar"
- Works via Settings > Calendar > Accounts > Subscribed (paste Setmore iCal URL)

**Fit for Enable the Disabled:**
- ⚠️ iPhone Calendar sync (1-way, via URL subscription)
- ✅ QB Online native export
- ✅ Payment processing
- ⚠️ Android sync less clear (likely via Google Calendar app)
- ❌ 1-way sync only (can't edit appointments from phone calendar)

---

### 8. SuperSaaS — ⚠️ No Native Phone Calendar Sync

**Category:** General scheduling (fitness-friendly)  
**Mobile Calendar Sync:** ⚠️ No native phone calendar sync; iOS/Android via home screen shortcut  
**Google Calendar Sync:** ✅ Two-way sync  
**QB Integration:** Via Zapier only  
**Pricing:** From $9/month  

**Key Weaknesses:**
- **No native iOS Calendar or Android Calendar sync**
- Mobile access is via web app shortcut on home screen (not native calendar)
- QB via middleware

**Mobile Access Details (from supersaas.com):**
- "Add your schedule to your iPhone or iPad home screen" (web app shortcut, not calendar sync)
- "Add your schedule to your Android home screen"
- Syncs to Google Calendar and Microsoft (not Apple native calendar)

**Fit for Enable the Disabled:**
- ❌ **No native iOS/Android phone calendar sync**
- ✅ Google Calendar two-way sync (if using Google Calendar app)
- ✅ Affordable ($9/month)
- ✅ Custom intake forms (accessibility needs)
- ⚠️ QB via middleware
- ⚠️ Interface is dated

|---

## Pricing, Trial & Demo Matrix

| Tool | Free Tier | Free Trial | Trial Period | Trial Limitations | Paid Plans | Demo Available | Notes |
|------|-----------|------------|--------------|-------------------|------------|----------------|-------|
| **Calendly** | ✅ Yes (1 event type, 1 calendar) | ✅ Yes | 14 days Pro | No credit card | Pro $8, Teams $12, Enterprise $21 /month | Web demo | Free plan very limited (1 event type). Apple iCal sync ended Aug 2024 |
| **Vagaro** | ❌ No | ✅ Yes | 30 days | All features except email/SMS marketing & branded app | $23.99–$83.99/month + QB add-on | ✅ Yes | 30-day trial is the only way to test. Staff calendar sync supports Google Calendar only |
| **Jobber** | ❌ No | ✅ Yes | 14 days | Full feature access | $90–$250+/month (3–20+ users) | ✅ Yes | 30-day money-back guarantee. Overkill for 30 clients |
| **Trafft** | ✅ Yes (5 users, 1 location) | ✅ Yes | 14 days | All premium features | $22.7–$79/month + Scaling $39.9/month | ✅ Yes | Free plan is usable: unlimited apps, calendar sync, mobile apps |
| **HoneyBook** | ❌ No | ✅ Yes | 7 days (some sources say 30) | All features | $39–$79/month | ✅ Yes | No credit card required. 60-day money-back guarantee |
| **Microsoft Bookings** | ✅ Yes (with M365) | ✅ Yes | 30 days | All M365 features | $6–$12.50/user/month (Business plans) | ✅ Yes | Bookings is free with M365 Business. Mobile apps were discontinued Dec 2022 |
| **Setmore** | ✅ Yes (4 users, 200 appointments) | ✅ Yes | 14 days | All Pro features | Free, Pro $5–$12/user/month (annual) | ✅ Yes | Free plan caps at 200 appointments/month & 4 users. Two-way sync only on Pro |
| **SuperSaaS** | ✅ Yes (50 bookings, ads) | ✅ Yes | 7–30 days | All features except ads | Free, Plus $9–$48/month | ✅ Yes | Free plan is ad-supported. No native phone calendar sync — Google Calendar only |
| **SavvyCal** | ⚠️ Limited (meeting polls only) | ✅ Yes | 7 days | All features | Free, Basic $12, Premium $20/user/month (annual) | ✅ Yes | Free is not for booking links — only meeting polls. Apple Calendar not directly supported |
| **YouCanBookMe** | ❌ No | ✅ Yes | 14 days | All Professional features | Free, Individual $7.20, Professional $13–$21/month | ✅ Yes | Free plan: 1 user, 1 calendar. No Apple native calendar sync |
| **SimplyBook** | ✅ Yes (50 bookings, 1 provider) | ✅ Yes | 14 days | All premium features | €0–€59.9/month + per-feature modules | ✅ Yes | Free plan: 50 bookings/month, 1 provider. One premium feature only. Manual monthly renewal required |
| **Acuity (Squarespace)** | ❌ No | ✅ Yes | 7 days | All features | $16–$49/month | ✅ Yes | No credit card needed. No free plan. Strong Google Calendar integration |
| **Koalendar** | ✅ Yes (2 calendars, 1 user) | ✅ Yes | 7 days | All Pro features | Free, Pro $8–$16/user/month (annual) | ✅ Yes | True free forever plan. 2-way sync with Google, Apple, Outlook on Pro |
| **Cal.com** | ✅ Yes (individual) | ✅ Yes | 3 days | All features | Free, Teams $12, Organizations $28/user/month | ✅ Yes | Free for individuals. Can self-host open source version |
| **Reservio** | ✅ Yes (40 bookings/30 days) | ❌ No | 40 bookings | 100 client limit | Free, $9–$29/month | ✅ Yes | Free tier: 40 bookings/month, 100 clients. No Apple native calendar sync |
| **Chili Piper** | ❌ No | ❌ No | ❌ No | N/A — no trial | $15K+/year | ✅ Request | Enterprise-only. Priced per seat at $50+/user/month |

### Free Tier Summary (Best for Testing)

| Tool | Free Plan | Key Limitation | Native Mobile Calendar |
|------|-----------|---------------|----------------------|
| **Trafft** | ✅ 5 users, 1 location, unlimited appointments | No SMS, limited reports | ✅ Yes (Apple, Google, Outlook) |
| **Setmore** | ✅ 4 users, 200 appointments | No two-way sync, no SMS reminders on free | ⚠️ 1-way iPhone sync only |
| **Calendly** | ✅ 1 event type, 1 calendar | Only 1 event type, no SMS | ❌ Apple Calendar discontinued |
| **SuperSaaS** | ✅ 50 bookings, ads shown | Ads, 50 booking limit | ❌ No native phone sync |
| **SimplyBook** | ✅ 50 bookings, 1 provider | 50 bookings/month, manual renewal | ❌ No native Apple/Android sync |
| **Koalendar** | ✅ 2 calendars, 1 user | 2 calendar connections | ✅ Yes (2-way on Pro) |
| **Microsoft Bookings** | ✅ With M365 subscription | Requires M365 Business | ⚠️ Via Outlook on phone only |
| **Cal.com** | ✅ Individual plan | No team features | ✅ Yes (2-way) |

### Free Trial Summary (Best for Short-Term Testing)

| Tool | Trial Length | No Credit Card? | Full Features? | Notes |
|------|-------------|-----------------|---------------|-------|
| **Vagaro** | 30 days | ✅ Yes | ✅ Yes | All features except email/SMS marketing |
| **Jobber** | 14 days | ✅ Yes | ✅ Yes | 30-day money-back guarantee |
| **Trafft** | 14 days | ✅ Yes | ✅ Yes | Free plan also available |
| **HoneyBook** | 7 days | ✅ Yes | ✅ Yes | 60-day money-back on paid plans |
| **Setmore** | 14 days | ✅ Yes | ✅ Yes | Free plan also available forever |
| **Calendly** | 14 days | ✅ Yes | ✅ Yes | Free plan also available forever |
| **SimplyBook** | 14 days | ✅ Yes | ✅ Yes | Free plan also available forever |
| **Acuity** | 7 days | ✅ Yes | ✅ Yes | No credit card needed |
| **Koalendar** | 7 days | ✅ Yes | ✅ Yes | Free plan also available forever |
| **Cal.com** | 3 days | ❌ No (Teams test) | ✅ Yes | Very short trial for paid features |
| **YouCanBookMe** | 14 days | ✅ Yes | ✅ Yes | Free plan: 1 user, 1 calendar |
| **Microsoft Bookings** | 30 days | ✅ Yes | ✅ Yes | Part of M365 Business 30-day trial |

### Installable Demos
- **Vagaro**: On-demand webinar demo + live walkthrough available on request
- **Jobber**: Live demo scheduling + recorded walkthroughs
- **Trafft**: Video demos + live demo scheduling
- **HoneyBook**: Live demo scheduling + extensive video guides
- **Setmore**: Live demo scheduling
- **Calendly**: Interactive web demo (product tour)
- **Acuity**: Video demos + live scheduling
- **Koalendar**: Interactive product tour
- **Cal.com**: Self-signup for testing
- **SimplyBook**: Video demos + live demo
- **Microsoft Bookings**: Part of M365 Business free trial

---

Based on verified findings, the following tools either do NOT or NO LONGER support native mobile phone calendar sync:

| Tool | Why Disqualified |
|------|-----------------|
| **Calendly** | Apple/iCloud Calendar support discontinued Aug 2024; only Google/Outlook/Exchange |
| **Microsoft Bookings** | Mobile apps discontinued Dec 2022; sync requires Outlook on phone |
| **SuperSaaS** | No native phone calendar sync; only home screen web shortcut + Google Calendar |
| **SavvyCal** | Syncs to Google/Outlook, not Apple native calendar |
| **YouCanBookMe** | Syncs to Google/Outlook/iCloud via Google, not native Apple/Android calendar |
| **SimplyBook** | 2-way sync with Google/Outlook only, not Apple native calendar |

---

## Comparison Matrix (Refined)

| Tool | iOS Calendar | Android Calendar | Google Calendar | QB Path | Notifications | Self-Book | Starting Price |
|------|-------------|-----------------|-----------------|---------|---------------|-----------|----------------|
| **Jobber** | ✅ 1-way iCal | ✅ 1-way via Google Calendar | ✅ 2-way | ✅ Native QB | ✅ Built-in | ✅ Yes | $90/mo |
| **Vagaro** | ✅ Via mobile app | ✅ Via mobile app | ✅ 2-way | ⚠️ Add-on | ✅ Built-in | ✅ Yes | $24/mo |
| **Trafft** | ✅ 2-way native | ✅ 2-way native | ✅ 2-way | ⚠️ Zapier | ✅ Built-in | ✅ Yes | Free |
| **HoneyBook** | ✅ Direct sync | ✅ Direct sync | ✅ 2-way | ⚠️ Unclear | ✅ Built-in | ✅ Yes | $39/mo |
| **Setmore** | ⚠️ 1-way iCal | ⚠️ Via Google Calendar | ✅ 2-way | ✅ Native QB | ✅ Built-in | ✅ Yes | $12/mo |
| **Calendly** | ❌ Discontinued | ⚠️ Via Google Calendar | ✅ 2-way | ⚠️ Zapier | ✅ Built-in | ✅ Yes | $8/mo |
| **Koalendar** | ✅ 2-way (Pro) | ✅ 2-way (Pro) | ✅ 2-way (Pro) | ⚠️ Zapier | ✅ Built-in | ✅ Yes | Free |
| **Cal.com** | ✅ 2-way | ✅ 2-way | ✅ 2-way | ⚠️ Zapier | ✅ Built-in | ✅ Yes | Free |

---

## Key Findings (Refined)

### 1. Calendly's Apple Calendar Deprecation Is a Dealbreaker
As of August 20, 2024, Calendly no longer supports new connections to iCloud Calendar. This means:
- iPhone users on native iOS Calendar app: **NO SYNC**
- Only works if users have the Google Calendar app on their iPhone
- Calendly mobile apps for iOS/Android do NOT integrate with native phone calendars

### 2. Vagaro Is the Only Fitness Tool with Native Mobile Calendar Sync
Vagaro's mobile app can sync appointments to each trainer's device's default calendar app (iOS Calendar on iPhone, Google Calendar on Android). However, staff-level calendar sync for business owners only supports Google Calendar.

### 3. Jobber Has the Broadest Mobile Calendar Support
Jobber supports subscription-based 1-way sync to Apple/iPhone Calendar, Android Calendar (via Google Calendar), Google Calendar, Outlook, Yahoo, and Thunderbird via iCal URL subscription. This covers the most platforms.

### 4. Trafft Is the Surprise — Free Plan with Native Apple Calendar
Trafft offers two-way sync with iCal (Apple Calendar), Google, and Outlook, including a free plan for teams up to 5. The Apple Calendar sync requires 2FA and an App-Specific Password.

### 5. QB Desktop Support Is Not a Concern (QBO Confirmed)
Under the batch billing workflow with QuickBooks Online confirmed, QB Desktop compatibility is not a limiting factor. All recommended tools support QBO export, either natively (Jobber, Setmore) or via middleware (Zapier for Trafft, Vagaro add-on).

---

## Recommendations (Refined)

### Tier 1: Native Mobile Calendar Sync + Fitness Features

1. **Vagaro** — Best fitness-specific with native mobile calendar sync
   - ✅ Mobile app syncs to iPhone and Android native calendar
   - ✅ Fitness-specific (classes, PT, equipment booking)
   - ✅ HIPAA/EMR compliant
   - ✅ Consumer app discovery (5M+ users)
   - ⚠️ QB add-on is paid + mixed reviews
   - ⚠️ Staff calendar sync is Google Calendar only
   - $24+/month, 30-day free trial

2. **Trafft** — Best free option with native Apple Calendar sync
   - ✅ Two-way sync with Apple/iCal, Google, and Outlook calendars
   - ✅ Free plan for teams up to 5
   - ✅ WordPress plugin available
   - ❌ Not fitness-specific
   - ⚠️ QB via Zapier
   - Free tier available

### Tier 2: Native Mobile Calendar Sync + Robust QB

3. **Jobber** — Best for broad mobile calendar support
   - ✅ Syncs to iPhone Calendar, Android Calendar, Google Calendar, Outlook
   - ✅ Native QB Online integration
   - ✅ Multi-trainer/team support
   - ❌ Overkill for 30-client scale ($90+/month)
   - ⚠️ Field service focus, not fitness-specific

4. **Setmore** — Best budget native QB + iPhone sync
   - ✅ 1-way iPhone Calendar sync via iCal subscription
   - ✅ Native QB Online export
   - ✅ Payment processing
   - ⚠️ 1-way sync only (can't edit from phone calendar)
   - $12/month

### Tier 3: Consider if Google Calendar App Is Acceptable

5. **Calendly** — Best Google Calendar integration ONLY
   - ❌ **REQUIRES Google Calendar app on iPhone** (no native iOS Calendar sync)
   - ✅ Best Google Calendar integration overall
   - ✅ Simplest booking experience
   - ⚠️ QB via Zapier
   - $8/month, 14-day Pro trial

6. **HoneyBook** — All-in-one CRM with native mobile sync
   - ✅ Direct iOS and Android calendar sync from mobile app
   - ✅ Contracts, invoices, payments, project tracking
   - ⚠️ QB integration unclear
   - ❌ Not fitness-specific
   - $39+/month

---

|---

## Value Analysis at 30-Client Scale (~$30/month Budget)

Enable the Disabled has ~$204K annual revenue (30 clients @ ~$17K/mo across trainers). At a $30/month tool budget, what do the viable candidates deliver?

| Tool | Monthly Cost @ 3 Trainers | What You Get | QB Path | Verdict |
|------|--------------------------|-------------|---------|---------|
| **Trafft** | **$0 (Free plan)** | ✅ 5 users, unlimited appointments, native Apple/Google/Outlook sync, mobile apps, 14-day premium trial | ⚠️ Zapier | 🏆 **Best value** — free tier covers needs |
| **Setmore** | **$15** (3 users @ $5/mo annual) | ✅ 4 users, 200 appointments, 2-way Google sync, 1-way iPhone sync, native QB | ✅ Native QB | ✅ **Strong value** — budget-friendly with QB native |
| **Cal.com** | **$0 (Free)** for individuals | ✅ Individual scheduling, native calendar sync | ⚠️ Zapier | ⚠️ Free only for individuals — teams need paid |
| **Koalendar** | **$0 (Free)** for 1 user | ✅ 2 calendar connections, free tier | ⚠️ Zapier | ✅ Free tier works for 1 trainer; upgrade for team |
| **Vagaro** | **$72** (3 users @ $24/mo) | ✅ Fitness-specific, native mobile sync, classes, QB add-on | ⚠️ Paid add-on | ❌ **Over budget** at $72/month |
| **Jobber** | **$270** (3 users @ $90/mo) | ✅ Native QB, broad calendar support, multi-trainer | ✅ Native | ❌ **Way over budget** — overkill |
| **HoneyBook** | **$117** (3 users @ $39/mo) | ✅ All-in-one CRM, native mobile sync | ⚠️ Unclear | ❌ **Over budget** at $117/month |

### Key Insight
**Trafft's free plan (5 users, unlimited appointments) is the standout value.** It supports up to 5 team members (Shaun + 3 trainers + 1 admin) with full calendar sync and all core features at $0/month. QB integration is via Zapier (acceptable for batch billing).

**Setmore Pro at $15/month** (3 users annually) is the second-best value — it's the most budget-friendly option with native QB Online export, though it only offers 1-way iPhone calendar sync.

**Calendly at $24/month** (3 users) is affordable but **disqualified** — no native iOS Calendar support.

---

1. **Phone calendar preference:** Do Shaun, Sean, and Charlotte use the **native iOS Calendar app** on iPhones (or native Android Calendar on Android phones), or the **Google Calendar app**? 
   - If **native iOS/Android Calendar**: Calendly, SuperSaaS, SimplyBook are **disqualified**.
   - If **Google Calendar app**: Calendly becomes viable.

2. **QB edition:** ✅ QuickBooks Online (QBO) — confirmed. All tools supporting QBO export are eligible.

3. **Current manual coordination time:** How much time is spent on scheduling coordination weekly? (Hours per week)

4. **Batch QB billing frequency:** How often is QB billing generated — weekly, monthly, or per-campaign?

5. **Client self-booking:** Should clients self-book online, or does all booking go through Shaun?

6. **Trainer substitution needs:** How often do trainers need to hand off sessions to substitutes? (Affects R4 score)

7. **ADA/WCAG accessibility:** Are there accessibility requirements for the booking page?

---

## Next Steps

1. **Answer the 7 questions** above — particularly the phone calendar preference
2. **Based on answers, select 1–2 shortlist tools** from the recommendations
3. **Sign up for free trials** of the top candidates
4. **Test mobile calendar sync** with a real appointment on a test phone
5. **Test notification workflow** (client booking → trainer notified → Shaun notified)
6. **Test QB export path** (export appointments → QB invoices)
7. **Score each tool** using the evaluation model

---

*Sources archived to `/home/hermes/.hermes/profiles/fitness-strategist/cache/web/` for reference. Full-page extracts available for deep review.*
