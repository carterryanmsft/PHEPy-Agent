# PHEPy Orchestrator Agent - Quick Start Guide

## 📋 What You Have

A complete, production-ready instruction set for an **8-sub-agent orchestrator** that synthesizes Purview health, escalations, and program intelligence.

### Files Created

| File | Purpose |
|------|---------|
| `AGENT_INSTRUCTIONS.md` | Orchestrator main spec (guardrails, operating principles, communication style) |
| `PROJECT_SUMMARY.md` | 30-page project overview with deliverables, folder tree, next steps |
| `FOLDER_STRUCTURE.md` | Organization guide + sub-agent → grounding doc mapping |
| `mcp.json` | MCP server config (DFM, ICM, ADO, enterprise, Kusto connectors) |
| **8× Sub-Agent Specs** | `sub_agents/[role]/AGENT_INSTRUCTIONS.md` |
| **30+ Placeholder Files** | `grounding_docs/[domain]/[topic].md` |

---

## 🚀 Quick Start: Next 3 Steps

### Step 1: Review Orchestrator (30 min)
Open [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md)
- Read: Agent identity, objectives, operating principles
- Skim: Communication style, interaction patterns
- Note: Reference content placeholders (you'll populate these next)

**Approval gate:** Get sign-off from PHE PM & Escalation Owner

### Step 2: Review Sub-Agents (1 hour)
Open each sub-agent spec in `sub_agents/*/AGENT_INSTRUCTIONS.md`

Quick read (10 min each):
- Purview Product Expert – "What does this agent do?"
- Support Case Manager – "SLA tracking & escalation detection"
- Escalation Manager – "Impact assessment & incident coordination"
- Work Item Manager – "Bug status & deployment planning"
- Program Onboarding Manager – "Cohort lifecycle management"
- Access & Role Manager – "Least-privilege access setup"
- Tenant Health Monitor – "Per-tenant KPI aggregation"
- Contacts & Escalation Finder – "Contact discovery & routing"

**Approval gate:** Assign owner to each sub-agent

### Step 3: Start Populating Grounding Docs (This Week)
Priority order:

1. **High Priority (Days 1-2):**
   - `grounding_docs/purview_product/purview_product_architecture.md`
   - `grounding_docs/phe_program_operations/mcs_ic_cohort_registry.md`
   - `grounding_docs/contacts_access/pg_css_contacts.md`

2. **Medium Priority (Days 3-5):**
   - `grounding_docs/support_escalation/dfm_integration_guide.md`
   - `grounding_docs/support_escalation/icm_integration_guide.md`
   - `grounding_docs/customer_tenant_data/customer_list_registry.md`

3. **Standard Priority (Days 6-10):**
   - All remaining grounding docs

---

## 🎯 Sub-Agent Summary Table

| Agent | Primary Role | Key Responsibility | Tools |
|-------|--------------|-------------------|-------|
| **Purview Product Expert** | Product knowledge | Answer architecture, diagnose issues, flag known bugs | Purview APIs, Kusto |
| **Support Case Manager** | DFM management | Retrieve cases, flag SLA breaches, detect patterns | DFM connector |
| **Escalation Manager** | ICM management | Analyze incidents, assess impact, coordinate response | ICM connector |
| **Work Item Manager** | ADO tracking | Track bugs/features, link to cases, assess blockers | ADO connector |
| **Program Onboarding Manager** | Cohort execution | Track milestones, validate readiness, coordinate comms | Cohort registry |
| **Access & Role Manager** | RBAC/provisioning | Assign least-privilege roles, onboarding, offboarding | Azure AD, approval systems |
| **Tenant Health Monitor** | Health tracking | Aggregate KPIs, detect anomalies, roll up cohort health | Kusto, tenant APIs |
| **Contacts & Escalation Finder** | Contact routing | Find PG/CSS leads, route escalations, validate contacts | Directory, org chart |

---

## 📁 Folder Structure at a Glance

```
grounding_docs/          ← Reference content (populate these)
├── purview_product/     ← Product architecture, known issues, playbooks
├── phe_program_operations/  ← Cohorts, onboarding, playbooks
├── support_escalation/   ← DFM/ICM/ADO integration guides
├── contacts_access/     ← Contacts, access setup, role mapping
└── customer_tenant_data/ ← Customer list, tenant health metrics

sub_agents/              ← Agent role specifications (COMPLETE)
├── purview_product_expert/
├── support_case_manager/
├── escalation_manager/
├── work_item_manager/
├── program_onboarding_manager/
├── access_role_manager/
├── tenant_health_monitor/
└── contacts_escalation_finder/
```

---

## 🔐 Critical Guardrails (Remember These!)

### Orchestrator
✅ **Always:** Cite DFM/ICM/ADO links, redact PII by default, escalate on thresholds (not gut)  
❌ **Never:** Guess emails/IDs, fabricate links, make personal judgments, expose PII carelessly

### Sub-Agents
✅ **Always:** Reference grounding docs, check authorization before escalating  
❌ **Never:** Commit on behalf of PG/support, bypass approval chains, make up contacts

---

## 🧪 Testing Checklist (Week 2)

- [ ] Configure MCP connectors (DFM, ICM, ADO, Kusto)
- [ ] Test orchestrator → sub-agent routing
- [ ] Validate PII masking works (redact by default)
- [ ] Smoke test 5 common scenarios:
  - "What's at SLA risk this week?"
  - "What's the status of MCS Alpha cohort?"
  - "Is Tenant X at risk?"
  - "Who's the PG lead for DLP?"
  - "Find case #123 root cause"

---

## 📊 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Escalation accuracy | > 95% | % of escalations → action within SLA |
| At-risk detection | > 90% | % of cases flagged before SLA breach |
| Response latency | < 2 min | Avg time to complex finding |
| False positive rate | < 10% | % escalations deemed unnecessary later |
| PII compliance | 0 | # of unauthorized PII exposures |
| Contact accuracy | > 99% | % of escalation contacts that respond |

---

## 🔧 Customization Points

### If you need to adjust:

**Communication style?**  
→ Edit `AGENT_INSTRUCTIONS.md` → "Communication Style & Templates"

**Sub-agent responsibilities?**  
→ Edit `sub_agents/[agent]/AGENT_INSTRUCTIONS.md` → "Responsibilities"

**Role definitions?**  
→ Create/edit `grounding_docs/phe_program_operations/roles_responsibilities_matrix.md`

**Escalation thresholds?**  
→ Edit `AGENT_INSTRUCTIONS.md` → "Escalate when risk exceeds thresholds"

**Add a new sub-agent?**  
→ Copy folder structure: `sub_agents/[new_agent]/AGENT_INSTRUCTIONS.md`

---

## 📞 Support & Questions

| Question | Where to Look |
|----------|---------------|
| "What does the orchestrator do?" | [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md) (top) |
| "What should sub-agent X do?" | [`sub_agents/[X]/AGENT_INSTRUCTIONS.md`](sub_agents/) |
| "How should I organize grounding docs?" | [`FOLDER_STRUCTURE.md`](FOLDER_STRUCTURE.md) |
| "What's the full project scope?" | [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md) |
| "Which grounding doc should I populate first?" | See "Quick Start: Step 3" above |

---

## ⏱️ Estimated Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Planning & Approval** | 1 week | Signed-off orchestrator + sub-agent specs |
| **Grounding Doc Population** | 2-3 weeks | All 30+ reference files populated |
| **MCP Integration** | 1 week | Connectors configured, basic testing |
| **UAT & Refinement** | 2 weeks | Feedback integration, production hardening |
| **Production Launch** | 1 day | Agent live, team trained |

**Total:** ~7-8 weeks to full production readiness

---

## 🎓 Training

**For Orchestrator Users (PMs, Escalation Owners):**
- Overview of agent capabilities (15 min)
- Common query patterns (15 min)
- How to interpret findings (15 min)
- When to escalate vs. accept recommendation (15 min)

**For Sub-Agent Owners:**
- Deep-dive on their agent's guardrails (30 min)
- Data sources & connectors (30 min)
- Scenario walkthroughs (1 hour)
- Metrics & SLAs (15 min)

**Total Training:** ~4 hours per team member

---

## 📈 Metrics Dashboard (To Build)

Track these KPIs once agent is live:

```
┌─────────────────────────────────────────┐
│ PHEPy Orchestrator KPI Dashboard        │
├─────────────────────────────────────────┤
│ Escalation Accuracy:      95%           │
│ At-Risk Detection Rate:   92%           │
│ Avg Response Time:        1.2 min       │
│ False Positive Rate:      8%            │
│ PII Violations:           0             │
│ Sub-Agent Availability:   99.8%         │
│ User Satisfaction:        8.5/10        │
└─────────────────────────────────────────┘
```

Set up in Kusto, Power BI, or equivalent.

---

## 🏁 Ready?

1. ✅ Review `AGENT_INSTRUCTIONS.md`
2. ✅ Assign sub-agent owners
3. ✅ Start populating grounding docs (high priority first)
4. ✅ Configure MCP connectors
5. ✅ Test, gather feedback, iterate

**You have everything you need. Go build!**

---

**Questions?** Contact: [Your Name / PHE PM]  
**Status:** 🟢 Ready for implementation
