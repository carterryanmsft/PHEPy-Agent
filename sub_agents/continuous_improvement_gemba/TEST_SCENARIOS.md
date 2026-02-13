# CI/Gemba Walker - Test Scenarios

**Agent:** Continuous Improvement & Gemba Walker  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 🧪 Test Scenario Categories

1. **Gemba Walk Execution**
2. **Waste Identification**
3. **Root Cause Analysis**
4. **Value Stream Mapping**
5. **Improvement Recommendations**

---

## 1. Gemba Walk Execution

### Test 1.1: Support Case Lifecycle Gemba
**Prompt:**  
"Conduct a gemba walk of the support case resolution process for the last 30 days"

**Expected Response:**
1. **Purpose:** Understand current case resolution process
2. **Scope:** Last 30 days, all cases
3. **Observations:**
   - Query DFM for case lifecycle data
   - Calculate cycle times per stage
   - Identify wait states
   - Document handoff patterns
4. **Waste Identified:** List specific wastes with examples
5. **Questions:** What needs deeper investigation?
6. **Recommendations:** Prioritized improvement opportunities

**Success Criteria:**
- ✅ Structured gemba format
- ✅ Data-backed observations
- ✅ Specific waste examples
- ✅ Actionable recommendations

---

### Test 1.2: Escalation Process Gemba
**Prompt:**  
"Observe how P1 escalations actually flow through ICM"

**Expected Response:**
- Map actual escalation path from data
- Compare to documented procedure
- Identify deviations and delays
- Quantify impact of process variation
- Recommend standardization points

**Success Criteria:**
- ✅ Actual vs intended process comparison
- ✅ Variance quantification
- ✅ Standardization recommendations

---

## 2. Waste Identification

### Test 2.1: Identify Waiting Waste
**Prompt:**  
"Where are cases spending the most time waiting in queues?"

**Expected Response:**
- Query for queue times by stage
- Rank by total wait time
- Calculate % of cycle time spent waiting
- Identify bottlenecks
- Recommend queue reduction strategies

**Success Criteria:**
- ✅ Quantified wait times
- ✅ Bottleneck identification
- ✅ Impact calculation
- ✅ Specific recommendations

---

### Test 2.2: Identify Defect Waste
**Prompt:**  
"How often are cases reopened or misrouted?"

**Expected Response:**
- Calculate reopen rate
- Count misrouted cases
- Identify common causes
- Quantify rework time
- Recommend quality improvements

**Success Criteria:**
- ✅ Defect rate calculation
- ✅ Root cause identification
- ✅ Rework impact quantified

---

### Test 2.3: Identify Transportation Waste
**Prompt:**  
"How many handoffs occur in the average case?"

**Expected Response:**
- Calculate average handoff count
- Map handoff patterns
- Identify unnecessary transfers
- Quantify handoff overhead
- Recommend handoff reduction

**Success Criteria:**
- ✅ Handoff metrics
- ✅ Unnecessary handoffs identified
- ✅ Reduction opportunities

---

## 3. Root Cause Analysis

### Test 3.1: 5-Whys Analysis
**Prompt:**  
"Why is the case reopen rate 15%?"

**Expected Response:**
```
Problem: Case reopen rate is 15%
Why? Cases are being closed prematurely
Why? Engineers are pressured to meet SLA
Why? SLA metrics prioritize speed over quality
Why? Performance reviews weight SLA heavily
Why? Management values time-to-close over first-time resolution

Root Cause: Misaligned performance incentives
```

**Success Criteria:**
- ✅ Systematic 5-Whys progression
- ✅ Reaches fundamental root cause
- ✅ Doesn't stop at symptoms
- ✅ Data-backed at each level

---

### Test 3.2: Fishbone Diagram
**Prompt:**  
"What factors contribute to slow case resolution?"

**Expected Response:**
- **Man:** Skill gaps, staffing levels
- **Machine:** Tool limitations, system downtime
- **Method:** Process inefficiency, unclear procedures
- **Material:** Insufficient documentation, missing info
- **Measurement:** Unclear metrics, misaligned KPIs
- **Mother Nature:** Customer responsiveness, external factors

**Success Criteria:**
- ✅ Covers all 6Ms
- ✅ Specific factors listed
- ✅ Prioritizes most impactful
- ✅ Evidence for each factor

---

## 4. Value Stream Mapping

### Test 4.1: Current State VSM
**Prompt:**  
"Create a value stream map for the case resolution process"

**Expected Response:**
```
Process Steps:
1. Case Created → 2. Initial Triage → 3. Assignment → 
4. Investigation → 5. Customer Engagement → 6. Resolution → 
7. Validation → 8. Closure

Metrics per Step:
- Cycle Time
- Wait Time
- Process Time
- Handoffs

Summary:
- Total Cycle Time: 5 days
- Total Wait Time: 3.5 days
- Total Process Time: 1.5 days
- Process Efficiency: 30%
```

**Success Criteria:**
- ✅ Complete process map
- ✅ Metrics for each step
- ✅ Efficiency calculation
- ✅ Visual or structured format

---

### Test 4.2: Future State Design
**Prompt:**  
"Design an improved case resolution process"

**Expected Response:**
- Current state recap
- Waste elimination opportunities
- Streamlined process flow
- Projected improvements:
  - Reduce wait time from 3.5d to 1d
  - Reduce cycle time from 5d to 2.5d
  - Increase efficiency from 30% to 60%
- Implementation considerations

**Success Criteria:**
- ✅ Clear before/after comparison
- ✅ Quantified improvements
- ✅ Realistic targets
- ✅ Implementation plan

---

## 5. Improvement Recommendations

### Test 5.1: Quick Wins Identification
**Prompt:**  
"What quick wins can reduce case resolution time?"

**Expected Response:**
- **Quick Win 1:** Automate case routing (saves 4 hours/case)
- **Quick Win 2:** Pre-fill common responses (saves 30 min/case)
- **Quick Win 3:** Eliminate approval for P3 cases (saves 1 day/case)
- Prioritized by impact vs effort
- Implementation timeline: 2-4 weeks
- Expected ROI: 20% cycle time reduction

**Success Criteria:**
- ✅ 3-5 quick wins identified
- ✅ Quantified impact
- ✅ Low implementation effort
- ✅ Realistic timeline

---

### Test 5.2: Strategic Improvements
**Prompt:**  
"What strategic changes would dramatically improve support quality?"

**Expected Response:**
- **Strategic 1:** Implement self-service portal (reduces case volume 30%)
- **Strategic 2:** Realign KPIs to first-time resolution (improves quality)
- **Strategic 3:** Cross-train engineers on multiple products (reduces handoffs)
- Timeline: 3-6 months each
- Resource requirements
- Change management considerations

**Success Criteria:**
- ✅ High-impact changes
- ✅ Realistic for strategic work
- ✅ Considers implementation complexity
- ✅ Change management included

---

### Test 5.3: Improvement Impact Estimation
**Prompt:**  
"If we reduce handoffs from 4 to 2, what's the impact?"

**Expected Response:**
- **Time Saved:** 4 hours per case (2 handoffs × 2 hours each)
- **Cases Affected:** 100 cases/month
- **Total Time Saved:** 400 hours/month
- **FTE Impact:** 0.5 FTE capacity freed
- **Quality Impact:** Expected 20% reduction in errors
- **Customer Impact:** Faster resolution, better experience

**Success Criteria:**
- ✅ Quantified time savings
- ✅ Volume calculation
- ✅ Resource impact
- ✅ Quality and customer impact

---

## 6. DIVE Framework Application

### Test 6.1: Full DIVE Analysis
**Prompt:**  
"Use DIVE to analyze why escalations take too long"

**Expected Response:**

**Define:**
- Problem: Average escalation resolution is 7 days
- Target: 3 days
- Impact: 50 escalations/month, 200 hours delayed
- Scope: All P1/P2 escalations

**Investigate:**
- Gemba walk of escalation process
- Root cause: Unclear escalation criteria cause delays
- Data: 40% of escalations are unnecessary

**Verify:**
- Tested improved criteria with pilot
- Pilot results: 30% reduction in unnecessary escalations
- Time to resolve: Improved from 7d to 4.5d

**Execute:**
- Roll out new criteria
- Train teams
- Monitor metrics
- Result: 35% improvement sustained

**Success Criteria:**
- ✅ Complete DIVE structure
- ✅ Data-driven at each phase
- ✅ Measurable outcomes
- ✅ Implementation tracked

---

## 🎯 Performance Benchmarks

| Metric | Target | Measurement |
|--------|--------|-------------|
| Gemba Execution Time | < 2 hours | Time to complete analysis |
| Waste Identification | 5-8 wastes | # of wastes found |
| Root Cause Depth | 4-5 whys | Levels to reach root cause |
| VSM Completion | < 1 hour | Time to create VSM |
| Recommendation Quality | >80% actionable | % recommendations implemented |

---

## 🔄 Test Execution Process

1. **Setup test environment** with real or synthetic data
2. **Run all test scenarios**
3. **Validate outputs** against success criteria
4. **Check data accuracy** (metrics, calculations)
5. **Verify recommendations** are actionable
6. **Pilot improvements** to validate estimates

---

## 📝 Test Log Template

```markdown
### Test Run: [Date]
**Tester:** [Name]
**Agent Version:** [Version]
**Data Period:** [Date Range]

| Test # | Scenario | Pass/Fail | Data Accuracy | Notes |
|--------|----------|-----------|---------------|-------|
| 1.1 | Case Lifecycle Gemba | ✅ Pass | ✅ | Good observations |
| 2.1 | Waiting Waste | ❌ Fail | ✅ | Missed key bottleneck |
| 3.1 | 5-Whys | ✅ Pass | ✅ | Reached root cause |
| ... | ... | ... | ... | ... |

**Overall Score:** 12/15 (80%)
**Action Items:**
- Improve bottleneck detection logic
- Add more waste identification patterns
```
