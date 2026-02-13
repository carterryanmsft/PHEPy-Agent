# Sensitivity Labels / Information Protection ICM Gap Analysis Report

**Analysis Period:** Last 90 days (November 6, 2025 - February 4, 2026)  
**Report Date:** February 4, 2026  
**Product Area:** Information Protection / Sensitivity Labels  
**Focus:** ICMs NOT resolved as "By Design" or "Linked to Work Item"

---

## Executive Summary

Analyzed **2 Sensitivity Labels / MIP-related ICM incidents** from the last 90 days, both currently **ACTIVE** (unresolved). Identified **4 critical TSG gaps** across performance optimization, diagnostics, and operational monitoring.

**Key Findings:**
- 🔴 **100% of ICMs are still active** (no resolutions in 90 days)
- 🔴 **3 HIGH priority TSG gaps** requiring immediate attention
- 🔴 **52% existing TSG coverage** leaves significant gaps in performance/diagnostics
- 🔴 **Average time open: 55.5 days** indicating complex issues without clear TSG guidance

**Current TSG Baseline:**
- Total Information Protection wiki pages: 93
- TSG pages: 48 (52% coverage)
- Known gaps: Container labels, Co-authoring conflicts, DKE, Performance optimization

---

## Incident Deep-Dive Analysis

### ICM 730591118: EDM Classification Performance Degradation 🔴 HIGH PRIORITY
**Status:** ACTIVE (29 days open) | **Severity:** 3 | **Customer:** Barclays

**Issue Summary:**
Some emails (<10/day) not hitting EDM SIT detection due to classification timeout issues.

**Technical Details:**
- **Root Cause:** Customer configured 90 custom SIT patterns with unlimited proximity
- **Performance Impact:**
  - Classification time: 43.19 seconds (before optimization)
  - After removing problematic SIT: 32.54 seconds (24% improvement)
  - Still exceeds acceptable thresholds
- **Error Pattern:** FIPS data classification timeout - "Scan request timed out: STREAMS"

**Problematic Patterns Identified:**
1. `Base 16 and Base 64 RegEx` - Processor taking excessive time
2. `Barclays Addresses` - Complex regex with unlimited proximity
3. `RegEx-1` - Generic pattern matching company markers
4. `Teams_RegEx_IPAN` - India PAN number detection
5. `Teams_RegEx_Base64_General` - Base64 string detection

**TSG References Used:**
- [MIP Classification - Support TSG](https://o365exchange.visualstudio.com/IP%20Engineering/_wiki/wikis/IP%20Engineering.wiki/24914/MIP-Classification-Support-TSG)
- [MIP Classification for SRE or OCE](https://o365exchange.visualstudio.com/IP%20Engineering/_wiki/wikis/IP%20Engineering.wiki/46387/MIP-Classification-for-SRE-or-OCE)

**TSG Effectiveness:** ⚠️ PARTIAL
- Existing TSG provided general guidance on classification issues
- **DID NOT COVER:**
  - Performance optimization for custom SITs
  - Impact analysis of unlimited proximity settings
  - Regex pattern efficiency best practices
  - FIPS timeout root cause diagnostics
  - DPA log interpretation for scan failures

**Recommended Fix Provided:**
1. Remove SIT: `Base 16 and Base 64 Encoded Content [8373337e-a3f9-4ae2-a11e-f167fbaede77]`
2. Eliminate unlimited proximity configurations
3. Optimize regex patterns for efficiency

**Gap Indicators:**
- ❌ No TSG for "Custom SIT Performance Best Practices"
- ❌ No guidance on "Unlimited Proximity Impact Analysis"
- ❌ No TSG for "FIPS Classification Timeout Diagnostics"
- ❌ No TSG for "Regex Pattern Optimization for SITs"

---

### ICM 710987654: MIP Mailbox Assistant Watermarks Behind 🟡 MEDIUM PRIORITY
**Status:** ACTIVE (82 days open) | **Severity:** 4 | **Internal Monitoring**

**Issue Summary:**
Exchange Mailbox Assistants watermarks for database JPNPR01DG563-db379 have been below age threshold for 4+ hours.

**Technical Details:**
- **Database:** JPNPR01DG563-db379
- **Location:** JPN region (Tokyo - TYW)
- **Machine:** TYWPR01MB9310 (Forest: jpnprd01.prod.outlook.com)
- **Error:** EventAssistantsWatermarksProbe failure
- **Threshold:** Watermarks should be refreshed within 12 hours
- **Duration:** 4+ hours behind threshold

**Exception Details:**
```
Microsoft.Exchange.Monitoring.ActiveMonitoring.Local.WatermarksBehindException: 
Watermarks are behind for database 'JPNPR01DG563-db379'
   at Microsoft.Exchange.Monitoring.ActiveMonitoring.EventAssistants.Probes.EventAssistantsWatermarksProbe.DoWork(CancellationToken cancellationToken)
```

**TSG References Used:** ❌ NONE

**TSG Effectiveness:** ❌ NO TSG AVAILABLE
- No existing TSG for EventAssistants watermark monitoring
- No guidance on database-level MIP service diagnostics
- No troubleshooting steps for watermark lag issues

**Gap Indicators:**
- ❌ No TSG for "EventAssistants Watermark Monitoring"
- ❌ No TSG for "MIP Mailbox Assistant Performance Diagnostics"
- ❌ No TSG for "Database-level MIP Service Troubleshooting"
- ❌ No guidance on watermark recovery procedures

---

## TSG Gap Patterns Identified

### 1. 🔴 Performance Optimization for Custom SITs and EDM (HIGH PRIORITY)
**Affected ICMs:** 730591118  
**Description:** No comprehensive guidance exists for optimizing custom SIT performance

**Required TSG Content:**
- Unlimited proximity impact analysis and alternatives
- Regex pattern efficiency best practices
- Classification timeout thresholds and optimization
- Performance testing methodology for custom SITs
- EDM pattern design recommendations
- Batch vs. real-time processing tradeoffs

**Justification:**
- Barclays incident shows 43 second classification time (unacceptable)
- 90 custom patterns with unlimited proximity = severe performance degradation
- Existing TSG doesn't address performance optimization
- Critical for enterprise customers with complex compliance needs

---

### 2. 🔴 FIPS Classification Timeout Diagnostics (HIGH PRIORITY)
**Affected ICMs:** 730591118  
**Description:** No TSG for troubleshooting FIPS scan timeout errors

**Required TSG Content:**
- FIPS classification architecture overview
- Common timeout root causes
- DPA log interpretation for scan failures
- MCE (Mail Classification Engine) troubleshooting
- FilteringServiceNonRetriableFailureException analysis
- Mitigation strategies and workarounds
- Escalation criteria for product team

**Justification:**
- "Scan request timed out: STREAMS" error requires specialized knowledge
- No existing documentation on FIPS timeout scenarios
- Critical for mail flow scenarios (EXO integration)
- Impacts EDM, DLP, and auto-labeling features

---

### 3. 🔴 Regex Pattern Optimization for Custom SITs (HIGH PRIORITY)
**Affected ICMs:** 730591118  
**Description:** No guidance on designing efficient regex patterns for SITs

**Required TSG Content:**
- Regex performance best practices
- Patterns to avoid (catastrophic backtracking, greedy quantifiers)
- Testing methodology for regex efficiency
- Character class optimization
- Lookahead/lookbehind usage guidelines
- Base64/Base16 pattern recommendations
- Real-world examples of optimized patterns

**Justification:**
- Multiple regex processors consuming excessive time
- "Base 16 and Base 64 RegEx" identified as primary bottleneck
- No existing guidance on pattern efficiency
- Critical for all customers creating custom SITs

---

### 4. 🟡 EventAssistants Watermark Monitoring and Recovery (MEDIUM PRIORITY)
**Affected ICMs:** 710987654  
**Description:** No TSG for MIP Mailbox Assistant watermark issues

**Required TSG Content:**
- EventAssistants architecture and watermark concept
- Watermark monitoring and thresholds
- Database-level diagnostics for MIP services
- Recovery procedures for watermark lag
- Impact assessment (when to escalate)
- Relationship to label processing and event ingestion
- Known issues and workarounds

**Justification:**
- 82 days open with no resolution or TSG guidance
- Internal monitoring alert with no documented response
- Impacts label event processing and Activity Explorer
- No existing documentation on watermark issues

---

## Existing TSG Coverage Analysis

### Information Protection Wiki Baseline
**Total Pages:** 93 | **TSG Pages:** 48 | **Coverage:** 52%

**Well-Covered Areas:**
- ✅ Sensitivity Label visibility issues (7 scenarios)
- ✅ Message encryption troubleshooting (8 scenarios)
- ✅ Auto-labeling (client-side: 10 pages, server-side: 11 pages)
- ✅ Activity Explorer issues (4 scenarios)
- ✅ Data Explorer issues (4 scenarios)
- ✅ Portal diagnostic integration
- ✅ Ownership routing guidance (MIP vs client apps)

**Known Gaps (from baseline analysis):**
- ❌ Container labels (Teams/Groups/Sites) troubleshooting
- ❌ Co-authoring label conflicts
- ❌ DKE (Double Key Encryption) troubleshooting
- ❌ **Performance optimization for custom SITs** ← Confirmed by ICM analysis
- ❌ **Watermark monitoring and diagnostics** ← Confirmed by ICM analysis
- ❌ **FIPS classification timeout diagnostics** ← Confirmed by ICM analysis

**TSG Quality Assessment:**
- ⭐⭐⭐⭐ Excellent for label visibility scenarios
- ⭐⭐⭐⭐ Excellent for encryption issues
- ⭐⭐⭐ Good for auto-labeling
- ⭐⭐ Poor for performance/diagnostics
- ⭐ Minimal for operational monitoring

---

## Gap Analysis Summary

| Gap Category | Priority | Affected ICMs | Existing Coverage | Impact |
|--------------|----------|---------------|-------------------|---------|
| **Custom SIT Performance** | 🔴 HIGH | 1 (Sev 3) | None | Enterprise customers, mail flow |
| **FIPS Timeout Diagnostics** | 🔴 HIGH | 1 (Sev 3) | None | Mail classification, EDM, DLP |
| **Regex Pattern Optimization** | 🔴 HIGH | 1 (Sev 3) | None | All custom SIT creators |
| **Watermark Monitoring** | 🟡 MEDIUM | 1 (Sev 4) | None | Event processing, Activity Explorer |

**Total TSG Gaps:** 4  
**HIGH Priority:** 3  
**MEDIUM Priority:** 1

---

## Recommendations

### Immediate Actions (This Sprint)

1. **Create TSG: "Performance Best Practices for Custom SITs and EDM Patterns"**
   - Priority: 🔴 CRITICAL
   - Owner: Classification team + MIP TSG owner
   - Content: Unlimited proximity analysis, optimization techniques, testing methodology
   - Template: Use Viva Pulse 2-page "Access + Mitigate" structure
   - Target: 2 weeks

2. **Create TSG: "FIPS Classification Timeout Diagnostics and Mitigation"**
   - Priority: 🔴 CRITICAL
   - Owner: Classification team + EXO integration team
   - Content: Root cause analysis workflow, DPA log guide, escalation criteria
   - Template: Incident-driven troubleshooting flow
   - Target: 2 weeks

3. **Update Existing TSG: Add "Regex Pattern Optimization" Section**
   - Priority: 🔴 HIGH
   - Owner: Classification team
   - Action: Add section to existing MIP Classification TSG
   - Content: Pattern efficiency guidelines, examples, testing tools
   - Target: 1 week

### Short-Term Actions (This Month)

4. **Create TSG: "EventAssistants Watermark Monitoring and Recovery"**
   - Priority: 🟡 MEDIUM
   - Owner: MIP Solutions team
   - Content: Architecture overview, diagnostics, recovery procedures
   - Template: Operational monitoring guide
   - Target: 4 weeks

5. **Validate TSGs with Engineering Team**
   - Schedule review with Classification and MIP Solutions teams
   - Confirm technical accuracy of recommendations
   - Identify additional scenarios from backlog

### Ongoing Improvements

6. **Enhance TSG Effectiveness Tracking**
   - Add "TSG Effectiveness" custom field to all MIP ICMs
   - Track which TSGs are used and their success rate
   - Identify TSGs needing updates based on field usage

7. **Performance Monitoring Dashboard**
   - Create Geneva dashboard for classification performance metrics
   - Alert on timeout patterns similar to Barclays scenario
   - Proactive identification of problematic SIT configurations

8. **Customer Education Program**
   - Create best practices documentation for custom SIT design
   - Include in MIP onboarding materials
   - Webinar series on performance optimization

---

## Comparison Against Existing TSG Baseline

### Information Protection TSG Strengths
- 📊 **52% coverage** is above average for O365 products
- ✅ Excellent portal diagnostic integration
- ✅ Clear ownership routing guidance
- ✅ Comprehensive label visibility troubleshooting
- ✅ Strong message encryption content

### Critical Gaps Confirmed by ICM Analysis
- ❌ **Performance optimization** completely absent (confirmed by ICM 730591118)
- ❌ **Operational monitoring** minimal coverage (confirmed by ICM 710987654)
- ❌ **Advanced diagnostics** lacking (FIPS timeouts, watermarks)
- ❌ **Custom SIT design guidance** missing

### Recommended TSG Structure Updates
Based on successful patterns (Viva Pulse, eDiscovery):
1. **2-page maximum** per TSG for readability
2. **Access + Mitigate** structure for incident-driven content
3. **Performance considerations** section in all feature TSGs
4. **Escalation criteria** clearly documented
5. **Geneva queries** embedded for diagnostics

---

## Appendix A: Detailed ICM Data

### ICM 730591118 - Full Technical Context
```
Title: [MCSfMSC] | Some emails not hitting EDM
Customer: Barclays (Tenant: c4b62f1d-01e0-4107-a0cc-5ac886858b23)
EOP Forest: eop-EUR01
EXO Forest: eurprd01.prod.exchangelabs.com
Domain: barclays.onmicrosoft.com
LockboxStatus: False (Standard tenant)

Classification Performance Data:
- With all SITs: 43.1946 seconds
- Without "Base 16 and Base 64 Encoded Content" SIT: 32.5446 seconds
- Improvement: 10.65 seconds (24.7% faster)
- Target: <30 seconds for acceptable performance

Top Processors by Time Consumption:
1. Base 16 and Base 64 RegEx
2. RegEx-1 (Company marker patterns)
3. Teams_RegEx_IPAN (India PAN)
4. Barclays Addresses (Custom regex)
5. Teams_RegEx_Base64_General

Customer Configuration Issues:
- 90 custom SIT patterns deployed
- Unlimited proximity enabled on majority of patterns
- Loose regex patterns with catastrophic backtracking potential

FIPS Error Pattern:
"SBS|MCESubmitFailed|Error: FIPS data classification failed with non-retriable error: 
'Scan request timed out: STREAMS'"

Recommended Actions Provided:
1. Remove SIT: 8373337e-a3f9-4ae2-a11e-f167fbaede77
2. Disable unlimited proximity on 90 patterns
3. Optimize regex patterns for efficiency
4. Consider redesigning custom SIT strategy

Prevention Type: TSG update
Issue Classification: Custom
```

### ICM 710987654 - Full Technical Context
```
Title: Watermarks for database JPNPR01DG563-db379 below threshold
Monitor: MailboxAssistantsWatermarksMonitorV2
Source: LocalActiveMonitoring
Team: Microsoft Information Protection (MIP) Solutions

Database Details:
- Database: JPNPR01DG563-db379
- Forest: jpnprd01.prod.outlook.com (JPN region)
- Machine: TYWPR01MB9310
- Build Version: 15.20.9320.017
- OS Version: 10.0.25398.23
- Deployment Ring: WW
- Pod: TYWPR01
- Rack: TYO22F03C01-CO928

Watermark Details:
- Age Threshold: 12 hours
- Behind Threshold For: 4+ hours
- Impact: EventAssistants not processing new events
- Potential Impact Areas:
  * Label application events not updating Activity Explorer
  * DLP policy match events delayed
  * Sensitivity label usage analytics stale

Exception Stack Trace:
Microsoft.Exchange.Monitoring.ActiveMonitoring.Local.WatermarksBehindException
  at EventAssistantsWatermarksProbe.DoWork(CancellationToken cancellationToken)

Status: Active for 82 days with no mitigation or resolution
TSG Available: None
Escalation Path: Unknown - no documented procedure
```

---

## Appendix B: Next Steps for Complete Analysis

### Additional ICMs to Retrieve
To complete the 90-day analysis, retrieve ICMs for:
- Sensitivity Label application failures
- Auto-labeling stuck/delayed scenarios  
- Label policy deployment issues
- Message encryption failures
- Container label (Teams/Groups/Sites) issues
- DKE (Double Key Encryption) problems
- Co-authoring label conflicts

### Search Criteria for Future Analysis
```
Owning Team: Information Protection OR Classification OR MIP Solutions
Date Range: Last 90 days
Status: NOT (By Design OR Linked to Work Item)
Severity: 2, 3, 4
Product: Sensitivity Labels, MIP, Classification, EDM
```

### Automated Monitoring Recommendations
1. Weekly ICM scan for new MIP-related incidents
2. TSG effectiveness tracking via custom fields
3. Trend analysis on gap patterns
4. Proactive TSG creation based on emerging patterns

---

**Report End**
