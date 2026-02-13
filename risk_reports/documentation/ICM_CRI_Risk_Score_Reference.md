# ICM CRI Risk Score - Risk Factors Reference
# Source: ICM Risk Assessment Documentation
# Date: February 4, 2026

## Risk Visibility at First Glance
Risk levels are surfaced directly in the incident list view, allowing teams to quickly scan, filter, and prioritize incidents by risk.

**Risk Levels:**
- 🔴 **Critical Risk Incidents (Severity 25)** - Highest priority
- 🟠 **High Risk Incidents (Severity 3)** - Elevated priority

---

## CRI Risk Score Factors

The CRI Risk Score evaluates 7 key factors to determine incident risk:

### 1. **Severity Changes**
**Risk Condition:** Severity is upgraded or remains unchanged without system changes  
**Example:** Severity unchanged (Sev B → Sev A)  
**Impact:** Indicates escalating or persistent issues

### 2. **Ownership Changes**
**Risk Condition:** Incident transferred between multiple owners/teams  
**Example:** Incident reassigned 3 times  
**Impact:** High transfer count indicates confusion, lack of expertise, or organizational gaps

### 3. **Idle Period Changes**
**Risk Condition:** No recorded engineer activity for extended window  
**Example:** 6/27-8/11 no activity  
**Impact:** Prolonged silence suggests stalled resolution or abandoned cases

### 4. **Reactivation Changes**
**Risk Condition:** Incident repeatedly reactivated after being idle or stalled  
**Example:** Multiple reopen / reactivate events  
**Impact:** Indicates unresolved root cause or incomplete mitigation

### 5. **Sentiment Analysis**
**Risk Condition:** Negative or risky sentiment inferred from interactions or prolonged inactivity  
**Example:** Negative sentiment  
**Impact:** Customer frustration, escalation risk, or poor communication

### 6. **Communication Proofs**
**Risk Condition:** No evidence of internal communication  
**Example:** System logs only  
**Impact:** Lack of collaboration or transparency

### 7. **Incident Details/Age/Status**
**Risk Condition:** Incident remains active beyond expected duration without resolution  
**Example:** Active for multiple weeks  
**Impact:** Age without progress indicates systemic or complex issues

---

## Clear Team Relevance and Ownership Context
Incidents are evaluated using backend mappings across CxE Care ICM teams and products, making it explicit what is considered "related to my team."

**Product Mappings:**
- MTP (Microsoft Threat Protection)
- Intune
- Entra
- Purview

---

## Who It's For
**Target Audience:**
- **CLEs** (Customer Lead Engineers) who need a prioritized list of high-risk or "problem" CRIs, with clear context (e.g., long idle periods, severity changes, ownership changes)
- **CSS and PHE Team Leads** who need a daily, incident-level view of ICM risk to quickly identify where intervention is required

---

## How It Scales and Future Plan
**Designed as a scalable, batch-capable solution:**
- Automatically evaluates hundreds to thousands of ICMs without manual review
- Enables consistent, repeatable risk assessment across teams and shifts
- Accessible beyond the agent, with **Power BI dashboard support coming in January** across four product verticals

---

## Integration with Support Case Risk Scoring

**Mapping to Support Case Risk Factors:**

| ICM CRI Factor | Support Case Equivalent | Weight |
|----------------|-------------------------|--------|
| Severity Changes | ServiceRequestCurrentSeverity escalation | 5 pts |
| Ownership Changes | OwnershipCount | 0-20 pts |
| Idle Period Changes | Days in current status without updates | 0-15 pts |
| Reactivation Changes | ReopenCount | 5 pts each |
| Sentiment Analysis | Customer sentiment (if available) | 0-10 pts |
| Communication Proofs | Last update time, engineer notes | 0-10 pts |
| Age/Status | DaysOpen (CaseAge) | 0-40 pts |

**Additional Support Case Factors:**
- **Transfer Count**: 0-15 pts (similar to ownership changes)
- **Related ICM Presence**: 10 pts (indicates escalation)
- **Crit Sit Status**: Automatic Critical rating

---

## Risk Score Calculation

**Total Score: 0-100 points**

**Risk Levels:**
- **Critical**: 80-100 points
- **High**: 60-79 points
- **Medium**: 40-59 points
- **Low**: 0-39 points

---

## Actionable Outputs

**For CLEs and PHE:**
1. **Prioritized Incident List** - Sorted by risk score
2. **Send Email to CLE** - Direct notification with context
3. **Portfolio Summary** - Overview of:
   - Total incidents
   - Final Rating distribution (Minimal, Low, Medium, High, Critical)
   - Medium+ incidents count

---

## References
- ICM CRI Risk Score Agent Documentation
- Power BI Dashboard (Coming January 2026)
- CxE Care ICM Team Mappings
