# Support Health Index v2 (SHI v2) – Reference Guide

**Version:** 2.0  
**Last Updated:** February 4, 2026  
**Presented by:** James Verdejo Jr  
**Status:** In Production (Running in Parallel with SHI v1)

---

## Executive Summary

Support Health Index v2 (SHI v2) is the primary support health signal used to:
1. **Nominate customers** for intensive care programs
2. **Confirm return to health** after intervention
3. **Inform MCS risk** assessment early in customer lifecycle
4. **Provide key input** for catalyst support scoring

SHI v2 represents a major evolution from v1 with comprehensive tenant scoring, proactive risk detection, and product-aware metrics.

---

## Purpose & Use Cases

### Primary Use Cases
1. **Intensive Care Nomination**
   - Identify customers requiring intensive support engagement
   - Trigger proactive intervention before escalation
   - Prioritize resource allocation based on risk severity

2. **Health Confirmation**
   - Validate customer return to healthy state
   - Inform engagement exit criteria
   - Track improvement trajectory

3. **Early MCS Risk Assessment**
   - Provide early warning signals for MCS (Microsoft Customer Success) teams
   - Enable proactive engagement before issues escalate
   - Support risk-based prioritization

4. **Catalyst Support Scoring**
   - Primary input for catalyst support scoring model
   - Informs customer success strategies
   - Drives targeted interventions

---

## Key Improvements from SHI v1 to v2

### 1. Comprehensive Tenant Scoring
**Problem in v1:** Only scored tenants with high case volumes; low/no-volume tenants were not assessed  
**Solution in v2:** Scores every tenant using binning logic for fair comparisons  
**Benefit:** No customer left unmonitored; reduces blind spots in support health

### 2. Improved Fairness for Low & No-Volume Tenants
**Problem in v1:** Distorted risk assessment for customers with few cases  
**Solution in v2:** Binning logic compares similar tenants (by case volume, ICM count)  
**Benefit:** Fair treatment across customer segments; eliminates volume bias

### 3. Proactive + Reactive Signals
**Problem in v1:** Reactive-only approach (detected issues after they occurred)  
**Solution in v2:** Hybrid model with proactive (risk formation) + reactive (closed case outcomes) signals  
**Benefit:** Early warning system; identifies risk before escalation or churn

### 4. Product-Aware Metrics
**Problem in v1:** One-size-fits-all scoring; didn't account for product differences  
**Solution in v2:** Tailored metrics by product (Purview, MTP, etc.) and severity  
**Benefit:** Accurate risk assessment per product motion; addresses stakeholder feedback

### 5. Model Reliability & Explainability
**Problem in v1:** Fragile model; score changes hard to explain  
**Solution in v2:** Stable scoring with clear attribution to specific metrics/cases  
**Benefit:** Confidence in using the model; actionable insights for engagement

---

## Model Architecture

### Hybrid Model Approach
SHI v2 uses a **hybrid model** combining:
- **Proactive Score** (50% weight) – Risk formation signals from open cases
- **Reactive Score** (50% weight) – Outcome signals from closed cases

### Binning Logic
- Customers are grouped by similar case volume and ICM count
- Enables fair peer-to-peer comparisons
- Reduces distortion from volume differences
- ML-analyzed binning (data-driven segmentation)

### Product & Severity Awareness
- Metrics and thresholds tailored by product (Purview, MTP, etc.)
- Severity-aware scoring (Sev A, Sev B, Sev C treated differently)
- Recognizes different support dynamics per product

---

## Scoring Components

### Final SHI v2 Score
```
SHI v2 Score = (Proactive Score × 0.5) + (Reactive Score × 0.5)
```

**Score Range:** 0-100
- **0-40:** Unhealthy (high risk, immediate intervention needed)
- **41-70:** At Risk (moderate risk, proactive engagement recommended)
- **71-100:** Healthy (low risk, standard monitoring)

---

## Proactive Scoring (Risk Formation)

### Purpose
Identifies risk **before** it escalates by analyzing open cases for early warning signals.

### Risk Conditions (High / Medium / Low)

#### High Risk Conditions
- **Case Age:** Case open > X days (threshold varies by product)
- **Time in Severity:** Case stuck in high severity > Y days
- **Initial TTE Breach:** Initial Time to Engagement exceeded
- **ICM Incidents:** Active critical incidents

#### Medium Risk Conditions
- **Case Age:** Case open > Z days (less than high threshold)
- **Time in Severity:** Case in medium severity > W days
- **Initial TTE Warning:** Approaching TTE breach

#### Low Risk Conditions
- **Case Age:** Case open within expected range
- **Time in Severity:** Progressing normally through severities
- **Initial TTE:** Met within SLA

### Proactive Scoring Workflow
1. **Identify Risky Cases**
   - Scan all open cases for threshold breaches
   - Categorize as High / Medium / Low risk

2. **Calculate Severity & Volume**
   - Count cases by risk category
   - Apply severity weighting (Sev A > Sev B > Sev C)

3. **Apply Logarithmic Scaling**
   - Normalize for case volume differences
   - Prevents skewing from high-volume customers

4. **Normalize Risk Score**
   - Scale to 0-100 range
   - Invert so 100 = healthy, 0 = unhealthy

5. **Generate Proactive Score**
   - Final proactive score (0-100)
   - Lower score = higher proactive risk

---

## Reactive Scoring (Closed Case Outcomes)

### Purpose
Assesses historical health based on how well closed cases were handled.

### Reactive Scoring Metrics

1. **TTMTICDTC (Time to Mitigation/Time in Customer/Days to Close)**
   - Measures speed of case resolution
   - Compares to product/severity benchmarks

2. **Initial TTE (Time to Engagement)**
   - How quickly was customer engaged?
   - Critical for first-touch experience

3. **Total Case Count**
   - Volume of closed cases in evaluation period
   - Contextualizes other metrics

4. **Crit Sit Case Count**
   - Number of critical situation cases
   - Indicates severity of issues

5. **Transfer Case Count**
   - Cases requiring transfers (multiple handoffs)
   - Indicates complexity or routing issues

### Reactive Scoring Workflow
1. **Retrieve Closed Case Metrics**
   - Query DFM for closed cases in lookback period (e.g., 90 days)
   - Extract metrics per case

2. **Apply Binning-Based Classification**
   - Group customers by case volume bin
   - Compare to peer cohort benchmarks

3. **Calculate Health Score per Metric**
   - TTMTICDTC score (0-100)
   - Initial TTE score (0-100)
   - Crit Sit impact score
   - Transfer impact score

4. **Normalize & Combine**
   - Weighted average of metric scores
   - Scale to 0-100 range

5. **Generate Reactive Score**
   - Final reactive score (0-100)
   - Lower score = poorer historical outcomes

---

## Special Handling & Edge Cases

### Default Score of 100
Applied when:
- No severity data available
- Negative variance in metrics
- Insufficient data for binning

**Rationale:** Prevents false negatives; assumes healthy unless proven otherwise

### Subjective Health vs. Model Risk
**Scenario:** Customer appears healthy (all cases accounted for) but SHI v2 flags risk  
**Reason:** High case volume itself is a risk signal (capacity strain, complexity)  
**Action:** Model surfaces case for **early engagement decision**; team decides whether to act

**Important:** Model does not suppress healthy-appearing customers; enables proactive choice

### No Exclusion Mechanism (Current State)
**Limitation:** Cannot flag customers as "confirmed healthy, no engagement needed"  
**Feedback:** Recognized need; planned for future enhancement  
**Workaround:** Document decision externally; monitor for changes

---

## Dashboard & Reporting

### SHI v2 Dashboard Features

#### Filters & Navigation
- **Program Filter:** Intensive Care, MCS, Catalyst
- **Product Filter:** Purview, MTP, all products
- **Health Status:** Healthy, At Risk, Unhealthy
- **Tenant Search:** Direct lookup by tenant name or ID

#### Tenant-Level View
- Overall SHI v2 score (0-100)
- Proactive score breakdown
- Reactive score breakdown
- Case count contributing to score
- Trend indicator (improving / declining / stable)

#### Case-Level Drill-Down
**Example: American Airlines Tenant**
- List of cases contributing to score
- Risk categorization per case (High / Medium / Low)
- Case age, severity, TTE status
- ICM incidents linked to tenant
- Detailed proactive/reactive metrics

#### Detailed Scoring View
- **Proactive Details:**
  - Count of High / Medium / Low risk cases
  - Severity distribution
  - Risk driver (case age, TTE, severity time)
- **Reactive Details:**
  - DTC (Days to Close) health score
  - TIC (Time in Customer) health score
  - TTM (Time to Mitigation) health score
  - Critical severity case impact

---

## Operational Strategy

### Parallel Model Operation
- **SHI v1** and **v2** running in parallel
- No further changes planned for v1
- Transition to v2 once broader consensus reached
- Validation period ongoing

### Cross-Functional Collaboration
Teams involved:
- Engineering (model infrastructure, data pipelines)
- Data Science (model development, ML analysis)
- PM (requirements, use case alignment)
- Business (PHE, MCS, Catalyst stakeholders)
- Continuous feedback & iteration

### Rollout Plan
1. **Phase 1 (Current):** Parallel operation, validation, feedback collection
2. **Phase 2:** Alignment with Purview team & broader stakeholders
3. **Phase 3:** Finalize updated UI & reporting
4. **Phase 4:** Broader rollout to all programs
5. **Phase 5:** Deprecate SHI v1

---

## Integration with Health 360

**Health 360** is an upcoming tool providing comprehensive customer health view.

### Integration Points
- **SHI v2 Score** as primary input
- **Additional Product Indicators:** Adoption, usage, engagement
- **Broader Health Context:** Beyond support metrics
- **Unified Dashboard:** Single pane of glass for customer health

### Timeline
Health 360 will leverage SHI v2 scores once v2 is available in production (estimated: Q2 2026)

---

## Future Enhancements

### Planned
1. **Customer Exclusion Mechanism**
   - Enable flagging customers as "confirmed healthy, no engagement needed"
   - Reduce noise for known-good customers

2. **ICMS Segmentation by Type**
   - Separate DCR (Design Change Request) vs. RFC (Request for Change)
   - Improve risk identification granularity

3. **Forecasting & Trend Analysis**
   - Forward-looking risk projection
   - Historical trend visualization
   - Case risk analysis (predictive)

4. **Tailored Recommendations**
   - Next best action suggestions per tenant
   - Automated escalation triggers
   - Integration with playbooks

### Under Consideration
- Real-time scoring (vs. daily batch)
- Multi-product composite scoring
- Customer segment-specific thresholds
- Integration with Catalyst workflows

---

## Using SHI v2 in PHEPy Agent

### Tenant Health Monitor Sub-Agent
**Primary consumer of SHI v2 data**

**Query Patterns:**
- "What's the SHI v2 score for Tenant X?"
- "Which tenants are unhealthy (SHI < 40)?"
- "Show me proactive risk drivers for Tenant Y"
- "Compare MCS Alpha cohort SHI scores"

**Actions:**
- Retrieve SHI v2 score from dashboard or API
- Analyze proactive/reactive breakdown
- Identify at-risk tenants for escalation
- Track score trends over time

### Support Case Manager Sub-Agent
**Uses SHI v2 for case prioritization**

**Query Patterns:**
- "Which cases are contributing to unhealthy SHI score?"
- "Are high-risk cases driving SHI decline?"
- "Recommend case prioritization for Tenant Z"

**Actions:**
- Link DFM cases to SHI v2 risk drivers
- Prioritize aged/high-severity cases
- Recommend escalation if SHI < threshold

### Program Onboarding Manager Sub-Agent
**Uses SHI v2 for cohort health**

**Query Patterns:**
- "What's the avg SHI v2 for MCS Beta cohort?"
- "Are any onboarding tenants unhealthy?"
- "Track SHI improvement post-go-live"

**Actions:**
- Monitor cohort SHI trends
- Flag tenants needing additional support
- Validate go-live readiness (SHI > 70)

---

## Metrics & Thresholds

### Intensive Care Nomination
- **Threshold:** SHI v2 < 40 (Unhealthy)
- **Action:** Immediate nomination for intensive care
- **Review Frequency:** Daily

### MCS Risk Assessment
- **Threshold:** SHI v2 < 55 (At Risk trending down)
- **Action:** Early engagement, proactive support
- **Review Frequency:** Weekly

### Catalyst Support Scoring
- **Input:** SHI v2 score (0-100)
- **Weight:** Primary input (40-50% of overall catalyst score)
- **Usage:** Combined with adoption, engagement, product health

### Health Confirmation (Exit Criteria)
- **Threshold:** SHI v2 > 70 (Healthy) sustained for 30 days
- **Action:** Exit intensive care, return to standard monitoring
- **Review Frequency:** Weekly

---

## Data Sources & Freshness

### Data Sources
- **DFM (Support Cases):** Open & closed case data, SLA metrics
- **ICM (Incidents):** Active incidents, severity, customer impact
- **Tenant Metadata:** Customer segment, product SKU, region
- **Historical Metrics:** 90-day lookback for reactive scoring

### Data Freshness
- **SHI v2 Scores:** Refreshed daily (batch process)
- **Dashboard:** Updated every 24 hours
- **Real-time Events:** ICM incidents reflected within 1 hour

### Data Latency
- **DFM Case Updates:** < 4 hours
- **ICM Incident Updates:** < 1 hour
- **Scoring Recalculation:** Daily at 00:00 UTC

---

## Known Limitations

1. **No Real-Time Scoring**
   - Daily batch updates only
   - Cannot detect intra-day risk spikes

2. **No Customer Exclusion**
   - Cannot mark "confirmed healthy, no action needed"
   - May surface false positives

3. **Limited Forecasting**
   - Historical view only; no forward projection
   - Trend analysis manual

4. **Product Coverage**
   - Optimized for Purview, MTP
   - Other products use generic thresholds

5. **Binning Granularity**
   - Fixed bins (ML-determined)
   - May not capture all customer nuances

---

## FAQs

### Q: Why does a customer with all cases accounted for show as unhealthy?
**A:** High case volume itself is a risk signal (capacity strain, support dependency). SHI v2 surfaces this for proactive engagement decision.

### Q: Can I override or exclude a customer from SHI v2?
**A:** Not currently. This is planned for future enhancement. Document decisions externally.

### Q: How is SHI v2 different from SHI v1?
**A:** v2 has proactive scoring, product-aware metrics, fair binning, and scores all tenants. v1 was reactive-only and volume-biased.

### Q: What if SHI v2 and subjective assessment disagree?
**A:** Use SHI v2 as a signal, not a decision. Combine with context (customer comms, relationship health) to decide action.

### Q: How often should I check SHI v2?
**A:** Daily for intensive care tenants, weekly for MCS, monthly for catalyst.

### Q: Can I get historical SHI v2 data?
**A:** Yes, dashboard provides historical view (limited lookback). Forecasting is future enhancement.

---

## References & Resources

### Documentation
- SHI v2 Dashboard: [Link TBD]
- Health 360 Tool: [Link TBD]
- SHI v2 Technical Spec: [Link TBD]

### Contacts
- **Model Owner:** James Verdejo Jr
- **Data Science Lead:** [TBD]
- **PM Lead:** [TBD]
- **Engineering Lead:** [TBD]

### Related Grounding Docs
- `tenant_health_metrics.md` – KPI definitions
- `dfm_sla_definitions.md` – SLA thresholds
- `icm_severity_mapping.md` – ICM severity classification
- `customer_list_registry.md` – Customer segment definitions

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 2.0 | 2026-02-04 | Initial SHI v2 production release; parallel operation with v1 |
| 1.0 | 2025-XX-XX | SHI v1 baseline (deprecated, no further updates) |

---

**Status:** ✅ Active in Production (Parallel with v1)  
**Next Review:** Q2 2026 (Broader rollout decision)  
**Owner:** James Verdejo Jr / PHE Data Science Team
