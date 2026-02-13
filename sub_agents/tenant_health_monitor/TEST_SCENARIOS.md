# Tenant Health Monitor - Test Scenarios

**Agent:** Tenant Health Monitor  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 🧪 Test Scenario Categories

1. **Per-Tenant Health Queries**
2. **Cohort Analytics**
3. **Risk Detection & Alerts**
4. **Trend Analysis**
5. **Recommendation Generation**

---

## 1. Per-Tenant Health Queries

### Test 1.1: Single Tenant Health Score
**Prompt:**  
"What's the health score for tenant c990bb7a-51f4-439b-bd36-9c07fb1041c0?"

**Expected Response:**
- Overall health score (0-100)
- Component breakdown (Adoption, Support, Performance, Engagement)
- Health status (Excellent/Good/Fair/At Risk/Critical)
- Key metrics driving the score
- Trend (improving/declining/stable)

**Success Criteria:**
- ✅ Provides numeric health score
- ✅ Breaks down by component
- ✅ Cites data sources (Kusto, DFM, etc.)
- ✅ Shows trend direction

---

### Test 1.2: Tenant Health Over Time
**Prompt:**  
"Show me health score trend for Ford Motor over the last 90 days"

**Expected Response:**
- Query Kusto for historical data
- Generate week-by-week health scores
- Identify inflection points (sudden changes)
- Correlate with events (deployments, cases, config changes)
- Visual representation or data table

**Success Criteria:**
- ✅ Retrieves historical data
- ✅ Shows trend direction
- ✅ Identifies significant changes
- ✅ Correlates with events when possible

---

### Test 1.3: Multi-Metric Drill-Down
**Prompt:**  
"Why did tenant X's health score drop from 85 to 62 this week?"

**Expected Response:**
1. Compare current vs previous component scores
2. Identify which component(s) declined most
3. Drill into that component's metrics
4. Identify root cause (case surge, performance issue, adoption drop)
5. Recommend corrective action

**Success Criteria:**
- ✅ Compares historical to current
- ✅ Identifies declining component
- ✅ Provides specific metric changes
- ✅ Suggests actionable next steps

---

## 2. Cohort Analytics

### Test 2.1: Cohort Health Summary
**Prompt:**  
"Give me MCS Alpha cohort health summary"

**Expected Response:**
- List all tenants in MCS Alpha cohort
- Average health score for cohort
- Score distribution (min, max, median, quartiles)
- Count by health status tier
- Top 3 at-risk tenants
- Top 3 high-performing tenants

**Success Criteria:**
- ✅ Identifies cohort members from grounding docs
- ✅ Calculates aggregate statistics
- ✅ Highlights outliers (both directions)
- ✅ Provides actionable summary

---

### Test 2.2: Peer Comparison
**Prompt:**  
"How does Contoso compare to other tenants in the IC Onboarding cohort?"

**Expected Response:**
- Contoso's health score
- Cohort average health score
- Percentile ranking
- Key differences in metrics
- Areas where Contoso excels or lags

**Success Criteria:**
- ✅ Compares tenant to cohort average
- ✅ Provides relative ranking
- ✅ Identifies specific metric differences
- ✅ Suggests areas for improvement

---

### Test 2.3: Cohort Trend Analysis
**Prompt:**  
"Is MCS Beta cohort improving or declining over the last month?"

**Expected Response:**
- Week-by-week cohort average health score
- Trend direction (improving/declining/stable)
- Number of tenants improving vs declining
- Common patterns across improving tenants
- Recommended interventions for declining tenants

**Success Criteria:**
- ✅ Shows historical cohort data
- ✅ Determines trend direction
- ✅ Identifies patterns
- ✅ Provides recommendations

---

## 3. Risk Detection & Alerts

### Test 3.1: VIP Tenant Alert
**Prompt:**  
"Are any VIP tenants at risk this week?"

**Expected Response:**
- Query customer registry for VIP tenants
- Check health score for each VIP
- Flag any with score < 75
- List active P0/P1 ICMs for VIPs
- Recommend immediate actions

**Success Criteria:**
- ✅ Identifies VIP tenants from registry
- ✅ Checks health status
- ✅ Flags at-risk VIPs
- ✅ Escalates appropriately

---

### Test 3.2: SLA Breach Risk Detection
**Prompt:**  
"Which tenants have cases at SLA risk today?"

**Expected Response:**
- Query DFM for cases with <4h to SLA breach
- Group by tenant
- List tenant name, case count, most urgent case
- Calculate aggregate SLA risk score per tenant
- Recommend escalation for critical cases

**Success Criteria:**
- ✅ Queries live DFM data
- ✅ Identifies at-risk cases
- ✅ Groups by tenant
- ✅ Prioritizes by urgency

---

### Test 3.3: Adoption Regression Detection
**Prompt:**  
"Have any tenants seen a significant drop in active users this week?"

**Expected Response:**
- Query Kusto for active user counts (current vs previous week)
- Calculate week-over-week change percentage
- Flag tenants with >30% decline
- Investigate potential causes (holidays, outages, config changes)
- Recommend follow-up actions

**Success Criteria:**
- ✅ Compares current to historical
- ✅ Calculates percentage change
- ✅ Identifies significant declines
- ✅ Suggests potential causes

---

## 4. Trend Analysis

### Test 4.1: Feature Adoption Trends
**Prompt:**  
"Show me DLP policy adoption trends across all MCS tenants over the last quarter"

**Expected Response:**
- Query Kusto for DLP policy counts by tenant over time
- Calculate adoption rate (% of tenants with active DLP)
- Show month-over-month growth
- Identify tenants that adopted DLP recently
- Identify tenants still without DLP

**Success Criteria:**
- ✅ Retrieves historical adoption data
- ✅ Calculates growth rate
- ✅ Identifies adoption patterns
- ✅ Highlights gaps

---

### Test 4.2: Support Health Trends
**Prompt:**  
"Has case volume been increasing or decreasing for IC cohort this month?"

**Expected Response:**
- Query DFM for case counts by week
- Compare to previous month
- Calculate percentage change
- Break down by case priority/severity
- Identify if increase is due to specific issue type

**Success Criteria:**
- ✅ Shows case volume trend
- ✅ Compares to baseline
- ✅ Breaks down by category
- ✅ Identifies potential causes

---

### Test 4.3: Performance Degradation Tracking
**Prompt:**  
"Are any tenants experiencing performance degradation in eDiscovery searches?"

**Expected Response:**
- Query Kusto for eDiscovery search latency by tenant
- Compare current to 30-day average
- Flag tenants with >50% increase in latency
- Cross-reference with known product issues
- Recommend escalation if widespread

**Success Criteria:**
- ✅ Retrieves performance metrics
- ✅ Compares to baseline
- ✅ Identifies degradation
- ✅ Correlates with known issues

---

## 5. Recommendation Generation

### Test 5.1: Intervention Recommendation
**Prompt:**  
"Which tenants in MCS Production cohort need PM attention this week?"

**Expected Response:**
- Calculate health scores for all MCS Production tenants
- Identify tenants with score < 70
- Rank by urgency (score + trend direction)
- Recommend specific interventions per tenant
- Provide PM engagement priorities (top 5)

**Success Criteria:**
- ✅ Identifies at-risk tenants
- ✅ Prioritizes by urgency
- ✅ Provides specific recommendations
- ✅ Limits to actionable list

---

### Test 5.2: Resource Allocation Guidance
**Prompt:**  
"Where should we focus support resources this week?"

**Expected Response:**
- Analyze support metrics across all tenants
- Identify hotspots (high case volume, SLA risk)
- Compare current to typical baseline
- Recommend resource allocation (tenants, product areas)
- Estimate impact of intervention

**Success Criteria:**
- ✅ Analyzes support load distribution
- ✅ Identifies resource needs
- ✅ Prioritizes interventions
- ✅ Provides actionable plan

---

### Test 5.3: Success Path Guidance
**Prompt:**  
"What should Fabrikam do to improve their health score from 65 to 80?"

**Expected Response:**
- Analyze Fabrikam's current component scores
- Identify which components are lowest
- Provide specific improvement actions:
  - Increase feature adoption
  - Resolve open support cases
  - Improve configuration coverage
- Estimate timeline to reach target score
- Provide milestone checkpoints

**Success Criteria:**
- ✅ Identifies improvement opportunities
- ✅ Provides specific actionable steps
- ✅ Estimates timeline
- ✅ Sets measurable milestones

---

## 6. Edge Cases & Error Handling

### Test 6.1: Insufficient Data
**Prompt:**  
"What's the health score for tenant that was just onboarded yesterday?"

**Expected Response:**
- "Insufficient historical data for health score calculation"
- "Minimum 7 days of data required for accurate scoring"
- "Current metrics available: [list what's available]"
- "Check back in [X] days for full health score"

**Success Criteria:**
- ✅ Does not fabricate scores
- ✅ Clearly states data limitation
- ✅ Provides partial info if available
- ✅ Sets expectations on timeline

---

### Test 6.2: Data Freshness Issue
**Prompt:**  
"Show me real-time health for tenant X"

**Expected Response:**
- "Most recent data is from [timestamp]"
- "Some metrics have 24-48 hour lag (Content Explorer)"
- Provide health score with data freshness disclaimer
- Note which components may be stale

**Success Criteria:**
- ✅ Discloses data age
- ✅ Identifies stale components
- ✅ Provides score with caveats
- ✅ Does not imply real-time when not

---

### Test 6.3: Tenant Not Found
**Prompt:**  
"What's the health score for tenant that doesn't exist in the registry?"

**Expected Response:**
- "Tenant [ID] not found in customer registry"
- "Verify tenant ID is correct"
- "Check if tenant is part of tracked cohorts"
- Offer to search by customer name if TenantId lookup failed

**Success Criteria:**
- ✅ Clearly states tenant not found
- ✅ Suggests verification steps
- ✅ Offers alternatives
- ✅ Does not guess or speculate

---

## 🎯 Performance Benchmarks

| Metric | Target | Measurement |
|--------|--------|-------------|
| Health Score Calculation Time | < 10 seconds | Single tenant health score |
| Cohort Analysis Time | < 30 seconds | Full cohort (up to 100 tenants) |
| Alert Detection Latency | < 1 minute | Time from metric change to alert |
| Trend Analysis Query | < 20 seconds | 90-day trend for single tenant |
| Recommendation Generation | < 15 seconds | Actionable recommendations per tenant |

---

## 🔄 Test Execution Process

1. **Setup test environment** with sample tenant data
2. **Run all test scenarios**
3. **Validate against success criteria**
4. **Document failures** with specific issues
5. **Verify data source integration** (Kusto, DFM, ICM)
6. **Test alert triggering** with synthetic data
7. **Validate recommendation quality** with PM review

---

## 📝 Test Log Template

```markdown
### Test Run: [Date]
**Tester:** [Name]
**Agent Version:** [Version]
**Data Source:** [Live/Test]

| Test # | Scenario | Pass/Fail | Response Time | Notes |
|--------|----------|-----------|---------------|-------|
| 1.1 | Single Tenant Health | ✅ Pass | 8s | Accurate score |
| 1.2 | Health Over Time | ❌ Fail | 25s | Missing correlation with events |
| ... | ... | ... | ... | ... |

**Overall Score:** 12/15 (80%)
**Action Items:**
- Improve event correlation logic
- Add data freshness indicators
- Optimize Kusto query performance
```
