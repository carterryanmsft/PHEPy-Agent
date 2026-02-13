# PHEPy Orchestrator Agent - Folder Structure

## Overview
This document describes the folder organization for the Comprehensive Purview Product Health & Escalation (CPPHE) Agent and its sub-agents.

---

## Folder Structure

### `/grounding_docs` – Reference & Grounding Content
Central repository for all grounding documentation that sub-agents and the orchestrator reference. Organized by domain.

#### `/grounding_docs/purview_product`
**Purpose:** Purview product knowledge, architecture, known issues, and troubleshooting playbooks.

**Contents:**
- `purview_product_architecture.md` – Service components, feature map, dependencies, scalability
- `purview_known_issues.md` – Known issues, active mitigations, status tracking
- `purview_troubleshooting_playbooks.md` – Symptom → Root Cause → Remediation
- `mip_dip_guide.md` – MIP/DIP feature coverage and configuration
- `dlp_policies_guide.md` – DLP policy framework and common patterns
- `ediscovery_guide.md` – eDiscovery workflows and performance at scale
- `irm_guide.md` – Information Rights Management, licensing, encryption
- `dlm_retention_guide.md` – Data Lifecycle Management and hold procedures
- `insider_risk_guide.md` – Insider Risk detection, tuning, investigator workflows
- `scanning_labeling_guide.md` – Data discovery, scanning, automated labeling

#### `/grounding_docs/phe_program_operations`
**Purpose:** PHE program execution, onboarding, playbooks, and operations.

**Contents:**
- `mcs_ic_cohort_registry.md` – Cohort definitions, tenant lists, timelines, ownership
- `phe_onboarding_runbook.md` – Phased onboarding tasks, gates, comms templates
- `roles_responsibilities_matrix.md` – RACI matrix, role definitions, responsibilities
- `phe_playbooks.md` – SLA breach, silent aging, VIP handling, bug filing, rollback playbooks
- `comms_templates.md` – Kickoff, weekly, risk alerts, completion comms
- `lifecycle_cadences.md` – Review schedules, governance meetings, decision checkpoints

#### `/grounding_docs/support_escalation`
**Purpose:** Support systems, escalation procedures, and integration guides.

**Contents:**
- `dfm_integration_guide.md` – DFM metadata schema, lifecycle, connector capabilities
- `dfm_sla_definitions.md` – SLA tiers, thresholds, escalation rules
- `icm_integration_guide.md` – ICM schema, incident classification, state machine
- `icm_severity_mapping.md` – Severity levels, escalation rules, customer impact
- `ado_integration_guide.md` – Work item types, priority mapping, release planning
- `escalation_decision_tree.md` – When to escalate, approval chains, communication
- `sla_breach_playbook.md` – Breach prevention, recovery, escalation procedures

#### `/grounding_docs/contacts_access`
**Purpose:** Contact information, access setup, and role-based runbooks.

**Contents:**
- `pg_css_contacts.md` – Product Group leads, CSS managers, on-call rotations
- `escalation_contacts.md` – Critical escalation paths by product area
- `initiatives_pilots.md` – Active initiatives, pilot cohorts, risks, blockers
- `role_access_runbooks.md` – PM, IC, CSS, Escalation Owner, Engineer access setup
- `least_privilege_defaults.md` – Default access levels by role
- `access_approval_workflows.md` – Request, approval, provisioning procedures

#### `/grounding_docs/customer_tenant_data`
**Purpose:** Customer registry, tenant metadata, and health tracking.

**Contents:**
- `customer_list_registry.md` – Customer ID, tenant ID, segment, assignment, criticality
- `tenant_registry.md` – Tenant IDs, customer mapping, region, national cloud
- `tenant_health_metrics.md` – KPIs, adoption, case volume, escalations per tenant
- `vip_customer_list.md` – VIP customers, escalation contacts, SLA overrides
- `customer_segments.md` – Enterprise, Mid-market, SMB, Government segment definitions

---

### `/sub_agents` – Role-Specific Agent Instructions
Each sub-agent has specialized responsibilities, tools access, and grounding docs.

#### `/sub_agents/purview_product_expert`
**Purpose:** Deep Purview product knowledge, troubleshooting, feature readiness.

**Contents:**
- `AGENT_INSTRUCTIONS.md` – Role definition, responsibilities, guardrails
- `GROUNDING_REFS.md` – Links to relevant grounding docs (purview_product/)
- `TOOLS_AND_CONNECTORS.md` – Available tools, API endpoints, data sources
- `COMMON_SCENARIOS.md` – Feature questions, troubleshooting requests, examples

**Responsibilities:**
- Answer Purview architecture, feature coverage, and capability questions
- Root-cause product issues and recommend workarounds
- Map customer issues to known bugs/DCRs
- Provide feature readiness and adoption guidance
- Detect systemic product issues

#### `/sub_agents/support_case_manager`
**Purpose:** DFM support case management, SLA tracking, escalation detection.

**Contents:**
- `AGENT_INSTRUCTIONS.md` – Role definition, responsibilities, guardrails
- `GROUNDING_REFS.md` – Links to relevant grounding docs (support_escalation/)
- `TOOLS_AND_CONNECTORS.md` – DFM connector, query patterns, SLA rules
- `CASE_ANALYSIS_PATTERNS.md` – At-risk case detection, aging analysis, clustering

**Responsibilities:**
- Retrieve and summarize support cases from DFM
- Detect SLA breaches and at-risk cases
- Identify customer patterns and trends
- Recommend case escalation or resolution paths
- Track case metrics and compliance

#### `/sub_agents/escalation_manager`
**Purpose:** ICM incident management, severity classification, escalation coordination.

**Contents:**
- `AGENT_INSTRUCTIONS.md` – Role definition, responsibilities, guardrails
- `GROUNDING_REFS.md` – Links to relevant grounding docs (support_escalation/)
- `TOOLS_AND_CONNECTORS.md` – ICM connector, incident queries, severity rules
- `INCIDENT_ANALYSIS_PATTERNS.md` – Incident clustering, customer impact, time-series

**Responsibilities:**
- Retrieve and analyze ICM incidents
- Map incidents to product areas and customers
- Assess customer/tenant impact severity
- Detect systemic issues (same bug, multiple tenants)
- Recommend escalation and mitigation actions
- Track incident SLA compliance

#### `/sub_agents/work_item_manager`
**Purpose:** ADO work item management, bug tracking, feature readiness.

**Contents:**
- `AGENT_INSTRUCTIONS.md` – Role definition, responsibilities, guardrails
- `GROUNDING_REFS.md` – Links to relevant grounding docs (support_escalation/)
- `TOOLS_AND_CONNECTORS.md` – ADO connector, query patterns, iteration planning
- `WORK_ITEM_PATTERNS.md` – Bug clustering, priority mapping, deployment tracking

**Responsibilities:**
- Retrieve ADO work items (bugs, features, DCRs)
- Link DFM/ICM incidents to ADO
- Assess fix ETA and deployment status
- Detect blockers and critical path items
- Recommend bug/DCR priority and escalation
- Track engineering velocity and rollback candidates

#### `/sub_agents/program_onboarding_manager`
**Purpose:** MCS/IC cohort management, onboarding execution, program health.

**Contents:**
- `AGENT_INSTRUCTIONS.md` – Role definition, responsibilities, guardrails
- `GROUNDING_REFS.md` – Links to relevant grounding docs (phe_program_operations/)
- `TOOLS_AND_CONNECTORS.md` – Cohort registry, communication systems
- `ONBOARDING_PLAYBOOKS.md` – Phase-by-phase execution, gate reviews, risk tracking

**Responsibilities:**
- Manage cohort status and milestones
- Validate onboarding checklist progress
- Coordinate comms (kickoff, weekly, risk alerts)
- Identify and escalate blockers
- Track go-live readiness and post-go-live reviews
- Manage customer communication and engagement

#### `/sub_agents/access_role_manager`
**Purpose:** Role-based access control, least-privilege defaults, onboarding setup.

**Contents:**
- `AGENT_INSTRUCTIONS.md` – Role definition, responsibilities, guardrails
- `GROUNDING_REFS.md` – Links to relevant grounding docs (contacts_access/)
- `TOOLS_AND_CONNECTORS.md` – Identity systems, approval workflows, provisioning
- `ACCESS_RUNBOOKS.md` – Step-by-step setup for PM, IC, CSS, Escalation Owner, Engineer

**Responsibilities:**
- Assign least-privilege roles to new hires/assignments
- Recommend access based on role and scope
- Validate compliance with least-privilege policies
- Track access reviews and deprovisioning
- Support access troubleshooting and escalation

#### `/sub_agents/tenant_health_monitor`
**Purpose:** Per-tenant health tracking, KPI aggregation, risk detection.

**Contents:**
- `AGENT_INSTRUCTIONS.md` – Role definition, responsibilities, guardrails
- `GROUNDING_REFS.md` – Links to relevant grounding docs (customer_tenant_data/)
- `TOOLS_AND_CONNECTORS.md` – Tenant data sources, Kusto queries, health metrics
- `HEALTH_METRICS_FRAMEWORK.md` – KPI definitions, thresholds, alerting

**Responsibilities:**
- Aggregate per-tenant health metrics
- Detect adoption anomalies and feature usage gaps
- Roll up MCS/IC cohort health
- Alert on tenant-level risk (SLA breaches, escalations)
- Recommend tenant-specific actions or escalations
- Track progress toward success milestones

#### `/sub_agents/contacts_escalation_finder`
**Purpose:** Contact discovery, PG/CSS routing, access provisioning.

**Contents:**
- `AGENT_INSTRUCTIONS.md` – Role definition, responsibilities, guardrails
- `GROUNDING_REFS.md` – Links to relevant grounding docs (contacts_access/)
- `TOOLS_AND_CONNECTORS.md` – Directory, org chart, on-call systems
- `CONTACT_FINDING_PATTERNS.md` – PG by product area, CSS by region, escalation paths

**Responsibilities:**
- Find PG lead for product area/component
- Find CSS manager for customer/tenant
- Route escalations to correct team
- Provide on-call contact information
- Validate contact info currency
- Never fabricate contacts; defer if ambiguous

---

## Reference Mapping

### Sub-Agent → Grounding Docs

| Sub-Agent | Primary Grounding Folder | Use Cases |
|-----------|--------------------------|-----------|
| Purview Product Expert | `purview_product/` | "What causes classification timeouts?", "Is there a known bug?" |
| Support Case Manager | `support_escalation/` | "Which cases are at SLA risk?", "Summarize open cases" |
| Escalation Manager | `support_escalation/` | "What's the incident severity?", "Map incident to tenant" |
| Work Item Manager | `support_escalation/` | "What's the fix status?", "Link case to ADO" |
| Program Onboarding Manager | `phe_program_operations/` | "Where's the cohort in onboarding?", "What's next?" |
| Access Role Manager | `contacts_access/` | "What access does this role need?", "Set up PM access" |
| Tenant Health Monitor | `customer_tenant_data/` | "How's tenant adoption?", "Compare cohort health" |
| Contacts Escalation Finder | `contacts_access/` | "Who's the PG lead?", "Find CSS manager" |

---

## Workflow Integration

### Orchestrator → Sub-Agents

**Orchestrator (CPPHE Agent) coordinates:**
1. User request arrives at orchestrator
2. Orchestrator analyzes request scope (health check, escalation, troubleshooting, etc.)
3. Routes to appropriate sub-agent(s):
   - Multiple sub-agents may collaborate (e.g., "Health check" → Tenant Health Monitor + Support Case Manager)
4. Sub-agents pull from grounding docs + connectors
5. Orchestrator synthesizes findings, applies guardrails, formats response
6. User gets actionable, evidence-backed decision

**Example: SLA Breach Escalation**
```
Request: "What's at SLA risk this week?"
  → Orchestrator routes to:
     - Support Case Manager (DFM SLA query)
     - Escalation Manager (ICM severity)
     - Tenant Health Monitor (scope impact)
  → Sub-agents return findings
  → Orchestrator synthesizes: "3 cases at risk; highest impact Contoso; blockers in ADO #999"
  → Contacts Escalation Finder (who to notify)
  → Orchestrator formats escalation comms with links, why, next steps
```

---

## Completion Checklist

### Grounding Docs
- [ ] Populate `purview_product/` with architecture, known issues, playbooks
- [ ] Populate `phe_program_operations/` with cohort, onboarding, playbook templates
- [ ] Populate `support_escalation/` with DFM/ICM/ADO integration guides
- [ ] Populate `contacts_access/` with contact lists, access runbooks
- [ ] Populate `customer_tenant_data/` with customer/tenant registries

### Sub-Agent Instructions
- [ ] Create `AGENT_INSTRUCTIONS.md` for each sub-agent
- [ ] Create `GROUNDING_REFS.md` linking to relevant grounding docs
- [ ] Create `TOOLS_AND_CONNECTORS.md` documenting available tools
- [ ] Create scenario/pattern docs for common use cases

### Integration & Testing
- [ ] Test orchestrator → sub-agent routing
- [ ] Test grounding doc references and accuracy
- [ ] Validate guardrails (PII masking, role-based access)
- [ ] Smoke test all workflows

---

## Contact & Governance

**Folder Owner:** [Your Name / PHE Operations]  
**Grounding Docs Owner:** [Knowledge Manager]  
**Sub-Agent Owners:** [Individual RACI owners per sub-agent]  

For updates: [email / channel]
