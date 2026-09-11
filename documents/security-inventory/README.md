# Security & Asset Inventory — Enable the Disabled

**Status:** Template — ready for Shaun to populate  
**Owner:** Shaun Kehoe  
**Purpose:** Centralized inventory of all digital accounts, application platforms, and physical assets for Enable the Disabled, with security posture visibility.

---

## What This Is

A three-tab Google Sheet that lets Shaun record and maintain an inventory of:

1. **Online Accounts / Emails** — every login credential for digital services used by the business
2. **Application Platforms** — software platforms and tools the business relies on
3. **Physical Assets** — hardware, equipment, and physical items of value

Each row identifies the security posture of the asset so that Eric (or any reviewer) can quickly see:
- **What the asset is** and **why it exists**
- **When it should be used** (or by whom)
- **Whether backup/recovery is available** for it

---

## How It Was Designed for Shaun

This template was kept intentionally simple for data entry. The columns match the questions you'd naturally ask yourself when cataloging each item — no dense security jargon.

---

## Tab 1: Account Security Inventory

For every online account (email, service login, platform, etc.):

| Column | What to Enter |
|--------|---------------|
| **Service Name** | The name of the service (e.g., "QuickBooks Online", "Google Workspace") |
| **Login URL** | Where you log in (e.g., `https://quickbooks.intuit.com`) |
| **Email/User ID** | The email or username used for this account |
| **Why (Purpose)** | What the account is for in the business |
| **When (Use Case)** | When / how often it's used (e.g., "Daily invoicing", "Monthly payroll") |
| **Backup Available?** | Yes/No — is there a backup/recovery method? |
| **Backup Details** | What the backup is (e.g., "Recovery email: shan@personal.com", "2FA via Authy") |
| **MFA Enabled** | Yes/No |
| **MFA Method** | e.g., SMS, Authenticator App, Hardware Key |
| **Password Manager** | e.g., "1Password", "Bitwarden", "Kept in my head" |
| **Owner** | Who primarily uses/manages it |
| **Notes** | Anything else worth recording |

---

## Tab 2: Application Platforms Inventory

For every software platform or tool the business uses:

| Column | What to Enter |
|--------|---------------|
| **Platform Name** | Name of the platform/tool |
| **Description** | Brief description of what it does |
| **Purpose** | Why the business uses this platform |
| **Access URL** | Where to access it |
| **Who Has Access** | Who uses it / has credentials (e.g., "Shaun only", "Shaun + Sean H") |
| **Login URL** | Direct login page if different from access URL |
| **Backup Available?** | Yes/No |
| **Backup Details** | What's backed up and where |
| **MFA Enabled** | Yes/No |
| **MFA Method** | e.g., SMS, Authenticator App, Hardware Key |
| **Owner** | Primary contact / manager |
| **Notes** | Anything else |

---

## Tab 3: Physical Assets Inventory

For every physical asset owned or managed by the business:

| Column | What to Enter |
|--------|---------------|
| **Item** | Name/type of the asset (e.g., "Adjustable Dumbbell Set", "Samsung Galaxy S24") |
| **Description** | Brief description (make, model, serial number) |
| **Purpose/Benefit** | What it's used for in the business |
| **Value** | Approximate value (can be a range e.g., "$500-700") |

---

## File Locations

- **Google Drive:** `Enable the Disabled - Admin > Corporate > 08_Security > Account & Asset Inventory`
- **Local repo:** `/home/hermes/enabling-the-disabled/documents/security-inventory/`
- **Template CSVs** (for re-importing into Sheets): `account-security-inventory.csv`, `application-platforms-inventory.csv`, `physical-assets-inventory.csv`

---

## Next Steps

1. **Shaun** populates each tab with current inventory
2. **Eric** reviews for gaps and security posture
3. Schedule quarterly reviews to keep the inventory current

---

*Template created by fitness-strategist profile • September 2026*
