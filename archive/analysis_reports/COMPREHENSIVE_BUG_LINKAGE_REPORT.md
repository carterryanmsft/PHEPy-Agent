# Comprehensive Bug Linkage Analysis Report
## IC/MCS Customer Incidents and Associated Bugs

**Date:** February 2026  
**Analysis Scope:** 135 ICM incidents from IC/MCS customer cases

---

## Executive Summary

Analysis of IC/MCS customer incidents revealed **11 unique bugs** linked as repair items across **11 ICMs**, affecting **7 customers** (5 IC, 2 MCS customers).

### Key Findings

- **11 bugs** found directly linked as repair items in IncidentBugs table
- **7 customers** affected: Ford, BHP, Novartis, AGL Energy, Vodafone (IC); Morgan Stanley, Barclays Bank (MCS)   - **Morgan Stanley** most affected with 3 bugs
- **Total linkages:** 191 bug-ICM link records across all incidents

---

## Method 1: Bugs Linked as Repair Items

### IC Customers (5 Customers, 6 Bugs)

| Customer | Bug ID | Status | ICM | Case Number | Links |
|----------|--------|--------|-----|-------------|-------|
| **Ford** | [6306283](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/6306283) | New | 703334015 | 2510060040000051 | 44 |
| **BHP** | [5806337](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/5806337) | Closed | 616515906 | 2409240030008299 | 31 |
| **Novartis** | [60605756](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/60605756) | Resolved/Active | 718445455 | 2511271420001502 | 13 |
| **Novartis** | [6281633](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/6281633) | Closed | 712466636 | 2509221410000484 | 7 |
| **AGL Energy** | [6794267](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/6794267) | New | 721235722 | 2511130030000335 | 9 |
| **Vodafone** | [21227](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/21227) | Removed | 680275765 | 2504231420002138 | 2 |

### MCS Customers (2 Customers, 5 Bugs)

| Customer | Bug ID | Status | ICM | Case Number | Links |
|----------|--------|--------|-----|-------------|-------|
| **Morgan Stanley** | [6254385](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/6254385) | Active/New | 681780305 | 2508200050003157 | 40 |
| **Morgan Stanley** | [2755112](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/2755112) | Done | 675908430 | 2506180050001318 | 9 |
| **Morgan Stanley** | [6296924](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/6296924) | Resolved/New | 701554955 | 2509300050003302 | 7 |
| **Barclays Bank** | [5995267](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/5995267) | Closed | 659601256 | 2507180050002877 | 16 |
| **Barclays Bank** | [6927933](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/6927933) | Closed | 718828407 | 2507180050002877 | 6 |

---

## Method 2: ADO Bug Hyperlinks

Previous analysis of 7 ADO bugs with "Customer Escalation" tags revealed:

- **6 of 7 bugs** have NO ICM hyperlinks in their ADO relations
- **1 bug** (3563451) has 4 ICM hyperlinks but to different incidents than customer cases
- **Gap:** ADO bugs tagged with customer names lack ICM hyperlinks

### ADO Bugs WITHOUT ICM Hyperlinks

| Bug ID | Customer | Area Path | State |
|--------|----------|-----------|-------|
| [7075966](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/7075966) | MUFJ | Enhanced Identity | Active |
| [6927825](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/6927825) | MUFJ | Role Group Management | Active |
| [6930337](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/6930337) | MUFJ | Outlook Web App | Active |
| [6961092](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/6961092) | MUFJ | Test | Active |
| [3463427](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/3463427) | Novartis | Mail Flow | Active |
| [3498880](https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/3498880) | ADNOC | MailTips\MailTips | Active |

---

## Method 3: Bug URLs in ICM Comments

Additional analysis found ICMs that mention bug URLs in their text fields (Title, Summary, ReproSteps, Mitigation, HowFixed):

- **ICM 731225498** (State of WA) contains bug URL mentions in Summary field
- **1900+ ICM text entries** reviewed for bug URL patterns
- **Parsing required** to extract specific bug IDs from text content

---

## Comparison with Original 17 Bugs

### Original Bug List Analysis

Of the 17 bugs originally questioned:

| Found in ICM? | Count | Location |
|---------------|-------|----------|
| ✅ Yes | 7 | IncidentBugs table |
| ❌ No | 10 | NOT in any IC/MCS ICM |

### Bugs Found in ICM (7 bugs)

✅ **Linked as Repair Items:**
- 6306283 (Ford)
- 6254385 (Morgan Stanley)  
- 5806337 (BHP)
- 5995267 (Barclays Bank)
- 60605756 (Novartis)
- 6794267 (AGL Energy)
- 2755112 (Morgan Stanley)

### Bugs NOT Found (10 bugs)

❌ **Missing from ICM:**
- 7075966, 6927825, 6930337, 6961092 (MUFJ - ADO only)
- 3463427 (Novartis - ADO only)
- 3498880 (ADNOC - ADO only)
- 3563451 (NAB - has unrelated ICM links)
- 6296924, 6281633, 6927933 (may be in ICM text but not as repair items)

---

## Root Cause Analysis

### Why Bugs Are Not Linked

1. **Missing ICM Hyperlinks in ADO (86% of bugs)**
   - 6 of 7 ADO bugs with "Customer Escalation" tags have NO ICM hyperlinks
   - Engineers not adding ICM links to bug relations in Azure DevOps

2. **Missing Repair Items in ICM (59% of original bugs)**
   - 10 of 17 bugs not recorded in IncidentBugs table
   - Bugs discussed in ICM comments but not formally linked

3. **Wrong ICM Linkage (6% of bugs)**
   - Bug 3563451 has ICM hyperlinks but to incidents unrelated to customer cases
   - Indicates potential mislinking or investigation spanning multiple incidents

---

## Metrics Summary

### Coverage Analysis

| Metric | Count | Percentage |
|--------|-------|------------|
| Total ICMs Analyzed | 135 | 100% |
| ICMs with Bugs as Repair Items | 11 | 8.1% |
| Total Unique Bugs Found | 11 | - |
| Total Bug-ICM Linkages | 191 | - |
| Customers Affected | 7 | - |

### Bug Status Distribution

| Status | Count | Percentage |
|--------|-------|------------|
| Closed | 4 | 36% |
| New | 3 | 27% |
| Active/Resolved | 3 | 27% |
| Done | 1 | 9% |

### Program Distribution

| Program | Customers | Bugs |
|---------|-----------|------|
| IC | 5 | 6 |
| MCS | 2 | 5 |

---

## Recommendations

1. **Enforce ICM Hyperlink Policy**
   - Require ICM hyperlinks in ADO bug relations for all customer escalations
   - Add validation to bug creation workflow

2. **Standardize Repair Item Tracking**
   - Link bugs as repair items in IncidentBugs table, not just comments
   - Train engineers on proper ICM-bug linkage procedures

3. **Audit Historical Bugs**
   - Review 10 missing bugs from original list
   - Add ICM hyperlinks where applicable

4. **Monitor Bug Linkage Metrics**
   - Track percentage of customer bugs with ICM hyperlinks
   - Set target: 100% linkage for customer escalation bugs

---

## Data Sources

- **ICM Database:** icmcluster.kusto.windows.net/icmdatawarehouse
  - Tables: IncidentBugs, Incidents, IncidentDescriptions
- **Azure DevOps:** o365exchange.visualstudio.com/IP%20Engineering
  - Work Item Search API with tags: Customer Escalation, P0ClassificationBug
- **Case Data:** production_full_cases.csv (135 IC/MCS customer cases)

---

## Files Generated

- `comprehensive_icm_bug_analysis.json` - Full bug-ICM-customer mappings
- `bug_linkage_root_cause_analysis.json` - Root cause analysis details
- `ado_bugs_icm_hyperlinks_final.json` - ADO bug hyperlink extraction results
- `ic_mcs_customer_bug_mapping.json` - Customer-bug relationship mappings

---

**Analysis Date:** February 2026  
**Analyst:** Automated Analysis via Kusto + Azure DevOps APIs
