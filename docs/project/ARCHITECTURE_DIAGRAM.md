# PHEPy Orchestrator – Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│                    COMPREHENSIVE PURVIEW HEALTH & ESCALATION                │
│                              ORCHESTRATOR AGENT                              │
│                              (CPPHE Agent)                                   │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Responsibilities:                                                   │   │
│  │  • Synthesize DFM/ICM/ADO/program knowledge                         │   │
│  │  • Detect risk & recommend actions                                  │   │
│  │  • Route requests to specialized sub-agents                         │   │
│  │  • Apply guardrails (PII, role-based access, escalation rules)     │   │
│  │  • Provide evidence-backed findings                                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ▲
                                      │
                  ┌───────────────────┼───────────────────┐
                  │                   │                   │
                  ▼                   ▼                   ▼
        ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐
        │  User Requests  │  │ System Triggers │  │ Scheduled Tasks  │
        │                 │  │                 │  │                  │
        │ • Query         │  │ • SLA breach    │  │ • Daily health   │
        │ • Escalate      │  │ • Incident      │  │ • Weekly review  │
        │ • Check status  │  │ • Case spike    │  │ • Trend analysis │
        └─────────────────┘  └─────────────────┘  └──────────────────┘
```

---

## Sub-Agent Routing

```
                          ┌──────────────────────┐
                          │  Orchestrator Agent  │
                          │  (Request Analysis)  │
                          └──────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            ┌───────▼────────┐  ┌──▼──────────┐  ┌─▼──────────────┐
            │ Single-Agent   │  │ Multi-Agent │  │ Complex Query  │
            │ Routing        │  │ Coordination│  │ Analysis       │
            └────────────────┘  └─────────────┘  └────────────────┘
                    │                   │               │
        ┌───────────┼───────────┐       │       ┌───────┼────────────┐
        │           │           │       │       │       │            │
        ▼           ▼           ▼       ▼       ▼       ▼            ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────┐  ┌────┐  ┌────────┐
    │Purview   │  │Support   │  │Escalation│  │+   │  │+   │  │+       │
    │Product   │  │Case      │  │Manager   │  │Work│  │Prog│  │Access  │
    │Expert    │  │Manager   │  │          │  │Item│  │Onb │  │Manager │
    └──────────┘  └──────────┘  └──────────┘  └────┘  └────┘  └────────┘
        │              │             │            │      │          │
        │              │             │            │      │          │
        ▼              ▼             ▼            ▼      ▼          ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────┐  ┌────┐  ┌────────┐
    │Tenant    │  │Contacts  │  │          │  │    │  │    │  │        │
    │Health    │  │&Escalation        │            │      │    │        │
    │Monitor   │  │Finder    │  │          │  │    │  │    │  │        │
    └──────────┘  └──────────┘  └──────────┘  └────┘  └────┘  └────────┘
```

---

## Data Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL DATA SOURCES                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │    DFM       │  │    ICM       │  │    ADO       │  │  Kusto   │ │
│  │  (Support   │  │ (Escalations)│  │  (Work Items)│  │(Telemetry)
│  │   Cases)    │  │              │  │              │  │           │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘ │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
                              ▲
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
    ┌───────▼────────┐  ┌────▼──────────┐  ┌──▼──────────┐
    │ MCP Connectors │  │  APIs         │  │ Graph APIs  │
    ├────────────────┤  ├───────────────┤  ├─────────────┤
    │• DFM Connector │  │ • Azure AD    │  │ • Directory │
    │• ICM Connector │  │ • Tenant APIs │  │ • Org Chart │
    │• ADO Connector │  │ • Service     │  │             │
    │• Kusto         │  │   Health      │  │             │
    └────────────────┘  └───────────────┘  └─────────────┘
            ▲                 ▲                 ▲
            │                 │                 │
            └─────────────────┴─────────────────┘
                              │
            ┌─────────────────▼─────────────────┐
            │   GROUNDING DOCS (Reference)      │
            ├───────────────────────────────────┤
            │                                   │
            │  ┌─────────────────────────────┐  │
            │  │ Domain 1: Purview Product   │  │
            │  │ (10 reference files)        │  │
            │  └─────────────────────────────┘  │
            │                                   │
            │  ┌─────────────────────────────┐  │
            │  │ Domain 2: PHE Program Ops   │  │
            │  │ (6 reference files)         │  │
            │  └─────────────────────────────┘  │
            │                                   │
            │  ┌─────────────────────────────┐  │
            │  │ Domain 3: Support/Escalat.  │  │
            │  │ (7 reference files)         │  │
            │  └─────────────────────────────┘  │
            │                                   │
            │  ┌─────────────────────────────┐  │
            │  │ Domain 4: Contacts/Access   │  │
            │  │ (6 reference files)         │  │
            │  └─────────────────────────────┘  │
            │                                   │
            │  ┌─────────────────────────────┐  │
            │  │ Domain 5: Customer/Tenant   │  │
            │  │ (5 reference files)         │  │
            │  └─────────────────────────────┘  │
            │                                   │
            └───────────────────────────────────┘
```

---

## Sub-Agent Relationships

```
┌──────────────────────────────────────────────────────────────────────┐
│                        SUB-AGENT ECOSYSTEM                           │
└──────────────────────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────────────┐
    │         1. PURVIEW PRODUCT EXPERT                          │
    │         (Product Knowledge & Troubleshooting)              │
    │    ────────────────────────────────────────────────────    │
    │    • Architecture questions, feature readiness              │
    │    • Root cause diagnosis, known issues                     │
    │    • Recommends to: Work Item Manager, Escalation Manager  │
    └────────────────────────────────────────────────────────────┘
                              ▲
                              │
    ┌──────────────────────────────────────────────────────────┐
    │      2. SUPPORT CASE MANAGER                             │
    │      (DFM Case Management & SLA Tracking)                │
    │   ──────────────────────────────────────────────────────  │
    │   • Case retrieval, at-risk detection, SLA compliance     │
    │   • Escalates to: Escalation Manager, Purview Expert     │
    │   • Requests from: Orchestrator, Escalation Manager      │
    └──────────────────────────────────────────────────────────┘
                              ▲
                              │
    ┌──────────────────────────────────────────────────────────┐
    │      3. ESCALATION MANAGER                               │
    │      (ICM Incident Management & Impact Assessment)       │
    │   ──────────────────────────────────────────────────────  │
    │   • Incident analysis, severity classification, impact    │
    │   • Escalates to: Incident Commander, PG Lead            │
    │   • Collaborates with: Support Mgr, Work Item Mgr        │
    └──────────────────────────────────────────────────────────┘
                              ▲
                              │
    ┌──────────────────────────────────────────────────────────┐
    │      4. WORK ITEM MANAGER                                │
    │      (ADO Work Item Tracking & Deployment)               │
    │   ──────────────────────────────────────────────────────  │
    │   • Work item linking, fix status, blocker detection     │
    │   • Collaborates with: Purview Expert, Escalation Mgr    │
    │   • Escalates to: Release Manager, PG Lead              │
    └──────────────────────────────────────────────────────────┘
                              ▲
                              │
    ┌──────────────────────────────────────────────────────────┐
    │      5. PROGRAM ONBOARDING MANAGER                       │
    │      (Cohort Execution & Program Health)                 │
    │   ──────────────────────────────────────────────────────  │
    │   • Cohort tracking, go-live readiness, blockers         │
    │   • Escalates to: PM, Escalation Owner                   │
    │   • Collaborates with: Tenant Monitor, Contacts Finder   │
    └──────────────────────────────────────────────────────────┘
                              ▲
                              │
    ┌──────────────────────────────────────────────────────────┐
    │      6. ACCESS & ROLE MANAGER                            │
    │      (RBAC Setup & Least-Privilege Management)           │
    │   ──────────────────────────────────────────────────────  │
    │   • Role assignment, least-privilege validation          │
    │   • Escalates to: IT Security, CISO (if needed)         │
    │   • Requests from: Contacts Finder, PM                   │
    └──────────────────────────────────────────────────────────┘
                              ▲
                              │
    ┌──────────────────────────────────────────────────────────┐
    │      7. TENANT HEALTH MONITOR                            │
    │      (Per-Tenant KPI Aggregation & Health Tracking)      │
    │   ──────────────────────────────────────────────────────  │
    │   • Per-tenant metrics, anomaly detection, cohort rollup  │
    │   • Escalates to: Support Mgr, Program Onboarding Mgr   │
    │   • Data from: Kusto, Support cases, ICM incidents       │
    └──────────────────────────────────────────────────────────┘
                              ▲
                              │
    ┌──────────────────────────────────────────────────────────┐
    │      8. CONTACTS & ESCALATION FINDER                     │
    │      (Contact Discovery & Routing)                       │
    │   ──────────────────────────────────────────────────────  │
    │   • PG/CSS contact discovery, escalation routing         │
    │   • Escalates to: Target contact (PG lead, CSS mgr)     │
    │   • Requests from: All agents, Orchestrator              │
    │   • GUARDRAIL: Never fabricate contacts                  │
    └──────────────────────────────────────────────────────────┘
```

---

## Request Routing Examples

### Example 1: "What's at SLA risk this week?"
```
User Request
    │
    ▼
Orchestrator
    ├─ Route to: Support Case Manager (DFM query)
    ├─ Route to: Escalation Manager (ICM analysis)
    ├─ Route to: Tenant Health Monitor (scope impact)
    │
    ▼ (parallel execution)
    ├── Support Case Manager
    │   └─ Find cases where SLA < 4 hours
    │
    ├── Escalation Manager
    │   └─ Assess severity & customer impact
    │
    └── Tenant Health Monitor
        └─ Roll up impact by cohort
    │
    ▼ (synthesis)
Orchestrator
    ├─ Combine findings
    ├─ Rank by risk
    ├─ Cite evidence (DFM #, ICM #, tenant list)
    ├─ Route to: Contacts Finder (who to notify)
    │
    ▼
User Response
    └─ "3 cases at risk; highest impact Contoso Tenant X; escalate to Y immediately"
```

---

### Example 2: "Diagnose DFM case #123"
```
User Request
    │
    ▼
Orchestrator (request analysis)
    │
    ├─ Route to: Support Case Manager (retrieve case details)
    │   └─ Get: issue description, customer, support history
    │
    ▼ (synthesis point)
    │
    ├─ Route to: Purview Product Expert (root cause diagnosis)
    │   └─ Check: known issues, troubleshooting playbook
    │
    ├─ Route to: Work Item Manager (check for linked ADO bug)
    │   └─ If linked: provide fix status & ETA
    │
    ├─ Route to: Escalation Manager (is this systemic?)
    │   └─ If systemic: flag & provide incident #
    │
    ▼
Orchestrator (synthesis)
    │
    ├─ If known issue: "Known bug ADO #999; workaround: [X]; ETA: [Y]"
    ├─ If root cause unknown: "Escalating to Purview PG for diagnosis"
    ├─ If systemic: "Affects 5 tenants; ICM incident #ABC opened"
    │
    ▼
User Response (evidence-backed, actionable)
```

---

### Example 3: "What access does a new PM need?"
```
User Request
    │
    ▼
Orchestrator
    │
    ├─ Route to: Access & Role Manager (role definition)
    │   └─ Look up: PM role definition, least-privilege defaults
    │
    ▼
Access & Role Manager
    │
    ├─ Provide: access checklist
    │   ├─ DFM: case reader, no edit
    │   ├─ ICM: viewer, org chart
    │   ├─ ADO: backlog viewer
    │   └─ Tenant: read-only, assigned customers only
    │
    ├─ Provide: approval workflow & SLA
    │ 
    └─ Route to: Contacts Finder (if approvals needed)
    │
    ▼
User Response (step-by-step, policy-compliant)
```

---

## Guardrail Enforcement

```
┌────────────────────────────────────────────────────┐
│        INPUT: User Request + Persona/Role          │
└────────────────────────────────────────────────────┘
                        ▼
        ┌───────────────────────────────────┐
        │  1. Authorization Check            │
        │  ├─ Is user authorized for data?  │
        │  └─ Deny if insufficient scope    │
        └───────────────────────────────────┘
                        ▼
        ┌───────────────────────────────────┐
        │  2. Data Retrieval & Processing   │
        │  ├─ Pull from DFM/ICM/ADO/Kusto  │
        │  └─ Apply business logic          │
        └───────────────────────────────────┘
                        ▼
        ┌───────────────────────────────────┐
        │  3. PII Redaction & Masking       │
        │  ├─ Default: redact all PII       │
        │  ├─ Exception: PM role → names OK │
        │  └─ Always mask emails, IDs       │
        └───────────────────────────────────┘
                        ▼
        ┌───────────────────────────────────┐
        │  4. Evidence Validation           │
        │  ├─ Cite source (DFM/ICM/ADO)    │
        │  ├─ Check for fabrication         │
        │  └─ Never guess contacts/IDs      │
        └───────────────────────────────────┘
                        ▼
        ┌───────────────────────────────────┐
        │  5. Escalation Rule Enforcement   │
        │  ├─ SLA < 4h? → Always escalate   │
        │  ├─ VIP at risk? → Escalate now   │
        │  └─ Otherwise → Check threshold   │
        └───────────────────────────────────┘
                        ▼
┌────────────────────────────────────────────────────┐
│  OUTPUT: Findings (redacted, evidence-backed,      │
│           escalation-ready, actionable)             │
└────────────────────────────────────────────────────┘
```

---

## Knowledge Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                  PURVIEW PRODUCT MAP                        │
│  (Master knowledge: features, architecture, limitations)    │
└─────────────────────────────────────────────────────────────┘
        ▲
        │ referenced by
        │
    ┌───┴────────────────────────────────────────────┐
    │                                                │
    ▼                                                ▼
┌──────────────────────────┐             ┌──────────────────────────┐
│ GROUNDING DOCS:          │             │ SUB-AGENT EXPERTISE:     │
│ Purview Product Domain   │             │ Purview Product Expert   │
│                          │             │                          │
│ • Architecture           │             │ • Answers questions      │
│ • Known issues           │             │ • Diagnoses problems     │
│ • Playbooks              │             │ • Maps to ADO            │
│ • Feature guides         │             │ • Assesses readiness     │
└──────────────────────────┘             └──────────────────────────┘
    │                                        │
    └────────────────────────┬───────────────┘
                             │
                             ▼ (informs)
                    ┌──────────────────────┐
                    │ Orchestrator Response│
                    │                      │
                    │ "Known issue ADO#X;  │
                    │  Workaround: [Y];    │
                    │  ETA: [Z]"           │
                    └──────────────────────┘
```

---

## Success Flow

```
Request In
    │
    ▼
Sub-agents execute
(in parallel when possible)
    │
    ├─ Purview Product Expert: ✓ Diagnosis
    ├─ Support Case Manager: ✓ Cases @ risk
    ├─ Escalation Manager: ✓ Impact scope
    ├─ Work Item Manager: ✓ Fix status
    ├─ Tenant Health Monitor: ✓ Cohort health
    └─ Contacts Finder: ✓ Escalation path
    │
    ▼
Orchestrator synthesis
    │
    ├─ ✓ Evidence collected
    ├─ ✓ Guardrails applied (PII, auth, escalation)
    ├─ ✓ Findings ranked by impact
    ├─ ✓ Next actions identified
    │
    ▼
Response generation
    │
    ├─ Finding (headline)
    ├─ Scope (who affected, how many)
    ├─ Evidence (DFM #, ICM #, ADO #, links)
    ├─ Why (root cause, context)
    ├─ Next best action (1-3 options)
    │
    ▼
User Response ✅
(Actionable, evidence-backed, escalation-ready)
```

---

**This architecture ensures comprehensive, evidence-backed, governance-compliant product health & escalation orchestration across the Purview ecosystem.**
