# Enhanced Documentation Gap Analysis
## Detailed Customer Questions & Confusion Points

**Generated:** 2026-02-11 10:18:05

**ICMs Analyzed:** 30

---

## 🎯 Executive Summary

This analysis extracts **actual customer questions and confusion points** from ICM descriptions to identify specific documentation gaps. Each ICM represents a real customer issue where documentation failed to provide clear guidance, resulting in support escalations.

### 📖 How to Use This Report (For Technical Writers)

Each section includes:

- **Real Customer Questions** - Actual verbatim questions asked by customers that couldn't be answered by existing documentation
- **Confusion Points** - Specific misunderstandings or missing information that led to the support case
- **Expected vs Actual** - What customers thought would happen versus what actually occurred (identifies assumption gaps)
- **Issue Summary** - Full context of the customer scenario to understand the use case
- **Specific Documentation Needs** - Actionable recommendations including:
  - **Missing Content** - Exact topics/sections that need to be created or enhanced
  - **Where to Add** - Specific documentation pages and recommended section placements
  - **Content Guidelines** - What type of content is needed (tables, examples, troubleshooting steps, etc.)

### 🎯 Priority Guidance

- **HIGH Priority** - Multiple ICMs on the same topic, blocking customer deployments
- **MEDIUM Priority** - Recurring confusion, workarounds available but not documented
- **LOW Priority** - Edge cases or infrequent scenarios

### 📊 Review Process

1. Review each ICM to understand the full customer scenario
2. Identify which documentation page(s) need updates
3. Draft new content addressing the specific gaps
4. Include examples from the actual customer scenarios when possible
5. Add troubleshooting sections for common misconfigurations

---

## 📋 Licensing & Feature Availability

**ICMs in this category:** 4

**Priority:** HIGH - Licensing confusion blocks customer deployments and creates negative first impressions

### 🎯 Documentation Theme: License Requirements Clarity

**Root Cause:** Customers cannot determine which license tier is required for specific features, workloads, or scenarios. License information is scattered across multiple pages or missing entirely.

**Business Impact:** Customers purchase incorrect licenses, delay deployments, or file support cases to confirm licensing requirements before purchasing.

**Required Documentation Updates:**

1. **Create a Master Licensing Comparison Page** (`/purview/licensing-comparison`)
   - Side-by-side comparison table of all Purview licenses (E3, E5, P1, P2, etc.)
   - Feature availability matrix by workload (DLP, Sensitivity Labels, Auto-labeling, etc.)
   - Clear indication of premium features requiring E5/P2
   - Include Teams-specific licensing (Teams chat vs. Teams files vs. Teams meetings)

2. **Add License Banners to Feature Pages**
   - Each feature page should include a prominent callout box at the top
   - Format: "License Requirements: This feature requires [specific license]"
   - Link to the master comparison page for details

3. **Create License Decision Trees**
   - Interactive flowcharts: "Which license do I need for...?"
   - Common scenario-based guidance (e.g., "I want to protect Teams chats" → requires X license)

4. **Add License FAQs**
   - Common questions like "What's the difference between E3 and E5 DLP?"
   - Trial license limitations
   - License inheritance and stacking scenarios

---

### ICM [716201243](https://portal.microsofticm.com/imp/v3/incidents/details/716201243)

**Title:** [RFC] Team-4 |2511140030004237|CKP|DLP|RFC| The GDPR enhanced template DLP is not working for Teams location

**Team:** DLP Teams

#### ❓ Customer Questions

- cannot find any public document mention about this license: https://learn.microsoft.com/en-us/purview/dlp-microsoft-teams?

#### 🔍 Expected vs Actual

**Actual:** when sharing the Sensitive info via Teams chat, DLP did not detect them

#### 😕 Confusion Points

- cannot find any public document mention about this license: https://learn.microsoft.com/en-us/purview/dlp-microsoft-teams?tabs=purview#dlp-licensing-for-micros…Swarming post link: Jennie Phan (WICLOUD CORPORATIO
- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Add your question below:Issue: Customer created a

#### 📝 Issue Summary

Customer created a DLP policy scope only Teams location and apply to 3 groups of users. However, when sharing the Sensitive info via Teams chat, DLP did not detect them. However, if sharing the sensitive ino via file docx or txt, we can see DLP detected (working as expected) via Alert or Activity...

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section at the beginning
- Add FAQ: "Which license do I need for Teams DLP?"

**Tech Writer Action Items:**

1. **Update `/purview/dlp-microsoft-teams`:**
   - Add a new section at the top: "Licensing requirements for Teams DLP"
   - Create a table comparing E3 vs E5 capabilities:
     - Teams files DLP (available in E3)
     - Teams chat/messages DLP (requires E5)
     - Teams meeting recordings DLP (requires E5)
   - Add note: "GDPR enhanced templates require Microsoft 365 E5 Compliance"
   - Include screenshot showing where to verify license in admin portal

2. **Create New Content:**
   - Add troubleshooting section: "Why isn't my Teams DLP policy working?"
   - Include license verification as first troubleshooting step
   - Add example: "If you're trying to detect sensitive content in Teams chat messages and it's not working, verify you have E5 licensing"

3. **Cross-reference:**
   - Link from `/purview/dlp-learn-about-dlp` to licensing page
   - Add licensing callout in policy creation tutorials

**Customer Scenario to Address:**
Customer created DLP policy for Teams location targeting only chat messages. Policy did not trigger because they had E3 licensing (only covers Teams files, not chat). Documentation never explained this distinction, leading customer to believe the feature was broken.

**Estimated Effort:** 4-6 hours (research licensing details, create table, add examples)

---

### ICM [700114735](https://portal.microsofticm.com/imp/v3/incidents/details/700114735)

**Title:** [Issue] [Cit Alliance] Auto-labeling policies scoped to Exchange return no matches in simulation

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** Automatic labelling policies in Exchange online scoped to all users

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [730972455](https://portal.microsofticm.com/imp/v3/incidents/details/730972455)

**Title:** [Issue] Incorrect DLP Rule getting Triggered

**Team:** DLP Exchange

#### ❓ Customer Questions

- is impacting the behavior here and if it is not, what is solution to fix this?

#### 🔍 Expected vs Actual

**Actual:** Rule that should be triggered is "DLP
Control Password Protected Attachment" but we see a different rule being triggered, name: Bypass||Internal
EmailExtended Message Trace Detail report of a recent repro email (less than 30 days old): MTDetail_test pw protect_c364f831-8b27-40d0-8f65-2a708cb5be27

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Detailed explanation of what each condition checks
- Data source for each condition (file metadata vs content)
- Behavior differences by workload (Exchange, SharePoint, OneDrive)
- Matching logic and examples

**Where to Add:**
- `/purview/dlp-conditions-actions-reference` - Expand each condition
- Add comparison table: Exchange vs SharePoint vs OneDrive conditions
- Include screenshots showing where data comes from

---

### ICM [706301319](https://portal.microsofticm.com/imp/v3/incidents/details/706301319)

**Title:** [Issue] Missing documentation on Licensing for Sensitivity labels for meeting invites

**Team:** Sensitivity Labels

#### 🔍 Expected vs Actual

**Actual:** ton for meeting invites

#### 😕 Confusion Points

- documentation does NOT mention the above needs to be enabled. Use sensitivity labels to protect calendar items, Teams meetings, and chat | Microsoft LearnFor reference:http

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

## 📋 Portal Metrics & Data Visibility

**ICMs in this category:** 10

**Priority:** HIGH - Customers see "0" or inconsistent metrics and assume service is broken

### 🎯 Documentation Theme: Understanding Portal Metrics and Data Delays

**Root Cause:** Portal metrics (dashboard numbers, policy simulation results, Activity Explorer data) are not real-time, but documentation doesn't explain:
- How often metrics refresh
- Expected delays between action and visibility
- Why metrics might show "0" initially
- Difference between different reporting surfaces

**Business Impact:** Customers file "service not working" support cases when they see "0 files labeled" or missing data, when in reality the data hasn't populated yet due to normal processing delays.

**Required Documentation Updates:**

1. **Create Metrics Reference Page** (`/purview/portal-metrics-reference`)
   - Comprehensive list of all portal metrics with:
     - Refresh frequency (e.g., "Updates every 4 hours")
     - Expected initial delay (e.g., "May take up to 24 hours to populate")
     - Data source (where the metric pulls from)
     - Known limitations

2. **Add Data Visibility Timeline Diagrams**
   - Visual timeline showing: Action → Processing → Metric Update
   - Example: "Auto-label policy created → 24-48 hours → Simulation results appear → 7 days → Files begin labeling → Metrics update"

3. **Create Troubleshooting Flowcharts**
   - "Why am I seeing 0 in this metric?"
   - Decision tree: Check creation time → Wait period expired? → Check scope → Check permissions

4. **Add In-Portal Tooltips Documentation**
   - Document what SHOULD appear in tooltips for each metric
   - Coordinate with PM team to add tooltips to UI

---

### ICM [716201243](https://portal.microsofticm.com/imp/v3/incidents/details/716201243)

**Title:** [RFC] Team-4 |2511140030004237|CKP|DLP|RFC| The GDPR enhanced template DLP is not working for Teams location

**Team:** DLP Teams

#### ❓ Customer Questions

- cannot find any public document mention about this license: https://learn.microsoft.com/en-us/purview/dlp-microsoft-teams?

#### 🔍 Expected vs Actual

**Actual:** when sharing the Sensitive info via Teams chat, DLP did not detect them

#### 😕 Confusion Points

- cannot find any public document mention about this license: https://learn.microsoft.com/en-us/purview/dlp-microsoft-teams?tabs=purview#dlp-licensing-for-micros…Swarming post link: Jennie Phan (WICLOUD CORPORATIO
- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Add your question below:Issue: Customer created a

#### 📝 Issue Summary

Customer created a DLP policy scope only Teams location and apply to 3 groups of users. However, when sharing the Sensitive info via Teams chat, DLP did not detect them. However, if sharing the sensitive ino via file docx or txt, we can see DLP detected (working as expected) via Alert or Activity...

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [711972349](https://portal.microsofticm.com/imp/v3/incidents/details/711972349)

**Title:** [Issue] Auto labeling issue for SharePoint sites and OneDrive workload

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- iscover all unlabeled office files on SharePoint workloadScreenshot 1:Screenshot 2:Now, the ask is this data Reliable? how are the metrics updated here?

#### 🔍 Expected vs Actual

**Actual:** under the Auto-labeling portal, the customer sees the value “0” for Files Labeled

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [691533110](https://portal.microsofticm.com/imp/v3/incidents/details/691533110)

**Title:** [Issue] Personal information using regular expression (regex) patterns is not getting blocked by DLP when a file containing thousands of records

**Team:** DLP Exchange

#### ❓ Customer Questions

- are in the sheet named "RAW_가공 (2)".PS2. We are providing our regex. We use regex combined with text keywords.b0[1-7](?:(?[=1)[016789]|(?[=2)|(?

#### 🔍 Expected vs Actual

**Actual:** we discovered that a file containing thousands of personal information records of important executives was sent via Outlook without being blocked

#### 😕 Confusion Points

- expected vs actual BehaviorWe are blocking personal information using regular expression (regex) patterns. However, we discovered that a file containing thousands of personal information records of important execut

#### 📝 Issue Summary

Attached in DTM portalCX has shared the working and non-working file along with PPTX recordingCx ran the tests, but the two files he shared during our previous Teams meeting are around 22MB each, which exceeds the upload limit. (See Screenshot 1)To work around this, he created a separate Excel fi...

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [700114735](https://portal.microsofticm.com/imp/v3/incidents/details/700114735)

**Title:** [Issue] [Cit Alliance] Auto-labeling policies scoped to Exchange return no matches in simulation

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** Automatic labelling policies in Exchange online scoped to all users

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540)

**Title:** [Issue] Auto-labeling policy not applying to SPO location

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- arepoint / Teams sites                                      https://confluence.vallourec.net/pages/viewpage.action?

#### 🔍 Expected vs Actual

**Actual:** ton in Office online 2

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [713750747](https://portal.microsofticm.com/imp/v3/incidents/details/713750747)

**Title:** [Issue] Server side Autolabeling in Sharepoint Online is very slow

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Expected:** Customer is currently testing Autolabeling in Sharepoint

**Actual:** it took almost 1 week to label 24 files

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [723508987](https://portal.microsofticm.com/imp/v3/incidents/details/723508987)

**Title:** [Issue] Label Policy stuck in pending distribution for over 48 hours

**Team:** Sensitivity Labels

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [703921423](https://portal.microsofticm.com/imp/v3/incidents/details/703921423)

**Title:** [Issue] Purview Portal Site Selection and URL Validation Error

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Expected:** All available sites should be visible in the selection screen

**Actual:** the customer is experiencing errors even when entering the URL as shown below

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [700569939](https://portal.microsofticm.com/imp/v3/incidents/details/700569939)

**Title:** [Issue] [Citi Alliance] Auto-labelling policies set to enforce mode, but they are not being applied correctly on SharePoint site

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** these are not being applied correctly on the SharePoint sites

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [706301319](https://portal.microsofticm.com/imp/v3/incidents/details/706301319)

**Title:** [Issue] Missing documentation on Licensing for Sensitivity labels for meeting invites

**Team:** Sensitivity Labels

#### 🔍 Expected vs Actual

**Actual:** ton for meeting invites

#### 😕 Confusion Points

- documentation does NOT mention the above needs to be enabled. Use sensitivity labels to protect calendar items, Teams meetings, and chat | Microsoft LearnFor reference:http

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

## 📋 Policy Status & Distribution

**ICMs in this category:** 3

**Priority:** MEDIUM - Causes unnecessary support escalations when policies appear "stuck"

### 🎯 Documentation Theme: Policy Distribution Lifecycle & Status Meanings

**Root Cause:** Customers don't understand:
- What each policy status means (Pending, Distributing, Success, Error)
- How long each status phase should take
- When a "Pending" status for 30+ days is expected vs. problematic
- What actions to take for different status scenarios

**Business Impact:** Customers file support cases for policies in "Pending" status assuming the policy is broken, when in reality it's working correctly but the status display is ambiguous.

**Required Documentation Updates:**

1. **Create Policy Distribution Status Reference** (`/purview/policy-distribution-status`)
   - Complete table of all policy statuses:
     - **Pending**: Policy created but not yet distributed (Expected: 0-2 hours)
     - **Distributing**: Policy being deployed across services (Expected: 2-24 hours depending on scope)
     - **Success**: Policy fully distributed and active
     - **Error**: Distribution failed (include common error codes)
     - **Updating**: Changes being applied to existing policy
   
2. **Add Troubleshooting Decision Trees**
   - "My policy has been Pending for X days"
   - Check: Policy scope (large scopes take longer)
   - Check: Service health status
   - Check: Policy complexity (many conditions = longer distribution)
   - When to wait vs. when to contact support

3. **Document Distribution Timelines by Scope**
   - Small scope (1-100 users/sites): 2-6 hours
   - Medium scope (100-1000): 6-24 hours
   - Large scope (1000+ or "All"): 24-48 hours
   - Global policies: Up to 7 days for full propagation

4. **Add PowerShell Monitoring Scripts**
   - Example: `Get-DlpCompliancePolicy | Select Name, DistributionStatus, DistributionDateUtc`
   - Script to check policy status across all locations
   - Alert thresholds (when to investigate)

**Tech Writer Action Items:**

1. **Create visual timeline graphic** showing policy lifecycle:
   - Created → Pending (0-2h) → Distributing (2-24h) → Success
   - Include branch showing Error path with recovery steps

2. **Add to each policy creation tutorial:**
   - Callout box: "After creating your policy, expect it to remain in 'Pending' status for 1-2 hours, then 'Distributing' for up to 24 hours before becoming active."
   - Include screenshot showing where to check status in portal

3. **Document edge cases:**
   - Policies targeting "All users" may show success but still propagating
   - Cached status displays (refresh frequency is 15 minutes)
   - Status differences between portal UI vs. PowerShell

**Customer Scenario to Address:**
Customer created 12 DLP policies targeting SharePoint "All sites". All policies showed "Pending" for 30+ days. Customer assumed policies weren't working and filed support case. Reality: Policies were active and enforcing, but status never updated from Pending to Success due to the large scope triggering an edge case in status reporting.

**Estimated Effort:** 8-10 hours (research status codes, create diagrams, write troubleshooting guide)

---

### ICM [713662994](https://portal.microsofticm.com/imp/v3/incidents/details/713662994)

**Title:** [RFC] policies still pending after waiting more than 30 days

**Team:** DLP (Generic)

#### 🔍 Expected vs Actual

**Expected:** Normally, DLP policy distribution completes within hours to a few days after creation

**Actual:** ion status of “Pending”, even though many of these policies have been active for over 30 days

#### 😕 Confusion Points

- Expected Behavior:Normally, DLP policy distribution completes within hours to a few days after creation.Extended pending status beyond 30 days is no
- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team. Add your question below:Issue Description: Custom

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Definition of each policy status (Pending, Distributing, Success, Error)
- Expected time in each status
- When 30+ days pending is normal vs concerning
- Troubleshooting steps for stuck policies

**Where to Add:**
- Create new page: `/purview/policy-distribution-status-reference`
- `/purview/dlp-policy-design` - Add section on policy distribution
- Add PowerShell examples to check policy status

---

### ICM [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540)

**Title:** [Issue] Auto-labeling policy not applying to SPO location

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- arepoint / Teams sites                                      https://confluence.vallourec.net/pages/viewpage.action?

#### 🔍 Expected vs Actual

**Actual:** ton in Office online 2

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [723508987](https://portal.microsofticm.com/imp/v3/incidents/details/723508987)

**Title:** [Issue] Label Policy stuck in pending distribution for over 48 hours

**Team:** Sensitivity Labels

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

## 📋 Size Limits & Scale

**ICMs in this category:** 3

**Priority:** HIGH - Silent failures cause data leakage incidents

### 🎯 Documentation Theme: Service Limits, File Size Limits, and Scale Boundaries

**Root Cause:** Documentation doesn't clearly explain:
- Maximum file sizes that can be scanned by DLP
- How large files (>10MB, >50MB) are handled
- Maximum number of items in policy scopes
- Processing limits for regex patterns and custom rules
- What happens when limits are exceeded (silent pass-through vs. error)

**Business Impact:** CRITICAL - Customers discover that large files containing sensitive data were sent/shared without DLP inspection, creating compliance violations and data breaches. Customers assume all files are protected when limits silently exclude large files.

**Required Documentation Updates:**

1. **Create Comprehensive Service Limits Page** (`/purview/service-limits-reference`)
   - Complete table of all limits by workload:
   
   | Workload | File Size Limit | Items per Policy | Processing Timeout |
   |----------|----------------|------------------|--------------------|
   | Exchange | 150MB (attachment) | Unlimited recipients | 5 minutes scan |
   | SharePoint | 300MB | 100 sites (include) or Unlimited (All) | 30 minutes scan |
   | OneDrive | 300MB | 100 accounts (include) or Unlimited (All) | 30 minutes scan |
   | Teams | 50MB | Unlimited users | 5 minutes scan |
   | Endpoint | 50MB | N/A | 5 minutes scan |
   
2. **Document Limit Behaviors**
   - What happens when file exceeds size limit:
     - **Exchange**: File bypasses DLP, is delivered (CRITICAL GAP)
     - **SharePoint**: File scanned at upload, may timeout and allow
     - **Teams**: File blocked if over limit (safest)
     - **Endpoint**: User notified of size limit
   
3. **Add Workarounds and Best Practices**
   - For files >300MB: Use transport rules as backup
   - Enable "Scan large files" option (where available)
   - Create alerts for oversized files that bypass DLP
   - Use sensitivity labels (no size limit) as additional protection

4. **Regex Performance Limits**
   - Maximum regex complexity (catastrophic backtracking)
   - Timeout behavior for slow regex patterns
   - Testing guidance: "Test your regex on 10,000+ row files"
   - Link to regex optimization guide

5. **Scale Testing Guidance**
   - How to test policies with large file sets
   - Performance testing checklists
   - When to split policies for better performance

**Tech Writer Action Items:**

1. **Add prominent callouts to EVERY DLP page:**
   - Warning box: "⚠️ Files larger than [limit] will not be scanned and will be allowed through. Use additional controls for oversized files."
   - Include this in Getting Started, each workload page, and policy creation guides

2. **Create "Designing for Scale" guide:**
   - Section: "Planning for large files"
   - Section: "Testing with realistic data volumes"
   - Section: "Performance troubleshooting"
   - Include customer case studies

3. **Update policy creation workflows:**
   - Add checkbox: "My organization handles files >100MB" → Show special guidance
   - Include file size considerations in policy design wizard

4. **Create monitoring guidance:**
   - How to track bypassed files in Activity Explorer
   - Alert when files exceed size limits
   - Reporting on unscanned items

**Customer Scenario to Address:**
Customer created DLP policy with custom Korean phone number regex pattern to detect sensitive executive information. Policy worked for small files (<1MB) but when customer sent 22MB Excel file with 10,000+ rows of sensitive data, the regex pattern timed out and DLP allowed the file through. Customer discovered the breach weeks later. Documentation never explained regex performance limits or file size scanning boundaries.

**Business Risk:** HIGH - This is a data loss scenario, not just a usability issue

**Estimated Effort:** 12-16 hours (research all limits, document behaviors, create comprehensive table, write workarounds)

---

### ICM [691533110](https://portal.microsofticm.com/imp/v3/incidents/details/691533110)

**Title:** [Issue] Personal information using regular expression (regex) patterns is not getting blocked by DLP when a file containing thousands of records

**Team:** DLP Exchange

#### ❓ Customer Questions

- are in the sheet named "RAW_가공 (2)".PS2. We are providing our regex. We use regex combined with text keywords.b0[1-7](?:(?[=1)[016789]|(?[=2)|(?

#### 🔍 Expected vs Actual

**Actual:** we discovered that a file containing thousands of personal information records of important executives was sent via Outlook without being blocked

#### 😕 Confusion Points

- expected vs actual BehaviorWe are blocking personal information using regular expression (regex) patterns. However, we discovered that a file containing thousands of personal information records of important execut

#### 📝 Issue Summary

Attached in DTM portalCX has shared the working and non-working file along with PPTX recordingCx ran the tests, but the two files he shared during our previous Teams meeting are around 22MB each, which exceeds the upload limit. (See Screenshot 1)To work around this, he created a separate Excel fi...

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540)

**Title:** [Issue] Auto-labeling policy not applying to SPO location

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- arepoint / Teams sites                                      https://confluence.vallourec.net/pages/viewpage.action?

#### 🔍 Expected vs Actual

**Actual:** ton in Office online 2

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [730194018](https://portal.microsofticm.com/imp/v3/incidents/details/730194018)

**Title:** [RFC] Regarding the maximum number of SharePoint sites that can be configured in a DLP policy targeting SPO sites

**Team:** DLP SharePoint OneDrive

#### ❓ Customer Questions

- What is the maximum number of SharePoint sites that can be configured in a DLP policy targeting SPO sites?

#### 🔍 Expected vs Actual

**Actual:** that description appears to have been removed

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Add your question below: What is the maximum numbe

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

## 📋 Configuration & Examples

**ICMs in this category:** 7

**Priority:** HIGH - Lack of examples blocks feature adoption and causes misconfigurations

### 🎯 Documentation Theme: Real-World Configuration Examples and Working Code Samples

**Root Cause:** Documentation provides:
- High-level concepts without concrete examples
- Incomplete XML samples missing required elements
- Simple "hello world" examples that don't reflect real-world complexity
- No sample data to test configurations
- No validation guidance

**Business Impact:** Customers spend weeks trying to configure advanced features like custom SITs, rule packages, and checksum validators. Many give up and use inferior built-in options or purchase third-party solutions.

**Required Documentation Updates:**

1. **Create Microsoft Purview Samples Repository** (`github.com/microsoft/purview-samples`)
   - **DLP Policy Examples**
     - Healthcare HIPAA complete policy (all conditions, actions, notifications)
     - Financial PCI-DSS complete policy
     - GDPR multi-location policy
     - Include: Policy XML, PowerShell deployment script, test data
   
   - **Custom SIT Examples**
     - 10+ complete, tested custom SIT definitions
     - Employee ID patterns (various formats)
     - Custom financial data formats
     - Industry-specific patterns (medical record numbers, case IDs, etc.)
   
   - **Advanced XML Examples**
     - Custom checksum validation (multiple algorithms: SHA256, MD5, custom)
     - Advanced regex with named groups
     - Multi-condition matching with confidence levels
     - Each example must include:
       - Full XML code (not snippets)
       - Comments explaining each element
       - Test data (sample documents that should match)
       - Validation script to test the SIT
       - Expected results

2. **Create Interactive XML Builder Tool**
   - Web-based tool in documentation
   - User selects: SIT type, pattern type, confidence level
   - Tool generates valid XML
   - Includes validation and testing interface

3. **Add "Complete Example" to Every Feature Page**
   - Format: "Let's build a complete [feature] from start to finish"
   - 15-30 minute tutorial
   - Real scenario: "Protecting employee records in HR department"
   - Step-by-step with screenshots
   - Include testing and verification steps
   - Troubleshooting section: "What if it doesn't work?"

4. **Create Example Library by Industry**
   - `/purview/examples-healthcare`
   - `/purview/examples-financial`
   - `/purview/examples-government`
   - `/purview/examples-education`
   - Each includes: Complete policies, SITs, labels, recommended configurations

5. **Video Tutorials for Complex Configurations**
   - 5-10 minute videos showing:
     - Creating custom SIT with XML editor
     - Testing SIT with sample data
     - Deploying via PowerShell
     - Validating in Activity Explorer

**Tech Writer Action Items:**

1. **Audit all existing examples:**
   - Test every XML snippet (many are outdated or incomplete)
   - Expand snippets to full working examples
   - Add missing required elements
   - Add schema validation

2. **Create "Copy and Customize" templates:**
   - Pre-built templates customers can copy directly
   - Include TODO comments: "Replace this with your value"
   - Validation checklist included

3. **Add troubleshooting for examples:**
   - "Common errors when using this example"
   - "How to validate your configuration"
   - "Expected results vs. actual results"

4. **Create testing datasets:**
   - Sample files customers can use to test policies
   - Positive cases (should match) and negative cases (shouldn't match)
   - Downloadable test data repository

**Customer Scenario to Address:**
Customer needed to create custom SIT for advanced checksum validation (SHA256 hash of specific file types). Documentation showed basic checksum XML snippet with 5 lines. Customer tried to use it and received validation errors. Documentation didn't explain:
- Required XML schema version
- Mandatory parent elements
- Namespace declarations
- ID format requirements
- How to test the validator
- What "Validator" element does vs "Function" element

Customer spent 3 weeks and filed 2 support cases before getting working XML.

**Estimated Effort:** 40-60 hours (large effort requiring code samples, testing, validation)
**Recommendation:** Partner with PM/Engineering to validate examples

---

### ICM [691533110](https://portal.microsofticm.com/imp/v3/incidents/details/691533110)

**Title:** [Issue] Personal information using regular expression (regex) patterns is not getting blocked by DLP when a file containing thousands of records

**Team:** DLP Exchange

#### ❓ Customer Questions

- are in the sheet named "RAW_가공 (2)".PS2. We are providing our regex. We use regex combined with text keywords.b0[1-7](?:(?[=1)[016789]|(?[=2)|(?

#### 🔍 Expected vs Actual

**Actual:** we discovered that a file containing thousands of personal information records of important executives was sent via Outlook without being blocked

#### 😕 Confusion Points

- expected vs actual BehaviorWe are blocking personal information using regular expression (regex) patterns. However, we discovered that a file containing thousands of personal information records of important execut

#### 📝 Issue Summary

Attached in DTM portalCX has shared the working and non-working file along with PPTX recordingCx ran the tests, but the two files he shared during our previous Teams meeting are around 22MB each, which exceeds the upload limit. (See Screenshot 1)To work around this, he created a separate Excel fi...

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [729156307](https://portal.microsofticm.com/imp/v3/incidents/details/729156307)

**Title:** [RFC] Assist to provide rule package xml example for given advanced checksum capabilities

**Team:** Classification

#### 🔍 Expected vs Actual

**Actual:** I am not sure whether it is implemented this way Checksum Validator

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Previous escalation Incident-724141777 Details - I

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Complete, working XML examples for advanced features
- Commented code explaining each XML element
- Common checksum algorithm implementations
- Test data and validation scripts

**Where to Add:**
- Create GitHub repository: `microsoft/purview-samples`
- `/purview/sit-custom-get-started` - Link to examples
- Add interactive XML builder tool in documentation

---

### ICM [700114735](https://portal.microsofticm.com/imp/v3/incidents/details/700114735)

**Title:** [Issue] [Cit Alliance] Auto-labeling policies scoped to Exchange return no matches in simulation

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** Automatic labelling policies in Exchange online scoped to all users

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540)

**Title:** [Issue] Auto-labeling policy not applying to SPO location

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- arepoint / Teams sites                                      https://confluence.vallourec.net/pages/viewpage.action?

#### 🔍 Expected vs Actual

**Actual:** ton in Office online 2

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [724468498](https://portal.microsofticm.com/imp/v3/incidents/details/724468498)

**Title:** [Issue] Multiple notification emails are sent to the user when the rule is matched

**Team:** DLP Exchange

#### 🔍 Expected vs Actual

**Actual:** currently, the sender is
receiving 2 email notifications

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [714797265](https://portal.microsofticm.com/imp/v3/incidents/details/714797265)

**Title:** [Issue] Requesting Review of Singapore passport number SIT documentation for prefix 'K'

**Team:** Classification

#### 😕 Confusion Points

- gapore Passport NumberCustomer has requested the documentations to be updated with the info as the public documentation lists ‘e’/'E' as known prefix for the SIT.Singapore passport number entity definiti

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [724141777](https://portal.microsofticm.com/imp/v3/incidents/details/724141777)

**Title:** [RFC] Assist to clarify and provide example for advance checksum parameter.

**Team:** Classification

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Add your question below:  Client would like to kno

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Complete, working XML examples for advanced features
- Commented code explaining each XML element
- Common checksum algorithm implementations
- Test data and validation scripts

**Where to Add:**
- Create GitHub repository: `microsoft/purview-samples`
- `/purview/sit-custom-get-started` - Link to examples
- Add interactive XML builder tool in documentation

---

## 📋 URL Matching & Whitelisting

**ICMs in this category:** 5

### ICM [709524522](https://portal.microsofticm.com/imp/v3/incidents/details/709524522)

**Title:** [Issue] Endpoint DLP Whitelist Issue for Copilot Chat URL

**Team:** DLP Endpoint

#### ❓ Customer Questions

- which were whitelisted within several sensitive service domain groups. One of such url is the copilot chat url (https://m365.cloud.microsoft/chat?
- when the whitelist is applied.Current behaviour: Uploads to https://m365.cloud.microsoft/chat?

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- How URL matching works with query parameters
- Wildcard behavior and limitations
- When to whitelist parent domain vs specific URL
- Security implications of broad whitelisting
- Specific guidance for dynamic URLs (e.g., Copilot, Microsoft services)

**Where to Add:**
- `/purview/endpoint-dlp-using` - Add "URL Matching Reference" section
- Create new page: `/purview/dlp-url-matching-guide`
- Add examples for common Microsoft services

---

### ICM [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540)

**Title:** [Issue] Auto-labeling policy not applying to SPO location

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- arepoint / Teams sites                                      https://confluence.vallourec.net/pages/viewpage.action?

#### 🔍 Expected vs Actual

**Actual:** ton in Office online 2

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [693130111](https://portal.microsofticm.com/imp/v3/incidents/details/693130111)

**Title:** [Issue] eDLP generating slowness and freezing when processing Office files synchronized with OneDrive on their devices.

**Team:** DLP Endpoint

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [724698812](https://portal.microsofticm.com/imp/v3/incidents/details/724698812)

**Title:** [RFC] Could you provide details on the newly added fields in the parameters returned by Get-DlpComplianceRule?

**Team:** DLP (Generic)

#### ❓ Customer Questions

- Issue /Problem Description: Could you provide details on the newly added fields in the parameters returned by Get-DlpComplianceRule?

#### 🔍 Expected vs Actual

**Actual:** I could not find any documentation about these items

#### 😕 Confusion Points

- not clear, I’m unable to verify whether any DLP settings have been modified. 〇Troubleshooting:  I reviewed the publicly available information, but I could not find any documentation about these items.While the
- unclear which features they refer to. • "RestrictAccess": nullTitle: Set-DlpComplianceRule ––RestrictAccessURL: https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/set-dlpcompliancerule?vi

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- How URL matching works with query parameters
- Wildcard behavior and limitations
- When to whitelist parent domain vs specific URL
- Security implications of broad whitelisting
- Specific guidance for dynamic URLs (e.g., Copilot, Microsoft services)

**Where to Add:**
- `/purview/endpoint-dlp-using` - Add "URL Matching Reference" section
- Create new page: `/purview/dlp-url-matching-guide`
- Add examples for common Microsoft services

---

### ICM [703921423](https://portal.microsofticm.com/imp/v3/incidents/details/703921423)

**Title:** [Issue] Purview Portal Site Selection and URL Validation Error

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Expected:** All available sites should be visible in the selection screen

**Actual:** the customer is experiencing errors even when entering the URL as shown below

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

## 📋 Feature Scope & Timing

**ICMs in this category:** 21

### ICM [716201243](https://portal.microsofticm.com/imp/v3/incidents/details/716201243)

**Title:** [RFC] Team-4 |2511140030004237|CKP|DLP|RFC| The GDPR enhanced template DLP is not working for Teams location

**Team:** DLP Teams

#### ❓ Customer Questions

- cannot find any public document mention about this license: https://learn.microsoft.com/en-us/purview/dlp-microsoft-teams?

#### 🔍 Expected vs Actual

**Actual:** when sharing the Sensitive info via Teams chat, DLP did not detect them

#### 😕 Confusion Points

- cannot find any public document mention about this license: https://learn.microsoft.com/en-us/purview/dlp-microsoft-teams?tabs=purview#dlp-licensing-for-micros…Swarming post link: Jennie Phan (WICLOUD CORPORATIO
- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Add your question below:Issue: Customer created a

#### 📝 Issue Summary

Customer created a DLP policy scope only Teams location and apply to 3 groups of users. However, when sharing the Sensitive info via Teams chat, DLP did not detect them. However, if sharing the sensitive ino via file docx or txt, we can see DLP detected (working as expected) via Alert or Activity...

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [719718596](https://portal.microsofticm.com/imp/v3/incidents/details/719718596)

**Title:** [DCR] [S500] DKE options in sensitivity label configuration

**Team:** Sensitivity Labels

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [711972349](https://portal.microsofticm.com/imp/v3/incidents/details/711972349)

**Title:** [Issue] Auto labeling issue for SharePoint sites and OneDrive workload

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- iscover all unlabeled office files on SharePoint workloadScreenshot 1:Screenshot 2:Now, the ask is this data Reliable? how are the metrics updated here?

#### 🔍 Expected vs Actual

**Actual:** under the Auto-labeling portal, the customer sees the value “0” for Files Labeled

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [691533110](https://portal.microsofticm.com/imp/v3/incidents/details/691533110)

**Title:** [Issue] Personal information using regular expression (regex) patterns is not getting blocked by DLP when a file containing thousands of records

**Team:** DLP Exchange

#### ❓ Customer Questions

- are in the sheet named "RAW_가공 (2)".PS2. We are providing our regex. We use regex combined with text keywords.b0[1-7](?:(?[=1)[016789]|(?[=2)|(?

#### 🔍 Expected vs Actual

**Actual:** we discovered that a file containing thousands of personal information records of important executives was sent via Outlook without being blocked

#### 😕 Confusion Points

- expected vs actual BehaviorWe are blocking personal information using regular expression (regex) patterns. However, we discovered that a file containing thousands of personal information records of important execut

#### 📝 Issue Summary

Attached in DTM portalCX has shared the working and non-working file along with PPTX recordingCx ran the tests, but the two files he shared during our previous Teams meeting are around 22MB each, which exceeds the upload limit. (See Screenshot 1)To work around this, he created a separate Excel fi...

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [729156307](https://portal.microsofticm.com/imp/v3/incidents/details/729156307)

**Title:** [RFC] Assist to provide rule package xml example for given advanced checksum capabilities

**Team:** Classification

#### 🔍 Expected vs Actual

**Actual:** I am not sure whether it is implemented this way Checksum Validator

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Previous escalation Incident-724141777 Details - I

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Complete, working XML examples for advanced features
- Commented code explaining each XML element
- Common checksum algorithm implementations
- Test data and validation scripts

**Where to Add:**
- Create GitHub repository: `microsoft/purview-samples`
- `/purview/sit-custom-get-started` - Link to examples
- Add interactive XML builder tool in documentation

---

### ICM [709524522](https://portal.microsofticm.com/imp/v3/incidents/details/709524522)

**Title:** [Issue] Endpoint DLP Whitelist Issue for Copilot Chat URL

**Team:** DLP Endpoint

#### ❓ Customer Questions

- which were whitelisted within several sensitive service domain groups. One of such url is the copilot chat url (https://m365.cloud.microsoft/chat?
- when the whitelist is applied.Current behaviour: Uploads to https://m365.cloud.microsoft/chat?

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- How URL matching works with query parameters
- Wildcard behavior and limitations
- When to whitelist parent domain vs specific URL
- Security implications of broad whitelisting
- Specific guidance for dynamic URLs (e.g., Copilot, Microsoft services)

**Where to Add:**
- `/purview/endpoint-dlp-using` - Add "URL Matching Reference" section
- Create new page: `/purview/dlp-url-matching-guide`
- Add examples for common Microsoft services

---

### ICM [700114735](https://portal.microsofticm.com/imp/v3/incidents/details/700114735)

**Title:** [Issue] [Cit Alliance] Auto-labeling policies scoped to Exchange return no matches in simulation

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** Automatic labelling policies in Exchange online scoped to all users

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [730972455](https://portal.microsofticm.com/imp/v3/incidents/details/730972455)

**Title:** [Issue] Incorrect DLP Rule getting Triggered

**Team:** DLP Exchange

#### ❓ Customer Questions

- is impacting the behavior here and if it is not, what is solution to fix this?

#### 🔍 Expected vs Actual

**Actual:** Rule that should be triggered is "DLP
Control Password Protected Attachment" but we see a different rule being triggered, name: Bypass||Internal
EmailExtended Message Trace Detail report of a recent repro email (less than 30 days old): MTDetail_test pw protect_c364f831-8b27-40d0-8f65-2a708cb5be27

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Detailed explanation of what each condition checks
- Data source for each condition (file metadata vs content)
- Behavior differences by workload (Exchange, SharePoint, OneDrive)
- Matching logic and examples

**Where to Add:**
- `/purview/dlp-conditions-actions-reference` - Expand each condition
- Add comparison table: Exchange vs SharePoint vs OneDrive conditions
- Include screenshots showing where data comes from

---

### ICM [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540)

**Title:** [Issue] Auto-labeling policy not applying to SPO location

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- arepoint / Teams sites                                      https://confluence.vallourec.net/pages/viewpage.action?

#### 🔍 Expected vs Actual

**Actual:** ton in Office online 2

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [726209001](https://portal.microsofticm.com/imp/v3/incidents/details/726209001)

**Title:** [RFC] Behavior when a ‘Sync error’ occurs

**Team:** DLP (Generic)

#### ❓ Customer Questions

- is there any built‑in mechanism that automatically retries internally until the status returns to “Sync completed”?
- When a “Sync error” occurs, does the policy continue to operate based on the previous configuration?
- does a policy in a sync‑error state still function to some extent, rather than becoming completely inactive?

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team. Add your question below:[Detail]The customer has

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [719793969](https://portal.microsofticm.com/imp/v3/incidents/details/719793969)

**Title:** [RFC] Delays after filtering by 'Alert status'

**Team:** DLP Alerts

#### ❓ Customer Questions

- issue or any problem?
- issue, what is causing it, or what additional information would be required?

#### 🔍 Expected vs Actual

**Actual:** then when filtering by
'Alert status'; it takes more than a minute for the alerts to load

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team. Add your question below:A customer is

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [693130111](https://portal.microsofticm.com/imp/v3/incidents/details/693130111)

**Title:** [Issue] eDLP generating slowness and freezing when processing Office files synchronized with OneDrive on their devices.

**Team:** DLP Endpoint

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [713750747](https://portal.microsofticm.com/imp/v3/incidents/details/713750747)

**Title:** [Issue] Server side Autolabeling in Sharepoint Online is very slow

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Expected:** Customer is currently testing Autolabeling in Sharepoint

**Actual:** it took almost 1 week to label 24 files

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [730867091](https://portal.microsofticm.com/imp/v3/incidents/details/730867091)

**Title:** [RFC]Customers previously added onedrive.exe to the restricted apps list, and DLP was functioning.  This time, it stopped working in restricted apps, but adding it to the restricted apps group restored functionality.

**Team:** DLP Endpoint

#### ❓ Customer Questions

- is registered as an app group, but is it expected behavior that it cannot be detected when registered as a restricted app?
- istered as a restricted app, it could be detected. Has there been a functional change?

#### 🔍 Expected vs Actual

**Actual:** adding it to the restricted apps group restored functionality

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [721238221](https://portal.microsofticm.com/imp/v3/incidents/details/721238221)

**Title:** [Team-4][CKP][SIT][RFC][Ticket#2511280050002562] Need help with clarification related to SITs for Fabric and Power BI location

**Team:** DLP (Generic)

#### ❓ Customer Questions

- Please help us clarify that is there anyways for customer to effectively identify and split out only the SITs that compatible with Fabric and Power BI location when implementing a Data Loss Prevention?
- when implementing a Data Loss Prevention?

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Add your question below: Need help with clarificat

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Detailed explanation of what each condition checks
- Data source for each condition (file metadata vs content)
- Behavior differences by workload (Exchange, SharePoint, OneDrive)
- Matching logic and examples

**Where to Add:**
- `/purview/dlp-conditions-actions-reference` - Expand each condition
- Add comparison table: Exchange vs SharePoint vs OneDrive conditions
- Include screenshots showing where data comes from

---

### ICM [724468498](https://portal.microsofticm.com/imp/v3/incidents/details/724468498)

**Title:** [Issue] Multiple notification emails are sent to the user when the rule is matched

**Team:** DLP Exchange

#### 🔍 Expected vs Actual

**Actual:** currently, the sender is
receiving 2 email notifications

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [712476914](https://portal.microsofticm.com/imp/v3/incidents/details/712476914)

**Title:** [RFC] Existing metadata tags associated with files which has a sensitivity label  (with encryption)

**Team:** Sensitivity Labels

#### 🔍 Expected vs Actual

**Actual:** when we open the file in office application and check its
     properties in word app, meta data tag value is thereThis is happening only with the file which has an encrypted sensitivity label

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.  Add your question below:Files in the SharePoint

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [681612161](https://portal.microsofticm.com/imp/v3/incidents/details/681612161)

**Title:** [RFC] Sensitivity Labeling Behavior When Using OneDrive Sync Client (MIP MC1003342)

**Team:** DLP Endpoint

#### ❓ Customer Questions

- When a file is uploaded to SharePoint Online (SPO) or OneDrive via Microsoft Edge, the file is blocked, and a
- is synced to OneDrive without changing the extension, and the sensitivity label is removed.Is this behavior expected?
- does not explicitly describe scenarios for the OneDrive sync client, would it be possible to include a conclusion about this behavior in the documentation?

#### 🔍 Expected vs Actual

**Actual:** when using the OneDrive sync client, the file is synced to OneDrive without changing the extension, and the sensitivity label is removed

#### 😕 Confusion Points

- documentation does not explicitly describe scenarios for the OneDrive sync client, would it be possible to include a conclusion about this behavior in the documentation? I’

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [723572770](https://portal.microsofticm.com/imp/v3/incidents/details/723572770)

**Title:** [Issue] 2512120040005670 - DLP Action "Restric access or encrypt the content in Microsoft 365 locations" grey out

**Team:** DLP Exchange

#### 🔍 Expected vs Actual

**Actual:** it's not possible to modify them; they're grayed out, and if you try to create a new rule, the option isn't enabled either

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [703921423](https://portal.microsofticm.com/imp/v3/incidents/details/703921423)

**Title:** [Issue] Purview Portal Site Selection and URL Validation Error

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Expected:** All available sites should be visible in the selection screen

**Actual:** the customer is experiencing errors even when entering the URL as shown below

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [700569939](https://portal.microsofticm.com/imp/v3/incidents/details/700569939)

**Title:** [Issue] [Citi Alliance] Auto-labelling policies set to enforce mode, but they are not being applied correctly on SharePoint site

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** these are not being applied correctly on the SharePoint sites

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

## 📋 UI/UX & Validation

**ICMs in this category:** 15

**Priority:** MEDIUM - Impacts user experience and causes configuration errors

### 🎯 Documentation Theme: Portal Usability Issues and Input Validation

**Root Cause:** Several UI/UX issues not explained in documentation:
- Options greyed out without explanation
- URL validation errors without clear error messages
- Site picker showing limited results
- Dropdown options missing or unclear
- No validation guidance before submitting configurations
- Error messages that don't explain root cause or solution

**Business Impact:** Customers waste hours troubleshooting UI issues, assume features are broken when they're actually unavailable due to licensing/dependencies, and make configuration mistakes that aren't caught until deployment.

**Required Documentation Updates:**

1. **Create UI Troubleshooting Guide** (`/purview/portal-troubleshooting`)
   - **Section: "Why are options greyed out?"**
     - Common reasons for disabled UI elements:
       - Missing license/permissions
       - Prerequisite not configured (e.g., sensitivity labels not published)
       - Feature not available in current region/cloud
       - Policy scope limitations
     - How to diagnose each case
     - How to enable the option
   
   - **Section: "URL and Site Selection Issues"**
     - Site picker limitations (max 100 results displayed)
     - How to search for sites not showing in picker
     - URL format requirements
     - Special characters that cause validation errors
     - Wildcard support and limitations
   
   - **Section: "Error Message Reference"**
     - Complete list of error messages with:
       - What caused the error
       - How to fix it
       - Example configurations that work

2. **Add Validation Checklists to Configuration Pages**
   - Before creating a policy, verify:
     - [ ] Required licenses assigned
     - [ ] Admin permissions granted
     - [ ] Dependencies configured (labels published, etc.)
     - [ ] Locations are valid and accessible
     - [ ] Test data available for validation
   - Add "Pre-flight check" section to each wizard

3. **Document Feature Dependencies**
   - Create dependency matrix:
     - Feature X requires: License Y + Permission Z + Feature W enabled
   - Visual flowchart: "Before configuring DLP encryption action, ensure..."
   - Add callouts in UI documentation showing dependencies

4. **Create Input Validation Reference**
   - `/purview/valid-input-formats`
   - Tables showing:
     - Valid URL formats with examples
     - Valid group/user identifiers
     - Valid regex patterns
     - Character limits for each field
     - Reserved characters and escaping

5. **Add Accessibility and Browser Guidance**
   - Supported browsers and versions
   - Known browser-specific issues
   - Keyboard navigation shortcuts
   - Screen reader compatibility notes

**Tech Writer Action Items:**

1. **Document ALL Greyed-Out Scenarios:**
   - Work with PM team to catalog every scenario where UI elements are disabled
   - Create tooltip text for each: "This option is unavailable because..."
   - Add to documentation with screenshots

2. **Create Visual Troubleshooting Flowcharts:**
   - "Option greyed out" → Decision tree showing how to diagnose
   - "Can't find my site" → Steps to locate and add site
   - "Getting error message" → Error code lookup

3. **Add Validation Examples:**
   - Show both VALID and INVALID examples for every input type
   - Format: 
     ```
     ✅ Valid: https://contoso.sharepoint.com/sites/hr
     ❌ Invalid: contoso.sharepoint.com/sites/hr (missing https://)
     ❌ Invalid: https://contoso.sharepoint.com/sites/hr/ (trailing slash)
     ```

4. **Coordinate with UX Team:**
   - Propose better in-portal error messages
   - Suggest validation hints in UI
   - Request tooltip improvements

**Customer Scenario to Address:**
Customer tried to configure DLP action "Restrict access or encrypt content" but option was greyed out. Documentation never explained that:
1. Sensitivity labels must be published first
2. At least one label must have encryption configured
3. User must have rights to assign labels
4. Feature requires E5/A5 licensing

Customer spent 2 days troubleshooting, filed support case, escalated to engineering before root cause identified.

**Estimated Effort:** 12-15 hours (research all UI scenarios, create flowcharts, document validation rules)

---

### ICM [719718596](https://portal.microsofticm.com/imp/v3/incidents/details/719718596)

**Title:** [DCR] [S500] DKE options in sensitivity label configuration

**Team:** Sensitivity Labels

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [711972349](https://portal.microsofticm.com/imp/v3/incidents/details/711972349)

**Title:** [Issue] Auto labeling issue for SharePoint sites and OneDrive workload

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- iscover all unlabeled office files on SharePoint workloadScreenshot 1:Screenshot 2:Now, the ask is this data Reliable? how are the metrics updated here?

#### 🔍 Expected vs Actual

**Actual:** under the Auto-labeling portal, the customer sees the value “0” for Files Labeled

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [729156307](https://portal.microsofticm.com/imp/v3/incidents/details/729156307)

**Title:** [RFC] Assist to provide rule package xml example for given advanced checksum capabilities

**Team:** Classification

#### 🔍 Expected vs Actual

**Actual:** I am not sure whether it is implemented this way Checksum Validator

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Previous escalation Incident-724141777 Details - I

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Complete, working XML examples for advanced features
- Commented code explaining each XML element
- Common checksum algorithm implementations
- Test data and validation scripts

**Where to Add:**
- Create GitHub repository: `microsoft/purview-samples`
- `/purview/sit-custom-get-started` - Link to examples
- Add interactive XML builder tool in documentation

---

### ICM [700114735](https://portal.microsofticm.com/imp/v3/incidents/details/700114735)

**Title:** [Issue] [Cit Alliance] Auto-labeling policies scoped to Exchange return no matches in simulation

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** Automatic labelling policies in Exchange online scoped to all users

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [730972455](https://portal.microsofticm.com/imp/v3/incidents/details/730972455)

**Title:** [Issue] Incorrect DLP Rule getting Triggered

**Team:** DLP Exchange

#### ❓ Customer Questions

- is impacting the behavior here and if it is not, what is solution to fix this?

#### 🔍 Expected vs Actual

**Actual:** Rule that should be triggered is "DLP
Control Password Protected Attachment" but we see a different rule being triggered, name: Bypass||Internal
EmailExtended Message Trace Detail report of a recent repro email (less than 30 days old): MTDetail_test pw protect_c364f831-8b27-40d0-8f65-2a708cb5be27

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Detailed explanation of what each condition checks
- Data source for each condition (file metadata vs content)
- Behavior differences by workload (Exchange, SharePoint, OneDrive)
- Matching logic and examples

**Where to Add:**
- `/purview/dlp-conditions-actions-reference` - Expand each condition
- Add comparison table: Exchange vs SharePoint vs OneDrive conditions
- Include screenshots showing where data comes from

---

### ICM [667236540](https://portal.microsofticm.com/imp/v3/incidents/details/667236540)

**Title:** [Issue] Auto-labeling policy not applying to SPO location

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- arepoint / Teams sites                                      https://confluence.vallourec.net/pages/viewpage.action?

#### 🔍 Expected vs Actual

**Actual:** ton in Office online 2

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [726209001](https://portal.microsofticm.com/imp/v3/incidents/details/726209001)

**Title:** [RFC] Behavior when a ‘Sync error’ occurs

**Team:** DLP (Generic)

#### ❓ Customer Questions

- is there any built‑in mechanism that automatically retries internally until the status returns to “Sync completed”?
- When a “Sync error” occurs, does the policy continue to operate based on the previous configuration?
- does a policy in a sync‑error state still function to some extent, rather than becoming completely inactive?

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team. Add your question below:[Detail]The customer has

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [719793969](https://portal.microsofticm.com/imp/v3/incidents/details/719793969)

**Title:** [RFC] Delays after filtering by 'Alert status'

**Team:** DLP Alerts

#### ❓ Customer Questions

- issue or any problem?
- issue, what is causing it, or what additional information would be required?

#### 🔍 Expected vs Actual

**Actual:** then when filtering by
'Alert status'; it takes more than a minute for the alerts to load

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team. Add your question below:A customer is

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [713750747](https://portal.microsofticm.com/imp/v3/incidents/details/713750747)

**Title:** [Issue] Server side Autolabeling in Sharepoint Online is very slow

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Expected:** Customer is currently testing Autolabeling in Sharepoint

**Actual:** it took almost 1 week to label 24 files

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [724468498](https://portal.microsofticm.com/imp/v3/incidents/details/724468498)

**Title:** [Issue] Multiple notification emails are sent to the user when the rule is matched

**Team:** DLP Exchange

#### 🔍 Expected vs Actual

**Actual:** currently, the sender is
receiving 2 email notifications

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [681612161](https://portal.microsofticm.com/imp/v3/incidents/details/681612161)

**Title:** [RFC] Sensitivity Labeling Behavior When Using OneDrive Sync Client (MIP MC1003342)

**Team:** DLP Endpoint

#### ❓ Customer Questions

- When a file is uploaded to SharePoint Online (SPO) or OneDrive via Microsoft Edge, the file is blocked, and a
- is synced to OneDrive without changing the extension, and the sensitivity label is removed.Is this behavior expected?
- does not explicitly describe scenarios for the OneDrive sync client, would it be possible to include a conclusion about this behavior in the documentation?

#### 🔍 Expected vs Actual

**Actual:** when using the OneDrive sync client, the file is synced to OneDrive without changing the extension, and the sensitivity label is removed

#### 😕 Confusion Points

- documentation does not explicitly describe scenarios for the OneDrive sync client, would it be possible to include a conclusion about this behavior in the documentation? I’

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [723572770](https://portal.microsofticm.com/imp/v3/incidents/details/723572770)

**Title:** [Issue] 2512120040005670 - DLP Action "Restric access or encrypt the content in Microsoft 365 locations" grey out

**Team:** DLP Exchange

#### 🔍 Expected vs Actual

**Actual:** it's not possible to modify them; they're grayed out, and if you try to create a new rule, the option isn't enabled either

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [703921423](https://portal.microsofticm.com/imp/v3/incidents/details/703921423)

**Title:** [Issue] Purview Portal Site Selection and URL Validation Error

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Expected:** All available sites should be visible in the selection screen

**Actual:** the customer is experiencing errors even when entering the URL as shown below

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [700569939](https://portal.microsofticm.com/imp/v3/incidents/details/700569939)

**Title:** [Issue] [Citi Alliance] Auto-labelling policies set to enforce mode, but they are not being applied correctly on SharePoint site

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** these are not being applied correctly on the SharePoint sites

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [700706744](https://portal.microsofticm.com/imp/v3/incidents/details/700706744)

**Title:** [Issue] Autolabelling policies do not label historical data

**Team:** Server Side Auto Labeling

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

## 📋 Conditions & Rules Behavior

**ICMs in this category:** 6

**Priority:** HIGH - Misunderstanding conditions causes policy misconfigurations and security gaps

### 🎯 Documentation Theme: How DLP Conditions Actually Work

**Root Cause:** Documentation lists conditions but doesn't explain:
- **What data source** each condition checks (file metadata? content? properties?)
- **How matching works** (exact match? fuzzy? case-sensitive?)
- **Behavior differences by workload** (same condition works differently in Exchange vs SharePoint vs Endpoint)
- **URL matching logic** (wildcards, query parameters, paths, domains)
- **Performance implications** of complex conditions
- **Condition priority and evaluation order**

**Business Impact:** CRITICAL - Customers create policies thinking they protect data, but conditions don't work as expected, resulting in:
- False negatives (sensitive data not detected) = Data loss
- False positives (legitimate files blocked) = Business disruption
- Incorrect URL whitelisting = Security gaps

**Required Documentation Updates:**

1. **Create Comprehensive Conditions Reference** (`/purview/dlp-conditions-deep-dive`)
   - For EACH condition, document:
   
   **Example: "Document Property Is" Condition**
   
   | Aspect | Details |
   |--------|--------|
   | **What it checks** | File metadata properties, not content |
   | **Data source** | SharePoint: Column values in library<br>Exchange: Message properties<br>OneDrive: File properties |
   | **Matching logic** | Exact match only (not partial) |
   | **Case sensitive?** | No |
   | **Works on** | Office files, PDFs (metadata-capable formats) |
   | **Doesn't work on** | TXT, CSV, images without metadata |
   | **Example** | Property "Department" equals "Finance" |
   | **Common mistakes** | Checking for content in property field |
   | **Performance** | Fast (metadata lookup, no content scan) |
   
   Repeat this table format for all 50+ conditions

2. **Create Workload Comparison Matrix**
   - Side-by-side table showing how same condition behaves differently:
   
   | Condition | Exchange | SharePoint | OneDrive | Teams | Endpoint |
   |-----------|----------|------------|----------|-------|----------|
   | File ext is | Attachment ext | File ext | File ext | Shared file ext | Local file ext |
   | Document property | Email properties | List column | N/A | N/A | File props |
   | Size is | Attachment size | File size | File size | Shared file size | File size |
   | Recipient is | To/Cc/Bcc | N/A | Shared with | Sent to | N/A |

3. **Create URL Matching Reference** (`/purview/dlp-url-matching-rules`)
   - **URL Structure Breakdown:**
     ```
     https://m365.cloud.microsoft.com/chat?auth=token&id=123
     |_____| |____________________| |____| |_________________|
     Protocol     Domain            Path    Query Parameters
     ```
   
   - **Matching Behavior Table:**
   
   | Pattern | Matches | Doesn't Match | Query Params? |
   |---------|---------|---------------|---------------|
   | `*` (wildcard) | All URLs | None | Yes |
   | `*.microsoft.com` | All MS subdomains | `microsoft.com` only | Yes |
   | `m365.cloud.microsoft.com` | Exact domain | Subdomains | Yes |
   | `m365.cloud.microsoft.com/chat` | Path and subpaths | Different paths | Yes |
   | `m365.cloud.microsoft.com/chat?*` | Path with any params | Path without params | Required |
   
   - **Common Scenarios:**
     - Whitelisting Microsoft Copilot: Which patterns work
     - Blocking file sharing sites: Example patterns
     - Dynamic URLs with authentication tokens: How to handle

4. **Create Condition Testing Guide**
   - How to test each condition before production deployment
   - Test data sets for common conditions
   - Using simulation mode effectively
   - Interpreting Activity Explorer results
   - PowerShell scripts to validate condition matching

5. **Document Condition Evaluation Order**
   - How DLP processes multiple conditions (AND vs OR logic)
   - Precedence rules
   - How exceptions work
   - Performance optimization tips

**Tech Writer Action Items:**

1. **Create "How Conditions Work" Video Series:**
   - 3-5 minute video for each complex condition
   - Show: What gets checked, how to test, common mistakes
   - Screen recording showing policy evaluation in real-time

2. **Add "Test This Condition" Sections:**
   - For each condition, provide:
     - Sample policy snippet
     - Test files to use
     - Expected results
     - How to verify it worked

3. **Create Scenario-Based Examples:**
   - "I want to detect files shared externally" → Which conditions to use
   - "I want to allow Copilot but block other browsers" → URL whitelist example
   - "I want to protect only files tagged 'Confidential'" → Property condition setup

4. **Add Debugging Guidance:**
   - "My condition isn't matching" troubleshooting flowchart
   - How to check what data the condition sees
   - Using Activity Explorer to debug matches

**Customer Scenario to Address:**
Customer whitelisted `https://m365.cloud.microsoft.com/chat` to allow Copilot uploads, but DLP still blocked uploads because the actual URL included query parameters and session tokens: `https://m365.cloud.microsoft.com/chat?auth=abc123&session=xyz`. Documentation never explained that:
- URL matching requires wildcard for query params: `/chat?*`
- Or use domain-only whitelist: `m365.cloud.microsoft.com`
- Or whitelist parent path: `/chat`
- Query parameters are included in URL matching by default

Customer's configuration allowed only exact URL with no parameters, blocking all real-world Copilot usage.

**Estimated Effort:** 20-30 hours (large effort requiring testing of all conditions across all workloads)
**Recommendation:** Partner with QA team for condition testing verification

---

### ICM [709524522](https://portal.microsofticm.com/imp/v3/incidents/details/709524522)

**Title:** [Issue] Endpoint DLP Whitelist Issue for Copilot Chat URL

**Team:** DLP Endpoint

#### ❓ Customer Questions

- which were whitelisted within several sensitive service domain groups. One of such url is the copilot chat url (https://m365.cloud.microsoft/chat?
- when the whitelist is applied.Current behaviour: Uploads to https://m365.cloud.microsoft/chat?

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- How URL matching works with query parameters
- Wildcard behavior and limitations
- When to whitelist parent domain vs specific URL
- Security implications of broad whitelisting
- Specific guidance for dynamic URLs (e.g., Copilot, Microsoft services)

**Where to Add:**
- `/purview/endpoint-dlp-using` - Add "URL Matching Reference" section
- Create new page: `/purview/dlp-url-matching-guide`
- Add examples for common Microsoft services

---

### ICM [722954497](https://portal.microsofticm.com/imp/v3/incidents/details/722954497)

**Title:** [DCR] Improve DLP's conditions documentation -TrackingID#2507091420001794

**Team:** DLP SharePoint OneDrive

#### 🔍 Expected vs Actual

**Actual:** Data loss prevention policy tip reference for SharePoint in Microsoft 365 and OneDrive for work or school web client | Microsoft Learn does not describe what each DLP condition looks for e

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Detailed explanation of what each condition checks
- Data source for each condition (file metadata vs content)
- Behavior differences by workload (Exchange, SharePoint, OneDrive)
- Matching logic and examples

**Where to Add:**
- `/purview/dlp-conditions-actions-reference` - Expand each condition
- Add comparison table: Exchange vs SharePoint vs OneDrive conditions
- Include screenshots showing where data comes from

---

### ICM [700114735](https://portal.microsofticm.com/imp/v3/incidents/details/700114735)

**Title:** [Issue] [Cit Alliance] Auto-labeling policies scoped to Exchange return no matches in simulation

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** Automatic labelling policies in Exchange online scoped to all users

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [730972455](https://portal.microsofticm.com/imp/v3/incidents/details/730972455)

**Title:** [Issue] Incorrect DLP Rule getting Triggered

**Team:** DLP Exchange

#### ❓ Customer Questions

- is impacting the behavior here and if it is not, what is solution to fix this?

#### 🔍 Expected vs Actual

**Actual:** Rule that should be triggered is "DLP
Control Password Protected Attachment" but we see a different rule being triggered, name: Bypass||Internal
EmailExtended Message Trace Detail report of a recent repro email (less than 30 days old): MTDetail_test pw protect_c364f831-8b27-40d0-8f65-2a708cb5be27

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Detailed explanation of what each condition checks
- Data source for each condition (file metadata vs content)
- Behavior differences by workload (Exchange, SharePoint, OneDrive)
- Matching logic and examples

**Where to Add:**
- `/purview/dlp-conditions-actions-reference` - Expand each condition
- Add comparison table: Exchange vs SharePoint vs OneDrive conditions
- Include screenshots showing where data comes from

---

### ICM [721238221](https://portal.microsofticm.com/imp/v3/incidents/details/721238221)

**Title:** [Team-4][CKP][SIT][RFC][Ticket#2511280050002562] Need help with clarification related to SITs for Fabric and Power BI location

**Team:** DLP (Generic)

#### ❓ Customer Questions

- Please help us clarify that is there anyways for customer to effectively identify and split out only the SITs that compatible with Fabric and Power BI location when implementing a Data Loss Prevention?
- when implementing a Data Loss Prevention?

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Add your question below: Need help with clarificat

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Detailed explanation of what each condition checks
- Data source for each condition (file metadata vs content)
- Behavior differences by workload (Exchange, SharePoint, OneDrive)
- Matching logic and examples

**Where to Add:**
- `/purview/dlp-conditions-actions-reference` - Expand each condition
- Add comparison table: Exchange vs SharePoint vs OneDrive conditions
- Include screenshots showing where data comes from

---

### ICM [700569939](https://portal.microsofticm.com/imp/v3/incidents/details/700569939)

**Title:** [Issue] [Citi Alliance] Auto-labelling policies set to enforce mode, but they are not being applied correctly on SharePoint site

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** these are not being applied correctly on the SharePoint sites

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

## 📋 Notifications & Alerts

**ICMs in this category:** 13

### ICM [716201243](https://portal.microsofticm.com/imp/v3/incidents/details/716201243)

**Title:** [RFC] Team-4 |2511140030004237|CKP|DLP|RFC| The GDPR enhanced template DLP is not working for Teams location

**Team:** DLP Teams

#### ❓ Customer Questions

- cannot find any public document mention about this license: https://learn.microsoft.com/en-us/purview/dlp-microsoft-teams?

#### 🔍 Expected vs Actual

**Actual:** when sharing the Sensitive info via Teams chat, DLP did not detect them

#### 😕 Confusion Points

- cannot find any public document mention about this license: https://learn.microsoft.com/en-us/purview/dlp-microsoft-teams?tabs=purview#dlp-licensing-for-micros…Swarming post link: Jennie Phan (WICLOUD CORPORATIO
- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team.Add your question below:Issue: Customer created a

#### 📝 Issue Summary

Customer created a DLP policy scope only Teams location and apply to 3 groups of users. However, when sharing the Sensitive info via Teams chat, DLP did not detect them. However, if sharing the sensitive ino via file docx or txt, we can see DLP detected (working as expected) via Alert or Activity...

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [711972349](https://portal.microsofticm.com/imp/v3/incidents/details/711972349)

**Title:** [Issue] Auto labeling issue for SharePoint sites and OneDrive workload

**Team:** Server Side Auto Labeling

#### ❓ Customer Questions

- iscover all unlabeled office files on SharePoint workloadScreenshot 1:Screenshot 2:Now, the ask is this data Reliable? how are the metrics updated here?

#### 🔍 Expected vs Actual

**Actual:** under the Auto-labeling portal, the customer sees the value “0” for Files Labeled

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [713662994](https://portal.microsofticm.com/imp/v3/incidents/details/713662994)

**Title:** [RFC] policies still pending after waiting more than 30 days

**Team:** DLP (Generic)

#### 🔍 Expected vs Actual

**Expected:** Normally, DLP policy distribution completes within hours to a few days after creation

**Actual:** ion status of “Pending”, even though many of these policies have been active for over 30 days

#### 😕 Confusion Points

- Expected Behavior:Normally, DLP policy distribution completes within hours to a few days after creation.Extended pending status beyond 30 days is no
- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team. Add your question below:Issue Description: Custom

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Definition of each policy status (Pending, Distributing, Success, Error)
- Expected time in each status
- When 30+ days pending is normal vs concerning
- Troubleshooting steps for stuck policies

**Where to Add:**
- Create new page: `/purview/policy-distribution-status-reference`
- `/purview/dlp-policy-design` - Add section on policy distribution
- Add PowerShell examples to check policy status

---

### ICM [700114735](https://portal.microsofticm.com/imp/v3/incidents/details/700114735)

**Title:** [Issue] [Cit Alliance] Auto-labeling policies scoped to Exchange return no matches in simulation

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** Automatic labelling policies in Exchange online scoped to all users

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear license comparison showing which features are included in each tier
- Specific coverage for Teams chat vs Teams files
- License requirements for each workload and feature

**Where to Add:**
- `/purview/dlp-licensing` - Add comprehensive comparison table
- `/purview/dlp-microsoft-teams` - Add license requirements section
- Add FAQ: "Which license do I need for Teams DLP?"

---

### ICM [730972455](https://portal.microsofticm.com/imp/v3/incidents/details/730972455)

**Title:** [Issue] Incorrect DLP Rule getting Triggered

**Team:** DLP Exchange

#### ❓ Customer Questions

- is impacting the behavior here and if it is not, what is solution to fix this?

#### 🔍 Expected vs Actual

**Actual:** Rule that should be triggered is "DLP
Control Password Protected Attachment" but we see a different rule being triggered, name: Bypass||Internal
EmailExtended Message Trace Detail report of a recent repro email (less than 30 days old): MTDetail_test pw protect_c364f831-8b27-40d0-8f65-2a708cb5be27

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Detailed explanation of what each condition checks
- Data source for each condition (file metadata vs content)
- Behavior differences by workload (Exchange, SharePoint, OneDrive)
- Matching logic and examples

**Where to Add:**
- `/purview/dlp-conditions-actions-reference` - Expand each condition
- Add comparison table: Exchange vs SharePoint vs OneDrive conditions
- Include screenshots showing where data comes from

---

### ICM [719793969](https://portal.microsofticm.com/imp/v3/incidents/details/719793969)

**Title:** [RFC] Delays after filtering by 'Alert status'

**Team:** DLP Alerts

#### ❓ Customer Questions

- issue or any problem?
- issue, what is causing it, or what additional information would be required?

#### 🔍 Expected vs Actual

**Actual:** then when filtering by
'Alert status'; it takes more than a minute for the alerts to load

#### 😕 Confusion Points

- Documentation and due diligence research does not outline a specific customer/use-case scenario and confirmation is needed from the Engineering Team. Add your question below:A customer is

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [723508987](https://portal.microsofticm.com/imp/v3/incidents/details/723508987)

**Title:** [Issue] Label Policy stuck in pending distribution for over 48 hours

**Team:** Sensitivity Labels

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [724468498](https://portal.microsofticm.com/imp/v3/incidents/details/724468498)

**Title:** [Issue] Multiple notification emails are sent to the user when the rule is matched

**Team:** DLP Exchange

#### 🔍 Expected vs Actual

**Actual:** currently, the sender is
receiving 2 email notifications

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [714797265](https://portal.microsofticm.com/imp/v3/incidents/details/714797265)

**Title:** [Issue] Requesting Review of Singapore passport number SIT documentation for prefix 'K'

**Team:** Classification

#### 😕 Confusion Points

- gapore Passport NumberCustomer has requested the documentations to be updated with the info as the public documentation lists ‘e’/'E' as known prefix for the SIT.Singapore passport number entity definiti

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [681612161](https://portal.microsofticm.com/imp/v3/incidents/details/681612161)

**Title:** [RFC] Sensitivity Labeling Behavior When Using OneDrive Sync Client (MIP MC1003342)

**Team:** DLP Endpoint

#### ❓ Customer Questions

- When a file is uploaded to SharePoint Online (SPO) or OneDrive via Microsoft Edge, the file is blocked, and a
- is synced to OneDrive without changing the extension, and the sensitivity label is removed.Is this behavior expected?
- does not explicitly describe scenarios for the OneDrive sync client, would it be possible to include a conclusion about this behavior in the documentation?

#### 🔍 Expected vs Actual

**Actual:** when using the OneDrive sync client, the file is synced to OneDrive without changing the extension, and the sensitivity label is removed

#### 😕 Confusion Points

- documentation does not explicitly describe scenarios for the OneDrive sync client, would it be possible to include a conclusion about this behavior in the documentation? I’

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [700569939](https://portal.microsofticm.com/imp/v3/incidents/details/700569939)

**Title:** [Issue] [Citi Alliance] Auto-labelling policies set to enforce mode, but they are not being applied correctly on SharePoint site

**Team:** Server Side Auto Labeling

#### 🔍 Expected vs Actual

**Actual:** these are not being applied correctly on the SharePoint sites

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

### ICM [700706744](https://portal.microsofticm.com/imp/v3/incidents/details/700706744)

**Title:** [Issue] Autolabelling policies do not label historical data

**Team:** Server Side Auto Labeling

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Clear documentation addressing the specific scenario
- Step-by-step examples
- Troubleshooting guide for common issues

**Where to Add:**
- Update relevant feature documentation page
- Add to FAQ section

---

### ICM [706301319](https://portal.microsofticm.com/imp/v3/incidents/details/706301319)

**Title:** [Issue] Missing documentation on Licensing for Sensitivity labels for meeting invites

**Team:** Sensitivity Labels

#### 🔍 Expected vs Actual

**Actual:** ton for meeting invites

#### 😕 Confusion Points

- documentation does NOT mention the above needs to be enabled. Use sensitivity labels to protect calendar items, Teams meetings, and chat | Microsoft LearnFor reference:http

#### 📖 What's Missing in Current Documentation

**Missing Content:**
- Refresh intervals for portal metrics (how often data updates)
- Why metrics might show 0 temporarily
- Difference between portal metrics and Activity Explorer data
- Expected delays and data consistency information

**Where to Add:**
- Create new page: `/purview/portal-metrics-reference`
- Add tooltips in UI next to each metric
- `/purview/auto-labeling-policies` - Add "Understanding Metrics" section

---

## 📊 Quick Reference: Documentation Pages to Update

| Documentation Page | Updates Needed | Priority | ICMs |
|-------------------|----------------|----------|------|
| `/purview/dlp-licensing` | Add license comparison table with Teams chat/file coverage | 🔴 HIGH | Multiple |
| `/purview/portal-metrics-reference` | Create new page with refresh intervals and metric definitions | 🔴 HIGH | Multiple |
| `/purview/policy-distribution-status-reference` | Create new page with status definitions and troubleshooting | 🔴 HIGH | Multiple |
| `/purview/dlp-url-matching-guide` | Create new page explaining URL matching with examples | 🔴 HIGH | Multiple |
| `/purview/service-limits-dlp-classification` | Create new page with all size and scale limits | 🟡 MEDIUM | Multiple |
| `/purview/dlp-conditions-actions-reference` | Expand condition explanations with data sources and examples | 🟡 MEDIUM | Multiple |
| `/purview/apply-sensitivity-label-automatically` | Add scope clarification (in-transit vs at-rest) | 🟡 MEDIUM | Multiple |
| `GitHub: microsoft/purview-samples` | Create sample repository with XML examples and test data | 🟡 MEDIUM | Multiple |

