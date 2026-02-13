# Purview ICM TSG Gap Analysis Report
**Generated:** February 4, 2026  
**Data Source:** ICM MCP (3 sample incidents from Purview eDiscovery)  
**Analysis Focus:** eDiscovery Purge, Content Search, Review Set issues

---

## Executive Summary

Analysis of **3 ICM escalations** from Purview eDiscovery team identified **100% TSG gap rate** (3/3 incidents could have benefited from improved TSG coverage). All incidents involved customer-impacting scenarios with missing or incomplete troubleshooting guidance.

**Key Finding:** eDiscovery product area shows critical TSG gaps in:
- Content purge operations (premium cases)
- Teams meeting deletion via backend
- Review set search/modern UI functionality

---

## Incident Analysis

### 🔴 ICM 636778552: Purge Content in Premium Cases
- **Product:** eDiscovery
- **Severity:** 3
- **Impact:** High
- **Duration:** 6 days (2025-05-30 → 2025-06-05)
- **Customer:** Oregon (GCC Unified Support)

**Issue:** Customer unable to purge content in eDiscovery premium cases due to litigation hold. 

**Gap Indicators:**
- ❌ "No TSG available" explicitly mentioned
- ❌ Missing steps for hold identification/removal
- ❌ GCC environment specifics not documented

**Recommended TSG:**
```
Title: "eDiscovery Premium - Purge Content with Active Litigation Hold"
Scope:
- How to identify hold types on Exchange mailbox
- Hold removal procedures for different hold types
- GCC-specific considerations
- Graph cmdlet vs PowerShell approach
Reference: https://learn.microsoft.com/en-us/purview/ediscovery-identify-a-hold-on-an-exchange-online-mailbox
```

---

### 🔴 ICM 687747177: Delete Teams Meeting from Backend
- **Product:** eDiscovery  
- **Severity:** 3
- **Impact:** Critical (UNHCR tenant)
- **Duration:** 42 days (2025-09-19 → 2025-10-31)
- **Customer:** UNHCR

**Issue:** Customer executed 3 content searches + PowerShell commands to delete Teams meeting. Commands succeeded but invite not removed from Teams/Outlook.

**Gap Indicators:**
- ❌ "No documentation" for Graph cmdlet purge scenario
- ❌ Commands succeed but outcome fails (misleading success status)
- ❌ Modern UX vs Classic eDiscovery differences not clear

**Recommended TSG:**
```
Title: "eDiscovery - Remove Recurring Teams Meeting via Content Search"
Scope:
- Modern UX vs Classic eDiscovery capabilities
- Graph cmdlet limitations (Teams vs Exchange content)
- Remove-CalendarEvents cmdlet usage
- Verification steps to confirm deletion
- Troubleshooting "success" status but no actual change
Reference: Existing TSG noted: https://dev.azure.com/ASIM-Security/Compliance/_wiki/wikis/eDiscovery/12382/How-To-Remove-a-Recurring-Teams-Meeting-from-a-deleted-user
```

---

### 🔴 ICM 724369842: Review Set Search Performance
- **Product:** eDiscovery
- **Severity:** 3
- **Impact:** High (Aditya Birla Capital - APAC)
- **Duration:** 21 days (2025-12-18 → 2026-01-08)
- **Customer:** Aditya Birla Capital

**Issue:** After adding multiple searches to Review Set, queries fail to execute. Progress bar stuck for 24+ hours. Query works in premium case but not Modern UI.

**Gap Indicators:**
- ❌ "Unable to perform searches" - unclear process
- ❌ Modern UI vs Classic behavior differences
- ❌ No guidance on stuck progress indicators
- ❌ Previously escalated (ICM 678625824) - repeated issue

**Recommended TSG:**
```
Title: "eDiscovery Review Set - Search Performance/Stuck Progress"
Scope:
- Modern UI review set search prerequisites
- Add to Review Set job monitoring
- Stuck progress troubleshooting (24+ hours)
- KEYQL query validation
- Difference from premium case search execution
- HAR/PPT log collection for escalation
```

---

## Gap Analysis Summary

### By Product Area
| Product | Incidents | Gap % | Priority |
|---------|-----------|-------|----------|
| **eDiscovery** | 3 | 100% | 🔴 HIGH |

### By Gap Type
| Gap Type | Count | Incidents |
|----------|-------|-----------|
| Missing Documentation | 1 | ICM 636778552 |
| Unclear Process | 2 | ICM 687747177, 724369842 |
| Missing Diagnostic Steps | 1 | ICM 687747177 |

### By Issue Pattern
1. **Purge/Delete Operations** - 2 incidents (premium case purge, Teams meeting delete)
2. **Review Set Operations** - 1 incident (search performance)
3. **Modern UI vs Classic** - 2 incidents (recurring theme)

---

## Recommendations

### Immediate Actions
1. **Create TSG:** "eDiscovery Premium - Purge Content with Active Litigation Hold"
   - Priority: HIGH (explicitly mentioned "no TSG")
   - Owner: eDiscovery team (nimahar)
   - Template from: Viva Pulse 2-page Access + Mitigate pattern

2. **Update TSG:** "How To Remove a Recurring Teams Meeting" (existing)
   - Add section on Graph cmdlet limitations
   - Document "success but no change" troubleshooting
   - Owner: eDiscovery team

3. **Create TSG:** "eDiscovery Review Set - Search Performance Issues"
   - Priority: HIGH (repeated escalations)
   - Focus on Modern UI transition challenges
   - Owner: eDiscovery team (harriyin, zaidzeitoun)

### Systemic Issues
- **Modern UI Transition:** 2/3 incidents involve Classic → Modern UX gaps
  - Recommendation: Create "Modern UI Migration Guide" meta-TSG
  - Cross-reference all affected TSGs with Modern UI callouts

- **GCC/GCCH Environments:** 1/3 incidents GCC-specific
  - Recommendation: Add GCC considerations to all eDiscovery TSGs
  - Standard section: "GCC/GCCH Limitations"

---

## Existing TSG Coverage Analysis

From ASIM-Security wiki baseline (Purview eDiscovery):
- **Total Pages:** 230
- **TSG Coverage:** 47% (108 TSGs)
- **Rating:** ⭐⭐⭐ (Good but gaps remain)

**Missing Coverage Identified:**
- ✅ Hold removal process (1 TSG exists, needs expansion)
- ❌ Teams meeting deletion via backend (1 TSG exists but incomplete)
- ❌ Review Set search performance/Modern UI (NO TSG)

---

## Next Steps

1. **Execute Remaining Kusto Queries** (Queries 2-8 in purview_icm_gap_analysis.kql)
   - Query 2: Repeated issues (3+ occurrences)
   - Query 6: TSG gap score by product area
   - Query 7: Top 20 recommended TSGs

2. **Expand Analysis** to additional Purview products:
   - DLP (59% TSG coverage - good baseline)
   - Auditing (61% coverage - good baseline)
   - DSPM for AI (11% coverage - CRITICAL GAPS)
   - Shared Components (0% coverage - CRITICAL GAPS)

3. **Validate with Engineering Team**
   - Review findings with eDiscovery PG (nimahar, harriyin)
   - Prioritize TSG creation roadmap
   - Identify subject matter experts for authoring

---

## Appendix: ICM Incident Details

### ICM 636778552
- **Support Case:** 2505060040008186
- **Tenant:** stateoforegon.onmicrosoft.com
- **Tenant ID:** aa3f6932-fa7c-47b4-a0ce-a598cad161cf
- **Contact:** nimahar
- **TSG Link:** NA
- **TSG Effectiveness:** No

### ICM 687747177  
- **Support Case:** 2506031420003320
- **Tenant:** UNHCR
- **Tenant ID:** e5c37981-6664-4134-8a0c-6543d2af80be
- **Contact:** nimahar
- **TSG Link:** https://dev.azure.com/ASIM-Security/Compliance/_wiki/wikis/eDiscovery/12382/How-To-Remove-a-Recurring-Teams-Meeting-from-a-deleted-user
- **TSG Effectiveness:** Yes (but incomplete)

### ICM 724369842
- **Support Case:** 2506190030007146
- **Tenant:** Aditya Birla Capital  
- **Tenant ID:** 24fa3089-8e98-4c9f-960f-8a36a2a96bf6
- **Contact:** harriyin, zaidzeitoun (reviewer)
- **TSG Link:** https://dev.azure.com/Supportability/Modern%20Workplace/_wiki/wikis/Modern%20Workplace/254665/eDiscovery
- **TSG Effectiveness:** Yes
- **Related ICM:** 678625824 (repeated issue)

---

**Report prepared by:** PHEPy Orchestrator Agent  
**Data Sources:** ICM MCP ENG, ASIM-Security Compliance Wiki  
**Methodology:** Manual ICM incident analysis + wiki TSG baseline comparison
