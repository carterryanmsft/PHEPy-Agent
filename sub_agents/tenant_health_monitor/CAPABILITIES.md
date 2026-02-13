# Tenant Health Monitor - Capabilities Matrix

**Agent:** Tenant Health Monitor  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 🎯 Core Capabilities

### 1. Per-Tenant Health Tracking

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Health Scorecard** | Generate comprehensive health score per tenant | Kusto, DFM, ICM | ✅ Ready |
| **Adoption Metrics** | Track feature adoption, user engagement, config completeness | Kusto telemetry | ✅ Ready |
| **Support Health** | Case volume, SLA compliance, escalation count | DFM, ICM | ✅ Ready |
| **Product Performance** | Error rates, timeouts, service availability | Kusto, Azure Monitor | ✅ Ready |
| **Trend Analysis** | Week-over-week, month-over-month progress | Historical Kusto data | ✅ Ready |

### 2. Cohort Analytics

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Cohort Rollup** | Aggregate metrics across MCS/IC cohorts | Grounding docs, Kusto | ✅ Ready |
| **Peer Comparison** | Compare tenant to cohort average | Kusto analytics | ✅ Ready |
| **Outlier Detection** | Flag tenants significantly above/below baseline | Statistical analysis | ✅ Ready |
| **Cohort Health Trends** | Track cohort progress over time | Historical data | ✅ Ready |
| **Success Milestone Tracking** | Monitor progress toward onboarding/adoption goals | Grounding docs KPIs | ✅ Ready |

### 3. Risk Detection & Alerting

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **SLA Risk Detection** | Flag tenants with SLA breach risk | DFM | ✅ Ready |
| **Escalation Spike** | Detect unusual increase in ICM incidents | ICM, Kusto | ✅ Ready |
| **Support Case Surge** | Alert on abnormal case volume | DFM | ✅ Ready |
| **Adoption Regression** | Detect declining feature usage | Kusto telemetry | ✅ Ready |
| **VIP Tenant Monitoring** | Proactive monitoring for high-value customers | Customer registry | ✅ Ready |

### 4. Actionable Recommendations

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Intervention Recommendations** | Suggest PM engagement, support boost, training | Multi-source analytics | ✅ Ready |
| **Feature Optimization** | Recommend configuration tuning based on usage | Kusto, best practices | ✅ Ready |
| **Success Path Guidance** | Provide roadmap to improve health score | Grounding docs | ✅ Ready |
| **Resource Allocation** | Suggest where to invest PM/support time | Cohort analytics | ✅ Ready |

---

## 📊 Health Metrics Tracked

### Adoption Metrics

| Metric | Description | Data Source | Update Frequency |
|--------|-------------|-------------|------------------|
| **Active Users** | Users engaging with Purview features | Kusto telemetry | Daily |
| **Feature Adoption Rate** | % of enabled features actively used | Kusto telemetry | Weekly |
| **Policy Coverage** | % of users/content covered by policies | Tenant APIs | Daily |
| **Label Coverage** | % of content with sensitivity labels | Content Explorer | Daily (24h lag) |
| **DLP Policy Count** | Active DLP policies per tenant | Tenant config | Real-time |
| **Retention Policy Count** | Active retention policies per tenant | Tenant config | Real-time |

### Support Health Metrics

| Metric | Description | Data Source | Update Frequency |
|--------|-------------|-------------|------------------|
| **Open Case Count** | Total open support cases | DFM | Real-time |
| **At-Risk Cases** | Cases with SLA breach risk (<4h) | DFM | Real-time |
| **Escalation Count** | Active ICM incidents | ICM | Real-time |
| **Case Resolution Time** | Average time to resolve (days) | DFM historical | Daily |
| **SLA Compliance %** | % of cases resolved within SLA | DFM historical | Daily |
| **Reopened Case Rate** | % of cases reopened after close | DFM historical | Weekly |

### Product Performance Metrics

| Metric | Description | Data Source | Update Frequency |
|--------|-------------|-------------|------------------|
| **Error Rate** | Service errors per 1000 operations | Kusto telemetry | Hourly |
| **Timeout Rate** | Operations timing out | Kusto telemetry | Hourly |
| **Search Performance** | Avg eDiscovery search duration | Kusto telemetry | Hourly |
| **Labeling Performance** | Avg time to apply label | Kusto telemetry | Hourly |
| **Policy Evaluation Latency** | DLP/retention policy eval time | Kusto telemetry | Hourly |
| **Service Availability** | Uptime % for tenant | Azure Monitor | Real-time |

### Engagement Metrics

| Metric | Description | Data Source | Update Frequency |
|--------|-------------|-------------|------------------|
| **Admin Activity** | Admin console logins and changes | Audit logs | Daily |
| **User Training Completion** | % of users who completed training | LMS integration | Weekly |
| **Feature Discovery Rate** | New features adopted over time | Kusto telemetry | Weekly |
| **Configuration Changes** | Policy/label updates per month | Audit logs | Daily |

---

## 📈 Health Score Calculation

### Overall Tenant Health Score (0-100)

**Formula:**
```
Health Score = (Adoption Score * 0.4) + (Support Score * 0.3) + (Performance Score * 0.2) + (Engagement Score * 0.1)
```

### Component Scores

#### Adoption Score (0-100)
- Active users vs licensed users (30%)
- Feature adoption rate (30%)
- Policy coverage (20%)
- Label coverage (20%)

#### Support Score (0-100)
- SLA compliance rate (40%)
- Case resolution time (30%)
- Escalation count (20%)
- Reopened case rate (10%)

#### Performance Score (0-100)
- Error rate (inverse) (40%)
- Timeout rate (inverse) (30%)
- Operation latency (inverse) (20%)
- Service availability (10%)

#### Engagement Score (0-100)
- Admin activity (40%)
- Configuration changes (30%)
- Training completion (20%)
- Feature discovery (10%)

### Health Score Thresholds

| Score Range | Health Status | Action Required |
|-------------|---------------|-----------------|
| 90-100 | 🟢 Excellent | Monitor, share success |
| 75-89 | 🟢 Good | Continue current engagement |
| 60-74 | 🟡 Fair | Increase check-ins, identify gaps |
| 45-59 | 🟠 At Risk | Active intervention required |
| 0-44 | 🔴 Critical | Immediate escalation, PM engagement |

---

## 🎭 Cohort Analysis Patterns

### MCS/IC Cohort Types

| Cohort | Description | Typical Size | Tracking Frequency |
|--------|-------------|--------------|-------------------|
| **MCS Alpha** | Early adopters, pilot tenants | 10-20 tenants | Weekly |
| **MCS Beta** | Second wave, broader rollout | 50-100 tenants | Bi-weekly |
| **MCS Production** | Full deployment cohort | 200+ tenants | Monthly |
| **IC Onboarding** | Implementation consultant customers | 20-50 tenants | Weekly |
| **IC Exit** | Post-implementation monitoring | 30-60 tenants | Monthly |

### Cohort Health Metrics

For each cohort, track:
- **Average Health Score** - Mean score across all tenants
- **Health Score Distribution** - Histogram of scores
- **Tenant Count by Status** - Count in each health tier
- **Outlier Tenants** - Tenants >2 std dev from mean
- **Trend Direction** - Improving, declining, stable

---

## 🚨 Alert Conditions

### Critical Alerts (Immediate Escalation)

| Alert | Condition | Escalation Path |
|-------|-----------|-----------------|
| **VIP Tenant at Risk** | VIP health score < 60 OR active P0/P1 ICM | Escalation Manager |
| **SLA Breach Imminent** | 3+ cases with <4h to SLA breach | Support Case Manager |
| **Service Outage** | Availability < 95% for >1 hour | Escalation Manager → ICM |
| **Adoption Collapse** | Active users drop >50% week-over-week | PHE PM, Tenant Owner |

### Warning Alerts (PM Attention Required)

| Alert | Condition | Action |
|-------|-----------|--------|
| **Health Score Declining** | Score drops >10 points in 2 weeks | PM check-in call |
| **Support Case Spike** | Case volume 2x above baseline | Review with Support Case Manager |
| **Feature Churn** | Enabled feature becomes unused | Investigate root cause |
| **Configuration Drift** | No admin changes in 30 days | Engagement check |

### Info Alerts (Monitor)

| Alert | Condition | Action |
|-------|-----------|--------|
| **New Feature Adopted** | Tenant enables new feature | Track adoption progress |
| **Peer Outlier (Positive)** | Score >2 std dev above cohort avg | Share success story |
| **Milestone Achieved** | Reaches onboarding KPI | Celebrate, document |

---

## 🔍 Diagnostic Workflows

### Workflow 1: Investigate Declining Health Score

```
1. Compare current vs historical scores:
   - Which component declined? (Adoption, Support, Performance, Engagement)
   
2. Drill into declining component:
   - If Adoption: Which features saw reduced usage?
   - If Support: What types of cases increased?
   - If Performance: Which operations are slower?
   - If Engagement: What changed in admin activity?

3. Correlate with events:
   - Recent deployments or config changes?
   - New cases or incidents filed?
   - Changes in user count or licenses?

4. Recommend interventions:
   - PM engagement for adoption issues
   - Support boost for case surge
   - PG escalation for performance issues
   - Training or communication for engagement gaps
```

### Workflow 2: Cohort Health Assessment

```
1. Calculate cohort health stats:
   - Average health score
   - Score distribution (quartiles)
   - Outlier count (both directions)

2. Identify patterns:
   - Common issues across low-scoring tenants
   - Success factors from high-scoring tenants
   - Cohort-wide trends (improving/declining)

3. Compare to baseline:
   - Expected score range for cohort stage
   - Variance from previous cohorts
   - Progress toward success criteria

4. Generate recommendations:
   - Which tenants need immediate attention?
   - What interventions to scale across cohort?
   - Where to invest PM/support resources?
```

### Workflow 3: VIP Tenant Monitoring

```
1. Identify VIP tenants:
   - From customer registry
   - Revenue tier, strategic importance
   - Special SLA or support requirements

2. Enhanced monitoring:
   - Daily health score tracking
   - Real-time alert on any issues
   - Proactive outreach before problems escalate

3. Escalation triggers:
   - Any P0/P1 ICM → Immediate escalation
   - Health score < 75 → PM check-in
   - SLA risk → Escalation Manager engagement

4. Success tracking:
   - Document what works for VIP tenants
   - Apply learnings to broader customer base
```

---

## 📊 Reporting Cadence

### Daily Reports
- VIP tenant health status
- Critical alerts (SLA risk, service issues)
- Outlier tenants (positive and negative)

### Weekly Reports
- Cohort health summary (MCS Alpha, IC Onboarding, etc.)
- Health score trends
- Top 10 at-risk tenants
- Success stories (score improvements)

### Monthly Reports
- Executive summary: overall program health
- Cohort comparison analysis
- Success milestone achievement
- Resource allocation recommendations

---

## 🔗 Integration with Other Agents

### Support Case Manager
- Provides case volume and SLA data for support health metrics
- Alerts on case surges or SLA risks

### Escalation Manager
- Provides ICM incident count and severity
- Receives alerts for VIP tenant issues

### Kusto Expert (Jacques)
- Executes telemetry queries for adoption and performance metrics
- Provides historical trend data

### Purview Product Expert
- Helps interpret performance issues (product bug vs config)
- Provides context on feature usage patterns

### Program Onboarding Manager
- Tracks onboarding milestone progress
- Identifies tenants falling behind on adoption

---

## 🚫 Out of Scope

This agent **does NOT**:
- Modify tenant configurations
- Make commitments about service improvements
- Access customer PII without authorization
- Diagnose root causes without data
- Recommend actions that conflict with customer needs

---

## 📏 Success Metrics

- **Alert Precision:** >90% of escalated alerts require action
- **Early Detection:** Identify declining health >1 week before crisis
- **Cohort Coverage:** 100% of tracked cohorts have weekly health reports
- **PM Satisfaction:** >85% of PMs find reports actionable

---

## 🆘 Escalation Paths

**When to Escalate:**
- VIP tenant health score < 60
- Any tenant with SLA breach imminent
- Cohort-wide health decline (>20% of tenants at risk)
- Service performance degradation (not tenant-specific)

**Escalation Targets:**
- **Support Issues** → Support Case Manager
- **ICM Incidents** → Escalation Manager
- **Product Issues** → Purview Product Expert
- **Onboarding Gaps** → Program Onboarding Manager
