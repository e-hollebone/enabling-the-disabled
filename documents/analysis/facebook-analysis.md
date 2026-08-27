# Facebook Analysis — Shaun Kehoe's Personal Training (`SPFKPT33`)

**Source page:** https://www.facebook.com/SPFKPT33/
**Captured:** 2026-08-27
**Method:** Direct public web fetch (`web_extract` + `web_search`) — NOT via Guacamole/RDP.
**Owner / next step:** Pending Eric confirmation. Recent (Jul–Aug 2026) posts NOT yet captured — see Gap below.

---

## Page Summary

- **Name:** Shaun Kehoe's Personal Training
- **Tagline (from index):** "My page is here to teach people how to exercise and eat in a healthier way and show everyone that if…"
- **Engagement (indexed):** ~759 likes · 3 talking about this

---

## Posts Captured (historical, from indexed/video URLs)

> NOTE: The main profile feed is a login wall. The captures below come from public video post URLs that search surfaced. Dates are from index where shown; some are older (2021) and are included because they are the only accessible caption text.

### 1. "Exercise helped save my life!"
- **URL:** https://www.facebook.com/SPFKPT33/videos/enable-the-disabledexercise-helped-save-my-life-it-helped-me-realize-that-i-can-/488691245764920/
- **Date:** Jul 3, 2021 (indexed)
- **Caption:** "Exercise helped save my life! It helped me realize that I can still reach goals and live a great life despite all of my brain surgeries, seizures, and voices in my head screaming for me to give up! I am on a mission in life to do the same for others, and absolutely nothing will stop me!!!!! 'I will sale my vessel until the river runs dry. Like a bird upon the wind these waters are my sky I'll never reach my destination if I never try. So I will sail my vessel until the river runs dry.' — Garth Brooks"

### 2. "One of the main lessons I learned early…"
- **URL:** https://www.facebook.com/SPFKPT33/videos/enable-the-disabled-one-of-the-main-lessons-i-learned-early-was-that-if-you-are-/4475021655863841/
- **Caption:** "One of the main lessons I learned early was that if you are not willing to build a strong, meaningful and wholesome relationship with people that have disabilities you're in the wrong career. There have to be days to just stop and forget about training. Show them you are a real friend that cares and can have fun. Not just some exercise robot. Matt and I dancing to In the Navy!"
- **Hashtags:** #enablethedisabled #epilepsy #epilepsywarrior #epilepsysupport #hydrocephalus #cerebralpalsy #autism #musculardystrophy #depression #anxiety #life #lift #live #love #fitfam #fitness #fun #happy

### 3. "Unbelievable sessions!"
- **URL:** https://www.facebook.com/SPFKPT33/videos/unbelievable-sessions-enablethedisabled-missioninlife-cerebral_palsy-motivation-/817450507854710/
- **Caption:** "Unbelievable sessions! #enablethedisabled #missioninlife #cerebral_palsy #motivation #fitness"

### 4. "Adapting and working hard!"
- **URL:** https://www.facebook.com/SPFKPT33/videos/adapting-and-working-hard-enablethedisabled-missioninlife-autism-cerebral_palsy-/1291768922941121/
- **Caption:** "Adapting and working hard! #enablethedisabled #missioninlife #autism #cerebral_palsy #inspiration"
- **Comment (indexed):** "I'm mavs mom your doing amazing with mav. He's looking great focusing and working hard. I'm wanting to know where you hide that cape cause you definitely are a super hero. You must change in a phone both like Clark Kent lol."

---

## Recurring Themes (observed)
- Mission framing: "Enable the Disabled" — fitness as rehabilitation/empowerment for people with disabilities.
- Disability communities named repeatedly: epilepsy, hydrocephalus, cerebral palsy, autism, muscular dystrophy, depression, anxiety.
- Relationship-first coaching philosophy ("real friend, not an exercise robot").
- Personal narrative of survival (brain surgeries, seizures) used as credibility/motivation.

---

## GAP — Recent Posts (Jul–Aug 2026) NOT CAPTURED
The handoff's target window (recent posts, Jul–Aug 2026) is **not** in the public index. The main feed is a login wall; direct fetch returned an empty body. To capture current posts we need ONE of:
1. **Kasm browser** (renfrew-kasm) — agent drives a logged-in browser session via CDP, reads current feed. No RDP loop.
2. **Eric relays** the recent post text from his own view of `eric-legion` (agent never opens `eric-legion`).

---

## Method Notes / Constraints
- Guacamole MCP is control-only (56 tools, no screen/session-launch). It confirms `eric-legion` (id `1`, rdp) is reachable but cannot render it.
- Agent must never open `eric-legion` — RDP-to-self causes a recursive screen loop that crashes the box.
- All captures above are from public/indexed URLs only; nothing behind the login wall was accessed.
