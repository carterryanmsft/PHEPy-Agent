# Specific Documentation Gap Analysis
## Actionable Recommendations Based on Customer Confusion

**Generated:** 2026-02-11 10:11:57

**ICMs Analyzed:** 30

---

## 🎯 Executive Summary

This analysis identifies **specific** documentation gaps based on actual customer confusion and questions from ICMs marked as 'By Design' with prevention type 'Public Documentation'. Each gap includes:

- **Current State:** What's missing or unclear
- **Impact:** Real customer ICM demonstrating the gap
- **Needed:** Specific content to add

**Total Specific Gaps Identified:** 22

---

## 📋 Licensing & Feature Coverage

**Gaps Identified:** 2

### ⚠️ DLP for Teams licensing unclear - which license covers Teams chat vs files

**Impact:** 2 customer incident(s)

**Example ICM:** [716201243](https://portal.microsofticm.com/imp/v3/incidents/details/716201243)

**Issue Title:** [RFC] Team-4 |2511140030004237|CKP|DLP|RFC| The GDPR enhanced template DLP is not working for Teams 

#### 📊 Current State

No clear documentation on DLP coverage differences between E5 base and E5 Information Protection add-on for Teams chat messages

#### ✅ What's Needed

License comparison table showing Teams chat, Teams files, and channel message coverage by license type

#### 🎬 Recommended Actions

1. **Create License Comparison Matrix**
   - Side-by-side comparison of E3, E5, and add-on licenses
   - Indicate feature availability by workload (Exchange, SharePoint, Teams, etc.)
   - Clarify chat vs file coverage in Teams
   - Add to main DLP licensing page with prominent placement

2. **Update Product Page**
   - Add licensing section to each feature page
   - Link to license comparison from feature descriptions

3. **Create FAQ Section**
   - "Do I need E5 or the add-on for Teams DLP?"
   - "What's included in each license tier?"

#### 📎 Other ICMs with Same Gap

- [706301319](https://portal.microsofticm.com/imp/v3/incidents/details/706301319) - [Issue] Missing documentation on Licensing for Sensitivity labels for meeting invites

#### 📖 Affected Documentation Pages

- `/purview/dlp-licensing`
- `/purview/dlp-microsoft-teams` (add licensing section)
- `/purview/information-protection` (license comparison)

---

## 📋 Metrics & Portal Data

**Gaps Identified:** 2

### ⚠️ Auto-labeling portal metrics reliability not documented

**Impact:** 1 customer incident(s)

**Example ICM:** [711972349](https://portal.microsofticm.com/imp/v3/incidents/details/711972349)

**Issue Title:** [Issue] Auto labeling issue for SharePoint sites and OneDrive workload

#### 📊 Current State

No documentation on metric update frequency, accuracy, or known limitations

#### ✅ What's Needed

Clear documentation on: 1) How often metrics refresh 2) Why counts may show 0 temporarily 3) Difference between portal metrics vs Activity Explorer 4) Known delays/limitations

#### 🎬 Recommended Actions

1. **Create Portal Data Reference Page**
   - Document refresh intervals for each report/metric
   - Explain known limitations and edge cases
   - Clarify difference between portal metrics and Activity Explorer

2. **Add In-Portal Help Text**
   - Hover tooltips explaining what each metric shows
   - "Last updated" timestamp on metrics
   - Warning when data may be incomplete

3. **Troubleshooting Guide**
   - "Why do my metrics show 0?"
   - "How long until I see results?"
   - When to wait vs escalate

#### 📖 Affected Documentation Pages

- `/purview/apply-sensitivity-label-automatically`
- `/purview/auto-labeling-exchange`
- `/purview/auto-labeling-sharepoint-onedrive`

---

### ⚠️ Data refresh timing not documented

**Impact:** 1 customer incident(s)

**Example ICM:** [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540)

**Issue Title:** [Issue] Auto-labeling policy not applying to SPO location

#### 📊 Current State

No information on expected delays for portal data

#### ✅ What's Needed

Service-level timing documentation for each portal/report type

#### 🎬 Recommended Actions

1. **Review and Update Documentation**
   - Address specific gap identified
   - Add examples and explanations
   - Include common edge cases

2. **Consider UI Improvements**
   - Contextual help where users encounter confusion
   - Validation/warnings for common mistakes

3. **Update FAQ/Troubleshooting**
   - Add section based on customer questions
   - Link to from related pages

#### 📖 Affected Documentation Pages

- *(To be determined based on specific gap)*

---

## 📋 Policy Distribution & Status

**Gaps Identified:** 3

### ⚠️ Policy distribution "Pending" status meaning unclear

**Impact:** 3 customer incident(s)

**Example ICM:** [713662994](https://portal.microsofticm.com/imp/v3/incidents/details/713662994)

**Issue Title:** [RFC] policies still pending after waiting more than 30 days

#### 📊 Current State

No documentation explaining what "Pending" means, expected duration, or when to be concerned

#### ✅ What's Needed

Status definitions with: 1) Expected time in each status 2) What triggers status changes 3) When to escalate vs wait 4) Troubleshooting steps for stuck policies

#### 🎬 Recommended Actions

1. **Create Policy Status Reference**
   - Define each status (Pending, Distributing, Success, Error)
   - Expected duration in each status
   - What triggers status transitions

2. **Add Status Indicators**
   - Contextual help next to status in UI
   - Progress indicator when available
   - Action buttons ("Check status", "Refresh")

3. **Troubleshooting Flow**
   - Decision tree for stuck policies
   - PowerShell commands to check status
   - When 30+ days pending is OK vs concerning

#### 📎 Other ICMs with Same Gap

- [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540) - [Issue] Auto-labeling policy not applying to SPO location
- [723508987](https://portal.microsofticm.com/imp/v3/incidents/details/723508987) - [Issue] Label Policy stuck in pending distribution for over 48 hours

#### 📖 Affected Documentation Pages

- *(To be determined based on specific gap)*

---

## 📋 Size Limits & Performance

**Gaps Identified:** 1

### ⚠️ File size limits for DLP/classification not documented

**Impact:** 1 customer incident(s)

**Example ICM:** [691533110](https://portal.microsofticm.com/imp/v3/incidents/details/691533110)

**Issue Title:** [Issue] Personal information using regular expression (regex) patterns is not getting blocked by DLP

#### 📊 Current State

No clear documentation on file size limits that affect DLP detection or classification accuracy

#### ✅ What's Needed

Comprehensive limits documentation: 1) File size limits by workload 2) Record count limits for SITs 3) Performance degradation thresholds 4) Workarounds for large files

#### 🎬 Recommended Actions

1. **Create Limits and Boundaries Page**
   - File size limits by workload
   - Record/row count limits for SITs
   - Performance degradation thresholds
   - Impact on classification accuracy

2. **Update Troubleshooting Docs**
   - "Why isn't DLP detecting in large files?"
   - Workarounds for files exceeding limits
   - Best practices for large datasets

3. **Add Warning in UI**
   - Alert when policy may not work on large files
   - Suggest alternatives (EDM, fingerprinting)

#### 📖 Affected Documentation Pages

- *(To be determined based on specific gap)*

---

## 📋 Configuration Examples

**Gaps Identified:** 4

### ⚠️ Regex pattern examples insufficient

**Impact:** 1 customer incident(s)

**Example ICM:** [691533110](https://portal.microsofticm.com/imp/v3/incidents/details/691533110)

**Issue Title:** [Issue] Personal information using regular expression (regex) patterns is not getting blocked by DLP

#### 📊 Current State

Limited examples for complex regex patterns

#### ✅ What's Needed

More real-world regex examples with explanations and common pitfalls

#### 🎬 Recommended Actions

1. **Create Code Sample Repository**
   - Complete, working XML examples for each feature
   - Commented code explaining each section
   - Common variations (e.g., different checksum algorithms)

2. **Add to GitHub**
   - Create microsoft/compliance-samples repo
   - Include test data and validation scripts
   - Link from docs to repo

3. **Interactive Examples**
   - Consider XML builder tool
   - Validation sandbox for testing

#### 📖 Affected Documentation Pages

- *(To be determined based on specific gap)*

---

### ⚠️ Advanced checksum XML examples missing

**Impact:** 2 customer incident(s)

**Example ICM:** [729156307](https://portal.microsofticm.com/imp/v3/incidents/details/729156307)

**Issue Title:** [RFC] Assist to provide rule package xml example for given advanced checksum capabilities

#### 📊 Current State

Documentation explains concepts but lacks working XML examples

#### ✅ What's Needed

Complete working XML examples for: 1) Lead digit replacement 2) Two-digit number handling 3) Post-computation replacement 4) Common checksum algorithms

#### 🎬 Recommended Actions

1. **Create Code Sample Repository**
   - Complete, working XML examples for each feature
   - Commented code explaining each section
   - Common variations (e.g., different checksum algorithms)

2. **Add to GitHub**
   - Create microsoft/compliance-samples repo
   - Include test data and validation scripts
   - Link from docs to repo

3. **Interactive Examples**
   - Consider XML builder tool
   - Validation sandbox for testing

#### 📎 Other ICMs with Same Gap

- [724141777](https://portal.microsofticm.com/imp/v3/incidents/details/724141777) - [RFC] Assist to clarify and provide example for advance checksum parameter.

#### 📖 Affected Documentation Pages

- *(To be determined based on specific gap)*

---

### ⚠️ Site selection limits not documented

**Impact:** 1 customer incident(s)

**Example ICM:** [730194018](https://portal.microsofticm.com/imp/v3/incidents/details/730194018)

**Issue Title:** [RFC] Regarding the maximum number of SharePoint sites that can be configured in a DLP policy target

#### 📊 Current State

No documentation on maximum number of SharePoint sites for DLP policies

#### ✅ What's Needed

Limits documentation: 1) Max sites per policy 2) Max locations total 3) Performance implications 4) Alternatives for large-scale deployment

#### 🎬 Recommended Actions

1. **Create Limits and Boundaries Page**
   - File size limits by workload
   - Record/row count limits for SITs
   - Performance degradation thresholds
   - Impact on classification accuracy

2. **Update Troubleshooting Docs**
   - "Why isn't DLP detecting in large files?"
   - Workarounds for files exceeding limits
   - Best practices for large datasets

3. **Add Warning in UI**
   - Alert when policy may not work on large files
   - Suggest alternatives (EDM, fingerprinting)

#### 📖 Affected Documentation Pages

- *(To be determined based on specific gap)*

---

## 📋 URL & Pattern Matching

**Gaps Identified:** 3

### ⚠️ URL matching with query parameters not documented

**Impact:** 3 customer incident(s)

**Example ICM:** [709524522](https://portal.microsofticm.com/imp/v3/incidents/details/709524522)

**Issue Title:** [Issue] Endpoint DLP Whitelist Issue for Copilot Chat URL

#### 📊 Current State

No documentation on how DLP handles URLs with dynamic query parameters

#### ✅ What's Needed

Clear documentation on: 1) How URL matching works 2) Query parameter handling 3) Wildcard behaviors 4) Parent domain whitelisting implications 5) Best practices for dynamic URLs

#### 🎬 Recommended Actions

1. **Create URL Matching Reference**
   - Explain URL matching logic in detail
   - How query parameters are handled
   - Wildcard behavior and limitations

2. **Best Practices Guide**
   - When to whitelist parent domain vs specific URLs
   - Security implications of broad whitelisting
   - Handling dynamic URLs (like Copilot)

3. **Examples Library**
   - Common scenarios (Microsoft services, cloud apps)
   - Testing methodology

#### 📎 Other ICMs with Same Gap

- [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540) - [Issue] Auto-labeling policy not applying to SPO location
- [724698812](https://portal.microsofticm.com/imp/v3/incidents/details/724698812) - [RFC] Could you provide details on the newly added fields in the parameters returned by Get-DlpCompl

#### 📖 Affected Documentation Pages

- *(To be determined based on specific gap)*

---

## 📋 Feature Scope & Behavior

**Gaps Identified:** 6

### ⚠️ DLP conditions not fully explained

**Impact:** 1 customer incident(s)

**Example ICM:** [722954497](https://portal.microsofticm.com/imp/v3/incidents/details/722954497)

**Issue Title:** [DCR] Improve DLP's conditions documentation -TrackingID#2507091420001794

#### 📊 Current State

Conditions are listed but behavior/source of match not explained

#### ✅ What's Needed

Enhanced conditions documentation: 1) What each condition checks 2) Data source (file metadata vs content) 3) Matching logic 4) Examples for each condition 5) SharePoint/OneDrive-specific behavior

#### 🎬 Recommended Actions

1. **Enhance Conditions Documentation**
   - Add detailed explanation for each condition
   - Specify data source (metadata vs content)
   - Include behavior differences by workload

2. **Add Visual Examples**
   - Screenshots showing where data comes from
   - Flowcharts for condition evaluation

3. **Create Comparison Table**
   - Exchange vs SharePoint vs OneDrive condition behavior
   - Note any workload-specific limitations

#### 📖 Affected Documentation Pages

- `/purview/dlp-conditions-actions-reference`
- `/purview/dlp-exchange-conditions-actions`
- `/purview/dlp-sharepoint-onedrive-conditions`

---

### ⚠️ Auto-labeling scope (in-transit vs at-rest) not clear

**Impact:** 3 customer incident(s)

**Example ICM:** [700114735](https://portal.microsofticm.com/imp/v3/incidents/details/700114735)

**Issue Title:** [Issue] [Cit Alliance] Auto-labeling policies scoped to Exchange return no matches in simulation

#### 📊 Current State

Confusion about when auto-labeling applies to emails

#### ✅ What's Needed

Clear documentation: 1) Exchange auto-labeling applies only to in-transit messages 2) Does not apply to existing mailbox content 3) Simulation behavior differences 4) Timeline for label application

#### 🎬 Recommended Actions

1. **Clarify Scope Documentation**
   - Explicitly state in-transit vs at-rest behavior
   - Add prominent callouts on feature pages
   - Explain simulation behavior differences

2. **Update UI Text**
   - Add scope information during policy creation
   - Clarify timing in simulation results

3. **Create Scope Comparison Page**
   - What's covered by each policy type
   - When labels apply (creation, modification, etc.)

#### 📎 Other ICMs with Same Gap

- [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540) - [Issue] Auto-labeling policy not applying to SPO location
- [700569939](https://portal.microsofticm.com/imp/v3/incidents/details/700569939) - [Issue] [Citi Alliance] Auto-labelling policies set to enforce mode, but they are not being applied 

#### 📖 Affected Documentation Pages

- `/purview/apply-sensitivity-label-automatically`
- `/purview/auto-labeling-exchange`
- `/purview/auto-labeling-sharepoint-onedrive`

---

### ⚠️ Notification email behavior not documented

**Impact:** 2 customer incident(s)

**Example ICM:** [730972455](https://portal.microsofticm.com/imp/v3/incidents/details/730972455)

**Issue Title:** [Issue] Incorrect DLP Rule getting Triggered

#### 📊 Current State

Unclear when/why multiple notification emails are sent

#### ✅ What's Needed

Documentation on: 1) Notification triggers 2) Expected number of emails 3) Deduplication logic 4) How to configure notification frequency

#### 🎬 Recommended Actions

1. **Review and Update Documentation**
   - Address specific gap identified
   - Add examples and explanations
   - Include common edge cases

2. **Consider UI Improvements**
   - Contextual help where users encounter confusion
   - Validation/warnings for common mistakes

3. **Update FAQ/Troubleshooting**
   - Add section based on customer questions
   - Link to from related pages

#### 📎 Other ICMs with Same Gap

- [724468498](https://portal.microsofticm.com/imp/v3/incidents/details/724468498) - [Issue] Multiple notification emails are sent to the user when the rule is matched

#### 📖 Affected Documentation Pages

- *(To be determined based on specific gap)*

---

## 📋 UI/UX Clarity

**Gaps Identified:** 1

### ⚠️ Mutually exclusive label options not clear in UI

**Impact:** 1 customer incident(s)

**Example ICM:** [719718596](https://portal.microsofticm.com/imp/v3/incidents/details/719718596)

**Issue Title:** [DCR] [S500] DKE options in sensitivity label configuration

#### 📊 Current State

DKE encryption and user-defined permissions are mutually exclusive but UI allows both to be selected

#### ✅ What's Needed

1) UI should disable incompatible options 2) Tooltip/help text explaining why 3) Documentation of all mutually exclusive options

#### 🎬 Recommended Actions

1. **Review and Update Documentation**
   - Address specific gap identified
   - Add examples and explanations
   - Include common edge cases

2. **Consider UI Improvements**
   - Contextual help where users encounter confusion
   - Validation/warnings for common mistakes

3. **Update FAQ/Troubleshooting**
   - Add section based on customer questions
   - Link to from related pages

#### 📖 Affected Documentation Pages

- *(To be determined based on specific gap)*

---

## 🎯 Priority Matrix

| Priority | Gap | Impact | Effort | ICMs |
|----------|-----|--------|--------|------|
| 🔴 HIGH | Policy distribution "Pending" status meaning unclear | 3 customers | Low-Medium | [713662994](https://portal.microsofticm.com/imp/v3/incidents/details/713662994), [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540), [723508987](https://portal.microsofticm.com/imp/v3/incidents/details/723508987) |
| 🔴 HIGH | URL matching with query parameters not documented | 3 customers | Low-Medium | [709524522](https://portal.microsofticm.com/imp/v3/incidents/details/709524522), [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540), [724698812](https://portal.microsofticm.com/imp/v3/incidents/details/724698812) |
| 🔴 HIGH | Auto-labeling scope (in-transit vs at-rest) not clear | 3 customers | Low-Medium | [700114735](https://portal.microsofticm.com/imp/v3/incidents/details/700114735), [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540), [700569939](https://portal.microsofticm.com/imp/v3/incidents/details/700569939) |
| 🔴 HIGH | DLP for Teams licensing unclear - which license covers Teams... | 2 customers | Low-Medium | [716201243](https://portal.microsofticm.com/imp/v3/incidents/details/716201243), [706301319](https://portal.microsofticm.com/imp/v3/incidents/details/706301319) |
| 🔴 HIGH | Advanced checksum XML examples missing | 2 customers | Low-Medium | [729156307](https://portal.microsofticm.com/imp/v3/incidents/details/729156307), [724141777](https://portal.microsofticm.com/imp/v3/incidents/details/724141777) |
| 🟡 MEDIUM | Notification email behavior not documented | 2 customers | Medium | [730972455](https://portal.microsofticm.com/imp/v3/incidents/details/730972455), [724468498](https://portal.microsofticm.com/imp/v3/incidents/details/724468498) |
| 🟡 MEDIUM | Auto-labeling portal metrics reliability not documented | 1 customers | Medium | [711972349](https://portal.microsofticm.com/imp/v3/incidents/details/711972349) |
| 🟡 MEDIUM | Data refresh timing not documented | 1 customers | Medium | [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540) |
| 🟡 MEDIUM | File size limits for DLP/classification not documented | 1 customers | Medium | [691533110](https://portal.microsofticm.com/imp/v3/incidents/details/691533110) |
| 🟡 MEDIUM | Regex pattern examples insufficient | 1 customers | Medium | [691533110](https://portal.microsofticm.com/imp/v3/incidents/details/691533110) |
| 🟢 LOW | Site selection limits not documented | 1 customers | Medium | [730194018](https://portal.microsofticm.com/imp/v3/incidents/details/730194018) |
| 🟢 LOW | DLP conditions not fully explained | 1 customers | Medium | [722954497](https://portal.microsofticm.com/imp/v3/incidents/details/722954497) |
| 🟢 LOW | Mutually exclusive label options not clear in UI | 1 customers | Medium | [719718596](https://portal.microsofticm.com/imp/v3/incidents/details/719718596) |

---

## 🗺️ Suggested Implementation Roadmap

### Phase 1: Quick Wins (1-2 weeks)

Focus on high-impact, low-effort improvements:

- Add missing definitions and explanations to existing pages
- Create FAQ sections for common questions
- Add tooltips/help text in UI where confusion occurs

### Phase 2: Documentation Updates (2-4 weeks)

- Create new reference pages (limits, status definitions, etc.)
- Enhance existing pages with examples and clarifications
- Add troubleshooting guides

### Phase 3: Enhanced Content (1-2 months)

- Develop code sample repositories
- Create video walkthroughs for complex scenarios
- Build interactive tools where helpful

### Phase 4: Product Improvements (2-3 months)

- UI changes to prevent common errors
- In-product guidance and validation
- Enhanced portal information displays

---

*Generated from analysis of real customer incidents. Each recommendation is backed by actual customer confusion and questions.*
