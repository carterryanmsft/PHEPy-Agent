# Purview Operations & Governance – Operational Rhythms Reference

**Last Updated:** February 4, 2026  
**Status:** Active  
**Owner:** PHE Operations / Purview ROB Team

---

## Executive Summary

This document captures the operational rhythms, governance cadences, and key meetings for Purview Product Health & Escalation (PHE) operations. It covers ROB (Rhythm of Business) calendar alignment, Weekly Support Reviews (WSR/WSuR), Voice of Customer (VoC/MBR), Shiprooms, and IC/MCS case risk reviews.

**Purpose:** Enable orchestrator agent and sub-agents to understand operational context, meeting schedules, deliverable expectations, and cross-functional touchpoints.

---

## 1. DSCGP ROB Calendar & Series

### Overview
The DSCGP (Data Security & Compliance Governance Program) ROB Calendar is the primary operational rhythm for Purview governance, planning, and cross-team alignment.

### Key Activities
- **Purview WSR Scheduling:** Weekly Support Review timing aligned to ROB calendar
- **Paper Planning:** Quarterly and monthly planning cycles
- **Cross-Team Discussions:** Alignment with CSS, Engineering, PM, Data Science
- **Governance Reviews:** Leadership checkpoints, go/no-go decisions

### Meeting Series
- **DSCGP WSR Series:** Weekly cadence, alternating focus areas
- **Purview Review Workflows:** Embedded in WSuR and Purview planning
- **ROB Planning Sessions:** Quarterly business reviews, roadmap alignment

### Email References
Multiple emails reference:
- DSCGP WSuR scheduling adjustments
- ROB calendar updates
- Cross-functional dependencies
- Planning cycles and paper deadlines

### Orchestrator Usage
**Relevant Sub-Agents:**
- Program Onboarding Manager (for planning cycles)
- Tenant Health Monitor (for governance checkpoints)
- Contacts & Escalation Finder (for ROB meeting attendees)

**Query Patterns:**
- "What's the next DSCGP ROB checkpoint?"
- "When is the next Purview planning cycle?"
- "Who attends DSCGP WSR?"

---

## 2. WSR Operations, Data Updates & Scorecards

### Overview
Weekly Support Review (WSR) Scorecard is the primary health dashboard for Purview support operations. Tracks SLA compliance, case metrics, escalation trends, and customer health.

### WSR Scorecard Components

#### A. Regular Updates
**Frequency:** Weekly (every Thursday or Friday)  
**Distribution:** PHE team, CSS leads, Engineering, PM

**Notification Examples:**
- WSR Scorecard Update notifications (weekly)
- Data dips and spikes analysis
- UI/dashboard changes
- Metric realignment announcements

#### B. Key Metrics Tracked
1. **SLA Compliance:**
   - Initial Time to Engagement (TTE)
   - Time to Mitigation (TTM)
   - Days to Close (DTC)
   - SLA breach rate

2. **Case Volume & Trends:**
   - Total open cases
   - New cases (week over week)
   - Aged cases (> 14 days, > 30 days)
   - Case severity distribution

3. **Escalation Metrics:**
   - ICM incident count
   - Critical situation (crit sit) cases
   - Transfer case rate
   - VIP customer issues

4. **Customer Health:**
   - Support Health Index (SHI v2) scores
   - Intensive care nominations
   - Tenant risk flags

5. **Product-Specific Metrics:**
   - MIP/DLP metrics
   - eDiscovery metrics
   - DLM metrics
   - Insider Risk metrics

#### C. Operational Changes Tracked
Recent examples include:
- **Target Realignment with CSS:** Updated SLA targets to align with CSS org changes
- **IPD/SHS Metric Changes:** Incident Priority/Support Health Score adjustments
- **SAP Path Transitions:** Service Access Point routing updates
- **Drilldown Dashboard Updates:** New drill-down capabilities in WSR dashboard
- **Data Dips & Spikes:** Explanations for anomalies (holidays, releases, incidents)
- **UI Changes:** Dashboard redesigns, new visualizations
- **SLA Notes:** Clarifications on SLA calculations and exceptions
- **Supportability Insights:** Product readiness and known issue tracking

### WSR Scorecard Distribution
**Owner:** WSR Data Lead  
**Recipients:** PHE PM, Escalation Owners, CSS Managers, Engineering Leads  
**Archive:** SharePoint / Teams channel  
**Access:** Restricted to PHE team + stakeholders

### Orchestrator Usage
**Relevant Sub-Agents:**
- Support Case Manager (SLA tracking, case metrics)
- Escalation Manager (ICM trends, escalation patterns)
- Tenant Health Monitor (SHI scores, customer health)
- Work Item Manager (supportability insights, bug tracking)

**Query Patterns:**
- "What's the current SLA compliance rate?"
- "Are there any data spikes this week?"
- "Show me the latest WSR scorecard"
- "What metrics changed in the last WSR update?"

---

## 3. Purview WSR Planning & Narrative

### Overview
Weekly prep and narrative development for Purview WSR presentations. Captures support health story, escalations, risks, and next actions.

### Narrative Components
1. **Executive Summary:**
   - Overall support health (Green/Yellow/Red)
   - Key trends (improving, stable, declining)
   - Top risks and escalations

2. **Case Highlights:**
   - At-risk cases (SLA breach imminent)
   - VIP customer issues
   - Aged cases requiring attention
   - Critical severity updates

3. **Product Health:**
   - Known issues impacting support
   - Feature readiness and rollout status
   - Bug fix ETAs
   - Workaround availability

4. **Escalation Deep-Dives:**
   - Active ICM incidents
   - Customer impact assessment
   - Mitigation plans
   - Leadership engagement needed

5. **Trends & Insights:**
   - Week-over-week changes
   - Root cause patterns
   - Process improvements
   - Training needs

### Planning Cadence
- **Monday:** Data refresh, preliminary analysis
- **Tuesday:** Narrative draft, stakeholder input
- **Wednesday:** Review & refinement, leadership preview
- **Thursday/Friday:** WSR presentation & distribution

### Orchestrator Usage
**Relevant Sub-Agents:**
- All sub-agents contribute to narrative
- Program Onboarding Manager (cohort status)
- Purview Product Expert (product health)
- Support Case Manager (case highlights)
- Escalation Manager (escalation deep-dives)

**Query Patterns:**
- "Generate WSR executive summary for this week"
- "What are the top 3 risks for WSR?"
- "Summarize escalation trends for narrative"

---

## 4. WSR Prep Meetings

### Overview
Weekly prep meetings to align on WSR content, review data, and prepare presentations.

### Meeting Structure
**Frequency:** Weekly (Tuesday or Wednesday)  
**Duration:** 1 hour  
**Attendees:** PHE PM, Escalation Owner, Sub-Agent Owners, WSR Data Lead

**Agenda:**
1. Review WSR scorecard data (15 min)
2. Identify at-risk cases and escalations (15 min)
3. Review narrative draft (15 min)
4. Assign follow-up actions (10 min)
5. Preview questions from leadership (5 min)

### Pre-Work
- [ ] WSR scorecard data refreshed
- [ ] SHI v2 scores updated
- [ ] ICM incidents reviewed
- [ ] Narrative draft prepared (80% complete)

### Deliverables
- Finalized WSR narrative
- Presentation deck (if applicable)
- Action item list
- Follow-up assignments

### Orchestrator Usage
**Relevant Sub-Agents:**
- All sub-agents provide input for their domain

**Query Patterns:**
- "Prepare WSR prep meeting summary"
- "What action items came out of last WSR prep?"
- "Generate pre-read for WSR prep meeting"

---

## 5. Monthly CXE/DSCGP Voice of Customer MBR

### Overview
Monthly Business Review (MBR) focused on Voice of Customer (VoC) feedback, customer sentiment, and program health. Cross-functional review with CXE (Customer Experience Engineering) and DSCGP stakeholders.

### VoC MBR Components

#### A. Customer Feedback
- NPS (Net Promoter Score) trends
- CSAT (Customer Satisfaction) scores
- Verbatim feedback from surveys
- Support case sentiment analysis
- Escalation feedback

#### B. Program Health
- MCS/IC cohort health
- Catalyst program performance
- Intensive care outcomes
- Customer success stories

#### C. Product & Feature Feedback
- Feature requests from customers
- Pain points and friction areas
- Adoption barriers
- Usability issues

#### D. Escalation & Risk Review
- High-impact escalations
- Customer churn risk
- Relationship health
- Executive sponsor engagement

#### E. Action Items & Follow-Up
- Prioritized improvement backlog
- Product roadmap alignment
- Process improvements
- Communication enhancements

### Meeting Cadence
**Frequency:** Monthly (first week of month)  
**Duration:** 2 hours  
**Attendees:** CXE Leadership, DSCGP Leadership, PHE PM, Product Managers, CSS Managers

### Deliverables
- VoC MBR deck (slides + data)
- Executive summary (1-pager)
- Action item register
- Follow-up assignments

### Orchestrator Usage
**Relevant Sub-Agents:**
- Program Onboarding Manager (cohort feedback)
- Tenant Health Monitor (customer health trends)
- Escalation Manager (escalation impact)
- Support Case Manager (case sentiment)

**Query Patterns:**
- "Summarize VoC feedback for this month"
- "What are top customer pain points?"
- "Generate VoC MBR executive summary"
- "Track VoC action items from last MBR"

---

## 6. VoC Organizational Shifts

### Overview
Ongoing restructuring of Voice of Customer program to improve feedback loops, program alignment, and customer advocacy.

### Recent Changes
- **VoC Program Ownership:** Shifted to CXE organization
- **Feedback Collection:** Consolidated survey tools and cadences
- **Cross-Functional Integration:** Embedded VoC in WSR, MBR, and ROB rhythms
- **Action Item Tracking:** Unified backlog for VoC improvements
- **Leadership Engagement:** Increased exec sponsorship and visibility

### Implications for PHE
- **Closer Alignment:** PHE support metrics integrated into VoC MBR
- **Customer Advocacy:** PHE represents customer voice in product discussions
- **Escalation Feedback:** Post-escalation surveys and NPS tracking
- **Program Improvements:** VoC insights drive PHE process changes

### Orchestrator Usage
**Relevant Sub-Agents:**
- Program Onboarding Manager (VoC integration into cohort reviews)
- Contacts & Escalation Finder (VoC program leads and contacts)

**Query Patterns:**
- "Who owns VoC program now?"
- "What VoC changes impact PHE?"
- "How do we submit VoC feedback?"

---

## 7. DSCGP WSuR Meeting Series

### Overview
Weekly Sync WSuR (Weekly Support Update Review) is the regional/DSCGP-specific variant of WSR. Covers broader DSCGP portfolio beyond Purview.

### Meeting Structure
**Frequency:** Weekly  
**Duration:** 1 hour  
**Attendees:** DSCGP PM leads, CSS managers, Engineering representatives, PHE team

**Agenda:**
1. DSCGP portfolio health (all products)
2. Cross-product escalations
3. Regional support issues
4. Resource allocation & staffing
5. Process improvements

### Purview Segment
Purview typically has 10-15 min dedicated segment in WSuR:
- Purview-specific metrics
- Escalations and at-risk cases
- Known issues and mitigations
- Upcoming releases and readiness

### Recent WSuR Summaries
Multiple detailed summary emails from Jan 2026 WSuR sessions include:
- Escalation trends across DSCGP portfolio
- Support staffing updates
- Process improvement initiatives
- Cross-team dependencies

### Task Assignments
WSuR documents include newly assigned tasks and content obligations:
- Data updates required
- Escalation investigations
- Process documentation
- Cross-team coordination

### Orchestrator Usage
**Relevant Sub-Agents:**
- Program Onboarding Manager (DSCGP portfolio context)
- Escalation Manager (cross-product escalations)
- Contacts & Escalation Finder (DSCGP contacts)

**Query Patterns:**
- "What's the DSCGP WSuR agenda for this week?"
- "Summarize Purview segment from last WSuR"
- "What tasks were assigned in WSuR?"

---

## 8. WSuR Staging Verification Meeting

### Overview
Dedicated sync meeting to verify WSuR staging environment, data pipelines, and dashboard readiness before production updates.

### Meeting Purpose
- **Data Quality:** Verify metrics accuracy in staging
- **UI Changes:** Review dashboard updates before prod release
- **Regression Testing:** Ensure no breaks in existing functionality
- **Stakeholder Approval:** Get sign-off before prod deployment

### Meeting Cadence
**Frequency:** As needed (typically before major WSuR updates)  
**Duration:** 30 min  
**Attendees:** WSuR Data Lead, Engineering, PHE PM, QA

### Orchestrator Usage
**Relevant Sub-Agents:**
- Tenant Health Monitor (data accuracy validation)
- Support Case Manager (metric verification)

**Query Patterns:**
- "When is the next WSuR staging verification?"
- "Are there any staging issues to resolve?"

---

## 9. Support Shiprooms (MIP/DLP)

### Overview
Bi-weekly or weekly shiprooms for Microsoft Information Protection (MIP) and Data Loss Prevention (DLP) support operations. Focuses on customer issue triage, bug prioritization, readiness, and escalations.

### Shiproom Agenda
1. **Customer Issue Triage (30 min):**
   - Active escalations review
   - At-risk cases discussion
   - Customer impact assessment
   - Mitigation plans

2. **Bug List Review (20 min):**
   - Critical bugs blocking customers
   - Fix status and ETA
   - Workaround availability
   - Prioritization changes

3. **Readiness & Rollout (10 min):**
   - Upcoming feature releases
   - Known issues and mitigations
   - Support readiness checklist
   - Training needs

4. **Action Items & Follow-Up (10 min):**
   - Assigned owners
   - Deadlines
   - Escalation paths

### Meeting Cadence
**Frequency:** Bi-weekly (typically Monday or Tuesday)  
**Duration:** 1 hour  
**Attendees:** MIP/DLP Engineering, PHE PM, CSS Managers, Escalation Owner

### Deliverables
- Shiproom notes (OneNote or Teams)
- Bug priority list
- Escalation summary
- Action item tracker

### Orchestrator Usage
**Relevant Sub-Agents:**
- Purview Product Expert (bug status, known issues)
- Work Item Manager (bug tracking, fix ETA)
- Escalation Manager (customer impact)
- Support Case Manager (at-risk cases)

**Query Patterns:**
- "What's on the agenda for next MIP/DLP shiproom?"
- "Summarize bug list from last shiproom"
- "Are there any readiness concerns for upcoming release?"

---

## 10. DLM Support Shiproom

### Overview
Data Lifecycle Management (DLM) support shiproom covering retention, holds, disposal, and compliance scenarios.

### Shiproom Focus Areas
- **Retention Policies:** Configuration issues, policy conflicts
- **Legal Holds:** Hold placement, removal, scope verification
- **Disposal:** Deletion failures, compliance violations
- **Compliance:** Audit readiness, record retention
- **Customer Escalations:** DLM-specific at-risk cases

### Meeting Cadence
**Frequency:** Bi-weekly  
**Duration:** 1 hour  
**Attendees:** DLM Engineering, PHE PM, Compliance team, CSS Managers

### Orchestrator Usage
**Relevant Sub-Agents:**
- Purview Product Expert (DLM feature knowledge)
- Work Item Manager (DLM bug tracking)
- Support Case Manager (DLM case review)

**Query Patterns:**
- "What DLM issues are being discussed in shiproom?"
- "Are there any DLM compliance concerns?"

---

## 11. eDiscovery Support Shiproom

### Overview
eDiscovery shiproom includes full deck with metrics, customer escalations, and case performance analysis.

### Shiproom Components
1. **Metrics Dashboard:**
   - Collection performance (TB processed, time to complete)
   - Search performance (query latency, result accuracy)
   - Hold compliance (hold placement rate, hold scope)
   - Export performance (export success rate, time to export)

2. **Customer Escalations:**
   - Active eDiscovery escalations
   - At-risk legal holds
   - Performance issues (large collections, slow queries)
   - Data integrity concerns

3. **Case Performance:**
   - Average case size (GB, item count)
   - Time to first production (collection → export)
   - Custodian count trends
   - Review set usage

4. **Upcoming Features:**
   - New eDiscovery capabilities
   - Preview releases
   - Support readiness

### Meeting Cadence
**Frequency:** Bi-weekly  
**Duration:** 1 hour  
**Attendees:** eDiscovery Engineering, PHE PM, Legal/Compliance, CSS Managers

### Orchestrator Usage
**Relevant Sub-Agents:**
- Purview Product Expert (eDiscovery feature knowledge)
- Escalation Manager (eDiscovery escalations)
- Tenant Health Monitor (eDiscovery adoption & performance)

**Query Patterns:**
- "Summarize eDiscovery shiproom metrics"
- "What eDiscovery escalations are active?"
- "Are there any eDiscovery performance issues?"

---

## 12. Shiproom Triage, Case Hygiene, Escalation Quality

### Overview
Cross-cutting initiatives to improve shiproom effectiveness, case hygiene, and escalation quality. Feeds into all shiprooms.

### Key Initiatives

#### A. Shiproom Triage Process
- **Pre-Shiproom Prep:** Cases reviewed 24h before shiproom
- **Risk Scoring:** Cases ranked by impact + urgency
- **Data Validation:** Metrics verified for accuracy
- **Action Item Hygiene:** Outstanding items reviewed & closed

#### B. Case Hygiene Standards
- **Case Tagging:** Proper categorization (product, severity, customer segment)
- **Case Aging:** Cases > 14 days flagged for review
- **Case Ownership:** Clear owner assigned, no orphaned cases
- **Case Updates:** Regular customer communication (every 3 days minimum)
- **Case Closure:** Resolution notes complete, root cause documented

#### C. Escalation Quality
- **Escalation Criteria:** Clear thresholds for escalation (SLA, VIP, systemic)
- **Escalation Documentation:** Complete context, impact assessment, timeline
- **Escalation Tracking:** From open → mitigation → resolution → closure
- **Escalation Feedback:** Post-escalation review, lessons learned
- **Escalation Metrics:** Escalation rate, time to mitigation, customer satisfaction

### Orchestrator Usage
**Relevant Sub-Agents:**
- Support Case Manager (case hygiene enforcement)
- Escalation Manager (escalation quality tracking)
- Work Item Manager (action item tracking)

**Query Patterns:**
- "Are there any case hygiene issues?"
- "What's the escalation quality score?"
- "Identify cases missing proper tagging"

---

## 13. IC/MCS Case Risk Reviews

### Overview
Intensive Care (IC) and Mission Critical Service (MCS) case risk reviews focus on high-risk customers requiring proactive engagement and escalation management.

### IC/MCS Program Overview
- **Intensive Care:** Customers with severe support health issues (SHI < 40)
- **Mission Critical Service:** High-revenue or strategic customers with elevated support
- **Case Risk Reviews:** Weekly review of IC/MCS cases to identify and mitigate risks

### Meeting Structure
**Frequency:** Weekly  
**Duration:** 1 hour  
**Attendees:** IC/MCS PM, Escalation Owner, CSS Managers, PHE team

**Agenda:**
1. **IC/MCS Tenant Health Review (20 min):**
   - SHI v2 scores for IC/MCS tenants
   - Risk trends (improving, stable, declining)
   - New IC nominations
   - Exit readiness (return to health)

2. **Case-Level Risk Review (30 min):**
   - At-risk cases (SLA breach, aged, VIP)
   - Escalation status (ICM incidents)
   - Mitigation plans
   - Resource needs (staffing, engineering support)

3. **Customer Engagement (10 min):**
   - Recent customer communications
   - Escalation feedback
   - Relationship health
   - Executive sponsor involvement

4. **Action Items (10 min):**
   - Assigned owners
   - Deadlines
   - Follow-up reviews

### Case Risk Email Threads
You are explicitly included in case-risk email threads covering:
- Individual IC/MCS tenant risk assessments
- Escalation triage flows
- Cross-functional coordination (CSS, Engineering, PM)
- Leadership updates

### Orchestrator Usage
**Relevant Sub-Agents:**
- Program Onboarding Manager (IC/MCS cohort health)
- Tenant Health Monitor (SHI v2 tracking, exit readiness)
- Support Case Manager (at-risk case identification)
- Escalation Manager (ICM incident management)
- Contacts & Escalation Finder (escalation routing)

**Query Patterns:**
- "Which IC/MCS tenants are at risk this week?"
- "Summarize case risk for [Tenant X]"
- "Are any IC tenants ready to exit?"
- "What escalations impact IC/MCS customers?"

---

## 14. Ford Gemba Walk (Customer Engagement Example)

### Overview
Gemba Walk is a lean practice of "going to the place where work happens" to understand processes, identify issues, and engage directly with customers. Ford Gemba Walk is an example IC/MCS customer engagement.

### Gemba Walk Structure
1. **Preparation:**
   - Customer background, support history, escalations
   - Current health (SHI v2 score, case status)
   - Key stakeholders (customer PM, CSS, technical leads)

2. **Execution:**
   - On-site or virtual customer meeting
   - Walkthrough of support experience
   - Identify pain points and friction areas
   - Capture feedback and action items

3. **Incorporation into WSR:**
   - Gemba Walk findings summarized in WSR narrative
   - Action items tracked in WSR prep meetings
   - Follow-up engagement planned

### Orchestrator Usage
**Relevant Sub-Agents:**
- Program Onboarding Manager (Gemba Walk planning & follow-up)
- Tenant Health Monitor (customer health context)
- Support Case Manager (case history review)

**Query Patterns:**
- "Prepare Gemba Walk brief for [Customer X]"
- "What were the findings from Ford Gemba Walk?"
- "Track Gemba Walk action items"

---

## Operational Rhythms Summary

| Meeting/Activity | Frequency | Duration | Primary Owner | Orchestrator Sub-Agents |
|-----------------|-----------|----------|---------------|------------------------|
| **DSCGP ROB Calendar** | Quarterly/Monthly | Varies | DSCGP PM | Program Onboarding, Contacts Finder |
| **WSR Scorecard Update** | Weekly | 30 min | WSR Data Lead | Support Case, Escalation, Tenant Health |
| **WSR Planning & Narrative** | Weekly | 2 hours | PHE PM | All Sub-Agents |
| **WSR Prep Meeting** | Weekly | 1 hour | PHE PM | All Sub-Agents |
| **VoC MBR** | Monthly | 2 hours | CXE Leadership | Program Onboarding, Tenant Health, Escalation |
| **DSCGP WSuR** | Weekly | 1 hour | DSCGP PM | Program Onboarding, Escalation, Contacts Finder |
| **WSuR Staging Verification** | As Needed | 30 min | WSuR Data Lead | Tenant Health, Support Case |
| **MIP/DLP Shiproom** | Bi-weekly | 1 hour | MIP/DLP Engineering | Purview Expert, Work Item, Escalation, Support Case |
| **DLM Shiproom** | Bi-weekly | 1 hour | DLM Engineering | Purview Expert, Work Item, Support Case |
| **eDiscovery Shiproom** | Bi-weekly | 1 hour | eDiscovery Engineering | Purview Expert, Escalation, Tenant Health |
| **IC/MCS Case Risk Review** | Weekly | 1 hour | IC/MCS PM | Program Onboarding, Tenant Health, Support Case, Escalation |

---

## Key Contacts

| Role | Name | Responsibility |
|------|------|----------------|
| **DSCGP PM Lead** | [TBD] | ROB Calendar, WSuR coordination |
| **WSR Data Lead** | [TBD] | Scorecard updates, data quality |
| **PHE PM** | [Your Name] | WSR narrative, prep meetings, shiprooms |
| **Escalation Owner** | [TBD] | IC/MCS reviews, escalation quality |
| **CXE VoC Lead** | [TBD] | VoC MBR, customer feedback |
| **MIP/DLP Engineering** | [TBD] | MIP/DLP shiproom, bug prioritization |
| **DLM Engineering** | [TBD] | DLM shiproom, compliance issues |
| **eDiscovery Engineering** | [TBD] | eDiscovery shiproom, performance |

---

## References & Resources

### Documentation
- DSCGP ROB Calendar: [Link TBD]
- WSR Scorecard Dashboard: [Link TBD]
- VoC MBR Archive: [Link TBD]
- Shiproom Notes Repository: [Link TBD]
- IC/MCS Case Risk Tracker: [Link TBD]

### Related Grounding Docs
- `shi_v2_support_health_index.md` – SHI v2 scoring model
- `mcs_ic_cohort_registry.md` – IC/MCS cohort definitions
- `dfm_sla_definitions.md` – SLA thresholds & rules
- `phe_playbooks.md` – Escalation & case management playbooks

---

**Last Updated:** February 4, 2026  
**Owner:** PHE Operations / Purview ROB Team  
**Status:** ✅ Active
