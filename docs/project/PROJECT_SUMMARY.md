# PHEPy Orchestrator Agent - Project Summary

## Overview
Complete instruction set and organizational structure for the Comprehensive Purview Product Health & Escalation (CPPHE) Orchestrator Agent and its 8 specialized sub-agents.

**Status:** ✅ Core structure complete; ready for grounding doc population and integration testing

---

## Deliverables Summary

### 1. Core Orchestrator Instructions
**File:** [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md)

Comprehensive instruction set covering:
- ✅ Agent identity, objectives, and operating principles
- ✅ Scope & expertise areas (Purview product, PHE program, operations)
- ✅ Refusals & guardrails (PII handling, data integrity, personal judgment avoidance)
- ✅ Communication style & interaction patterns
- ✅ Reference content placeholders across 5 domains
- ✅ Connector & integration requirements
- ✅ Metrics & observability framework

**Key Features:**
- Executive-crisp communication style
- Evidence-backed findings ("why," "evidence," "next action")
- Tenant-centric awareness & impact assessment
- Risk detection with escalation thresholds
- PII redaction & role-based access controls

---

### 2. Project Organization Guide
**File:** [`FOLDER_STRUCTURE.md`](FOLDER_STRUCTURE.md)

Documents:
- ✅ Complete folder hierarchy (grounding docs + sub-agents)
- ✅ Purpose & contents of each folder
- ✅ Sub-agent responsibilities & tool access
- ✅ Reference mapping (sub-agent → grounding docs)
- ✅ Workflow integration patterns
- ✅ Completion checklist

---

### 3. Grounding Docs Folders (5 domains)

#### Domain 1: Purview Product Reference
**Folder:** `grounding_docs/purview_product/`

**Placeholder files:**
- `purview_product_architecture.md` – Service components, features, dependencies
- `purview_known_issues.md` – Known issues, workarounds, status
- `purview_troubleshooting_playbooks.md` – Symptom → Root Cause → Remediation
- `mip_dip_guide.md` – MIP/DIP coverage & config
- `dlp_policies_guide.md` – DLP framework & patterns
- `ediscovery_guide.md` – eDiscovery workflows & performance
- `irm_guide.md` – Information Rights Management
- `dlm_retention_guide.md` – Data Lifecycle Management
- `insider_risk_guide.md` – Insider Risk detection & tuning
- `scanning_labeling_guide.md` – Data discovery & labeling

#### Domain 2: PHE Program & Operations
**Folder:** `grounding_docs/phe_program_operations/`

**Placeholder files:**
- `mcs_ic_cohort_registry.md` – Cohort definitions, ownership, timelines
- `phe_onboarding_runbook.md` – Phased onboarding tasks & gates
- `roles_responsibilities_matrix.md` – RACI, role definitions
- `phe_playbooks.md` – SLA breach, VIP handling, bug filing, rollback
- `comms_templates.md` – Kickoff, weekly, risk alerts
- `lifecycle_cadences.md` – Review schedules, governance
- `cxe_care_expert_resource.md` – (Reference: https://microsoft.sharepoint-df.com/sites/CxE-Security-Care)

#### Domain 3: Support & Escalation
**Folder:** `grounding_docs/support_escalation/`

**Placeholder files:**
- `dfm_integration_guide.md` – DFM metadata, lifecycle, connector
- `dfm_sla_definitions.md` – SLA tiers, thresholds, rules
- `icm_integration_guide.md` – ICM schema, incident classification
- `icm_severity_mapping.md` – Severity levels, escalation rules
- `ado_integration_guide.md` – Work item types, priority mapping
- `escalation_decision_tree.md` – When to escalate, approval chains
- `sla_breach_playbook.md` – Breach prevention & recovery

#### Domain 4: Contacts & Access
**Folder:** `grounding_docs/contacts_access/`

**Placeholder files:**
- `pg_css_contacts.md` – Product Group leads, CSS managers, on-call
- `escalation_contacts.md` – Critical escalation paths
- `initiatives_pilots.md` – Active initiatives, pilot cohorts
- `role_access_runbooks.md` – PM, IC, CSS, Engineer access setup
- `least_privilege_defaults.md` – Default access by role
- `access_approval_workflows.md` – Request, approval, provisioning

#### Domain 5: Customer & Tenant Data
**Folder:** `grounding_docs/customer_tenant_data/`

**Placeholder files:**
- `customer_list_registry.md` – Customer ID, tenant ID, segment, assignment
- `tenant_registry.md` – Tenant IDs, customer mapping, region
- `tenant_health_metrics.md` – KPIs, adoption, case volume, escalations
- `vip_customer_list.md` – VIP customers, contacts, SLA overrides
- `customer_segments.md` – Segment definitions

---

### 4. Sub-Agent Instructions (8 specialized agents)

#### Sub-Agent 1: Purview Product Expert
**Folder:** `sub_agents/purview_product_expert/`  
**File:** `AGENT_INSTRUCTIONS.md`

**Role:** Deep Purview product knowledge, troubleshooting, feature readiness

**Capabilities:**
- Answer architecture & capability questions
- Diagnose product issues & recommend workarounds
- Map customer issues to known bugs/DCRs
- Assess feature readiness & adoption
- Detect systemic product issues

**Guardrails:** Never fabricate features; cite grounding docs

---

#### Sub-Agent 2: Support Case Manager
**Folder:** `sub_agents/support_case_manager/`  
**File:** `AGENT_INSTRUCTIONS.md`

**Role:** DFM support case management, SLA tracking, at-risk detection

**Capabilities:**
- Retrieve & summarize support cases
- Detect at-risk & aging cases
- Recommend resolution or escalation
- Trend analysis & reporting
- Alert on SLA breaches

**Guardrails:** Redact customer PII unless user authorized

---

#### Sub-Agent 3: Escalation Manager
**Folder:** `sub_agents/escalation_manager/`  
**File:** `AGENT_INSTRUCTIONS.md`

**Role:** ICM incident management, severity classification, impact assessment

**Capabilities:**
- Retrieve & analyze ICM incidents
- Classify severity & urgency
- Detect systemic issues (same bug, multiple tenants)
- Coordinate escalation response
- Post-incident analysis

**Guardrails:** Escalate based on confirmed impact, not speculation

---

#### Sub-Agent 4: Work Item Manager
**Folder:** `sub_agents/work_item_manager/`  
**File:** `AGENT_INSTRUCTIONS.md`

**Role:** ADO work item tracking, bug/feature status, deployment planning

**Capabilities:**
- Retrieve & link work items
- Assess blockers & critical path items
- Track fix & feature readiness
- Recommend priority & filing
- Support deployment & release

**Guardrails:** Never change work item status without authorization

---

#### Sub-Agent 5: Program Onboarding Manager
**Folder:** `sub_agents/program_onboarding_manager/`  
**File:** `AGENT_INSTRUCTIONS.md`

**Role:** MCS/IC cohort execution, onboarding progress, program health

**Capabilities:**
- Manage cohort lifecycle
- Validate onboarding execution
- Coordinate customer comms
- Track risks & blockers
- Support go-live readiness

**Guardrails:** Respect customer readiness signals; no over-commitment

---

#### Sub-Agent 6: Access & Role Manager
**Folder:** `sub_agents/access_role_manager/`  
**File:** `AGENT_INSTRUCTIONS.md`

**Role:** Role-based access control, least-privilege assignment, onboarding setup

**Capabilities:**
- Assign least-privilege roles
- Validate role-based access
- Support access troubleshooting
- Document & governance
- Support onboarding & offboarding

**Guardrails:** Default to minimum required; never bypass approval workflows

---

#### Sub-Agent 7: Tenant Health Monitor
**Folder:** `sub_agents/tenant_health_monitor/`  
**File:** `AGENT_INSTRUCTIONS.md`

**Role:** Per-tenant health tracking, KPI aggregation, adoption monitoring

**Capabilities:**
- Aggregate per-tenant KPIs
- Detect adoption anomalies
- Roll up cohort health
- Alert on tenant-level risk
- Recommend tenant-specific actions

**Guardrails:** Redact customer names; provide anonymized metrics

---

#### Sub-Agent 8: Contacts & Escalation Finder
**Folder:** `sub_agents/contacts_escalation_finder/`  
**File:** `AGENT_INSTRUCTIONS.md`

**Role:** Contact discovery, PG/CSS routing, escalation path guidance

**Capabilities:**
- Find PG contacts by product area
- Find CSS contacts by customer/tenant
- Route escalations
- Validate contact currency
- Support initiative/pilot contacts

**Guardrails:** NEVER fabricate contacts; defer if ambiguous

---

## Folder Tree

```
PHEPy/
├── AGENT_INSTRUCTIONS.md              ← Orchestrator main instruction set
├── FOLDER_STRUCTURE.md                ← Organization & integration guide
├── mcp.json                           ← MCP server configuration
│
├── grounding_docs/                    ← Reference & grounding content
│   ├── purview_product/
│   │   ├── purview_product_architecture.md     [PLACEHOLDER]
│   │   ├── purview_known_issues.md             [PLACEHOLDER]
│   │   ├── purview_troubleshooting_playbooks.md [PLACEHOLDER]
│   │   ├── mip_dip_guide.md                    [PLACEHOLDER]
│   │   ├── dlp_policies_guide.md               [PLACEHOLDER]
│   │   ├── ediscovery_guide.md                 [PLACEHOLDER]
│   │   ├── irm_guide.md                        [PLACEHOLDER]
│   │   ├── dlm_retention_guide.md              [PLACEHOLDER]
│   │   ├── insider_risk_guide.md               [PLACEHOLDER]
│   │   └── scanning_labeling_guide.md          [PLACEHOLDER]
│   │
│   ├── phe_program_operations/
│   │   ├── mcs_ic_cohort_registry.md           [PLACEHOLDER]
│   │   ├── phe_onboarding_runbook.md           [PLACEHOLDER]
│   │   ├── roles_responsibilities_matrix.md    [PLACEHOLDER]
│   │   ├── phe_playbooks.md                    [PLACEHOLDER]
│   │   ├── comms_templates.md                  [PLACEHOLDER]
│   │   └── lifecycle_cadences.md               [PLACEHOLDER]
│   │
│   ├── support_escalation/
│   │   ├── dfm_integration_guide.md            [PLACEHOLDER]
│   │   ├── dfm_sla_definitions.md              [PLACEHOLDER]
│   │   ├── icm_integration_guide.md            [PLACEHOLDER]
│   │   ├── icm_severity_mapping.md             [PLACEHOLDER]
│   │   ├── ado_integration_guide.md            [PLACEHOLDER]
│   │   ├── escalation_decision_tree.md         [PLACEHOLDER]
│   │   └── sla_breach_playbook.md              [PLACEHOLDER]
│   │
│   ├── contacts_access/
│   │   ├── pg_css_contacts.md                  [PLACEHOLDER]
│   │   ├── escalation_contacts.md              [PLACEHOLDER]
│   │   ├── initiatives_pilots.md               [PLACEHOLDER]
│   │   ├── role_access_runbooks.md             [PLACEHOLDER]
│   │   ├── least_privilege_defaults.md         [PLACEHOLDER]
│   │   └── access_approval_workflows.md        [PLACEHOLDER]
│   │
│   └── customer_tenant_data/
│       ├── customer_list_registry.md           [PLACEHOLDER]
│       ├── tenant_registry.md                  [PLACEHOLDER]
│       ├── tenant_health_metrics.md            [PLACEHOLDER]
│       ├── vip_customer_list.md                [PLACEHOLDER]
│       └── customer_segments.md                [PLACEHOLDER]
│
└── sub_agents/                        ← Role-specific agent instructions
    ├── purview_product_expert/
    │   └── AGENT_INSTRUCTIONS.md      ✅ Complete
    ├── support_case_manager/
    │   └── AGENT_INSTRUCTIONS.md      ✅ Complete
    ├── escalation_manager/
    │   └── AGENT_INSTRUCTIONS.md      ✅ Complete
    ├── work_item_manager/
    │   └── AGENT_INSTRUCTIONS.md      ✅ Complete
    ├── program_onboarding_manager/
    │   └── AGENT_INSTRUCTIONS.md      ✅ Complete
    ├── access_role_manager/
    │   └── AGENT_INSTRUCTIONS.md      ✅ Complete
    ├── tenant_health_monitor/
    │   └── AGENT_INSTRUCTIONS.md      ✅ Complete
    └── contacts_escalation_finder/
        └── AGENT_INSTRUCTIONS.md      ✅ Complete
```

---

## Key Features & Design

### Orchestrator Capabilities
✅ **Information Synthesis** – aggregates data from DFM, ICM, ADO, program knowledge  
✅ **Risk Detection** – flags SLA breaches, VIP escalations, systemic issues  
✅ **Least-Privilege Governance** – enforces PII redaction, role-based access  
✅ **Evidence-Backed Recommendations** – every finding includes "why," "evidence," "next action"  
✅ **Tenant-Centric Awareness** – tracks cohorts, customer impact, adoption  

### Sub-Agent Specialization
Each sub-agent has:
- ✅ Clear role definition & responsibilities
- ✅ Dedicated tool access (connectors, APIs)
- ✅ Guardrails & boundary conditions
- ✅ Common scenarios with expected flows
- ✅ Success metrics & SLAs
- ✅ Escalation criteria

### Grounding Doc Organization
5 knowledge domains with 30+ placeholder files:
- ✅ Purview product (architecture, known issues, playbooks)
- ✅ PHE program operations (cohorts, onboarding, playbooks)
- ✅ Support & escalation (DFM, ICM, ADO integration)
- ✅ Contacts & access (PG/CSS routing, role setup)
- ✅ Customer & tenant data (registries, metrics)

---

## Next Steps

### Immediate (This Week)
- [ ] Review orchestrator instructions with PHE PM & Escalation Owner
- [ ] Begin populating highest-priority grounding docs:
  - [ ] `purview_product_architecture.md` (product knowledge foundation)
  - [ ] `mcs_ic_cohort_registry.md` (program foundation)
  - [ ] `pg_css_contacts.md` (escalation routing foundation)

### Short-term (Weeks 2–3)
- [ ] Complete grounding doc population (all 30+ files)
- [ ] Configure MCP server connectors (DFM, ICM, ADO, Kusto)
- [ ] Set up guardrail enforcement (PII masking, role-based redaction)
- [ ] Smoke test sub-agent routing & common scenarios

### Medium-term (Weeks 4–6)
- [ ] Integration testing with real data
- [ ] User acceptance testing (PHE team, PM, Escalation Owner)
- [ ] Refine based on feedback
- [ ] Deploy to production

### Ongoing
- [ ] Keep grounding docs updated (weekly)
- [ ] Monitor sub-agent accuracy & escalation quality (metrics dashboard)
- [ ] Gather user feedback & iterate
- [ ] Track reference content currency & freshness

---

## Resources & References

### Official Documentation
- **Purview:** https://learn.microsoft.com/en-us/purview/purview
- **CxE Care:** https://microsoft.sharepoint-df.com/sites/CxE-Security-Care

### Key Files to Reference
- [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md) – Orchestrator main instruction set
- [`FOLDER_STRUCTURE.md`](FOLDER_STRUCTURE.md) – Project organization & integration guide
- [`sub_agents/*/AGENT_INSTRUCTIONS.md`](sub_agents/) – Individual sub-agent specs
- [`mcp.json`](mcp.json) – MCP server configuration

---

## Success Criteria

### Operational Metrics
- **Escalation accuracy:** > 95% of escalations lead to action within SLA
- **At-risk detection:** > 90% of at-risk cases flagged before breach
- **Response latency:** < 2 min for complex findings, < 30 sec for cached queries
- **False positive rate:** < 10% of escalations deemed unnecessary in retrospect

### Quality Metrics
- **Citation accuracy:** 100% of findings backed by evidence (link to DFM/ICM/ADO)
- **PII compliance:** 0 cases of unauthorized PII exposure
- **Contact accuracy:** > 99% of provided escalation contacts respond properly
- **Fabrication rate:** 0% of contacts, IDs, or links made up

### Adoption Metrics
- **User satisfaction:** > 80% of users find recommendations actionable
- **Time savings:** > 50% reduction in time to escalate/resolve issues
- **Coverage:** Agent supports > 80% of PHE workflow use cases

---

## Contact & Ownership

**Project Owner:** [Carter Ryan / PHE PM]  
**Orchestrator Owner:** [To be assigned]  
**Sub-Agent Owners:** [Individual RACI per agent]  
**Grounding Docs Owner:** [Knowledge Manager / Ops Lead]  

For questions or updates: [email / Slack channel]

---

## Version History

| Version | Date | Summary |
|---------|------|---------|
| 1.0 | 2026-02-04 | Initial project structure, orchestrator instructions, 8 sub-agent specs, folder organization |

---

**Status:** 🟢 READY FOR POPULATION & INTEGRATION TESTING
