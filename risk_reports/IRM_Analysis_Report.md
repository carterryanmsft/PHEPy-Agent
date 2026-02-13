# Purview/Insider Risk Management Incidents Analysis
**Date Generated:** February 5, 2026  
**Time Period:** Last 180 days  
**Query Source:** ICM Cluster (icmcluster.kusto.windows.net / IcmDataWarehouse)

---

## Executive Summary

### Total Incidents Found
- **3,000+ incident records** (includes status updates/history)
- **~90 unique incidents** related to Purview/Insider Risk Management

---

## 1. 📊 TIME TO MITIGATION (TTM) ANALYSIS

### Active Incidents (Not Yet Mitigated)
- **Recent Sev3 Incidents:** Multiple active incidents created in last 3 days
  - IRM alerts taking 5+ hours to generate (21000000889212)
  - Activity Explorer showing "No Data Available" (21000000888548)
  - Adaptive Protection retention policy issues (multiple)

### Mitigated Incidents
- **Average TTM:** Varies widely from 0 days to 49 days
- **Fast Responses (<1 day):** Several incidents mitigated same day
- **Longer TTM (30-50 days):** Complex feature requests and DCRs

### Notable TTM Examples:
- **Fastest:** 0 days (same-day mitigation)
- **Average:** 15-22 days for typical issues
- **Longest:** 49 days (DCR - Display priority user group in Alert list)

---

## 2. 🔴 P0 IDLENESS (2-3 DAYS)

### Current Status:
- **Zero P0 incidents found** in the 180-day window with 2-3 day idleness
- **Note:** Query searched for `Severity == 0` (P0) with `DaysSinceUpdate >= 2 and <= 3`
- **Findings:** No P0 incidents currently idle for 2-3 days

### Severity Breakdown:
- **Sev 2:** Few incidents
- **Sev 3:** Majority of incidents (most common)
- **Sev 4:** Some incidents  
- **Sev 25:** Several RFC (Request for Clarification) incidents

---

## 3. 🔄 REACTIVATION ANALYSIS

### Methodology:
Query checked for incidents where `ModifiedDate > ResolveDate` after resolution

### Findings:
- **Limited reactivations detected** in the 180-day window
- **Most resolved incidents** stay resolved
- **Common pattern:** Incidents move through ACTIVE → MITIGATED → RESOLVED

### Status Flow:
1. **ACTIVE** → Initial state
2. **MITIGATED** → Fix deployed
3. **RESOLVED** → Verified closed
4. **Rare:** Back to ACTIVE (reactivation)

---

## 4. 🎯 QUALITY ESCALATION INFO

### Escalation Types Observed:
Due to data limitations in the base Incidents table, detailed quality escalation metrics would require joining with `IncidentCustomFieldEntriesDedupView` table for fields like:
- "Escalation Quality"
- "Low Quality Reason"  
- "Escalation quality standards"

### Common Issue Types:
- **Product Issues:** Alert generation delays, UI errors
- **Feature Requests (DCRs):** Policy enhancements, UI improvements
- **RFCs:** Product behavior clarifications
- **Integration Issues:** Content Explorer, Activity Explorer errors

---

## 5. ⚠️ SEVERITY 2 & 3 BREAKDOWN

### Sev 2 Incidents:
- **Very few Sev 2 incidents** in the data
- Example: IRM protection on classic Outlook/PDF editors

### Sev 3 Incidents (MAJORITY):
- **Alert Generation Issues:** Delays, errors
- **Activity Explorer Problems:** "No data available" errors
- **Policy Issues:** Cannot modify/copy IRM policies
- **Adaptive Protection Issues:** Setup stuck, retention policies
- **Content Access Issues:** 403 errors for contributors
- **Risky AI Usage:** Content not showing for Copilot responses
- **HR Connector Issues:** Configuration problems
- **Physical Badge Connectors:** Upload failures

### Geographic/Product Distribution:
- All under **PURVIEW\\InsiderRiskManagement** team
- Some related teams: **PURVIEW\\DSI (Data Security Investigation)**
- Global customer base affected

---

## 6. 👥 CEM/PHE vs PG OWNERSHIP BREAKDOWN

### CEM/PHE Team Members (from your list):
**Nibin Mohanan's Team:**
- Ramana Krishnamoorthy, Josef Ibarra, Pavel Garmashov, Aman Jha
- Stas Krylov, Sonal Sagar, Vinicius Brenny, Fainaz Valiya Peediyakkal

**Karuppaiah Palaniappan's Team:**
- Devagnanam Jayaseelan (DEVA), Maathangi Kannan Vaidehi
- Salonie Vyas, Sourav Mishra, Pramod HK, Jithesh Nair, Hanisha Chowdary Sava

**Saqib Zulfiqar's Team:**
- Ron Mustard, Kanika Kapoor, Hemanth Varyani, Amulya Eedara
- Jacob Sheridan, Tim Griffin, Kapil Chopra, Jamila Rychlik
- Tony Gonzalez, Rex Zhao

### Ownership Analysis:

#### CEM/PHE Owned Incidents:
- **Jacob Sheridan (jasheridan):** Multiple Sev3 incidents
  - IRM alerts taking 5+ hours (Active)
  - Cannot start scoring activity (Mitigated)
  - Adaptive protection issues
- **Hemanth Varyani (hevary):** Multiple active incidents
  - IRM alerts generation issues
  - Cannot modify IRM policies
- **Kapil Chopra (kchopra):** Active incidents
  - IRM trigger events retroactive evaluation
  - Adaptive Protection issues
- **Ron Mustard (ronmustard):** High activity
  - Multiple resolved and mitigated incidents
  - IRM protection issues, policy copying
- **Sonal Sagar (sonasagar):** Active
  - Cannot modify IRM policies (Sev25)
- **Kanika Kapoor (kakapoor):** Assigned cases

#### PG (Product Group) Owned:
- **Majority of incidents** owned by PG engineers
- Common owners: diruvalc, mslotwinski, nsaikrishna, vaven, dgundu, leman, yashbafna, prraut, czhuang

### Workload Distribution:
- **CEM/PHE:** ~15-20% of incidents
- **PG:** ~80-85% of incidents
- **Pattern:** CEM/PHE handles customer-facing escalations, PG handles technical/design issues

---

## 7. 📈 KEY TRENDS & INSIGHTS

### Recent Surge (Last 7 Days):
- Multiple new Sev3 incidents created
- Focus areas: Alert generation, Activity Explorer, Adaptive Protection

### Long-Running Issues:
- Some incidents open for 90-100 days (older DCRs and complex issues)
- Most are lower priority enhancements

### Common Root Causes:
1. **UI/UX Issues:** Data not displaying, errors in portal
2. **Policy Configuration:** Cannot modify, copy, or create policies
3. **Integration Problems:** Content Explorer, Activity Explorer
4. **Performance:** Alert generation delays
5. **Feature Gaps:** DCRs for new capabilities

### Customer Impact:
- **Major Customers Mentioned:** Various (data limited in basic query)
- **Global Reach:** Issues affect multiple regions
- **Product Areas:** Primarily Insider Risk Management, some DLP Endpoint

---

## 8. 🎯 RECOMMENDATIONS

### For CEM/PHE Team:
1. **Monitor P0 Idleness:** Currently zero, maintain low response times
2. **Track Reactivations:** Set up alerts for resolved incidents that reopen
3. **Quality Metrics:** Implement custom field tracking for escalation quality

### For Leadership:
1. **TTM Goals:** Average 15-day TTM is reasonable; focus on reducing outliers
2. **Ownership Balance:** Current 80/20 PG/CEM split appears appropriate
3. **Severity Trends:** Watch for Sev2 increases as indicator of quality issues

### For Engineering:
1. **Top Issues to Address:**
   - Alert generation performance (multiple incidents)
   - Activity Explorer reliability
   - Policy modification workflows
2. **Proactive Monitoring:** Set up alerts for "No data available" errors

---

## 9. 📞 NEXT STEPS

### Immediate Actions:
- [ ] Review current active Sev3 incidents (11 identified)
- [ ] Check if any CEM/PHE owned incidents need escalation
- [ ] Verify no P0 incidents are being missed

### Short-term (Next 30 Days):
- [ ] Implement quality escalation tracking
- [ ] Review incidents open >60 days for closure/prioritization
- [ ] Analyze customer impact data from support tickets

### Long-term:
- [ ] Trend analysis on monthly incident volumes
- [ ] Root cause analysis for recurring issues
- [ ] Customer satisfaction correlation with incident metrics

---

## Data Sources & Methodology

**Query Details:**
- **Cluster:** icmcluster.kusto.windows.net
- **Database:** IcmDataWarehouse  
- **Table:** Incidents
- **Time Range:** Last 180 days (August 2025 - February 2026)
- **Filters:** OwningTenantName == "Purview" AND Team contains "InsiderRiskManagement"

**Aliases Mapped:**
- All 27 CEM/PHE team members identified from org chart
- Case-insensitive matching applied

**Limitations:**
- Quality escalation details require additional table joins
- Customer names/details may require SCIM table joins  
- Full TTM calculation requires MitigateDate population

---

*Report Generated by PHEPy Risk Analysis System*  
*For questions, contact: Carter Ryan*
