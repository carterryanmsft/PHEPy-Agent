# By Design ICM Analysis - Real Data with ICM IDs & Customers
**Data Source:** IC/MCS Production Cases  
**Total ICMs Analyzed:** 135  
**Affected Customers:** 18  
**Date:** February 10, 2026

---

## Executive Summary

Analyzed 135 unique ICMs across 90 IC/MCS cases affecting 18 strategic customers. Focus on 5 priority Purview feature areas commonly associated with "By Design" resolutions.

### Key Findings

1. **DLP** has highest ICM volume (34 ICMs) but focus is on core Info Protection features
2. Priority features represent **89** ICMs across **16** customers
3. Top customer: **Morgan Stanley** (12 ICMs)

---

## Feature Area Analysis with ICM IDs


### 🎯 Sensitivity Labels

**Total ICMs:** 13  
**Customers:** 5  
**Cases:** 7  

**Most Referenced ICMs:**

- **ICM 725859865**: 1 cases
  - Customers: State of WA
  - Case #: 2510030010001581
- **ICM 731225498**: 1 cases
  - Customers: State of WA
  - Case #: 2510030010001581
- **ICM 695639748**: 1 cases
  - Customers: State of WA
  - Case #: 2510030010001581
- **ICM 692107101**: 1 cases
  - Customers: Autodesk
  - Case #: 2508250060002344
- **ICM 650527915**: 1 cases
  - Customers: Morgan Stanley
  - Case #: 2506180050001318

**Affected Customers:**

- **Morgan Stanley**: 4 ICMs, 4 cases
  - ICMs: 650527915, 664019513, 675908430...
- **State of WA**: 4 ICMs, 4 cases
  - ICMs: 725859865, 731225498, 695639748...
- **Novartis**: 3 ICMs, 3 cases
  - ICMs: 705189268, 712466636, 21000000856644
- **Autodesk**: 1 ICMs, 1 cases
  - ICMs: 692107101
- **Santander**: 1 ICMs, 1 cases
  - ICMs: 687188371


### 🎯 Purview Message Encryption

**Total ICMs:** 57  
**Customers:** 14  
**Cases:** 38  

**Most Referenced ICMs:**

- **ICM 725828510**: 2 cases
  - Customers: Barclays Bank
  - Case #: 2510200030005670
- **ICM 704121978**: 2 cases
  - Customers: Barclays Bank
  - Case #: 2510200030005670
- **ICM 719540148**: 2 cases
  - Customers: Barclays Bank
  - Case #: 2510200030005670
- **ICM 726186526**: 2 cases
  - Customers: Barclays Bank
  - Case #: 2512230050000977
- **ICM 51000000883229**: 2 cases
  - Customers: BHP
  - Case #: 2601090030005190

**Affected Customers:**

- **Barclays Bank**: 7 ICMs, 11 cases
  - ICMs: 725828510, 719540148, 704121978...
- **MUFJ**: 10 ICMs, 10 cases
  - ICMs: 694997702, 670828774, 724667306...
- **Huntington**: 9 ICMs, 9 cases
  - ICMs: 693849812, 693543577, 694142803...
- **Morgan Stanley**: 6 ICMs, 6 cases
  - ICMs: 701554955, 711102686, 710971405...
- **Novartis**: 5 ICMs, 5 cases
  - ICMs: 723058663, 21000000873960, 730114940...


### 🎯 Classification

**Total ICMs:** 10  
**Customers:** 5  
**Cases:** 7  

**Most Referenced ICMs:**

- **ICM 730591118**: 1 cases
  - Customers: Barclays Bank
  - Case #: 2510230050001992
- **ICM 708806387**: 1 cases
  - Customers: Barclays Bank
  - Case #: 2510230050001992
- **ICM 717584340**: 1 cases
  - Customers: Barclays Bank
  - Case #: 2510230050001992
- **ICM 681780305**: 1 cases
  - Customers: Morgan Stanley
  - Case #: 2508200050003157
- **ICM 704668547**: 1 cases
  - Customers: Huntington
  - Case #: 2510270040012508

**Affected Customers:**

- **Barclays Bank**: 4 ICMs, 4 cases
  - ICMs: 730591118, 708806387, 717584340...
- **Huntington**: 2 ICMs, 2 cases
  - ICMs: 704668547, 51000000859513
- **Morgan Stanley**: 2 ICMs, 2 cases
  - ICMs: 681780305, 730544548
- **MUFJ**: 1 ICMs, 1 cases
  - ICMs: 51000000864264
- **Santander**: 1 ICMs, 1 cases
  - ICMs: 21000000862533


---

## Top 10 Customers by ICM Count

| Customer | ICMs | Cases | Top Features |
|----------|------|-------|-------------|
| Morgan Stanley | 12 | 8 | Purview Message Encryption, Sensitivity Labels |
| Huntington | 11 | 4 | Purview Message Encryption, Classification |
| MUFJ | 11 | 8 | Purview Message Encryption, Classification |
| Barclays Bank | 11 | 6 | Purview Message Encryption, Classification |
| Novartis | 8 | 4 | Purview Message Encryption, Sensitivity Labels |
| State of WA | 5 | 3 | Sensitivity Labels, Purview Message Encryption |
| AGL Energy | 4 | 3 | Purview Message Encryption |
| EY | 4 | 4 | Purview Message Encryption |
| NAB | 3 | 2 | Purview Message Encryption |
| Vodafone | 3 | 2 | Purview Message Encryption |

---

## 🎯 Recommendations

Based on real ICM data patterns:

### 1. 🔴 HIGH: Create ICM-Specific "By Design" Documentation

**Action:** For top 20 recurring ICMs, create dedicated KB articles
- Include ICM ID, customer names (if applicable), and clear "By Design" explanation
- Add to public docs with "Expected Behavior" tag
- **Priority ICMs to document first:** Top 5 from each feature area (see above)

### 2. 🔴 HIGH: Customer-Specific Playbooks

**Target customers:** Top 10 (see table above)
- Create custom runbook for each customer's specific ICM patterns
- Include PHE/CSA contact info
- Proactive communication strategy

### 3. 🟡 MEDIUM: ICM Pattern Analysis

**Action:** Deep dive into recurring ICM IDs
- Why do same ICMs appear across multiple customers?
- Are these genuine "By Design" or needing feature improvements?
- Prioritize by customer impact (IC vs MCS)

### 4. 🟢 LOW: Self-Service ICM Lookup

**Action:** Create internal tool
- Input ICM ID → Get "By Design" status + explanation
- Link to KB articles automatically
- Reduce support ticket volume

---

## Next Steps

1. **Week 1:** Review top 10 ICMs per feature for "By Design" status validation
2. **Week 2:** Create KB articles for confirmed "By Design" ICMs
3. **Week 3:** Share with PHEs for top 10 customers
4. **Ongoing:** Monitor new ICM patterns monthly

---

## Data Files

- **Excel**: `icm_by_design_analysis_with_customers.xlsx`
  - Full ICM-Customer mapping
  - Feature summaries
  - Customer breakdowns
  - Raw data for analysis

