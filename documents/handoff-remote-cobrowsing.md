# Handoff — Remote Co-Browsing via Guacamole MCP

**Date:** 2026-08-27  
**Purpose:** Enable the fitness-strategist profile to co-browse with Eric via Guacamole RDP, starting with reading Shaun Kehoe's Facebook page.

---

## What's Done

### Guacamole MCP Server
- **Server:** `guacamole-mcp` (from `https://github.com/andhit-r/apache-guacamole-mcp`)
- **URL:** `http://renfrew-unraid.renfrew.hollebone.ca:8080`
- **Username:** `hermes`
- **Password:** `hermesagent`
- **Tools:** 56/56 enabled
- **Config location:** `~/.hermes/profiles/fitness-strategist/config.yaml`
- **Connection name in Guacamole:** `eric-legion` (RDP to Eric's Windows desktop)
- **Status:** Connected and verified via `hermes mcp test guacamole`

### Repo State
- All business documents committed and pushed to `enabling-the-disabled`
- Journal and effort log active
- Business context collection complete
- Key facts document created
- Social media/website analysis created (baseline)
- Shaun question list (Round 1) pending answers

---

## What the Next Session Must Do

1. **Verify MCP tools load** — Run `hermes mcp list` to confirm `guacamole` server is active with 56 tools
2. **List Guacamole connections** — Use the `list_connections` MCP tool to find `eric-legion`
3. **Start an RDP session** — Use Guacamole's session/token tools to initiate the RDP connection
4. **Open Facebook** — Navigate to `https://www.facebook.com/SPFKPT33/` (Shaun's business page)
5. **Read posts** — Scroll through Shaun's recent posts (July–August 2026), capture content, dates, likes, comments
6. **Capture data** — Record into `documents/analysis/facebook-analysis.md`
7. **Co-browse** — Eric watches through the Guacamole HTML5 client at `http://renfrew-unraid.renfrew.hollebone.ca:8080/`

---

## Architecture

```
Eric's PC (Windows)
    ↓ RDP
renfrew-unraid.renfrew.hollebone.ca (Unraid)
    ↓ Guacamole daemon + HTML5 client (port 8080)
hermes-agent LXC container (Linux)
    ↓ MCP stdio
guacamole-mcp server
    ↓ MCP tools
fitness-strategist Hermes session
```

Eric watches/interacts via Guacamole web interface. Agent drives via MCP tools.

---

## Key Files & Locations

| Resource | Path/URL |
|----------|----------|
| Repo | `/home/hermes/enabling-the-disabled` |
| Guacamole web | `http://renfrew-unraid.renfrew.hollebone.ca:8080/` |
| Guacamole connection | `eric-legion` (RDP to Eric's desktop) |
| Shaun Facebook | `https://www.facebook.com/SPFKPT33/` |
| Shaun website | `https://shaunkehoe.com/` |
| Config | `~/.hermes/profiles/fitness-strategist/config.yaml` |

---

## User Preferences (MANDATORY)

- **Eric's instructions are commands, not suggestions.** Execute directly. No alternatives, no overcomplicating, no "let me research."
- **Use FQDNs only** — never short names. `renfrew-unraid.renfrew.hollebone.ca`, not `renfrew-unraid`.
- **Go through MCP servers** — never bypass an MCP server to call the underlying API directly.
- **Nothing goes into shared Drive folder** (`Enable the Disabled - Shaun Kehoe`) without Eric's explicit approval.

---

## Open Questions for Shaun (Round 1, Unsent)

1. Client count (active clients trained in last 30 days)
2. Average monthly revenue
3. Session rate (per session, by type)
4. Top 3 monthly expenses

File: `documents/needs-documents/shaun-questions-round-1.md`

---

*End of handoff. Good luck to the next session — this one ran out of patience.*
