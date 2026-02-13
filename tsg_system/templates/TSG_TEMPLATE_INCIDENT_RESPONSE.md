# Incident Response: [Incident Type]

**TSG ID:** IR-[YYYYMMDD]-[Sequential Number]  
**Product Area:** [e.g., Microsoft Purview - DLP / eDiscovery / Audit / Retention]  
**Severity:** [Critical / High / Medium / Low]  
**Last Updated:** [Date]  
**Last Reviewed By:** [Name/Alias]  
**Version:** 1.0

---

## 🚨 Quick Action Summary

**THIS IS A CRITICAL INCIDENT RESPONSE GUIDE**

**Immediate Actions (First 15 minutes):**
1. [Critical action 1]
2. [Critical action 2]
3. [Critical action 3]

**Who to Notify:**
- On-Call PHE: [Contact method]
- ICM DRI: [Create ICM with severity X]
- Customer: [Communication template in section X]

---

## Incident Overview

### Incident Type
[Clear description of what type of incident this guide addresses]

**Incident Indicators:**
- [Sign 1 that this incident is occurring]
- [Sign 2 that this incident is occurring]
- [Sign 3 that this incident is occurring]

### Severity Classification

#### Severity 1 (Critical)
- Multiple customers affected (>10)
- Data loss or security breach
- Complete service unavailability
- IC/MCS customer with business-critical impact

**Response Time:** Immediate (within 15 minutes)
**ICM Required:** Yes - Sev 1

#### Severity 2 (High)
- Limited customers affected (1-10)
- Partial service degradation
- Workaround available but complex
- Single IC/MCS customer affected

**Response Time:** Within 1 hour
**ICM Required:** Yes - Sev 2

#### Severity 3 (Medium)
- Isolated customer issue
- Workaround readily available
- Non-critical functionality impacted

**Response Time:** Within 4 hours
**ICM Required:** Based on customer program

---

## Incident Response Team

### Roles and Responsibilities

**Incident Commander (IC):**
- Overall incident coordination
- Decision authority
- Communication lead
- [Name/Alias or On-Call rotation]

**Technical Lead (TL):**
- Technical investigation
- Root cause analysis
- Mitigation implementation
- [Name/Alias or On-Call rotation]

**Communications Lead:**
- Customer communications
- Internal status updates
- Post-incident report
- [Name/Alias or escalation path]

**Subject Matter Experts (SMEs):**
- Product-specific expertise
- Engineering escalation point
- [List of SME contacts by product area]

---

## Phase 1: Detection and Assessment (0-15 minutes)

### Step 1: Confirm Incident
**Objective:** Verify that an actual incident is occurring

**Validation Checklist:**
- [ ] Check service health dashboard: [URL]
- [ ] Review monitoring alerts: [Location]
- [ ] Confirm with multiple data sources
- [ ] Determine if this is service-wide or tenant-specific

**Kusto Queries for Validation:**
```kql
// Quick incident validation query
[Insert query to check scope and impact]
```

**Decision Point:** 
- If confirmed: Proceed to Step 2
- If false alarm: Document findings and close

---

### Step 2: Assess Impact
**Objective:** Determine scope and severity

**Impact Assessment:**
1. **Customer Count**
   - [ ] How many customers affected?
   - [ ] Are any IC/MCS customers affected?
   - [ ] Query: [Insert query to identify affected tenants]

2. **Functional Impact**
   - [ ] What functionality is impacted?
   - [ ] Is data at risk?
   - [ ] Can users work around the issue?

3. **Geographic Scope**
   - [ ] Specific regions affected?
   - [ ] Global or localized?

4. **Severity Determination**
   - [ ] Assign severity based on criteria above
   - [ ] Document justification

**Output:** Complete Impact Assessment Report (template in Appendix A)

---

### Step 3: Initial Notification
**Objective:** Alert stakeholders and mobilize response team

**Notification Matrix:**

| Severity | Notify Who | Method | Timeframe |
|----------|-----------|--------|-----------|
| Sev 1 | PHE On-Call, CLE, ICM | Phone + Teams | Immediately |
| Sev 2 | PHE, CLE, Create ICM | Teams + Email | Within 15 min |
| Sev 3 | PHE, Update case | Email | Within 1 hour |

**Create ICM:**
```
Title: [Product Area] - [Brief description]
Severity: [1/2/3]
Owning Team: [Team]
Description: [Impact summary from Step 2]
Customer Impact: [Tenant count and business impact]
```

**Initial Customer Communication:**
[Use template in Appendix B]

---

## Phase 2: Investigation and Diagnosis (15-60 minutes)

### Step 4: Gather Diagnostic Data
**Objective:** Collect all relevant information for root cause analysis

**Data Collection Checklist:**
- [ ] Service logs from affected timeframe
- [ ] Tenant configuration
- [ ] Recent changes (last 48 hours)
- [ ] User activity logs
- [ ] Related incidents/cases

**Key Diagnostic Queries:**

#### Query 1: Error Pattern Analysis
```kql
// [Description of what this query shows]
[Kusto query]
```

#### Query 2: Affected Tenant Analysis
```kql
// [Description of what this query shows]
[Kusto query]
```

#### Query 3: Timeline Reconstruction
```kql
// [Description of what this query shows]
[Kusto query]
```

---

### Step 5: Identify Root Cause
**Objective:** Determine what caused the incident

**Common Root Causes:**

#### Cause A: [e.g., Configuration Change]
**How to Identify:**
- [Indicator 1]
- [Indicator 2]

**Validation Steps:**
1. [Step to confirm]
2. [Step to confirm]

**If Confirmed:** Proceed to Mitigation Path A

---

#### Cause B: [e.g., Service Degradation]
**How to Identify:**
- [Indicator 1]
- [Indicator 2]

**Validation Steps:**
1. [Step to confirm]
2. [Step to confirm]

**If Confirmed:** Proceed to Mitigation Path B

---

#### Cause C: [e.g., External Dependency Failure]
**How to Identify:**
- [Indicator 1]
- [Indicator 2]

**Validation Steps:**
1. [Step to confirm]
2. [Step to confirm]

**If Confirmed:** Proceed to Mitigation Path C

---

### Step 6: Develop Mitigation Plan
**Objective:** Create action plan to restore service

**Mitigation Planning Template:**
```markdown
## Mitigation Plan

**Root Cause:** [Identified cause]
**Mitigation Strategy:** [High-level approach]
**Estimated Time to Restore:** [Duration]
**Risk of Mitigation:** [Low/Medium/High]
**Rollback Plan:** [How to undo if mitigation fails]

### Actions:
1. [Action 1] - Owner: [Name] - ETA: [Time]
2. [Action 2] - Owner: [Name] - ETA: [Time]
3. [Action 3] - Owner: [Name] - ETA: [Time]

### Success Criteria:
- [How we'll know service is restored]
- [Metrics to monitor]
```

**Approval Required:**
- [ ] Incident Commander approval
- [ ] Risk assessment completed
- [ ] Customer communication prepared

---

## Phase 3: Mitigation and Recovery (60+ minutes)

### Mitigation Path A: [Configuration Rollback]
**When to Use:** Configuration change caused incident

**Pre-Mitigation Checklist:**
- [ ] Backup current configuration
- [ ] Identify rollback target state
- [ ] Estimate propagation time
- [ ] Prepare rollback plan

**Mitigation Steps:**
1. **[Action 1]**
   ```
   [Commands or steps]
   ```
   - Expected result: [Outcome]
   - Verification: [How to confirm]

2. **[Action 2]**
   ```
   [Commands or steps]
   ```
   - Expected result: [Outcome]
   - Verification: [How to confirm]

3. **[Validation]**
   - Run validation query: [Query]
   - Expected result: [What indicates success]
   - Propagation time: [Duration]

**Monitoring During Mitigation:**
- [Metric 1]: [Where to watch]
- [Metric 2]: [Where to watch]

---

### Mitigation Path B: [Service Recovery]
**When to Use:** Service component failure

[Same structure as Mitigation Path A]

---

### Mitigation Path C: [Emergency Workaround]
**When to Use:** Cannot immediately fix root cause

**Workaround Description:**
[Describe temporary solution]

**Workaround Steps:**
[Detailed steps]

**Limitations:**
- [What this doesn't fix]
- [How long this will work]
- [When permanent fix needed]

---

## Phase 4: Validation and Monitoring (Post-Mitigation)

### Step 7: Validate Service Recovery
**Objective:** Confirm incident is fully resolved

**Validation Checklist:**
- [ ] Run end-to-end test cases
- [ ] Verify no new errors appearing
- [ ] Check affected customer tenants specifically
- [ ] Monitor for regression for [X hours]

**Validation Test Cases:**

**Test 1: [Core Functionality]**
- Action: [What to test]
- Expected: [Normal behavior]
- Result: [Pass/Fail]

**Test 2: [Edge Case]**
- Action: [What to test]
- Expected: [Normal behavior]
- Result: [Pass/Fail]

---

### Step 8: Continuous Monitoring
**Objective:** Ensure incident doesn't recur

**Monitoring Period:** [Duration, typically 24-72 hours]

**Metrics to Monitor:**
```kql
// Monitoring query
[Kusto query to track key metrics]
```

**Alert Thresholds:**
- [Metric 1]: Alert if > [value]
- [Metric 2]: Alert if > [value]

**Escalation Trigger:**
If [condition], immediately re-engage incident response team

---

## Phase 5: Communication and Closure

### Step 9: Customer Communication
**Objective:** Keep customers informed throughout incident

**Communication Frequency:**
- **During incident:** Every 2 hours or when status changes
- **Post-mitigation:** Initial recovery notice + 24-hour follow-up
- **Post-incident:** Final resolution notice with RCA

**Communication Templates:**
See Appendix B for:
- Initial notification
- Status update
- Resolution notification
- Post-incident summary

---

### Step 10: Post-Incident Activities
**Objective:** Learn from incident and prevent recurrence

**Required Actions:**
- [ ] Complete Post-Incident Review (PIR) within 5 business days
- [ ] Update ICM with final RCA
- [ ] Document lessons learned
- [ ] Create action items for prevention
- [ ] Update this TSG if gaps identified

**PIR Template:**
See Appendix C

**Action Item Tracking:**
- [ ] [Prevention action 1] - Owner: [Name] - Due: [Date]
- [ ] [Prevention action 2] - Owner: [Name] - Due: [Date]
- [ ] [Monitoring improvement] - Owner: [Name] - Due: [Date]

---

## Escalation Matrix

### When to Escalate Further

| Situation | Escalate To | Contact Method |
|-----------|-------------|----------------|
| Cannot identify root cause in 60 min | Product Engineering | [Contact] |
| Mitigation requires backend changes | Service Team | [Contact] |
| Data breach suspected | Security Team | [Contact] |
| Multiple services affected | Platform Team | [Contact] |
| Customer threatens legal action | Customer Success + Legal | [Contact] |

---

## Appendix A: Impact Assessment Template

```markdown
# Incident Impact Assessment

**Date/Time:** [Timestamp]
**Assessed By:** [Name/Alias]
**Incident ID:** [ICM number]

## Scope
- **Total Customers Affected:** [Number]
- **IC Customers:** [List TPIDs]
- **MCS Customers:** [List TPIDs]
- **Total Users Impacted:** [Estimate]

## Functional Impact
- **Service/Feature:** [What's broken]
- **Impact Description:** [What users experience]
- **Data at Risk:** [Yes/No - describe]
- **Workaround Available:** [Yes/No - describe]

## Business Impact
- **Revenue at Risk:** [Estimate if possible]
- **Compliance Risk:** [Yes/No - describe]
- **Reputation Risk:** [Low/Medium/High]
- **Customer Escalation Risk:** [Low/Medium/High]

## Technical Details
- **Start Time:** [When incident began]
- **Detection Time:** [When we detected it]
- **Detection Method:** [How we found it]
- **Affected Components:** [List]
- **Affected Regions:** [List]

## Initial Hypothesis
[What we think is causing this]

**Severity Determination:** Sev [1/2/3]
**Justification:** [Why this severity level]
```

---

## Appendix B: Communication Templates

### Template 1: Initial Incident Notification
```
Subject: [INCIDENT] Microsoft Purview [Feature] - [Brief Description]

Dear [Customer Name],

We are aware of an issue affecting [functionality] in your Microsoft Purview environment.

**Impact:** [What customers are experiencing]
**Affected Tenants:** [Your tenant ID(s) if specific]
**Start Time:** [Approximate time issue began]
**Current Status:** Investigation in progress

Our team is actively working to resolve this issue. We will provide updates every 2 hours or when significant progress is made.

Next update expected: [Time]

For urgent questions, please contact: [Contact info]

Incident Tracking: [ICM number]

Best regards,
[Your name]
Microsoft Support
```

### Template 2: Status Update
```
Subject: [UPDATE] Microsoft Purview [Feature] - [Brief Description]

Dear [Customer Name],

Status Update: [Timestamp]

**Root Cause Identified:** [Yes/No - brief description if yes]
**Mitigation in Progress:** [Description of actions being taken]
**Estimated Time to Resolution:** [Conservative estimate]

**Current Impact:** [Any changes to impact]

We continue to work on resolving this issue and will provide another update in 2 hours or when resolved.

For urgent questions, please contact: [Contact info]

Best regards,
[Your name]
Microsoft Support
```

### Template 3: Resolution Notification
```
Subject: [RESOLVED] Microsoft Purview [Feature] - [Brief Description]

Dear [Customer Name],

The issue affecting [functionality] has been resolved as of [Time].

**Resolution Summary:** [Brief description of what was done]
**Root Cause:** [High-level explanation]

**Actions Required from You:** [None / List any customer actions needed]

We will continue to monitor the service for the next 24 hours to ensure stability. A detailed Post-Incident Review will be provided within 5 business days.

If you experience any continued issues, please contact us immediately.

Thank you for your patience during this incident.

Best regards,
[Your name]
Microsoft Support
```

---

## Appendix C: Post-Incident Review (PIR) Template

```markdown
# Post-Incident Review

**Incident ID:** [ICM number]
**Date of Incident:** [Date]
**Date of PIR:** [Date]
**PIR Owner:** [Name/Alias]
**Attendees:** [List]

## Executive Summary
[2-3 paragraph summary of incident, impact, and resolution]

## Timeline of Events

| Time (UTC) | Event | Owner |
|------------|-------|-------|
| [Time] | [What happened] | [Who] |
| [Time] | [What happened] | [Who] |

## Impact Analysis
- **Duration:** [Start to resolution]
- **Customer Count:** [Number affected]
- **User Count:** [Estimated]
- **Revenue Impact:** [If applicable]
- **Data Loss:** [Yes/No - details]

## Root Cause Analysis
**Root Cause:** [Detailed technical explanation]

**Contributing Factors:**
1. [Factor 1]
2. [Factor 2]

**Why Did This Happen:**
[Deeper analysis - 5 Whys recommended]

## What Went Well
- [Positive aspect 1]
- [Positive aspect 2]

## What Could Be Improved
- [Improvement area 1]
- [Improvement area 2]

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Preventive action 1] | [Name] | [Date] | [Status] |
| [Detection improvement] | [Name] | [Date] | [Status] |
| [TSG update] | [Name] | [Date] | [Status] |

## Lessons Learned
1. [Lesson 1]
2. [Lesson 2]
3. [Lesson 3]

## Recommendations
- **Short-term:** [Immediate improvements]
- **Long-term:** [Strategic changes]

---

**PIR Status:** [Draft / Final]
**Reviewed By:** [Names of reviewers]
**Approval:** [Manager/Director approval]
```

---

## Change History

| Date | Version | Changed By | Changes |
|------|---------|------------|---------|
| [Date] | 1.0 | [Alias] | Initial creation |
| | | | |

---

## Feedback

**Was this incident response guide helpful?**
- Rating: ⭐⭐⭐⭐⭐
- What worked well during the incident:
- What was confusing or missing:
- Suggestions for improvement:

Submit feedback to: [Email/Teams Channel/Form Link]

---

**Keywords for Search:** [incident, outage, service_degradation, emergency]
