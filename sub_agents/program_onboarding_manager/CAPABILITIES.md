# Program Onboarding Manager - Capabilities Matrix

**Agent:** Program Onboarding Manager  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 🎯 Core Capabilities

### 1. Cohort Lifecycle Management

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Cohort Progress Tracking** | Track onboarding phase and milestone completion | Cohort registry | ✅ Ready |
| **Timeline Management** | Monitor against planned timeline | Grounding docs | ✅ Ready |
| **Tenant Membership** | Manage which tenants are in which cohorts | Cohort registry | ✅ Ready |
| **Phase Transitions** | Track Discover → Plan → Implement → Optimize | Onboarding runbook | ✅ Ready |
| **Completion Percentage** | Calculate % complete per cohort | Milestone tracking | ✅ Ready |

### 2. Onboarding Execution & Validation

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Runbook Validation** | Check execution against standard runbook | Grounding docs | ✅ Ready |
| **Gate Sign-Off Tracking** | Validate completion of required gates | Milestone docs | ✅ Ready |
| **Deliverable Checklist** | Track completion of required deliverables | Onboarding templates | ✅ Ready |
| **Risk Assessment** | Identify at-risk onboardings | Multi-source | ✅ Ready |
| **Blocker Identification** | Flag technical and operational blockers | Issue tracking | ✅ Ready |

### 3. Customer Communication Management

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Template Activation** | Apply appropriate comms template | Comms library | ✅ Ready |
| **Cadence Tracking** | Monitor communication frequency | Comms tracking | ✅ Ready |
| **Engagement Monitoring** | Track customer responsiveness | Email/meeting data | ✅ Ready |
| **Escalation Alerts** | Flag communication gaps | Activity tracking | ✅ Ready |

### 4. Go-Live Readiness Assessment

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Pre-Go-Live Checklist** | Validate readiness criteria | Grounding docs | ✅ Ready |
| **Customer Confidence Score** | Assess customer readiness | Survey/feedback | ✅ Ready |
| **Technical Validation** | Confirm configuration complete | Tenant health | ✅ Ready |
| **Rollback Planning** | Ensure rollback plan exists | Grounding docs | ✅ Ready |
| **Post-Go-Live Review** | Capture lessons learned | Retrospective | ✅ Ready |

---

## 📊 Onboarding Phases & Milestones

### Phase 1: Discover (Weeks 1-2)

**Milestones:**
- Customer discovery call complete
- Current state assessment documented
- Success criteria agreed upon
- Cohort assignment confirmed

**Deliverables:**
- Discovery document
- Success metrics definition
- Risk assessment initial

### Phase 2: Plan (Weeks 3-4)

**Milestones:**
- Deployment architecture designed
- Policy framework defined
- Pilot group identified
- Timeline agreed with customer

**Deliverables:**
- Deployment plan
- Policy design document
- Pilot plan
- Communication plan

### Phase 3: Implement (Weeks 5-8)

**Milestones:**
- Tenant configured
- Policies deployed to pilot
- Pilot feedback collected
- Production rollout plan approved

**Deliverables:**
- Configuration documentation
- Pilot results report
- Rollout schedule
- Training materials

### Phase 4: Optimize (Weeks 9-12)

**Milestones:**
- Full production deployment
- Adoption metrics tracked
- False positive tuning complete
- Customer sign-off received

**Deliverables:**
- Production readiness report
- Adoption dashboard
- Optimization recommendations
- Completion certificate

---

## 🚦 Cohort Health Status

| Status | Criteria | Action Required |
|--------|----------|-----------------|
| 🟢 **On Track** | All milestones on schedule, no blockers | Continue monitoring |
| 🟡 **At Risk** | 1-2 milestones delayed, minor blockers | Increase PM engagement |
| 🟠 **Delayed** | 3+ milestones delayed, major blockers | Active intervention, escalation |
| 🔴 **Critical** | Timeline at risk, go-live in jeopardy | Executive escalation, timeline reset |
| ✅ **Complete** | All milestones achieved, customer sign-off | Transition to BAU monitoring |

---

## 📋 Success Metrics Per Cohort

### Adoption Metrics
- Active users at week 12: >80% of licensed users
- Policies deployed: All core policies (MIP, DLP, Retention)
- Label coverage: >60% of content labeled
- DLP incidents: <5% false positive rate

### Support Metrics
- SLA compliance: >95%
- Escalations: <2 per tenant during onboarding
- Reopened cases: <10%

### Timeline Metrics
- On-time go-live: Week 12 ±1 week
- Milestone completion: >90% on schedule
- Unplanned delays: <2 weeks total

### Customer Satisfaction
- Customer confidence score: >4/5 at go-live
- Post-go-live NPS: >8/10
- Renewal/expansion intent: Documented

---

## 🚫 Out of Scope

This agent **does NOT**:
- Execute technical configuration (coordinates, doesn't implement)
- Make go-live decisions unilaterally (requires PM + customer sign-off)
- Provide product roadmap or unreleased feature commitments
- Handle contract or licensing negotiations

---

## 📏 Success Metrics

- **On-Time Completion:** >80% of cohorts complete within planned timeline
- **Milestone Accuracy:** >95% milestone tracking accuracy
- **Early Risk Detection:** Flag delays >1 week before critical
- **Customer Satisfaction:** >85% positive feedback on onboarding

---

## 🆘 Escalation Paths

**When to Escalate:**
- Cohort >2 weeks behind schedule
- Customer unresponsive for >1 week
- Technical blocker with no ETA
- Go-live at risk

**Escalation Targets:**
- **Timeline Risk** → PHE PM + Customer Success
- **Technical Blocker** → Purview Product Expert → PG
- **Customer Engagement** → Account Manager
- **Resource Constraint** → PHE Operations Lead
