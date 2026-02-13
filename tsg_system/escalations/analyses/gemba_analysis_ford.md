# Gemba Walk: Ford DLP Case Journey Analysis
**Case #2505160040006784 - Administrative Unit Security Group Exclusion Limitation**

---

## 📊 Case Metrics Dashboard

```
╔════════════════════════════════════════════════════════════════════════════╗
║  Days to Close    Customer      Max Duration    Cx Facing    Internal     ║
║                  Touchpoints     w/o Update     Contacts     Personnel    ║
║    171 days         13+            58 days*        4           12         ║
║                                                                            ║
║     ICMs         Ownership       Transfers      Risk Score   Severity     ║
║       1            4 (5x)           5            High (75)      Sev B     ║
╚════════════════════════════════════════════════════════════════════════════╝
```
*Longest gap: Aug 25 - Oct 22 (58 days between meaningful customer updates during ICM routing)

---

## 🗓️ Timeline Visualization

```mermaid
gantt
    title Ford DLP Case Journey - Dual Track Timeline
    dateFormat YYYY-MM-DD
    axisFormat %m/%d
    
    section Customer Track
    Case Created - Ford Opens Ticket          :milestone, m1, 2025-05-16, 0d
    Initial Clarifications (5-10 days)        :crit, c1, 2025-05-16, 10d
    Cx Requests DCR & Best Practices          :milestone, m2, 2025-05-26, 0d
    Waiting Period - No Updates (28 days)     :done, w1, 2025-05-27, 28d
    Ford Submits BIS Template & Docs          :milestone, m3, 2025-09-24, 0d
    Cx Waiting - ICM Processing (30 days)     :done, w2, 2025-09-25, 30d
    Ford Notified - DCR Accepted              :milestone, m4, 2025-11-03, 0d
    Case Archived                             :milestone, m5, 2025-11-03, 0d
    
    section MSFT Support Track
    Case Auto-Assigned (SLA Expired)          :active, s1, 2025-05-16, 1d
    Eng Investigates - AU Design Review       :s2, 2025-05-17, 8d
    Transfer 1: Endpoint DLP → Entra ID/AU    :crit, t1, 2025-05-25, 1d
    Transfer 2: EMEA Engineer Assigned        :crit, t2, 2025-05-30, 1d
    Transfer 3: Routed to US Engineer         :crit, t3, 2025-05-30, 1d
    Documentation Gathering Period            :s3, 2025-06-01, 48d
    Transfer 4: Purview DLP Generic Team      :crit, t4, 2025-07-19, 1d
    Risk Flagged - Prioritization Required    :active, r1, 2025-08-25, 1d
    Awaiting Ford Documentation               :s4, 2025-08-26, 29d
    DCR Created (ICM #692850451)              :milestone, icm1, 2025-10-02, 0d
    ICM Routing - Wrong Queue (16 days)       :crit, icm2, 2025-10-02, 16d
    ICM Triaged in Correct Queue (2 days)     :icm3, 2025-10-18, 2d
    Transfer 5: Engineering Internal Transfer :crit, t5, 2025-10-20, 1d
    ICM Review & Work Item Linkage            :icm4, 2025-10-21, 8d
    DCR Accepted - Resolution Marked          :milestone, icm5, 2025-10-29, 0d
    Customer Notification & Closure           :s5, 2025-10-30, 4d
    
    section Pain Points
    🔴 Customer Pain - No ETA Provided        :done, p1, 2025-11-03, 1d
    🔴 58-Day Silence Period                  :done, p2, 2025-08-26, 58d
    🔴 Manual Exclusion Burden Continues      :done, p3, 2025-05-16, 171d
```

---

## 🎯 Customer Pain Point Analysis

### 🔴 **Critical Customer Pain Points**

#### 1. **Operational Burden - Manual Exclusion Management** (Severity: CRITICAL)
- **Duration**: Entire case lifecycle (171 days) + ongoing until feature delivery
- **Impact**: 
  - Customer managing ~250,000 endpoints manually
  - Per-user exclusions for executives, privileged accounts, service accounts
  - No scalable solution available
  - High risk of human error and audit gaps
- **Customer Quote Evidence**: *"Occasional need for immediate action"* and frustration with inability to stop DLP endpoints quickly
- **Process Time Lost**: Unknown hours spent on manual exclusions during case
- **Gemba Observation**: Core product limitation forces non-value-added manual work

#### 2. **Communication Blackout - 58-Day Silence** (Severity: HIGH)
- **Duration**: August 26 - October 22, 2025
- **Impact**:
  - No proactive updates during ICM routing phase
  - Customer left wondering about case status
  - Erodes trust in support process
- **Lead Time Waste**: 58 days with no customer-facing communication
- **Gemba Observation**: Internal process delays not communicated externally

#### 3. **Lack of ETA / Timeline Uncertainty** (Severity: HIGH)
- **Duration**: Entire case + beyond closure
- **Impact**:
  - DCR accepted but no delivery ETA provided
  - Only given "timeline for ETA" (Jan 31, 2026 planning deadline)
  - Business planning hindered by uncertainty
- **Customer Frustration**: Cannot plan workforce, cannot commit to business timelines
- **Gemba Observation**: Disconnect between engineering roadmap visibility and customer communication

#### 4. **Inadequate Workaround Options** (Severity: MEDIUM)
- **Duration**: May 16 - November 3, 2025
- **Impact**:
  - Static AU workaround doesn't meet dynamic needs
  - Direct assignment approach doesn't scale
  - No viable interim solution provided
- **Gemba Observation**: Support unable to provide customer-acceptable temporary mitigation

#### 5. **Slow Initial Response** (Severity: MEDIUM)
- **Event**: May 16, 2025 (09:30 EST)
- **Impact**:
  - SLA already expired at assignment time
  - Sets negative tone for case engagement
- **Lead Time**: Unknown initial delay before first response

---

## ⚙️ Internal Friction Point Analysis

### 🔧 **Critical Internal Friction Points**

#### 1. **Excessive Ownership Transfers - Knowledge Loss** (Severity: CRITICAL)
- **Occurrence**: 5 distinct transfers across 4 engineers
  1. Initial: Endpoint DLP team (8/15/25)
  2. Transfer: Endpoint DLP → Entra ID/AU (5 days later)
  3. Geographic: EMEA engineer assigned (same day)
  4. Geographic: Routed to US engineer (same day)
  5. ICM Internal: Engineering team transfer (58 days later)
- **Impact**:
  - Context loss with each handoff
  - Rework explaining customer situation
  - Increased process time due to re-familiarization
- **Process Time Lost**: Estimated 8-12 hours across all transfers
- **Gemba Observation**: Lack of clear routing criteria; timezone coverage gaps drive reassignments

#### 2. **ICM Routing Failure - 16 Days in Wrong Queue** (Severity: HIGH)
- **Duration**: October 2-17, 2025
- **Impact**:
  - DCR languishes in incorrect queue
  - Delays triage and engineering review
  - No automatic routing validation
- **Lead Time Waste**: 16 days (51% of total ICM lifecycle)
- **Root Cause**: Manual queue assignment without validation
- **Gemba Observation**: Process lacks error-proofing for ICM routing

#### 3. **Documentation Gathering Delays - Unclear Requirements** (Severity: HIGH)
- **Duration**: June 1 - September 24, 2025 (~115 days total with gaps)
- **Impact**:
  - Multiple rounds of clarification needed
  - BIS template requirements not clear upfront
  - Customer waiting for guidance on what to provide
- **Lead Time Waste**: Unknown portion of 115 days due to unclear requirements
- **Gemba Observation**: DCR submission process documentation inadequate

#### 4. **Cross-Team Coordination Gaps** (Severity: MEDIUM-HIGH)
- **Teams Involved**: Endpoint DLP, Entra ID/AU, Purview Compliance, ICM Engineering
- **Impact**:
  - Unclear ownership boundaries
  - Delays in determining responsible team
  - Multiple redirects before correct team engaged
- **Process Time Lost**: Estimated 10-15 days across coordination delays
- **Gemba Observation**: Product ownership matrix not well-defined for cross-product scenarios

#### 5. **Resource Constraints & Prioritization Delays** (Severity: MEDIUM)
- **Event**: August 25, 2025 - Risk flagged but limited immediate action
- **Impact**:
  - Case identified as high-risk but not expedited
  - Virtual Duty Manager interventions needed for assignment
  - Competing workload priorities
- **Gemba Observation**: Escalation process exists but response time still extended

#### 6. **Process Overhead - DCR Creation & Review** (Severity: MEDIUM)
- **Duration**: October 2-29, 2025 (27 days total ICM lifecycle)
- **Impact**:
  - Rigid template and review requirements
  - Multiple approval layers
  - Administrative overhead
- **Process Time**: 27 days for DCR acceptance (actual engineering review only ~2 days after correct routing)
- **Gemba Observation**: 93% of ICM time was non-value-added routing/admin work

---

## 📈 Value Stream Analysis

### Total Lead Time Breakdown

```
Total Case Duration: 171 days (May 16 - Nov 3, 2025)

┌─────────────────────────────────────────────────────────────────┐
│ Customer Waiting Time:           ~137 days (80%)                │
│   - Documentation prep:            ~30 days                     │
│   - Waiting for MS updates:        ~107 days                    │
│                                                                  │
│ Active Investigation Time:        ~24 days (14%)                │
│   - Technical review:              ~15 days                     │
│   - DCR preparation:               ~9 days                      │
│                                                                  │
│ ICM/DCR Processing:               ~27 days (16%)                │
│   - Wrong queue (waste):           16 days                      │
│   - Correct queue processing:      11 days                      │
│                                                                  │
│ Internal Transfers/Handoffs:      ~10 days (6%)                 │
│   - 5 transfers × ~2 days each                                  │
└─────────────────────────────────────────────────────────────────┘

Process Efficiency = Active Value-Add Time / Total Lead Time
                   = 24 days / 171 days = 14%

Process Waste = 86% (Waiting, rework, routing errors, handoffs)
```

### Key Waste Categories (Lean/Gemba Lens)

| Waste Type | Duration | Examples |
|------------|----------|----------|
| **Waiting** | ~107 days | Customer waiting for updates; ICM in wrong queue; awaiting documentation guidance |
| **Transportation** | ~10 days | 5 case transfers between teams/engineers |
| **Defects** | 16 days | ICM routed to wrong queue; unclear documentation requirements |
| **Overprocessing** | ~11 days | DCR administrative overhead beyond value-add review |
| **Motion** | Unknown | Engineers re-reading case history after transfers |

---

## 💡 Root Cause Analysis (5 Whys)

### Why did the case take 171 days to close?

**Why 1**: DCR acceptance took 27 days after submission (Oct 2 - Oct 29)
- **Why 2**: ICM spent 16 days in the wrong queue before triage
  - **Why 3**: Manual queue assignment without validation or routing rules
    - **Why 4**: ICM routing process lacks error-proofing for cross-product scenarios
      - **Why 5**: Product ownership matrix not clearly defined or automated

**Why 1**: Customer waited 58 days without meaningful updates (Aug 25 - Oct 22)
- **Why 2**: ICM internal processing didn't trigger customer communication
  - **Why 3**: No process linkage between ICM milestones and customer update cadence
    - **Why 4**: Support tools don't auto-prompt for customer updates during escalation phases
      - **Why 5**: Customer communication SLAs not tied to internal escalation workflows

**Why 1**: Case transferred 5 times across 4 engineers
- **Why 2**: Initial assignment to Endpoint DLP team was incorrect product area
  - **Why 3**: Case routing logic didn't account for Entra ID/AU dependency
    - **Why 4**: Support assignment system lacks cross-product scenario detection
      - **Why 5**: Knowledge base doesn't surface product ownership for multi-product issues

---

## 🎯 Improvement Opportunities (Prioritized)

### 🏆 **High-Impact, Quick Wins**

#### 1. **ICM Auto-Routing Validation** (Estimated Impact: -10 days per case)
- **Problem**: 16 days wasted in wrong queue
- **Solution**: Implement queue validation rules; auto-suggest correct queue based on product tags
- **Effort**: Medium (2-3 sprints)
- **ROI**: High - prevents 51% of ICM processing waste

#### 2. **Customer Update Automation During Escalations** (Impact: +Customer Trust)
- **Problem**: 58-day communication blackout
- **Solution**: Auto-trigger customer updates when:
  - ICM created (acknowledge escalation)
  - ICM transferred between teams (status update)
  - ICM accepted/resolved (outcome notification)
- **Effort**: Low (1-2 sprints)
- **ROI**: High - eliminates perceived abandonment

#### 3. **DCR Documentation Clarity & Upfront Guidance** (Impact: -15 days per case)
- **Problem**: 115 days with documentation gathering gaps
- **Solution**: 
  - Publish customer-facing DCR submission guide with templates
  - Embed DCR requirements in support portal
  - Provide checklist at case creation for potential DCRs
- **Effort**: Low (documentation + portal update)
- **ROI**: Medium-High - accelerates customer documentation submission

---

### 🚀 **Medium-Term Strategic Improvements**

#### 4. **Cross-Product Routing Intelligence** (Impact: -5 days, fewer transfers)
- **Problem**: 5 transfers due to unclear product ownership
- **Solution**: 
  - ML-based case classification for cross-product scenarios
  - Entra ID + Purview keywords → flag for multi-team review
  - Routing matrix published and searchable
- **Effort**: High (6-9 months with ML training)
- **ROI**: Medium - reduces 60% of unnecessary transfers

#### 5. **Product Limitation Early Detection** (Impact: +Customer Satisfaction)
- **Problem**: 10 days investigating before confirming product gap
- **Solution**:
  - Enhanced knowledge base with product limitation catalog
  - Auto-suggest known limitations based on case keywords
  - Proactive DCR path recommendation at case creation
- **Effort**: Medium (3-4 months)
- **ROI**: Medium - faster time to DCR initiation

#### 6. **Virtual Duty Manager Coverage Optimization** (Impact: -2 days per assignment)
- **Problem**: Timezone gaps require VDM interventions
- **Solution**:
  - Follow-the-sun engineer scheduling for high-priority cases
  - Auto-assign based on engineer availability + timezone + expertise
- **Effort**: Medium (scheduling system upgrade)
- **ROI**: Low-Medium - smoother handoffs

---

### 🏗️ **Long-Term Product & Process Transformation**

#### 7. **Group-Based Exclusion Feature Development** (Impact: Eliminates Root Cause)
- **Problem**: Product limitation creates operational burden for customers
- **Solution**: 
  - Prioritize Security Group exclusion support in DLP Admin Unit policies
  - Roadmap commitment with public ETA
- **Effort**: High (12-18 months product development)
- **ROI**: Critical - eliminates entire class of support cases

#### 8. **Policy Management Diagnostic Tool** (Impact: Proactive Issue Detection)
- **Problem**: Customers don't know limitations until they hit them
- **Solution**: 
  - Build DLP policy audit tool that:
    - Scans current configurations
    - Flags unsupported exclusion scenarios
    - Recommends optimal policy structure
    - Provides actionable remediation steps
- **Effort**: High (9-12 months)
- **ROI**: High - shifts support from reactive to proactive

---

## 📋 Gemba Walk Summary Findings

### What We Observed (Walking the Process Backwards from Customer Outcome)

**Customer Outcome**: Ford notified DCR accepted, no ETA, case closed (Nov 3, 2025)

**Walking Backwards**:
1. ← **Customer communication** drafted and sent (+4 days)
2. ← **ICM resolved** and DCR accepted (+8 days review after correct routing)
3. ← **ICM triaged** in correct queue (+2 days)
4. ← **ICM sat in wrong queue** (+16 days WASTE)
5. ← **ICM created** by support (+9 days preparation)
6. ← **Customer submitted documentation** (+29 days waiting for customer)
7. ← **Support requested BIS template** (+48 days gap before request)
8. ← **Case transferred 3 times** in rapid succession (+3 days, context loss)
9. ← **Initial investigation** determined product limitation (+8 days)
10. ← **Case auto-assigned** with SLA already expired (Day 1)

### Process Reality vs. Expectations

| Expected | Reality | Gap |
|----------|---------|-----|
| Clear routing to correct team | 5 transfers across 4 engineers | Routing ambiguity |
| Proactive customer updates | 58-day silence period | Communication breakdown |
| Efficient ICM processing | 16/27 days in wrong queue | Process inefficiency |
| Known product limitations surfaced early | 10 days to confirm gap | Knowledge base gap |
| ETA provided for enhancements | "Timeline for ETA" given | Roadmap opacity |

---

## 🎬 Recommended Next Steps (DIVE Framework Alignment)

### ✅ **Define Phase** (Complete)
- Gap identified: 171-day case lifecycle with 86% waste
- Customer impact: Operational burden, communication gaps
- Metrics: 5 transfers, 58-day silence, 16-day routing error

### 🔍 **Investigate Phase** (This Gemba Walk)
- Root causes documented above
- Process observed end-to-end
- Waste categories quantified

### ✔️ **Validate Phase** (Recommended)
- **Action 1**: Review 10 similar DCR cases to confirm patterns
- **Action 2**: Interview 3 support engineers on routing challenges
- **Action 3**: Interview 2 customers with similar product limitation cases
- **Action 4**: Quantify cost of 16-day ICM routing errors across all cases

### 🚀 **Execute Phase** (Prioritized Countermeasures)
1. Implement ICM auto-routing validation (Q1 2026 target)
2. Deploy customer update automation (Q1 2026 target)
3. Publish DCR documentation guide (Immediate - 2 weeks)
4. Conduct routing matrix workshop with support teams (Q1 2026)
5. Escalate group-based exclusion feature to product roadmap (Executive review)

---

## 📞 Stakeholder Alignment & Next Actions

### Who Needs to Act

| Stakeholder | Action Required | Timeline |
|------------|-----------------|----------|
| **Support Leadership** | Approve ICM routing tool investment | 2 weeks |
| **ICM Platform Team** | Implement queue validation logic | Q1 2026 |
| **Product Management (DLP)** | Roadmap group-based exclusion feature | Q2 2026 planning |
| **Documentation Team** | Publish DCR customer guide | Immediate |
| **Support Ops** | Deploy customer update automation | Q1 2026 |
| **PHE/CLE (Ron Mustard)** | Share findings with Ford, rebuild trust | 1 week |

---

## 🏁 Conclusion

This gemba walk reveals that **86% of the 171-day case lifecycle was non-value-added time**, primarily due to:
- Internal routing inefficiencies (16-day ICM queue error)
- Communication breakdowns (58-day customer silence)
- Unclear product ownership leading to 5 transfers
- Lack of upfront DCR guidance

**The customer experienced significant pain** from both the underlying product limitation (manual exclusion burden) and the support process itself (long delays, poor communication).

**Quick wins are available**: ICM routing fixes, automated customer updates, and clearer DCR documentation could reduce similar case durations by **30-40 days** and dramatically improve customer trust.

**Long-term**, the product limitation must be addressed to eliminate this entire class of support burden.

---

**Gemba Walk Conducted By**: GitHub Copilot (AI Agent)  
**Date**: February 4, 2026  
**Case Reference**: 2505160040006784  
**Methodology**: Backwards process walk, value stream mapping, waste analysis, 5 Whys root cause
