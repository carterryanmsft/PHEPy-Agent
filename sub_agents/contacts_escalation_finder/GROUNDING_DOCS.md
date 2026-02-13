# Contacts & Escalation Finder - Grounding Documents

**Agent:** Contacts & Escalation Finder  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 📚 Required Grounding Documents

### 1. PG & CSS Contact Registry
**File:** `grounding_docs/contacts_access/pg_css_contacts.md`

**Required Content:**
- Product area owners (MIP, DLP, eDiscovery, etc.)
- PG leads, Dev leads, PM leads per component
- CSS managers by region and customer segment
- Team aliases for each product area
- Last updated timestamps

**Status:** 🟡 Needs Creation

---

### 2. Escalation Contacts
**File:** `grounding_docs/contacts_access/escalation_contacts.md`

**Required Content:**
- Designated escalation contacts per severity
- On-call rotation schedules
- Executive escalation paths
- Response time SLAs per contact type

**Status:** 🟡 Needs Creation

---

### 3. Customer Contact Assignments
**File:** `grounding_docs/contacts_access/CUSTOMER_LOOKUP_GUIDE.md`

**Required Content:**
- Customer to CSS manager mapping
- TAM assignments for VIP customers
- Account tier information
- Regional support coverage

**Status:** ✅ Exists (reference in contacts_access/)

---

### 4. Initiative & Pilot Contacts
**File:** `grounding_docs/contacts_access/initiatives_pilots.md`

**Required Content:**
- MCS/IC program PM contacts
- Pilot program leads
- Customer-facing communication contacts

**Status:** 🟡 Needs Creation

---

## 🔗 External Data Sources

- **Azure AD / Microsoft Graph:** Real-time directory lookups
- **On-Call System:** Current on-call assignments
- **Exchange:** OOF status checks
- **Org Chart API:** Manager relationships

**All grounding docs should be updated monthly.**
