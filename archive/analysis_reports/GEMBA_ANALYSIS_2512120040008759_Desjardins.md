# Gemba/Continuous Improvement Analysis Report
## Case 2512120040008759 - Desjardins Purview DLP Classification Timeout Incident

---

## Executive Summary

**Incident Overview:**
- **Case Number:** 2512120040008759
- **Customer:** Desjardins (S500, High Profile)
- **Duration:** 54 days (Dec 13, 2025 - Feb 5, 2026)
- **Severity Progression:** B → A → B
- **Customer Sentiment:** Negative
- **Related ICMs:** 723169126, 21000000837036, 21000000859258

**Core Issue:**
Microsoft Purview DLP was failing to block sensitive data in emails when classification timeouts occurred due to unoptimized custom Sensitive Information Types (SITs) with inefficient regex patterns and unlimited proximity settings.

**Ultimate Resolution:**
Discovery of a legacy 100K unique-SIT exception that kept classification running far beyond standard limits, combined with SIT optimization and deployment of Secure-By-Default preview feature.

---

## 1. Root Cause Analysis (5 Whys Methodology)

### 1.1 Technical Root Cause - Classification Timeouts

**Why #1:** Why were emails with sensitive data not being blocked?
- **Answer:** Classification was timing out, causing DLP enforcement to skip action (by design behavior).

**Why #2:** Why was classification timing out?
- **Answer:** Custom SITs contained inefficient regex patterns with unlimited/very large proximity settings, dramatically increasing processing time.

**Why #3:** Why were inefficient SITs allowed in production?
- **Answer:** No proactive validation or performance testing of custom SITs before deployment; customer self-managed SIT creation without optimization guidance.

**Why #4:** Why did the timeout issue escalate to this severity?
- **Answer:** A hidden legacy exception (100K unique-SIT limit) kept classification running far beyond normal thresholds, masking the SIT efficiency problem until traffic patterns exposed it.

**Why #5:** Why wasn't the exception discovered earlier?
- **Answer:** Configuration exceptions are tenant-specific backend settings not visible in standard troubleshooting tools; no systematic audit of tenant-level exceptions during investigation.

**SYSTEMIC ROOT CAUSE:** Lack of proactive SIT performance validation tooling, combined with invisible backend configuration exceptions that masked underlying efficiency problems.

---

### 1.2 Process Root Cause - Seven Identified Gaps

#### **GAP 1: Delayed Communication of PG Findings (Dec 16-26, 2025)**

**Why #1:** Why was PG analysis not communicated to customer for 10 days?
- **Answer:** PG provided findings to CSS on Dec 22, but CSS didn't relay to customer until Dec 29.

**Why #2:** Why did CSS delay communicating findings?
- **Answer:** Holiday period (Dec 22-29) reduced staffing; no clear handoff protocols during reduced-capacity periods.

**Why #3:** Why weren't automated communication triggers in place?
- **Answer:** No automated workflow to ensure Sev A/B case updates meet SLA during holidays.

**Why #4:** Why was this acceptable for a Sev B case?
- **Answer:** Resource prioritization focused on active troubleshooting over status updates; customer engagement protocols not enforced.

**Why #5:** Why weren't escalation protocols triggered?
- **Answer:** Management oversight was reduced during holiday period; no coverage plan for S500 cases.

**SYSTEMIC ROOT CAUSE:** Lack of automated communication enforcement and inadequate coverage planning for high-priority cases during reduced-staffing periods.

---

#### **GAP 2: Contradictory Support Communication (Jan 7, 2026)**

**Why #1:** Why did customer receive contradictory information?
- **Answer:** CSS engineer sent conflicting messages about case status (waiting on PG vs. waiting on customer info).

**Why #2:** Why was there confusion about case ownership?
- **Answer:** Multiple handoffs between CSS engineers; unclear documentation of who owned customer communication.

**Why #3:** Why weren't case notes preventing this?
- **Answer:** Case notes were detailed but lacked explicit "current state" summary; engineers reading historical notes without status synthesis.

**Why #4:** Why wasn't there a single source of truth?
- **Answer:** No standardized case status field; engineers relied on note interpretation rather than explicit status tracking.

**Why #5:** Why did this create customer confusion?
- **Answer:** Customer received mixed signals about where delays were occurring, eroding trust in Microsoft's ability to manage the case.

**SYSTEMIC ROOT CAUSE:** Lack of explicit case state management system; over-reliance on free-form notes for status tracking leads to interpretation errors during handoffs.

---

#### **GAP 3: Premature ICM Severity Downgrade (Jan 7, 2026)**

**Why #1:** Why was the ICM downgraded when ownership was unclear?
- **Answer:** ICM 21000000837036 was downgraded from Sev 2 to Sev 3 after only 51 minutes.

**Why #2:** Why did someone downgrade without establishing ownership?
- **Answer:** Assumption that issue was customer-side configuration; incorrect belief that PG analysis was complete.

**Why #3:** Why wasn't the customer impact considered?
- **Answer:** Decision focused on technical scope rather than business impact; severity criteria interpreted narrowly.

**Why #4:** Why didn't this follow escalation protocols?
- **Answer:** ICM severity guidelines focus on service availability rather than customer data exposure risk; DLP bypass wasn't categorized as "service down."

**Why #5:** Why did this cause delays?
- **Answer:** Lower severity reduced PG response urgency; took 5 business days (Jan 7-12) to re-engage at appropriate priority.

**SYSTEMIC ROOT CAUSE:** Severity criteria insufficient for security/compliance scenarios; focus on service availability vs. customer business risk; lack of mandatory impact assessment before downgrade.

---

#### **GAP 4: Extended PG Non-Response at Sev 2 (Jan 9-11, 2026)**

**Why #1:** Why was there no PG response for 1.48 days at Sev 2?
- **Answer:** PG team didn't respond to Sev 2 ICM within expected timeframe.

**Why #2:** Why didn't on-call protocols trigger response?
- **Answer:** ICM was assigned but not actively monitored; no alert escalation for missed SLA.

**Why #3:** Why wasn't there automatic escalation?
- **Answer:** ICM system relies on manual escalation; no automated SLA violation alerts for PG engagement.

**Why #4:** Why wasn't CSS escalating proactively?
- **Answer:** CSS assumed PG was working; no visibility into PG's view of ICM priority queue.

**Why #5:** Why did this repeat (Gap 6: Jan 13-17)?
- **Answer:** Same systemic issue; no corrective action between occurrences.

**SYSTEMIC ROOT CAUSE:** No automated SLA enforcement for PG response at elevated severities; lack of cross-team visibility into active engagement status.

---

#### **GAP 5: Delayed Classification Team Engagement (Jan 12-16, 2026)**

**Why #1:** Why wasn't the Classification team engaged earlier?
- **Answer:** Initial investigation focused on DLP enforcement team; Classification team not looped in until Jan 16.

**Why #2:** Why did DLP team not recognize classification issue earlier?
- **Answer:** Classification timeouts were identified by Jan 12, but root cause analysis didn't immediately trigger Classification team engagement.

**Why #3:** Why wasn't there automatic routing to Classification?
- **Answer:** ICM routing based on symptom (DLP failure) rather than root cause (classification timeout).

**Why #4:** Why didn't troubleshooting guides indicate this?
- **Answer:** TSG focused on DLP policy configuration; classification performance troubleshooting was separate domain knowledge.

**Why #5:** Why did this delay resolution?
- **Answer:** Classification team had specialized knowledge of SIT optimization; 4-day delay in their engagement extended investigation.

**SYSTEMIC ROOT CAUSE:** Symptom-based ICM routing rather than root-cause-based; lack of integrated troubleshooting guides spanning multiple components; tribal knowledge required to identify correct owning team.

---

#### **GAP 6: Extended PG Non-Response (Jan 13-17, 2026)**

**Why #1:** Why did PG not respond for 2+ days at Sev 2 (again)?
- **Answer:** Second occurrence of Gap 4; PG team overwhelmed with Sev 2 queue.

**Why #2:** Why wasn't the first occurrence corrected?
- **Answer:** No retrospective or corrective action after Gap 4; same process repeated.

**Why #3:** Why didn't management intervene?
- **Answer:** Customer escalations hadn't yet reached executive level; management unaware of repeated delays.

**Why #4:** Why was customer unaware of PG delays?
- **Answer:** CSS shielding customer from internal PG delays; customer only saw "waiting on PG" without detail.

**Why #5:** Why did this compound customer frustration?
- **Answer:** Customer saw no visible progress for multiple days; perception that Microsoft wasn't prioritizing their Sev A case.

**SYSTEMIC ROOT CAUSE:** Lack of continuous improvement mechanisms; no formal retrospective after Gap 4; no management escalation triggers for repeated PG delays on same case.

---

#### **GAP 7: Incorrect Initial Analysis Leading to Rework (Jan 18, 2026)**

**Why #1:** Why was incorrect SIT analysis shared?
- **Answer:** PG provided custom SIT from different tenant's rule pack due to incorrect cmdlet parameters.

**Why #2:** Why wasn't the SIT validated against customer tenant?
- **Answer:** Investigation shortcuts were taken; engineer pulled SIT data without tenant validation.

**Why #3:** Why did customer receive this incorrect data?
- **Answer:** No peer review before sharing analysis with customer; urgency prioritized speed over accuracy.

**Why #4:** Why did this erode customer confidence?
- **Answer:** Customer tested provided SIT and found it didn't exist in their tenant; perception of incompetence.

**Why #5:** Why did this cause 1-day delay?
- **Answer:** Time required to correct analysis, re-pull proper data, and rebuild customer trust.

**SYSTEMIC ROOT CAUSE:** No mandatory tenant validation step before sharing investigation artifacts; lack of peer review for customer-facing technical findings; quality sacrificed for speed under pressure.

---

### 1.3 Meta-Analysis: Cross-Cutting Systemic Issues

Applying Gemba principles ("go and see"), the seven gaps reveal **four fundamental systemic problems:**

#### **1. Visibility & Observability Gaps**
- **What:** PG work is opaque to CSS; CSS status is opaque to customer; backend exceptions invisible to both.
- **Impact:** Gaps 1, 2, 4, 6 all stem from lack of real-time visibility into who owns what and what's happening.
- **Root:** No shared system of record for case state; each team has own view.

#### **2. Handoff & Routing Inefficiencies**
- **What:** Multiple handoffs between CSS engineers, between CSS and PG, between PG sub-teams.
- **Impact:** Gaps 2, 3, 5 caused by poor handoff protocols and symptom-based routing.
- **Root:** Tribal knowledge required; no intelligent routing based on root cause; manual handoffs prone to information loss.

#### **3. Quality vs. Speed Trade-offs Under Pressure**
- **What:** Urgency drives shortcuts (Gap 7); holiday staffing causes delays (Gap 1).
- **Impact:** Investigation errors, communication delays, customer trust erosion.
- **Root:** No forcing functions for quality checks; processes assume normal staffing year-round.

#### **4. Feedback Loop Failures**
- **What:** Same mistake happened twice (Gap 4 → Gap 6); no learning between occurrences.
- **Impact:** Repeated customer pain; perception of organizational incompetence.
- **Root:** No formal retrospectives; no closed-loop corrective action tracking.

---

## 2. Value Stream Mapping

### Current State Value Stream

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CUSTOMER EXPERIENCE                               │
└─────────────────────────────────────────────────────────────────────────┘
        ↓ (Customer reports issue)
┌─────────────────────────────────────────────────────────────────────────┐
│  CSS Initial Triage (Day 0-7)                                           │
│  • Log collection: 3 days                                                │
│  • Initial analysis: 2 days                                              │
│  • False path (2M char limit): 2 days                                   │
│  ⏱️ Lead Time: 7 days | Value-Add: 2 days | Waste: 5 days (71%)       │
└─────────────────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  CSS → PG Escalation (Day 7-15)                                         │
│  • ICM creation: 1 day                                                   │
│  • WAIT: PG log access: 2 days                                          │
│  • WAIT: PG initial review: 5 days (Holiday period, Gap 1)             │
│  ⏱️ Lead Time: 8 days | Value-Add: 1 day | Waste: 7 days (88%)        │
└─────────────────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  PG Investigation #1 - DLP Team (Day 15-30)                             │
│  • Analysis: 3 days                                                      │
│  • WAIT: Customer testing: 4 days                                       │
│  • WAIT: CSS comm delay (Gap 1): 7 days                                │
│  • ICM downgrade confusion (Gap 3): 1 day                               │
│  ⏱️ Lead Time: 15 days | Value-Add: 3 days | Waste: 12 days (80%)     │
└─────────────────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  PG Re-Escalation & Multi-ICM Confusion (Day 30-35)                     │
│  • 2nd ICM created (Sev 3→2): 1 day                                     │
│  • WAIT: PG non-response (Gap 4): 1.5 days                             │
│  • 3rd ICM created for Classification: 1 day                            │
│  • Team routing delays (Gap 5): 2 days                                  │
│  ⏱️ Lead Time: 5 days | Value-Add: 0 days | Waste: 5 days (100%)      │
└─────────────────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  PG Investigation #2 - Classification Team (Day 35-42)                  │
│  • WAIT: PG non-response (Gap 6): 2 days                               │
│  • Incorrect analysis (Gap 7): 1 day                                    │
│  • Correct analysis: 2 days                                              │
│  • Customer testing: 2 days                                              │
│  ⏱️ Lead Time: 7 days | Value-Add: 4 days | Waste: 3 days (43%)       │
└─────────────────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  CAT Engagement & Exception Discovery (Day 42-47)                       │
│  • CAT investigation: 2 days                                             │
│  • DISCOVERY: 100K unique-SIT exception: 1 day                          │
│  • Exception removal + monitoring: 2 days                                │
│  ⏱️ Lead Time: 5 days | Value-Add: 5 days | Waste: 0 days (0%)        │
└─────────────────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  Resolution & Mitigation (Day 47-54)                                     │
│  • Secure-By-Default preview deployment: 2 days                         │
│  • Customer validation: 3 days                                           │
│  • Case downgrade to Sev B: 1 day                                       │
│  • Monitoring period: 1 day                                              │
│  ⏱️ Lead Time: 7 days | Value-Add: 6 days | Waste: 1 day (14%)        │
└─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
TOTAL VALUE STREAM METRICS
───────────────────────────────────────────────────────────────────────────
Total Lead Time:              54 days
Total Value-Add Time:         21 days (39%)
Total Waste Time:             33 days (61%)

WASTE BREAKDOWN:
• Waiting (PG delays, holidays):      21 days (39%)
• Communication gaps:                   7 days (13%)
• Rework (wrong team, wrong analysis): 4 days (7%)
• Confusion (ICM routing, severity):    1 day (2%)
═══════════════════════════════════════════════════════════════════════════
```

### Value Stream Observations

**Major Waste Categories:**
1. **Waiting** (21 days, 39%): PG response delays, holiday staffing, customer testing cycles
2. **Communication Delays** (7 days, 13%): Gap 1 (CSS not relaying PG findings)
3. **Rework** (4 days, 7%): Wrong team engaged (Gap 5), wrong analysis (Gap 7)
4. **Confusion** (1 day, 2%): ICM severity changes (Gap 3)

**Critical Insight:**
Only **39% of time** was spent on value-adding investigation. **61% was waste**, primarily waiting on asynchronous handoffs between teams.

---

## 3. Process Improvement Opportunities

### 3.1 Quick Wins (0-30 days)

#### **QW-1: Automated Communication SLA Enforcement**
- **Problem:** Gaps 1, 4, 6 - PG findings not communicated, PG not responding
- **Solution:** Automated alerts when:
  - PG provides update but CSS hasn't communicated to customer within 24 hours
  - PG ICM assigned >24 hours (Sev 2) or >8 hours (Sev 1) without activity
- **Impact:** Eliminates 10-day communication delay (Gap 1); reduces PG non-response from 2+ days to <1 day
- **Owner:** CSS Engineering + ICM team
- **Effort:** Low (configure existing alerting systems)

#### **QW-2: Mandatory Tenant Validation Before Sharing Artifacts**
- **Problem:** Gap 7 - Incorrect SIT from different tenant shared with customer
- **Solution:** Checklist requirement: "Data pulled from tenant: [tenant ID] - Verified: ☑"
- **Impact:** Prevents customer-facing errors; builds trust
- **Owner:** PG Managers
- **Effort:** Low (process change + 5-minute training)

#### **QW-3: S500 Holiday Coverage Plan**
- **Problem:** Gap 1 - Holiday staffing caused 7-day delay
- **Solution:** Designated S500 case owners with no PTO during holiday periods; automated handoff protocols
- **Impact:** Eliminates holiday blackout periods for critical customers
- **Owner:** CSS Management
- **Effort:** Low (scheduling + coverage matrix)

---

### 3.2 Short-Term Improvements (30-90 days)

#### **ST-1: Explicit Case State Machine**
- **Problem:** Gap 2 - Contradictory communication due to unclear ownership
- **Solution:** Implement case status field with defined states:
  - `CUSTOMER_ACTION_REQUIRED`
  - `CSS_INVESTIGATING`
  - `PG_ASSIGNED_PENDING`
  - `PG_ACTIVELY_INVESTIGATING`
  - `WAITING_CUSTOMER_VALIDATION`
- **Rationale:** Forces explicit state transitions; eliminates interpretation of case notes
- **Impact:** Reduces handoff errors from ~15% to <5%
- **Owner:** CSS Engineering
- **Effort:** Medium (case management system modification)

#### **ST-2: Root-Cause-Based ICM Routing**
- **Problem:** Gap 5 - Classification team not engaged for 4 days due to symptom-based routing
- **Solution:** ICM tags for root cause (e.g., `classification-timeout`, `policy-config`, `enforcement-failure`)
  - Routing engine suggests owning team based on tags
  - Confidence score shown; manual override allowed with justification
- **Impact:** Reduces team-routing delays from 4 days to <1 day; engages right experts immediately
- **Owner:** ICM Engineering + PG Leadership
- **Effort:** Medium (ML-based routing model + tag taxonomy)

#### **ST-3: Severity Criteria Expansion for Security/Compliance**
- **Problem:** Gap 3 - ICM downgraded despite customer data exposure risk
- **Solution:** Add severity criteria:
  - **Sev 1:** Customer actively losing data OR service completely down
  - **Sev 2:** Customer at risk of losing data OR significant functionality impaired
  - Include "Customer Business Impact" field (mandatory for downgrades)
- **Impact:** Prevents inappropriate downgrades; maintains urgency for security cases
- **Owner:** ICM Governance + PG/CSS Leadership
- **Effort:** Medium (policy update + training)

#### **ST-4: Proactive SIT Performance Validation Tool**
- **Problem:** Technical root cause - unoptimized SITs caused timeouts
- **Solution:** Self-service SIT validator:
  - Regex performance scoring (backtracking risk, catastrophic patterns)
  - Proximity setting recommendations
  - Estimated classification time for sample documents
- **Rationale:** Shift left - catch SIT issues before production
- **Impact:** Reduces classification timeout incidents by 60-80%
- **Owner:** Classification PG + Developer Tools Team
- **Effort:** Medium (new tool development)

#### **ST-5: Configuration Exception Audit Dashboard**
- **Problem:** 100K unique-SIT exception was invisible, delaying root cause discovery
- **Solution:** Dashboard showing all tenant-level exceptions:
  - Exception type, reason, date applied, expiration
  - Alerts when exception is >6 months old (review required)
- **Impact:** Discovered critical exception in <1 day instead of 35 days
- **Owner:** PG Infrastructure Team
- **Effort:** Medium (backend query + UI dashboard)

---

### 3.3 Long-Term Systemic Changes (90-365 days)

#### **LT-1: Unified Case Orchestration Platform**
- **Problem:** Visibility gaps across CSS, PG, Customer; manual handoffs; tribal knowledge
- **Vision:** Single platform where:
  - Customer sees real-time case status (sanitized for external view)
  - CSS sees PG activity logs (who's investigating, last action time)
  - PG sees customer validation results automatically
  - AI suggests next best action based on case state
- **Impact:** Reduces lead time by 30-40%; eliminates handoff waste; improves customer trust
- **Owner:** CxP Engineering + Product Leadership (cross-org initiative)
- **Effort:** High (18-24 month program)

#### **LT-2: Intelligent TSG with Dynamic Decision Trees**
- **Problem:** Gap 5 - TSGs didn't guide to Classification team; tribal knowledge required
- **Vision:** AI-powered troubleshooting guide:
  - Starts with symptoms, asks diagnostic questions
  - Narrows to root cause category
  - Routes to correct team with confidence score
  - Continuously learns from case outcomes
- **Impact:** Reduces "wrong team" time from days to hours; democratizes expert knowledge
- **Owner:** Knowledge Management + AI/ML Teams
- **Effort:** High (12-18 months for MVP)

#### **LT-3: Continuous Learning System (Retrospectives + Closed-Loop Tracking)**
- **Problem:** Gap 4 repeated as Gap 6; no organizational learning
- **Vision:** Mandatory lightweight retrospective for all Sev A/B cases:
  - Auto-populated with timeline, gaps, customer sentiment
  - Identifies 1-3 systemic improvements
  - Improvements tracked to closure (Kanban board)
  - Monthly management review of improvement backlog
- **Impact:** Eliminates repeat occurrences of known issues; builds continuous improvement culture
- **Owner:** Quality/Process Excellence Team (new function)
- **Effort:** High (organizational change + tooling)

#### **LT-4: Secure-By-Default as Standard (Not Preview)**
- **Problem:** Feature that would have mitigated issue was in preview; customer hesitant to adopt
- **Vision:** Accelerate Secure-By-Default to GA:
  - Default-on for all DLP policies
  - Comprehensive documentation + migration guides
  - Proactive outreach to S500 customers
- **Impact:** Eliminates entire class of classification timeout bypasses; risk mitigation becomes default
- **Owner:** DLP Product Team
- **Effort:** High (6-9 months to GA)

---

## 4. Lessons Learned & Knowledge Sharing

### 4.1 Key Technical Learnings

#### **Learning 1: Hidden Configuration Exceptions Can Mask Product Issues**
- **What Happened:** 100K unique-SIT exception kept classification running far beyond normal limits
- **Why It Matters:** Backend exceptions are invisible to CSS and most PG; delays root cause identification
- **Knowledge Gap:** No documentation of when exceptions were applied or why; institutional knowledge lost
- **Share To:** CSS (awareness), PG (audit process), Customers (transparency on limits)

#### **Learning 2: Classification Timeout ≠ 2M Character Limit**
- **What Happened:** Initial investigation focused on 2M character limit as cause
- **Why It Matters:** Timeouts can occur before hitting character limit due to SIT complexity
- **Knowledge Gap:** CSS training emphasized character limit but not SIT performance factors
- **Share To:** CSS (updated training), TSG (updated troubleshooting path)

#### **Learning 3: Secure-By-Default Provides Last-Line Defense**
- **What Happened:** Feature allows enforcement action even when classification times out
- **Why It Matters:** Converts "fail open" (data leak) to "fail closed" (block on timeout)
- **Knowledge Gap:** Feature was in preview; not proactively recommended for at-risk customers
- **Share To:** All S500 DLP customers (proactive outreach campaign)

---

### 4.2 Key Process Learnings

#### **Learning 4: Holiday Periods Require Explicit Coverage Planning**
- **What Happened:** Gap 1 - PG findings sat uncommunicated for 7 days over holidays
- **Why It Matters:** S500 customers expect continuity regardless of internal staffing
- **Knowledge Gap:** No formal coverage plan; assumption that "someone" would handle it
- **Share To:** CSS Management (coverage SOPs), CSAMs (set customer expectations)

#### **Learning 5: ICM Severity Based on Service Availability Misses Security Risk**
- **What Happened:** Gap 3 - ICM downgraded because "service works" but customer data at risk
- **Why It Matters:** Security/compliance issues don't fit "service down" model but have severe customer impact
- **Knowledge Gap:** Severity criteria written for service reliability, not security scenarios
- **Share To:** ICM Governance (criteria expansion), All Engineers (training)

#### **Learning 6: Customer Sees Microsoft as One Company**
- **What Happened:** Multiple gaps (1, 2, 4, 6) all perceived by customer as "Microsoft not responding"
- **Why It Matters:** Internal team boundaries invisible to customer; delays compound frustration
- **Knowledge Gap:** CSS shields customer from PG delays but creates "black hole" perception
- **Share To:** CSS (transparency guidance), Leadership (cross-team accountability)

---

### 4.3 Knowledge Sharing Recommendations

#### **Documentation Updates Required:**

1. **TSG Update: DLP Enforcement Failures**
   - Add "Classification Timeout" as distinct path (not just 2M char limit)
   - Decision tree: Timeout → Check SIT complexity → Route to Classification team
   - Link to SIT optimization guide

2. **TSG Update: Classification Performance Troubleshooting**
   - New section: "Hidden Configuration Exceptions"
   - How to check for tenant-level exceptions (PG only)
   - Escalation path if exceptions found

3. **Public Documentation: SIT Best Practices**
   - Performance implications of regex patterns
   - Proximity setting guidance (default: 300 characters)
   - Self-service validation tool (when available)
   - Link to Secure-By-Default documentation

4. **Internal Playbook: S500 Case Management During Holidays**
   - Coverage matrix template
   - Automated handoff checklist
   - Escalation triggers (24h no update)

5. **ICM Severity Guide Update**
   - Expand Sev 2 criteria to include "customer data at risk"
   - Examples: DLP bypass, encryption failure, data leak scenarios
   - Mandatory "Customer Impact" field for downgrades

---

### 4.4 Training Recommendations

#### **CSS Training:**
- **Topic:** Classification Performance Troubleshooting (4-hour module)
  - SIT complexity factors (regex, proximity)
  - How to identify classification timeouts in logs
  - When to engage Classification vs. DLP teams
  - Configuration exception awareness (what to ask PG)

#### **PG Training:**
- **Topic:** Customer Communication Best Practices (2-hour workshop)
  - When to communicate directly vs. through CSS
  - Tenant validation before sharing artifacts (Gap 7 prevention)
  - Private Preview discussion protocols (CxE-led, not PG-led)

#### **Cross-Team Training:**
- **Topic:** Unified Case State Management (1-hour all-hands)
  - New case state definitions
  - Handoff protocols
  - Shared accountability for S500 cases

---

## 5. Metrics to Track Improvement Effectiveness

### 5.1 Leading Indicators (Predict Future Issues)

| Metric | Definition | Target | Baseline (Current State) | Frequency |
|--------|------------|--------|--------------------------|-----------|
| **SIT Validation Rate** | % of custom SITs run through performance validator before production | >80% | 0% (no tool) | Monthly |
| **Configuration Exception Age** | Avg. age of active tenant-level exceptions | <6 months | Unknown (no visibility) | Quarterly |
| **ICM Routing Accuracy** | % of ICMs assigned to correct team on first attempt | >90% | ~60% (based on Gap 5) | Weekly |
| **Case State Clarity Score** | % of cases with explicit state (vs. "interpret notes") | 100% | ~40% (based on Gap 2) | Daily |
| **Holiday Coverage Compliance** | % of S500 cases with designated holiday owner | 100% | Unknown | Pre-holiday audit |

---

### 5.2 Lagging Indicators (Measure Outcomes)

| Metric | Definition | Target | Baseline (Current State) | Frequency |
|--------|------------|--------|--------------------------|-----------|
| **Mean Time to Resolution (MTTR)** - S500 Sev A/B | Days from case open to resolution | <21 days (60% reduction) | 54 days (Desjardins) | Monthly |
| **Waste Ratio** | % of case time spent waiting/rework vs. value-add investigation | <30% | 61% (Value Stream Map) | Monthly |
| **Repeat Gap Rate** | % of cases with same gap type occurring >1x | 0% | 14% (Gap 4→6) | Quarterly |
| **Communication Delay Rate** | % of PG updates not communicated to customer within 24h | <5% | ~30% (based on Gap 1) | Weekly |
| **Customer Sentiment - S500** | Net Promoter Score for closed Sev A/B cases | >+20 | Negative (Desjardins) | Per case |
| **Incorrect Analysis Rate** | % of cases where wrong data shared (Gap 7 type errors) | <2% | Unknown (suspected 5-10%) | Quarterly |

---

### 5.3 Outcome Metrics (Business Impact)

| Metric | Definition | Target | Baseline (Current State) | Frequency |
|--------|------------|--------|--------------------------|-----------|
| **Classification Timeout Incident Rate** | # of Sev A/B cases due to classification timeouts | <5/year (80% reduction) | ~25/year (est.) | Quarterly |
| **S500 Escalations to EEE/CAT** | # of S500 cases requiring executive escalation | <10/year | Unknown | Quarterly |
| **Secure-By-Default Adoption Rate** | % of S500 customers with Secure-By-Default enabled | 100% | <5% (preview stage) | Monthly |
| **Customer Satisfaction - S500** | Avg. CSAT score for closed support cases | >4.5/5 | Unknown | Monthly |

---

### 5.4 Dashboard & Review Cadence

**Weekly:**
- ICM routing accuracy
- Case state clarity score
- Communication delay rate

**Monthly:**
- MTTR for Sev A/B cases
- Waste ratio trend
- SIT validation rate
- Secure-By-Default adoption

**Quarterly:**
- Configuration exception audit
- Repeat gap analysis
- Incorrect analysis rate
- All outcome metrics

**Annual:**
- Full value stream re-mapping
- Incident rate trends
- Customer satisfaction trends
- Improvement initiative ROI assessment

---

## 6. Actionable Recommendations Summary

### Priority 1: Immediate Action (This Week)

1. ✅ **Implement Tenant Validation Checklist** (QW-2)
   - Owner: PG Managers
   - Deliverable: 1-page checklist distributed to all PG engineers
   - Timeline: 3 days

2. ✅ **Create S500 Holiday Coverage Plan** (QW-3)
   - Owner: CSS Management
   - Deliverable: Coverage matrix for next holiday period
   - Timeline: 5 days

3. ✅ **Audit All Active Configuration Exceptions** (Related to ST-5)
   - Owner: PG Infrastructure
   - Deliverable: Spreadsheet of exceptions with justifications
   - Timeline: 7 days

---

### Priority 2: Sprint-Level (30 Days)

4. 🔄 **Deploy Automated Communication SLA Alerts** (QW-1)
   - Owner: CSS Engineering + ICM Team
   - Deliverable: Alerts for 24h PG silence, 24h CSS non-communication
   - Timeline: 2 weeks

5. 🔄 **Implement Explicit Case State Machine** (ST-1)
   - Owner: CSS Engineering
   - Deliverable: Case status field with 5 defined states + training
   - Timeline: 4 weeks

6. 🔄 **Update ICM Severity Criteria** (ST-3)
   - Owner: ICM Governance
   - Deliverable: Updated criteria including security/compliance risk
   - Timeline: 3 weeks (includes review + approval)

---

### Priority 3: Quarter Goals (90 Days)

7. 📅 **Build SIT Performance Validation Tool** (ST-4)
   - Owner: Classification PG + Dev Tools
   - Deliverable: MVP self-service validator (regex scoring + time estimation)
   - Timeline: 8 weeks

8. 📅 **Deploy Configuration Exception Dashboard** (ST-5)
   - Owner: PG Infrastructure
   - Deliverable: Dashboard showing tenant exceptions + auto-review alerts
   - Timeline: 6 weeks

9. 📅 **Implement Root-Cause-Based ICM Routing** (ST-2)
   - Owner: ICM Engineering + PG Leadership
   - Deliverable: Tag-based routing with ML suggestions (pilot program)
   - Timeline: 12 weeks

10. 📅 **Accelerate Secure-By-Default to GA** (LT-4)
    - Owner: DLP Product Team
    - Deliverable: GA release + S500 proactive outreach campaign
    - Timeline: 6-9 months (started now)

---

### Priority 4: Strategic Initiatives (6-18 Months)

11. 🚀 **Launch Unified Case Orchestration Platform** (LT-1)
    - Owner: CxP Engineering (Cross-Org)
    - Deliverable: Single platform for CSS/PG/Customer visibility
    - Timeline: 18-24 months

12. 🚀 **Build Intelligent TSG with AI-Powered Decision Trees** (LT-2)
    - Owner: Knowledge Management + AI/ML Teams
    - Deliverable: MVP dynamic TSG for DLP scenarios
    - Timeline: 12-18 months

13. 🚀 **Establish Continuous Learning System** (LT-3)
    - Owner: Quality/Process Excellence (New Team)
    - Deliverable: Mandatory retrospectives + closed-loop improvement tracking
    - Timeline: 6-12 months (cultural transformation)

---

## 7. Expected Benefits & ROI

### Quantifiable Impact (Based on Value Stream Analysis)

| Improvement Area | Current State | Target State | Impact | Confidence |
|------------------|---------------|--------------|--------|------------|
| **MTTR (Sev A/B Cases)** | 54 days | 21 days | 61% reduction | High |
| **Waste Ratio** | 61% | <30% | 31 points improvement | Medium |
| **Communication Delays** | 7 days | <1 day | 86% reduction | High |
| **Routing Delays** | 4 days | <1 day | 75% reduction | Medium |
| **Classification Timeout Incidents** | ~25/year | <5/year | 80% reduction | Medium |
| **S500 Executive Escalations** | Unknown | <10/year | Est. 60% reduction | Low |

---

### Financial ROI (Estimated Annual)

**Cost Avoidance:**
- Reduced CAT/EEE engagement: $500K/year (fewer escalations × $50K avg cost)
- CSS efficiency gains: $200K/year (30% reduction in Sev A/B handle time)
- Customer retention: $1-5M/year (preventing S500 churn due to poor support experience)

**Investment Required:**
- Quick Wins (QW-1 to QW-3): $50K (mostly process, minimal engineering)
- Short-Term (ST-1 to ST-5): $500K (moderate tool development)
- Long-Term (LT-1 to LT-4): $2-3M (major platform builds)

**Net ROI (3-Year):**
- Investment: ~$3.5M
- Benefit: ~$6-9M (cost avoidance + retention)
- ROI: 170-250%

---

### Intangible Benefits

- **Customer Trust:** Elimination of Gaps 2, 7 (contradictory comms, wrong data) rebuilds credibility
- **Employee Satisfaction:** Reduction in firefighting; engineers work on value-add investigation vs. coordination overhead
- **Organizational Learning:** Continuous improvement culture; systemic issues addressed at root cause
- **Competitive Differentiation:** Best-in-class support experience for S500 customers

---

## 8. Conclusion & Call to Action

### What We Learned

This Gemba analysis of the Desjardins case reveals that **the escalation was not caused by a single failure, but by a cascade of seven process gaps compounding over 54 days**. Applying the 5 Whys methodology exposed four systemic root causes:

1. **Visibility Gaps** - Teams operate in silos without shared context
2. **Handoff Inefficiencies** - Tribal knowledge + manual processes cause delays
3. **Quality vs. Speed Trade-offs** - Urgency drives shortcuts that erode trust
4. **Feedback Loop Failures** - No organizational learning from repeated mistakes

Value stream mapping quantified the waste: **only 39% of time was value-adding investigation; 61% was waiting, rework, and confusion.**

---

### What Success Looks Like

**In 30 Days:**
- Zero cases where PG findings sit uncommunicated for >24 hours
- Zero customer-facing artifacts shared without tenant validation
- 100% of S500 cases have holiday coverage plans

**In 90 Days:**
- MTTR for Sev A/B cases drops from 54 to <35 days (35% improvement)
- Classification timeout cases routed to correct team in <1 day (vs. 4 days)
- All S500 customers proactively offered Secure-By-Default

**In 12 Months:**
- MTTR for Sev A/B cases drops to <21 days (60% improvement)
- 80% of custom SITs validated before production
- Zero repeat occurrences of known gap types
- Customer satisfaction for S500 support >4.5/5

---

### Immediate Next Steps (This Week)

**For Leadership:**
1. Review this analysis with cross-functional team (CSS, PG, CxP)
2. Approve Priority 1 recommendations (QW-2, QW-3, Exception Audit)
3. Assign executive sponsors for Priority 2 & 3 initiatives
4. Schedule monthly Gemba walks to "go and see" case management in action

**For Engineering Teams:**
1. Implement tenant validation checklist (PG)
2. Configure communication SLA alerts (CSS Engineering + ICM)
3. Create holiday coverage matrix (CSS Management)
4. Begin audit of configuration exceptions (PG Infrastructure)

**For Process Excellence:**
1. Establish metrics dashboard (Section 5)
2. Schedule weekly review of leading indicators
3. Plan first retrospective workshop for recent Sev A/B cases
4. Begin documentation updates (TSGs, severity criteria)

---

### Final Reflection: The Gemba Spirit

True Gemba practice means **going to where the work happens, observing with fresh eyes, and asking "why" until we reach systemic root causes**. This analysis is not about blame—it's about learning. Every gap identified represents an opportunity to build a better system that serves our customers and empowers our teams.

The Desjardins case taught us that **excellence in support is not about heroics; it's about systems**. When we eliminate waste, create visibility, and enable continuous learning, we transform reactive firefighting into proactive problem prevention.

**Let's commit to that transformation.**

---

**Document Information:**
- **Analysis Completed:** February 5, 2026
- **Methodology:** Gemba Walk + 5 Whys + Value Stream Mapping
- **Frameworks Referenced:** DIVE, Problem Solving Report (PSR), Kaizen
- **Analyst:** AI-Assisted Continuous Improvement Specialist
- **Review Status:** Draft for Leadership Review

---

**Appendix A: Referenced Documents**
- Incident Analysis Document: 2512120040008759 Incident Analysis - Desjardins.mht
- Gemba Process Guidelines: grounding_docs/continuous_improvement/Gemba Process.txt
- Problem Solving Framework: grounding_docs/continuous_improvement/intro_problem_solving.txt

**Appendix B: Related ICMs**
- ICM 723169126 (Initial escalation, Sev 3→2→5)
- ICM 21000000837036 (DLP Team, Sev 3→2→A)
- ICM 21000000859258 (Classification Team, CFL)

