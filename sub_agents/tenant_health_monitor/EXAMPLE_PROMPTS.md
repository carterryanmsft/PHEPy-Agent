# Tenant Health Monitor - Example Prompts

**Agent:** Tenant Health Monitor  
**Last Updated:** February 4, 2026

---

## 🎯 Single Tenant Health Queries

### Get Overall Health Score
```
What's the health score for tenant c990bb7a-51f4-439b-bd36-9c07fb1041c0?
```

```
Show me Ford Motor's current health status
```

```
How healthy is [customer name] right now?
```

### Component Breakdown
```
Break down the health score for [tenant/customer] by component
```

```
What's driving the low health score for [customer]?
```

```
Show me adoption, support, performance, and engagement scores for [tenant]
```

### Historical Trends
```
How has [customer]'s health score changed over the last 90 days?
```

```
Show me health score trend for [tenant] since onboarding
```

```
When did [customer]'s health score start declining?
```

---

## 📊 Cohort Analytics

### Cohort Summary
```
Give me MCS Alpha cohort health summary
```

```
How is the IC Onboarding cohort doing this week?
```

```
Show me health distribution for MCS Production cohort
```

### Peer Comparison
```
How does Contoso compare to other tenants in their cohort?
```

```
Is [customer] above or below cohort average?
```

```
Show me where [tenant] ranks in their cohort
```

### Cohort Trends
```
Is MCS Beta cohort improving or declining this month?
```

```
Which cohorts are performing best right now?
```

```
Show me month-over-month cohort health trends
```

---

## 🚨 Risk Detection & Alerts

### At-Risk Tenants
```
Which tenants are at risk this week?
```

```
Show me all tenants with health score < 60
```

```
Are any VIP customers at risk right now?
```

### SLA Risk
```
Which tenants have cases at SLA breach risk today?
```

```
Show me tenants with multiple at-risk support cases
```

```
Are we going to miss any SLAs this week?
```

### Anomaly Detection
```
Have any tenants seen a significant drop in active users this week?
```

```
Which tenants have unusual case volume spikes?
```

```
Are any tenants experiencing performance degradation?
```

---

## 📈 Adoption & Usage Analysis

### Feature Adoption
```
Show me DLP adoption across all MCS tenants
```

```
Which tenants haven't adopted [feature X] yet?
```

```
What's the average feature adoption rate for IC cohort?
```

### Usage Trends
```
Is [customer] using Purview more or less than last month?
```

```
Show me active user trends across all monitored tenants
```

```
Which features are most/least adopted across cohorts?
```

---

## 💡 Recommendations & Action Items

### Intervention Needs
```
Which tenants need PM attention this week?
```

```
Where should we focus support resources?
```

```
What tenants should we prioritize for engagement?
```

### Improvement Guidance
```
What should [customer] do to improve their health score?
```

```
How can we get [tenant] from 65 to 80 health score?
```

```
What's blocking [customer] from better adoption?
```

### Success Planning
```
Which tenants are on track to meet their success milestones?
```

```
What cohorts need course correction?
```

```
Show me progress toward onboarding goals for [cohort]
```

---

## 🔄 Comparative Analysis

### Cross-Cohort Comparison
```
Compare MCS Alpha to MCS Beta cohort health
```

```
Which cohort has the best support metrics?
```

```
Show me adoption rates across all cohorts
```

### Tenant Comparison
```
Compare health scores for [customer A] vs [customer B]
```

```
Which tenants in [cohort] are performing best?
```

```
Show me top 5 and bottom 5 tenants by health score
```

---

## 📅 Time-Based Queries

### This Week/Month
```
What changed in tenant health this week?
```

```
Show me new at-risk tenants this month
```

```
Which tenants improved their score this week?
```

### Historical Analysis
```
How has overall cohort health evolved over the last quarter?
```

```
Show me health score progression since onboarding for [customer]
```

```
When did [tenant] reach their peak health score?
```

---

## 🎯 Specific Metric Queries

### Support Metrics
```
Which tenants have the worst SLA compliance?
```

```
Show me case volume trends for [customer]
```

```
Are escalations increasing or decreasing for [cohort]?
```

### Performance Metrics
```
Which tenants are experiencing high error rates?
```

```
Show me search performance for [tenant]
```

```
Are any tenants hitting performance limits?
```

### Engagement Metrics
```
Which tenants have low admin activity?
```

```
Show me configuration change frequency for [customer]
```

```
Are admins actively managing their tenants?
```

---

## 🔔 Alert & Notification Queries

### Current Alerts
```
What alerts are active right now?
```

```
Show me all critical alerts for VIP tenants
```

```
Are there any urgent interventions needed today?
```

### Alert History
```
What alerts triggered for [tenant] in the last 30 days?
```

```
Show me alert frequency by type
```

```
Which tenants have the most alerts?
```

---

## 🎭 Complex Multi-Agent Scenarios

### Combined Health + Support Analysis
```
Show me tenants with declining health AND increasing case volume
```
*Routes to: Tenant Health Monitor → Support Case Manager*

---

```
For all at-risk tenants, what are their open support cases?
```
*Routes to: Tenant Health Monitor → Support Case Manager*

---

### Health + Product Issues
```
Are any tenants with low health scores experiencing known product issues?
```
*Routes to: Tenant Health Monitor → Support Case Manager → Purview Product Expert*

---

### Cohort Health + Escalations
```
Does MCS Alpha cohort have any active ICM incidents affecting health?
```
*Routes to: Tenant Health Monitor → Escalation Manager*

---

### Health + Telemetry Deep Dive
```
Why is [customer]'s performance score low? Show me the telemetry.
```
*Routes to: Tenant Health Monitor → Kusto Expert (Jacques)*

---

## 📊 Executive Reporting Queries

### High-Level Summary
```
Give me executive summary of all tenant health this month
```

```
How is the overall PHE program performing?
```

```
Show me health metrics for board presentation
```

### Success Metrics
```
How many tenants reached their success milestones this quarter?
```

```
What's the average time to reach 80+ health score?
```

```
Show me ROI indicators for MCS program
```

---

## 💡 Pro Tips

### Be Specific with Time Ranges
❌ "Show me trends"  
✅ "Show me trends over the last 90 days"

### Use Customer Names or TenantIds
❌ "That tenant"  
✅ "Contoso" or "tenant c990bb7a-51f4-439b-bd36-9c07fb1041c0"

### Specify Cohorts When Relevant
❌ "Show me all tenants"  
✅ "Show me all MCS Alpha tenants"

### Ask for Actionable Insights
❌ "What's the score?"  
✅ "What's the score and what should we do about it?"

---

## 🔗 Related Agents

- **Support Case Manager** - Query support cases affecting health
- **Escalation Manager** - Check ICM incidents
- **Kusto Expert (Jacques)** - Deep dive into telemetry
- **Purview Product Expert** - Understand product-level issues
- **Program Onboarding Manager** - Track onboarding progress

---

## 🆘 Need Help?

### Not Sure About Health Score?
```
Explain how tenant health scores are calculated
```

### Want to Understand a Metric?
```
What does "adoption score" mean?
```

### Need to Set Up Monitoring?
```
What data do you need to calculate health scores?
```

---

## 📚 Common Workflows

### Weekly Health Check
1. "Show me all at-risk tenants this week"
2. "For each at-risk tenant, what are the open support cases?"
3. "Which at-risk tenants need PM engagement?"

### Monthly Executive Review
1. "Give me cohort health summary for the last month"
2. "Show me top 5 success stories and top 5 concerns"
3. "What resource allocation changes do you recommend?"

### VIP Customer Monitoring
1. "Are any VIP tenants at risk?"
2. "Show me health trends for all VIP customers"
3. "What proactive actions should we take for VIPs?"
