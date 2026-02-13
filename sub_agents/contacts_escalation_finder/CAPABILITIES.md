# Contacts & Escalation Finder - Capabilities Matrix

**Agent:** Contacts & Escalation Finder  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 🎯 Core Capabilities

### 1. Product Group (PG) Contact Discovery

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **PG Lead by Component** | Find PG lead for Purview components (MIP, DLP, etc.) | Contact registry | ✅ Ready |
| **On-Call Lookup** | Current on-call engineer for off-hours escalation | On-call system | ✅ Ready |
| **Feature Owner** | Find owner for specific feature or capability | Grounding docs | ✅ Ready |
| **Escalation Contact** | Designated contact for critical escalations | Contact registry | ✅ Ready |
| **PM Contact** | Program Manager for product area | Contact registry | ✅ Ready |

### 2. Customer Support Services (CSS) Contact Discovery

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **CSS Manager by Customer** | Find CSS manager assigned to customer | Customer registry | ✅ Ready |
| **Regional Support Team** | Identify support team by region/geo | Contact registry | ✅ Ready |
| **CSS On-Call** | Current on-call CSS engineer | On-call system | ✅ Ready |
| **Account Manager** | Customer success/account manager | Customer registry | ✅ Ready |
| **Technical Account Manager** | TAM for enterprise customers | Customer registry | ✅ Ready |

### 3. Escalation Path Guidance

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Escalation Ladder** | Recommended escalation sequence | Escalation playbooks | ✅ Ready |
| **Severity-Based Routing** | Route based on issue severity | Escalation rules | ✅ Ready |
| **Business Hours vs On-Call** | Route based on time/urgency | On-call system | ✅ Ready |
| **Fallback Contacts** | Alternative contacts if primary unavailable | Contact registry | ✅ Ready |
| **Response Time Estimates** | Expected response SLA per contact | SLA definitions | ✅ Ready |

### 4. Contact Information Retrieval

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Email Address** | Official work email | Azure AD | ✅ Ready |
| **Slack/Teams Handle** | IM contact method | Directory | ✅ Ready |
| **Phone Number** | Official work phone | Directory | ✅ Ready |
| **Availability Status** | Online, Away, DND status | Microsoft Graph | ✅ Ready |
| **Out of Office** | OOF status and duration | Exchange/Outlook | ✅ Ready |

### 5. Initiative & Program Contacts

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **MCS/IC Program Contacts** | Find PM for specific cohort | Grounding docs | ✅ Ready |
| **Pilot/Preview Contacts** | Contacts for feature pilots | Grounding docs | ✅ Ready |
| **Customer-Facing Contacts** | Approved contacts for customer communication | Contact registry | ✅ Ready |
| **Executive Sponsors** | Leadership contacts for strategic customers | Grounding docs | ✅ Ready |

---

## 📋 Contact Types & Categories

### Product Group Contacts

| Role | Responsibility | When to Contact |
|------|----------------|-----------------|
| **PG Lead** | Overall product area ownership | Strategic decisions, roadmap questions |
| **Dev Lead** | Engineering leadership | Technical architecture questions |
| **PM Lead** | Program management | Feature planning, customer feedback |
| **On-Call Engineer** | 24/7 incident response | After-hours P0/P1 incidents |
| **Feature Owner** | Specific feature/capability | Feature bugs, enhancement requests |
| **Escalation Contact** | Designated for critical issues | SLA breach, VIP customer issues |

### CSS Contacts

| Role | Responsibility | When to Contact |
|------|----------------|-----------------|
| **CSS Manager** | Customer account ownership | Account-level escalations |
| **Support Engineer** | Technical case support | Case troubleshooting |
| **CSS On-Call** | After-hours support | Urgent customer issues off-hours |
| **Escalation Engineer** | Complex issue resolution | Technical escalations |
| **Regional Lead** | Geographic support leadership | Regional issues, capacity |

### Executive & Leadership

| Role | Responsibility | When to Contact |
|------|----------------|-----------------|
| **VP/CVP** | Executive leadership | Strategic customer issues, crisis |
| **GM** | Product line ownership | Product direction, major incidents |
| **Director** | Team leadership | Team-level escalations |
| **Principal PM** | Senior technical leadership | Complex technical decisions |

---

## 🔍 Lookup Methods

### By Product Area

```
Product Areas:
- Microsoft Information Protection (MIP)
  - Classification & Labeling
  - Sensitivity Labels
  - Auto-labeling
  
- Data Loss Prevention (DLP)
  - Email DLP
  - Endpoint DLP
  - Teams DLP
  
- eDiscovery
  - Content Search
  - Legal Hold
  - Advanced eDiscovery
  
- Information Rights Management (IRM)
  
- Data Lifecycle Management (DLM)
  - Retention Policies
  - Records Management
  
- Insider Risk Management
  
- Communication Compliance
  
- Content Explorer / Activity Explorer
```

**Query Pattern:**
```
"Who is the PG lead for [Product Area]?"
"Who owns [specific feature]?"
"Who can I escalate [Product Area] issues to?"
```

---

### By Customer

```
Customer Attributes:
- Customer Name
- TenantId
- Account Tier (VIP, Enterprise, Standard)
- Region/Geo
- Segment (Commercial, Government, EDU)
```

**Query Pattern:**
```
"Who is the CSS manager for [Customer Name]?"
"Who supports tenant [TenantId]?"
"Who is the TAM for [VIP Customer]?"
```

---

### By Escalation Type

```
Escalation Types:
- Technical Issue (product bug, performance)
- Customer Escalation (VIP, SLA breach)
- Feature Request (DCR, enhancement)
- Service Incident (outage, degradation)
- Security Issue (vulnerability, breach)
```

**Routing Logic:**
| Escalation Type | Severity | Business Hours | After Hours |
|-----------------|----------|----------------|-------------|
| Technical Issue | P0/P1 | PG Escalation Contact | PG On-Call |
| Technical Issue | P2/P3 | Feature Owner | Wait for business hours |
| Customer Escalation | Any | CSS Manager + PG Lead | CSS On-Call + PG On-Call |
| Service Incident | P0 | PG On-Call + VP | PG On-Call + VP |
| Security Issue | Any | Security Response Team | Security On-Call |

---

## 📞 Contact Methods & SLAs

### Contact Methods (Priority Order)

1. **P0 Critical (Immediate Response Required)**
   - Phone call to on-call
   - ICM incident creation (auto-pages)
   - Slack DM with @mention
   - Email (CC: manager + team alias)

2. **P1 Urgent (Same-Day Response)**
   - Slack DM
   - Email (to individual)
   - Teams chat
   - ICM incident (if escalating to PG)

3. **P2 Normal (Next Business Day)**
   - Email
   - Slack/Teams
   - Team channel

4. **P3 Low (Best Effort)**
   - Email to team alias
   - GitHub issue / ADO work item
   - Teams channel post

---

### Expected Response Times

| Priority | Business Hours | After Hours | Escalation if No Response |
|----------|----------------|-------------|---------------------------|
| **P0** | 15 minutes | 30 minutes | Manager after 30 min |
| **P1** | 2 hours | 4 hours | Manager after 4 hours |
| **P2** | 8 hours (same day) | Next business day | Team lead after 1 day |
| **P3** | 2 business days | 5 business days | No escalation |

---

## 🚨 Escalation Paths

### Technical Issue Escalation Path

```
Level 1: Feature Owner / Support Engineer
   ↓ (If unresolved in 2 hours for P1, 4 hours for P2)
Level 2: Dev Lead / CSS Escalation Engineer
   ↓ (If unresolved in 4 hours for P1, 1 day for P2)
Level 3: PG Lead / CSS Manager
   ↓ (If customer impact high or SLA risk)
Level 4: Director / VP
```

### Customer Escalation Path

```
Level 1: CSS Manager + PG Feature Owner
   ↓ (If VIP or SLA breach imminent)
Level 2: CSS Director + PG Lead
   ↓ (If strategic account or exec visibility)
Level 3: VP (CSS) + VP (PG)
```

### Service Incident Path

```
Level 1: PG On-Call Engineer
   ↓ (Create ICM incident - auto-escalates)
Level 2: Dev Lead / Service Owner
   ↓ (If multi-service or widespread)
Level 3: Director / GM
   ↓ (If CVP attention needed)
Level 4: CVP / Corporate VP
```

---

## 🔐 Privacy & Security Guardrails

### Information That Can Be Shared

✅ **Allowed:**
- Official work email (name@microsoft.com)
- Work phone number (from directory)
- Slack/Teams handle
- Job title and team
- Office location
- Manager name (public org chart)

❌ **Not Allowed:**
- Personal email addresses
- Personal phone numbers
- Home address
- Private calendar details (beyond OOF)
- Performance information
- Org changes not yet announced

---

### Contact Information Verification

**Before providing contact:**
1. Verify contact is current (check last updated date)
2. Check for OOF status
3. Provide alternative if contact unavailable
4. Never guess or fabricate

**If contact not found:**
- "I don't have current information for [person/role]"
- "Please check [official source]: org chart, on-call system"
- "Would you like me to find the team alias instead?"

---

## 🔄 Contact Currency & Maintenance

### Data Freshness Indicators

| Source | Update Frequency | Staleness Warning |
|--------|------------------|-------------------|
| Azure AD | Real-time | None (always current) |
| On-Call System | Real-time | None |
| Contact Registry | Monthly | Warn if >90 days old |
| Grounding Docs | Quarterly | Warn if >6 months old |

---

### Fallback Strategy

**If primary contact unavailable:**
1. Check on-call system for current assignment
2. Provide team alias (e.g., purview-mip-team@microsoft.com)
3. Suggest manager escalation
4. Offer to find backup contact

---

## 🚫 Out of Scope

This agent **does NOT**:
- Make introductions or send emails on behalf of user
- Schedule meetings between parties
- Make commitments about response times
- Provide performance or personnel information
- Share contacts for non-work purposes
- Bypass official escalation procedures

---

## 📏 Success Metrics

- **Contact Accuracy:** >95% of provided contacts are current and correct
- **Routing Precision:** >90% of escalation recommendations are appropriate
- **Response Time:** < 30 seconds to provide contact info
- **Fabrication Rate:** 0% (never guess)
- **Privacy Compliance:** 100% (never share private info)

---

## 🆘 Escalation Paths

**When to Escalate:**
- Cannot find contact info in authoritative sources
- Multiple possible contacts and need disambiguation
- User needs help deciding who to contact
- Contact info appears outdated
- Privacy concern with requested contact info

**Escalation Target:**
- **Unknown PG Contact** → Check with PG leadership or use team alias
- **Unknown CSS Contact** → Check customer registry or regional lead
- **Outdated Contact** → Request grounding doc update
- **Privacy Concern** → Clarify use case, provide team alias instead
