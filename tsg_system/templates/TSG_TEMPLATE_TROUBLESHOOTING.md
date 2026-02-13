# [TSG Title: Describe the Issue/Symptom]

**TSG ID:** TSG-[YYYYMMDD]-[Sequential Number]  
**Product Area:** [e.g., Microsoft Purview - DLP / eDiscovery / Audit / Retention]  
**Severity:** [Critical / High / Medium / Low]  
**Last Updated:** [Date]  
**Last Reviewed By:** [Name/Alias]  
**Version:** 1.0

---

## Quick Reference
**Estimated Resolution Time:** [e.g., 15 minutes - 2 hours]  
**Required Permissions:** [e.g., Compliance Administrator, Security Administrator, Kusto Access]  
**Tools Needed:** [e.g., Azure Portal, PowerShell, Kusto Explorer, ASC Portal]

**When to Use This TSG:**
- [Symptom/Error Message 1]
- [Symptom/Error Message 2]
- [Specific scenario or customer report]

---

## Problem Statement

### Symptom Description
[Detailed description of what the customer/engineer observes]
- What error messages appear (include exact text)
- What functionality is not working
- When did the issue start
- What triggers the issue

**Example:**
> Customer reports that DLP policies are not applying to emails sent from Outlook desktop client. Users see no warning messages when sending emails containing sensitive data, even though policies are configured and enabled in the Compliance portal.

### Customer Impact
- **Business Impact:** [e.g., Data loss risk, compliance violation, user productivity]
- **Affected Users:** [e.g., All users, specific group, single user]
- **Frequency:** [e.g., Intermittent, consistent, specific time periods]

### Known Affected Products/Versions
- [Product version or configuration]
- [Specific tenant configurations]
- [Prerequisites that must be met]

---

## Root Cause Analysis

### Common Causes
1. **[Most Common Cause]**
   - Technical explanation
   - Why this happens
   - How to identify if this is the cause

2. **[Second Most Common Cause]**
   - Technical explanation
   - Why this happens
   - How to identify if this is the cause

3. **[Additional Causes]**
   - Continue listing in order of likelihood

### Related Product Limitations
- [Any known product limitations relevant to this issue]
- [Links to official documentation]

---

## Diagnostic Steps

### Prerequisites Check
Before beginning diagnostics, verify:
- [ ] Confirm user has appropriate license (E5, E5 Compliance, etc.)
- [ ] Verify admin has required permissions
- [ ] Ensure product feature is enabled in tenant
- [ ] Check service health status: https://admin.microsoft.com/servicehealthDashboard

### Step-by-Step Diagnostics

#### Step 1: [First Diagnostic Action]
**Purpose:** [Why we're doing this step]

**Instructions:**
```
[Command, script, or UI navigation steps]
```

**Expected Output:**
```
[What you should see if things are normal]
```

**What to Look For:**
- ✅ **Normal:** [Description of normal state]
- ⚠️ **Issue Indicator:** [What indicates a problem]

---

#### Step 2: [Second Diagnostic Action]
**Purpose:** [Why we're doing this step]

**Instructions:**
```
[Command, script, or UI navigation steps]
```

**Expected Output:**
```
[What you should see if things are normal]
```

**What to Look For:**
- ✅ **Normal:** [Description of normal state]
- ⚠️ **Issue Indicator:** [What indicates a problem]

---

[Continue with additional diagnostic steps as needed]

---

## Resolution Steps

### Solution Path A: [Most Common Resolution]
**When to Use:** [Conditions that indicate this is the right solution]
**Estimated Time:** [Duration]

1. **[Action 1]**
   ```
   [Specific command, script, or UI steps]
   ```
   - **Why:** [Explanation of what this does]
   - **Expected Result:** [What should happen]

2. **[Action 2]**
   ```
   [Specific command, script, or UI steps]
   ```
   - **Why:** [Explanation of what this does]
   - **Expected Result:** [What should happen]

3. **[Validation Step]**
   - How to confirm the issue is resolved
   - What to test
   - Expected behavior after fix

**Rollback Plan:**
[How to undo these changes if needed]

---

### Solution Path B: [Alternative Resolution]
**When to Use:** [Conditions that indicate this is the right solution]
**Estimated Time:** [Duration]

[Same structure as Solution Path A]

---

### Solution Path C: [Complex/Escalation Required]
**When to Use:** [When simpler solutions don't work]

⚠️ **Warning:** This solution requires [specific permissions/risk/downtime]

[Same structure as above, with additional warnings/notes]

---

## Validation and Testing

### How to Verify Resolution
1. **[Test 1]:** [What to do and what result confirms fix]
2. **[Test 2]:** [What to do and what result confirms fix]
3. **[Test 3]:** [What to do and what result confirms fix]

### Expected Timeline for Changes
- [Configuration propagation time, if applicable]
- [Replication delay, if applicable]
- [When customer should see improvements]

**Note:** Some changes may take up to [X hours/days] to fully propagate.

---

## Prevention and Best Practices

### How to Avoid This Issue
1. [Preventive measure 1]
2. [Preventive measure 2]
3. [Preventive measure 3]

### Monitoring Recommendations
- [What to monitor to detect this issue early]
- [Alerts or queries to set up]
- [Recommended check frequency]

### Configuration Best Practices
- [Recommended settings]
- [Common misconfigurations to avoid]

---

## Escalation Criteria

### When to Escalate to Product Group
Escalate if:
- [ ] Issue persists after all resolution steps attempted
- [ ] Root cause appears to be service-side bug
- [ ] Data corruption or loss is observed
- [ ] Issue affects multiple customers or is widespread
- [ ] Issue requires backend configuration change

### When to Engage On-Call/ICM
Create ICM if:
- [ ] Severity 1 issue (widespread customer impact)
- [ ] Data breach or security incident suspected
- [ ] Service degradation affecting multiple tenants
- [ ] Customer is IC/MCS program with business-critical impact

### Escalation Information to Provide
When escalating, include:
- Tenant ID and TPID
- Case/ICM number
- All diagnostic outputs collected
- Steps already attempted
- Customer business impact statement
- Timeline of events

---

## Related Resources

### Internal Documentation
- [Link to related TSGs]
- [Link to product documentation]
- [Link to architecture diagrams]

### Kusto Queries
- [Link or embed relevant queries for diagnostics]

### Support Articles
- [Public documentation]
- [Known issues]
- [Feature announcements]

### Training Materials
- [Relevant training videos]
- [Walkthrough documentation]

---

## References and Source Cases

### Cases Used to Build This TSG
- **Case #1:** [Case Number] - [Brief description]
- **Case #2:** [Case Number] - [Brief description]
- **Case #3:** [Case Number] - [Brief description]

### Product Team Contacts
- **Feature Owner:** [Name/Alias]
- **PM:** [Name/Alias]
- **Engineering Contact:** [Name/Alias]

---

## Change History

| Date | Version | Changed By | Changes |
|------|---------|------------|---------|
| [Date] | 1.0 | [Alias] | Initial creation |
| | | | |

---

## Feedback

**Was this TSG helpful?** Please provide feedback:
- What worked well:
- What was confusing:
- Missing information:
- Suggestions for improvement:

Submit feedback to: [Email/Teams Channel/Form Link]

---

**Keywords for Search:** [keyword1, keyword2, error_code, product_feature]
