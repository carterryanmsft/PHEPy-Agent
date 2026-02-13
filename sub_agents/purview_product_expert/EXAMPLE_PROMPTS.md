# Purview Product Expert - Example Prompts

**Agent:** Purview Product Expert  
**Last Updated:** February 4, 2026

---

## 🎯 How to Use This Guide

Copy and paste these prompts to interact with the Purview Product Expert agent. Modify the bracketed placeholders with your specific details.

---

## 1️⃣ Product Knowledge Questions

### Service Architecture
```
How does [sensitivity labeling / DLP / retention] work across [SharePoint / Exchange / Teams]?
```

```
Explain the relationship between [sensitivity labels] and [encryption / DLP policies / retention policies].
```

```
What happens to a [sensitivity label / retention policy] when a file is [moved / copied / shared externally]?
```

### Feature Capabilities
```
What can I do with [Insider Risk Management / Communication Compliance / eDiscovery]?
```

```
What's the difference between [retention policies and retention labels]?
```

```
How does [auto-labeling] work and what are the prerequisites?
```

### Licensing
```
What Purview features are included in [E3 / E5 / A5]?
```

```
Do I need an add-on license for [Advanced eDiscovery / Insider Risk / Communication Compliance]?
```

```
What's the upgrade path from [E3 to E5]?
```

---

## 2️⃣ Troubleshooting & Diagnostics

### Configuration Issues
```
My [DLP policy / retention policy / sensitivity label] is not working. What should I check?
```

```
Users are not seeing [sensitivity labels] in [Outlook / Word / Excel]. How do I diagnose this?
```

```
[Auto-labeling] is not applying to [emails / SharePoint documents]. Why?
```

```
I configured a [DLP policy] but it's not generating alerts. What's wrong?
```

### Performance Issues
```
[eDiscovery search / content export / policy application] is taking too long. Is this normal?
```

```
What are the scale limits for [eDiscovery / labels / policies / searches]?
```

```
How can I optimize performance for [large mailbox search / bulk labeling / policy evaluation]?
```

### Error Messages
```
What does error code "[SensitivityLabelNotFound / DLPRuleEvaluationFailed / ExportTimeout]" mean?
```

```
Users are getting "[cannot open this document / access denied / encryption error]". What's the cause?
```

```
I'm seeing "[throttling / timeout / service unavailable]" errors. How do I resolve this?
```

---

## 3️⃣ Feature Availability & Limitations

### Regional & Cloud Support
```
Is [feature X] available in [GCC / GCC High / DoD / Azure Germany / Azure China]?
```

```
What Purview features have parity between [Commercial and Government clouds]?
```

```
When will [feature X] be available in [region/cloud Y]?
```

### Feature Maturity
```
Is [Endpoint DLP / Insider Risk / Communication Compliance] ready for production at scale?
```

```
What are the known limitations of [feature X]?
```

```
Should I deploy [feature X] to [10,000 users] or start with a pilot?
```

### Scale & Limits
```
How many [labels / policies / rules] can I create in a tenant?
```

```
What's the maximum [mailbox size / item count / export size] for eDiscovery?
```

```
Can I apply [feature X] to [1 million items / 50,000 users / 100 TB of data]?
```

---

## 4️⃣ Known Issues & Bugs

### Check Known Issues
```
Is there a known issue with [sensitivity labels in Outlook Mac / DLP false positives / eDiscovery timeouts]?
```

```
Are other customers experiencing [symptom X]? Is this a known bug?
```

```
What's the ADO bug number for [issue X] and when will it be fixed?
```

### Workarounds
```
What's the workaround for [known issue X]?
```

```
Is there a temporary fix for [bug Y] while waiting for the product fix?
```

```
How can I mitigate [performance degradation / false positives / service interruption]?
```

---

## 5️⃣ Best Practices & Guidance

### Policy Design
```
What's the best way to structure [DLP policies / retention policies / label taxonomy]?
```

```
How do I reduce [false positives] in my [DLP policy]?
```

```
What's the recommended approach for [multi-stage retention / sensitivity label inheritance]?
```

### Feature Adoption
```
What's the recommended rollout strategy for [Endpoint DLP / Insider Risk / auto-labeling]?
```

```
How should I phase deployment of [feature X] to [enterprise organization]?
```

```
What success metrics should I track for [DLP / labeling / retention] adoption?
```

### Migration
```
How do I migrate from [AIP to unified labeling / legacy DLP to modern DLP]?
```

```
What's the process for [cross-tenant Purview migration]?
```

```
Can I migrate [labels / policies / rules] from [old system to Purview]?
```

---

## 6️⃣ Integration & Interoperability

### Office Integration
```
How does [sensitivity labeling / DLP] integrate with [Word / Excel / Outlook / Teams]?
```

```
What Purview features work in [Office on the web / mobile apps / desktop apps]?
```

```
How do I enable [labeling / DLP] in [Office application X]?
```

### Third-Party Integration
```
Can I integrate Purview with [Google Workspace / Box / Dropbox / Salesforce]?
```

```
Does Purview have APIs for [custom labeling / policy management / reporting]?
```

```
How do I build a [custom connector / integration] with Purview?
```

---

## 7️⃣ Multi-Case Pattern Detection

### Systemic Issue Detection
```
I'm seeing [N] support cases about [issue X] since [date]. Is this a widespread problem?
```

```
Are there multiple customers reporting [symptom Y] after [recent deployment / date]?
```

```
Should I escalate [issue X] as a potential regression or systemic issue?
```

### Root Cause Analysis
```
What's the common root cause for [multiple cases with symptom X]?
```

```
Is [issue Y] related to [recent service change / deployment / feature rollout]?
```

```
Are [case A, case B, case C] all caused by the same underlying bug?
```

---

## 8️⃣ Customer-Specific Questions

### Tenant Configuration
```
For tenant [TenantId], what [labels / policies / features] are currently configured?
```

```
What's the [labeling coverage / DLP compliance / retention status] for [customer X]?
```

```
Does [tenant Y] have the required [licenses / permissions / configuration] for [feature Z]?
```

---

## 9️⃣ Escalation & Follow-Up

### When to Escalate
```
Should I escalate [issue X] to the product group?
```

```
Is [symptom Y] something you can help with or should I file an ICM?
```

```
Who's the right contact for [product question / bug / feature request]?
```

### Get Escalation Info
```
What information do I need to provide when escalating [issue X]?
```

```
What diagnostic data should I collect for [performance issue / configuration problem]?
```

```
What's the escalation path for [urgent issue / VIP customer problem]?
```

---

## 🎭 Complex Multi-Agent Scenarios

### Combined Queries (Orchestrator Routes to Multiple Agents)

```
Show me all high-priority DLP cases for [customer X] in the last 30 days, check if there are related ICM incidents, and determine if this is a known product issue.
```
*Routes to: Support Case Manager → Escalation Manager → Purview Product Expert*

---

```
Are there any at-risk eDiscovery cases this week? Check if performance degradation is a known issue and recommend next steps.
```
*Routes to: Support Case Manager → Purview Product Expert → Kusto Expert*

---

```
Find all ADO bugs related to [sensitivity labeling in Outlook] and determine if any are causing customer cases.
```
*Routes to: Work Item Manager → Purview Product Expert → Support Case Manager*

---

```
What's the adoption rate for [Endpoint DLP] across MCS customers? Are there any common issues or blockers?
```
*Routes to: Tenant Health Monitor → Purview Product Expert → Support Case Manager*

---

## 💡 Pro Tips

### Be Specific
❌ "DLP not working"  
✅ "DLP policy not generating alerts for credit card numbers in Exchange Online emails"

### Provide Context
❌ "How do I fix this?"  
✅ "Sensitivity labels not appearing in Outlook Mac version 16.55 for 50 users in GCC High tenant"

### Reference IDs When Available
❌ "That bug we talked about"  
✅ "ADO bug #12345678 about auto-labeling in SharePoint"

### Ask Follow-Up Questions
```
You mentioned there's a workaround for [issue X]. Can you walk me through the steps?
```

```
The documentation says [Y]. Can you explain what that means in practice?
```

---

## 📚 Related Agents

- **Support Case Manager** - Query and track DFM support cases
- **Escalation Manager** - ICM incident tracking
- **Work Item Manager** - ADO bug/DCR lookup
- **Kusto Expert (Jacques)** - Query telemetry and diagnostics
- **Tenant Health Monitor** - Customer health metrics

---

## 🆘 Need Help?

If you're not sure how to phrase your question:
1. Start with the problem or symptom
2. Include relevant context (tenant, feature, users affected)
3. Ask what you want to know or what action to take

The agent will ask clarifying questions if needed!
