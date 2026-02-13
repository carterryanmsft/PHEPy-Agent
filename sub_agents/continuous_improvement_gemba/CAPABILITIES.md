# CI/Gemba Walker - Capabilities Matrix

**Agent:** Continuous Improvement & Gemba Walker  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 🎯 Core Capabilities

### 1. Data-Driven Gemba Walks

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Process Observation** | Observe actual workflows through data | DFM, ICM, ADO, Kusto | ✅ Ready |
| **Variance Detection** | Identify deviations from standard process | Process data | ✅ Ready |
| **Documentation** | Structure observations using gemba framework | Templates | ✅ Ready |
| **Pattern Recognition** | Identify recurring issues and waste | Historical data | ✅ Ready |
| **Visual Mapping** | Create process flow visualizations | VSM tools | ✅ Ready |

### 2. Waste Identification (8 Wastes)

| Waste Type | Detection Method | Example in PHE | Status |
|------------|------------------|----------------|--------|
| **Defects** | Query reopened cases, escalations | Case reopens >10% | ✅ Ready |
| **Overproduction** | Identify unnecessary work outputs | Unused reports | ✅ Ready |
| **Waiting** | Calculate idle/queue times | Cases in queue >2 days | ✅ Ready |
| **Non-Utilized Talent** | Skill vs. task analysis | Engineers doing admin work | ✅ Ready |
| **Transportation** | Count handoffs and transfers | >3 handoffs per case | ✅ Ready |
| **Inventory** | Measure backlog and pile-ups | Case backlog >50 | ✅ Ready |
| **Motion** | Track tool switches and context shifts | >5 tools per workflow | ✅ Ready |
| **Extra Processing** | Identify redundant steps | Duplicate data entry | ✅ Ready |

### 3. Root Cause Analysis

| Capability | Description | Technique | Status |
|------------|-------------|-----------|--------|
| **5-Whys Analysis** | Drill down to fundamental root cause | 5-Whys | ✅ Ready |
| **Fishbone Diagram** | Categorize causes (6Ms) | Ishikawa | ✅ Ready |
| **Pareto Analysis** | Identify vital few vs trivial many | 80/20 rule | ✅ Ready |
| **Hypothesis Testing** | Validate cause-effect relationships | Data analysis | ✅ Ready |
| **Pattern Analysis** | Find common factors across incidents | Statistical | ✅ Ready |

### 4. Value Stream Mapping

| Capability | Description | Metrics | Status |
|------------|-------------|---------|--------|
| **Current State Mapping** | Document existing process flow | Process steps | ✅ Ready |
| **Cycle Time Analysis** | Measure time per process step | Minutes/hours | ✅ Ready |
| **Lead Time Calculation** | Total elapsed time end-to-end | Days | ✅ Ready |
| **Wait Time Identification** | Time between value-add steps | Hours/days | ✅ Ready |
| **Process Efficiency** | Calculate value-add ratio | Percentage | ✅ Ready |
| **Future State Design** | Optimize process with waste removed | Target metrics | ✅ Ready |

### 5. Improvement Recommendations

| Capability | Description | Output | Status |
|------------|-------------|--------|--------|
| **Impact Estimation** | Quantify improvement benefits | Time, cost, quality | ✅ Ready |
| **Prioritization** | Rank by effort vs impact | Quick wins first | ✅ Ready |
| **Implementation Roadmap** | Step-by-step execution plan | Timeline, owners | ✅ Ready |
| **Pilot Design** | Test improvements at small scale | Pilot plan | ✅ Ready |
| **Metrics Tracking** | Monitor improvement effectiveness | Before/after | ✅ Ready |

---

## 📊 DIVE Framework Application

### Define Phase
- **Problem Statement:** Clear, specific, measurable
- **Impact Quantification:** Time, cost, quality, customer impact
- **Scope Definition:** What's in/out of scope
- **Baseline Metrics:** Current state measurement

### Investigate Phase
- **Data Collection:** Gather relevant metrics and observations
- **Gemba Walks:** Observe actual process
- **Root Cause Analysis:** 5-Whys, Fishbone
- **Hypothesis Formation:** What causes the problem?

### Verify Phase
- **Data Validation:** Confirm root cause with evidence
- **Solution Testing:** Pilot improvements
- **Impact Measurement:** Quantify actual improvement
- **Stakeholder Review:** Validate findings

### Execute Phase
- **Implementation Plan:** Rollout strategy
- **Change Management:** Communication, training
- **Monitoring:** Track metrics post-implementation
- **Standardization:** Document new process

---

## 🔍 Process Analysis Patterns

### Support Case Lifecycle Analysis

**Key Metrics:**
- **Mean Time to Resolution (MTTR):** Average case resolution time
- **First Contact Resolution (FCR):** % resolved without escalation
- **Reopen Rate:** % of cases reopened after closure
- **Handoff Count:** Average # of transfers per case
- **Wait Time:** Time in queue between actions

**Common Wastes:**
- Cases waiting in queue (Inventory)
- Multiple handoffs (Transportation)
- Misrouted cases (Defects)
- Manual data entry (Motion)

---

### Escalation Process Analysis

**Key Metrics:**
- **Escalation Rate:** % of cases escalated to ICM
- **Time to Escalate:** Delay before escalation triggered
- **Escalation Duration:** Time to resolve after escalation
- **Unnecessary Escalations:** False alarms
- **Escalation Paths:** Actual vs optimal routing

**Common Wastes:**
- Delayed escalation triggers (Waiting)
- Unclear escalation criteria (Defects)
- Too many approval layers (Extra Processing)

---

### Onboarding Process Analysis

**Key Metrics:**
- **Time to Onboard:** Days from start to go-live
- **Milestone Completion:** % on-time milestones
- **Blocker Frequency:** # and duration of blockers
- **Rework Rate:** Steps repeated due to errors
- **Customer Engagement:** Meeting attendance, responsiveness

**Common Wastes:**
- Waiting for approvals (Waiting)
- Duplicate configuration (Defects)
- Unused templates/guides (Overproduction)

---

## 📐 Value Stream Metrics

### Standard Process Efficiency Calculation

```
Process Efficiency = (Value-Add Time / Total Lead Time) × 100%

Value-Add Time = Time spent on activities customer values
Total Lead Time = End-to-end elapsed time
```

**Benchmarks:**
- **World Class:** >25% process efficiency
- **Good:** 15-25%
- **Typical:** 5-15%
- **Poor:** <5%

---

### Process Velocity

```
Process Velocity = 1 / Average Cycle Time

Higher velocity = faster throughput
```

---

### Queue Theory Metrics

```
Average Wait Time = (Queue Length × Cycle Time) / (1 - Utilization)

Utilization = Actual Work Time / Available Time
```

---

## 🎯 Improvement Prioritization Matrix

### Impact vs Effort Grid

| | Low Effort | Medium Effort | High Effort |
|---|---|---|---|
| **High Impact** | 🟢 Quick Win | 🟡 Strategic | 🟠 Major Initiative |
| **Medium Impact** | 🟢 Easy Win | 🟡 Consider | ⚪ Backlog |
| **Low Impact** | 🟢 Nice-to-Have | ⚪ Backlog | 🔴 Avoid |

**Priority Order:**
1. 🟢 Quick Wins (High Impact, Low Effort)
2. 🟡 Strategic (High Impact, Medium Effort)
3. 🟢 Easy Wins (Medium Impact, Low Effort)
4. 🟡 Consider (Medium Impact, Medium Effort)
5. 🟠 Major Initiatives (High Impact, High Effort)

---

## 🔄 Kaizen Event Structure

### 1-Week Kaizen Sprint

**Day 1: Define & Plan**
- Problem statement
- Baseline metrics
- Team formation
- Gemba walk planning

**Day 2-3: Investigate**
- Conduct gemba walks
- Collect data
- Root cause analysis
- Value stream mapping

**Day 4: Verify & Design**
- Validate findings
- Design future state
- Estimate impact
- Pilot planning

**Day 5: Execute & Monitor**
- Implement quick wins
- Set up metrics tracking
- Document changes
- Share results

---

## 📊 Improvement Impact Tracking

### Before/After Metrics

| Metric | Baseline | Target | Actual | % Improvement |
|--------|----------|--------|--------|---------------|
| Cycle Time | 5 days | 3 days | 3.2 days | 36% |
| Wait Time | 2 days | 0.5 days | 0.6 days | 70% |
| Handoffs | 4 | 2 | 2 | 50% |
| Reopen Rate | 12% | 5% | 6% | 50% |
| FCR | 65% | 80% | 78% | 20% |

---

## 🔗 Integration with Other Agents

### Kusto Expert (Jacques)
- **Provides:** Telemetry, metrics, cycle times
- **Used For:** Quantifying waste, measuring improvement

### Support Case Manager
- **Provides:** Case lifecycle data, SLA metrics
- **Used For:** Support process analysis

### Escalation Manager
- **Provides:** Escalation patterns, resolution times
- **Used For:** Escalation process optimization

### Tenant Health Monitor
- **Provides:** Before/after health scores
- **Used For:** Improvement impact validation

### Work Item Manager
- **Provides:** ADO workflow data
- **Used For:** Development process analysis

---

## 🚫 Out of Scope

This agent **does NOT**:
- Make personnel or organizational decisions
- Implement changes directly (provides recommendations)
- Guarantee specific ROI (estimates based on data)
- Replace domain expertise or human judgment
- Optimize at expense of quality or safety

---

## 📏 Success Metrics

- **Waste Reduction:** >20% reduction in identified waste
- **Cycle Time:** >15% improvement in process cycle time
- **Quality:** >10% increase in first-time resolution
- **Efficiency:** >5% increase in value-add ratio
- **Sustainability:** Improvements maintained >90 days

---

## 🆘 Escalation Paths

**When to Escalate:**
- Improvement requires executive sponsorship
- Cross-team/organizational change needed
- Resource constraints blocking improvement
- Cultural resistance encountered

**Escalation Target:**
- **Process Owner** → For process-specific improvements
- **PHE Operations Lead** → For operational changes
- **Executive Sponsor** → For strategic initiatives
- **Change Management** → For cultural/adoption issues
