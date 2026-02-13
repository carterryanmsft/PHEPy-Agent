# PHEPy Orchestrator Agent – Comprehensive To-Do List

**Last Updated:** February 5, 2026  
**Project Status:** ✅ Core Structure Complete | ⏳ Implementation Phase | 🧹 Optimization Ready

---

## 🧹 WORKSPACE OPTIMIZATION (NEW - February 5, 2026)

### ✅ Analysis Complete
- [x] Comprehensive workspace review completed
- [x] Identified 60+ old HTML reports for cleanup
- [x] Identified 15+ duplicate scripts for consolidation
- [x] Identified 25+ temp/test files for archiving
- [x] Created optimization roadmap

### 📚 Documentation Created
- [x] **WORKSPACE_REVIEW_SUMMARY.md** - Executive summary with quick start
- [x] **CLEANUP_PLAN.md** - Complete 4-phase cleanup plan
- [x] **OPTIMIZATION_GUIDE.md** - Function-level optimization details

### ⏳ Ready to Implement

#### Phase 1: Safe Cleanup (Priority: HIGH) ⚡
**Time**: 15 minutes | **Risk**: ZERO | **Impact**: Save 150 MB

- [ ] **1.1** Archive old HTML reports (60+ files)
  - **Action**: Run PowerShell script in WORKSPACE_REVIEW_SUMMARY.md
  - **Impact**: ~50-80 MB saved
  - **Risk**: None - keeps latest 3 reports
  
- [ ] **1.2** Archive temp/test data files
  - **Location**: risk_reports/data/
  - **Impact**: ~20-30 MB saved
  - **Files**: *test*.csv, *sample*.csv, *temp*.json
  
- [ ] **1.3** Archive old exports
  - **Files**: export (9).csv, temp_data.json
  - **Impact**: ~5-10 MB saved

#### Phase 2: Script Consolidation (Priority: MEDIUM) 🔧
**Time**: 1-2 hours | **Risk**: LOW | **Impact**: Single source of truth

- [ ] **2.1** Archive duplicate "131 case" scripts (15 files)
  - **Keep**: write_all_cases.py
  - **Archive**: save_*131*.py, complete_131_report.py, etc.
  
- [ ] **2.2** Consolidate report generators (12 files)
  - **Keep**: ic_mcs_risk_report_generator.py, run_ic_report.py, run_mcs_report.py
  - **Archive**: generate_*report*.py (10+ files)
  
- [ ] **2.3** Consolidate workflow scripts (5 files)
  - **Keep**: automated_workflow.py
  - **Archive**: complete_workflow.py, full_workflow.py, etc.
  
- [ ] **2.4** Test all workflows after consolidation
  - [ ] IC report generation
  - [ ] MCS report generation
  - [ ] Email sending
  - [ ] Sub-agent functionality

#### Phase 3: Performance Optimization (Priority: MEDIUM) 🚀
**Time**: 4-6 hours | **Risk**: MEDIUM | **Impact**: 30-40% faster

- [ ] **3.1** Create shared utilities module (phepy_utils.py)
  - **Functions**: load_kusto_json, save_to_csv, deduplicate_cases, parse_icm_ids
  - **Impact**: Eliminate 40% code duplication
  
- [ ] **3.2** Optimize ic_mcs_risk_report_generator.py
  - [ ] Replace row iteration with vectorized operations
  - [ ] Extract HTML templates to separate files
  - [ ] Implement caching layer for ICM/bug data
  - **Impact**: 30-40% faster report generation
  
- [ ] **3.3** Enhance write_all_cases.py
  - [ ] Add data validation
  - [ ] Add progress indicators
  - [ ] Add deduplication logic
  - **Impact**: 10-15% faster processing
  
- [ ] **3.4** Performance testing
  - [ ] Benchmark before/after times
  - [ ] Verify identical output
  - [ ] Test with large datasets

#### Phase 4: Documentation Cleanup (Priority: LOW) 📚
**Time**: 2-3 hours | **Risk**: ZERO | **Impact**: Better navigation

- [ ] **4.1** Reorganize root documentation
  - **Move to docs/**: ADVANCED_CAPABILITIES.md, CAPABILITY_MATRIX.md, etc.
  - **Keep in root**: README.md, INDEX.md, TODO.md, GETTING_STARTED.md
  
- [ ] **4.2** Consolidate risk_reports documentation
  - **Merge into**: README.md, docs/workflow_guide.md, docs/troubleshooting.md
  
- [ ] **4.3** Update all internal links
  - [ ] Verify no broken references
  - [ ] Update navigation in INDEX.md

---

## 📊 Project Status Summary

### ✅ COMPLETED (100%)

#### Core Documentation (10 files)
- [x] README.md – Root project overview
- [x] QUICK_START.md – 3-step quick start guide
- [x] EXECUTIVE_BRIEFING.md – Leadership briefing with ROI
- [x] AGENT_INSTRUCTIONS.md – 50-page orchestrator specification
- [x] PROJECT_SUMMARY.md – 30-page comprehensive overview
- [x] FOLDER_STRUCTURE.md – Organization & integration guide
- [x] ARCHITECTURE_DIAGRAM.md – Visual system design
- [x] COMPLETION_SUMMARY.md – Deliverables summary
- [x] INDEX.md – Complete documentation index
- [x] mcp.json – MCP server configuration (5 connectors)

#### Sub-Agent Specifications (8 files)
- [x] purview_product_expert/AGENT_INSTRUCTIONS.md
- [x] support_case_manager/AGENT_INSTRUCTIONS.md
- [x] escalation_manager/AGENT_INSTRUCTIONS.md
- [x] work_item_manager/AGENT_INSTRUCTIONS.md
- [x] program_onboarding_manager/AGENT_INSTRUCTIONS.md
- [x] access_role_manager/AGENT_INSTRUCTIONS.md
- [x] tenant_health_monitor/AGENT_INSTRUCTIONS.md
- [x] contacts_escalation_finder/AGENT_INSTRUCTIONS.md

#### Folder Structure (14 directories)
- [x] grounding_docs/ (6 domain folders)
  - [x] purview_product/
  - [x] phe_program_operations/
  - [x] support_escalation/
  - [x] contacts_access/
  - [x] customer_tenant_data/
  - [x] continuous_improvement/
- [x] sub_agents/ (8 sub-agent folders)

**Total Complete:** 18 files, 14 folders

---

## ⏳ IN PROGRESS / TO DO

### Phase 1: Review & Approval (Week 1) – 0% Complete

#### Team Alignment
- [ ] **1.1** Schedule kickoff meeting with PHE leadership
  - **Owner:** [Your Name]
  - **Duration:** 1 hour
  - **Attendees:** PHE PM, Escalation Owner, key stakeholders
  - **Goal:** Present project, get sign-off, assign roles

- [ ] **1.2** Distribute core documentation to team
  - [ ] Share QUICK_START.md with all team members
  - [ ] Share EXECUTIVE_BRIEFING.md with leadership
  - [ ] Share AGENT_INSTRUCTIONS.md with architects/engineers
  - **Owner:** [Your Name]
  - **Deadline:** End of Week 1

- [ ] **1.3** Review session: Orchestrator spec
  - **Owner:** PHE PM + Architects
  - **Duration:** 2 hours
  - **Action:** Review AGENT_INSTRUCTIONS.md, confirm operating principles, guardrails
  - **Output:** Approved spec or change requests

- [ ] **1.4** Review session: Sub-agent roles
  - **Owner:** PHE PM + Team Leads
  - **Duration:** 2 hours
  - **Action:** Review 2-3 sub-agent specs, validate responsibilities
  - **Output:** Approved sub-agent roles

#### Role Assignments
- [ ] **1.5** Assign Sub-Agent Owners (8 people)
  - [ ] Purview Product Expert Owner: [TBD]
  - [ ] Support Case Manager Owner: [TBD]
  - [ ] Escalation Manager Owner: [TBD]
  - [ ] Work Item Manager Owner: [TBD]
  - [ ] Program Onboarding Manager Owner: [TBD]
  - [ ] Access & Role Manager Owner: [TBD]
  - [ ] Tenant Health Monitor Owner: [TBD]
  - [ ] Contacts & Escalation Finder Owner: [TBD]
  - **Owner:** PHE PM
  - **Deadline:** End of Week 1

- [ ] **1.6** Assign Grounding Doc Lead
  - **Owner:** PHE PM
  - **Role:** Coordinates population of 44 reference files
  - **Assigned to:** [TBD]
  - **Deadline:** End of Week 1

- [ ] **1.7** Assign MCP Integration Lead
  - **Owner:** PHE PM
  - **Role:** Configures connectors, tests connectivity
  - **Assigned to:** [TBD]
  - **Deadline:** End of Week 1

#### Budget & Resource Approval
- [ ] **1.8** Finalize budget & resource allocation
  - **Owner:** PHE PM + Finance
  - **Required:** 2-3 FTE for 8 weeks + 0.5 FTE ongoing
  - **Deadline:** End of Week 1

- [ ] **1.9** Get leadership sign-off
  - **Owner:** PHE PM
  - **Approvers:** [List key decision-makers]
  - **Deadline:** End of Week 1

---

### Phase 2: Grounding Doc Population (Weeks 2-4) – 0% Complete

#### Domain 1: Purview Product (10 files) – HIGH PRIORITY
- [ ] **2.1** purview_product_architecture.md
  - **Content:** Service map, features, dependencies, scalability thresholds
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐⭐⭐ CRITICAL (Day 1-2)
  - **Estimated Time:** 4 hours

- [ ] **2.2** purview_known_issues.md
  - **Content:** Known issues, workarounds, ADO links, status
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐⭐⭐ CRITICAL (Day 1-2)
  - **Estimated Time:** 6 hours

- [ ] **2.3** purview_troubleshooting_playbooks.md
  - **Content:** Symptom → Root Cause → Remediation
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 8 hours

- [ ] **2.4** mip_dip_guide.md
  - **Content:** MIP/DIP feature coverage, configuration, common issues
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐⭐ HIGH (Day 6-10)
  - **Estimated Time:** 4 hours

- [ ] **2.5** dlp_policies_guide.md
  - **Content:** DLP framework, policy patterns, false positives
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐⭐ HIGH (Day 6-10)
  - **Estimated Time:** 4 hours

- [ ] **2.6** ediscovery_guide.md
  - **Content:** eDiscovery workflows, performance at scale
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 3 hours

- [ ] **2.7** irm_guide.md
  - **Content:** Information Rights Management, licensing, encryption
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 3 hours

- [ ] **2.8** dlm_retention_guide.md
  - **Content:** Data Lifecycle Management, retention schedules, holds
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 3 hours

- [ ] **2.9** insider_risk_guide.md
  - **Content:** Insider Risk detection, tuning, investigator workflows
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 3 hours

- [ ] **2.10** scanning_labeling_guide.md
  - **Content:** Data discovery, scanning, automated labeling
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 3 hours

**Domain 1 Total Time:** ~40 hours (~1 week for 1 person)

---

#### Domain 2: PHE Program Operations (6 files) – HIGH PRIORITY
- [ ] **2.11** mcs_ic_cohort_registry.md
  - **Content:** Cohort definitions, tenant lists, timelines, ownership
  - **Owner:** Program Onboarding Manager Owner
  - **Priority:** ⭐⭐⭐ CRITICAL (Day 1-2)
  - **Estimated Time:** 6 hours

- [ ] **2.12** phe_onboarding_runbook.md
  - **Content:** Phased tasks, gates, checklist, comms templates
  - **Owner:** Program Onboarding Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 6 hours

- [ ] **2.13** roles_responsibilities_matrix.md
  - **Content:** RACI, role definitions, responsibilities
  - **Owner:** Access & Role Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 4 hours

- [ ] **2.14** phe_playbooks.md
  - **Content:** SLA breach, VIP handling, bug filing, rollback playbooks
  - **Owner:** Escalation Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 6 hours

- [ ] **2.15** comms_templates.md
  - **Content:** Kickoff, weekly, risk alerts, completion comms
  - **Owner:** Program Onboarding Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 6-10)
  - **Estimated Time:** 4 hours

- [ ] **2.16** lifecycle_cadences.md
  - **Content:** Review schedules, governance meetings, decision checkpoints
  - **Owner:** Program Onboarding Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 6-10)
  - **Estimated Time:** 3 hours

**Domain 2 Total Time:** ~30 hours (~1 week for 1 person)

---

#### Domain 3: Support & Escalation (7 files) – MEDIUM PRIORITY
- [ ] **2.17** dfm_integration_guide.md
  - **Content:** DFM metadata, lifecycle, connector capabilities
  - **Owner:** Support Case Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 5 hours

- [ ] **2.18** dfm_sla_definitions.md
  - **Content:** SLA tiers, thresholds, escalation rules
  - **Owner:** Support Case Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 4 hours

- [ ] **2.19** icm_integration_guide.md
  - **Content:** ICM schema, incident classification, state machine
  - **Owner:** Escalation Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 5 hours

- [ ] **2.20** icm_severity_mapping.md
  - **Content:** Severity levels, customer impact classification
  - **Owner:** Escalation Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 6-10)
  - **Estimated Time:** 4 hours

- [ ] **2.21** ado_integration_guide.md
  - **Content:** Work item types, priority mapping, release planning
  - **Owner:** Work Item Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 6-10)
  - **Estimated Time:** 5 hours

- [ ] **2.22** escalation_decision_tree.md
  - **Content:** When to escalate, approval chains, comms
  - **Owner:** Escalation Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 4 hours

- [ ] **2.23** sla_breach_playbook.md
  - **Content:** Breach prevention, recovery, escalation procedures
  - **Owner:** Support Case Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 4 hours

**Domain 3 Total Time:** ~31 hours (~1 week for 1 person)

---

#### Domain 4: Contacts & Access (6 files) – HIGH PRIORITY
- [ ] **2.24** pg_css_contacts.md
  - **Content:** PG leads, CSS managers, on-call rotations
  - **Owner:** Contacts & Escalation Finder Owner
  - **Priority:** ⭐⭐⭐ CRITICAL (Day 1-2)
  - **Estimated Time:** 6 hours

- [ ] **2.25** escalation_contacts.md
  - **Content:** Critical escalation paths by component
  - **Owner:** Contacts & Escalation Finder Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 4 hours

- [ ] **2.26** initiatives_pilots.md
  - **Content:** Active initiatives, pilot cohorts, risks, blockers
  - **Owner:** Program Onboarding Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 6-10)
  - **Estimated Time:** 4 hours

- [ ] **2.27** role_access_runbooks.md
  - **Content:** PM, IC, CSS, Engineer access setup
  - **Owner:** Access & Role Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 6 hours

- [ ] **2.28** least_privilege_defaults.md
  - **Content:** Default access levels by role
  - **Owner:** Access & Role Manager Owner
  - **Priority:** ⭐⭐ HIGH (Day 6-10)
  - **Estimated Time:** 4 hours

- [ ] **2.29** access_approval_workflows.md
  - **Content:** Request, approval, provisioning procedures
  - **Owner:** Access & Role Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 3 hours

**Domain 4 Total Time:** ~27 hours (~1 week for 1 person)

---

#### Domain 5: Customer & Tenant Data (5 files) – MEDIUM PRIORITY
- [ ] **2.30** customer_list_registry.md
  - **Content:** Customer ID, tenant ID, segment, assignment, SLA tier
  - **Owner:** Tenant Health Monitor Owner
  - **Priority:** ⭐⭐ HIGH (Day 3-5)
  - **Estimated Time:** 6 hours

- [ ] **2.31** tenant_registry.md
  - **Content:** Tenant IDs, customer mapping, region, national cloud
  - **Owner:** Tenant Health Monitor Owner
  - **Priority:** ⭐⭐ HIGH (Day 6-10)
  - **Estimated Time:** 5 hours

- [ ] **2.32** tenant_health_metrics.md
  - **Content:** KPIs, adoption, support metrics per tenant
  - **Owner:** Tenant Health Monitor Owner
  - **Priority:** ⭐⭐ HIGH (Day 6-10)
  - **Estimated Time:** 5 hours

- [ ] **2.33** vip_customer_list.md
  - **Content:** VIP customers, contacts, SLA overrides
  - **Owner:** Support Case Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 3 hours

- [ ] **2.34** customer_segments.md
  - **Content:** Segment definitions (Enterprise, Mid-market, SMB, Gov)
  - **Owner:** Tenant Health Monitor Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 2 hours

**Domain 5 Total Time:** ~21 hours (~0.5 week for 1 person)

---

#### Domain 6: Continuous Improvement (10 files) – MEDIUM PRIORITY
- [ ] **2.35** lessons_learned_registry.md
  - **Content:** Post-mortem findings, root causes, prevention measures
  - **Owner:** PHE PM / Ops Lead
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 4 hours

- [ ] **2.36** customer_feedback_log.md
  - **Content:** Customer satisfaction, NPS, feature requests, pain points
  - **Owner:** Program Onboarding Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 3 hours

- [ ] **2.37** team_feedback_log.md
  - **Content:** Internal feedback, process improvements, tool enhancements
  - **Owner:** PHE PM / Ops Lead
  - **Priority:** ⭐ MEDIUM (Day 11-15)
  - **Estimated Time:** 3 hours

- [ ] **2.38** kpi_trends_analysis.md
  - **Content:** Historical KPI data, trend analysis, performance tracking
  - **Owner:** Tenant Health Monitor Owner
  - **Priority:** ⭐ MEDIUM (Day 16-20)
  - **Estimated Time:** 4 hours

- [ ] **2.39** escalation_pattern_analysis.md
  - **Content:** Recurring escalation patterns, root cause themes
  - **Owner:** Escalation Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 16-20)
  - **Estimated Time:** 4 hours

- [ ] **2.40** sla_compliance_trends.md
  - **Content:** SLA performance over time, breach analysis, improvements
  - **Owner:** Support Case Manager Owner
  - **Priority:** ⭐ MEDIUM (Day 16-20)
  - **Estimated Time:** 4 hours

- [ ] **2.41** process_optimization_backlog.md
  - **Content:** Identified inefficiencies, proposed improvements, status
  - **Owner:** PHE PM / Ops Lead
  - **Priority:** ⭐ MEDIUM (Day 16-20)
  - **Estimated Time:** 3 hours

- [ ] **2.42** automation_opportunities.md
  - **Content:** Manual tasks to automate, ROI estimates, priorities
  - **Owner:** Engineering Lead
  - **Priority:** ⭐ MEDIUM (Day 16-20)
  - **Estimated Time:** 3 hours

- [ ] **2.43** runbook_improvements.md
  - **Content:** Updates to playbooks, onboarding, troubleshooting guides
  - **Owner:** Purview Product Expert Owner
  - **Priority:** ⭐ LOW (Day 21+)
  - **Estimated Time:** 3 hours

- [ ] **2.44** pilot_results.md
  - **Content:** Pilot program outcomes, success metrics, scale recommendations
  - **Owner:** Program Onboarding Manager Owner
  - **Priority:** ⭐ LOW (Day 21+)
  - **Estimated Time:** 3 hours

- [ ] **2.45** feature_adoption_analysis.md
  - **Content:** Feature usage trends, adoption barriers, enablement plans
  - **Owner:** Tenant Health Monitor Owner
  - **Priority:** ⭐ LOW (Day 21+)
  - **Estimated Time:** 3 hours

- [ ] **2.46** tool_evaluation.md
  - **Content:** New tools evaluated, pros/cons, adoption decisions
  - **Owner:** Engineering Lead
  - **Priority:** ⭐ LOW (Day 21+)
  - **Estimated Time:** 3 hours

**Domain 6 Total Time:** ~40 hours (~1 week for 1 person)

---

**GROUNDING DOCS TOTAL:** 44 files, ~189 hours (~5 weeks for 1 dedicated person or 2-3 weeks with team)

---

### Phase 3: MCP Integration (Week 5) – 0% Complete

#### MCP Server Configuration
- [ ] **3.1** Configure o365exchange-mcp-server (ADO bugs/DCRs)
  - **Owner:** MCP Integration Lead
  - **Action:** Test connectivity, validate ID format (3563451)
  - **Estimated Time:** 4 hours
  - **Deadline:** Day 1

- [ ] **3.2** Configure ASIM-Security-mcp-server
  - **Owner:** MCP Integration Lead
  - **Action:** Test connectivity, validate query patterns
  - **Estimated Time:** 3 hours
  - **Deadline:** Day 1

- [ ] **3.3** Configure ICM MCP ENG (HTTP endpoint)
  - **Owner:** MCP Integration Lead
  - **Action:** Test connectivity, validate ID format (728221759, 51000000877262, 21000000855343)
  - **Estimated Time:** 4 hours
  - **Deadline:** Day 2

- [ ] **3.4** Configure enterprise-mcp (DFM support cases)
  - **Owner:** MCP Integration Lead
  - **Action:** Test connectivity, validate PII guardrails, test ID format
  - **Estimated Time:** 6 hours
  - **Deadline:** Day 2

- [ ] **3.5** Configure kusto-mcp (telemetry & diagnostics)
  - **Owner:** MCP Integration Lead
  - **Action:** Test connectivity, validate query syntax, test data retrieval
  - **Estimated Time:** 5 hours
  - **Deadline:** Day 3

#### Connector Testing
- [ ] **3.6** Test DFM connector with real case IDs
  - **Owner:** Support Case Manager Owner + MCP Integration Lead
  - **Test Cases:** Retrieve case, redact PII, validate SLA data
  - **Estimated Time:** 4 hours
  - **Deadline:** Day 3

- [ ] **3.7** Test ICM connector with real incident IDs
  - **Owner:** Escalation Manager Owner + MCP Integration Lead
  - **Test Cases:** Retrieve incident, assess severity, validate timeline
  - **Estimated Time:** 4 hours
  - **Deadline:** Day 4

- [ ] **3.8** Test ADO connector with real work item IDs
  - **Owner:** Work Item Manager Owner + MCP Integration Lead
  - **Test Cases:** Retrieve work item, check status, validate links
  - **Estimated Time:** 4 hours
  - **Deadline:** Day 4

- [ ] **3.9** Test Kusto queries for tenant health
  - **Owner:** Tenant Health Monitor Owner + MCP Integration Lead
  - **Test Cases:** Run KPI query, validate data freshness, test aggregation
  - **Estimated Time:** 4 hours
  - **Deadline:** Day 5

#### Guardrail Testing
- [ ] **3.10** Test PII redaction rules
  - **Owner:** MCP Integration Lead + Security
  - **Test Cases:** Retrieve customer data, verify masking, test role-based reveal
  - **Estimated Time:** 4 hours
  - **Deadline:** Day 5

- [ ] **3.11** Test role-based access controls
  - **Owner:** Access & Role Manager Owner + MCP Integration Lead
  - **Test Cases:** PM role, IC role, Escalation Owner role access scopes
  - **Estimated Time:** 4 hours
  - **Deadline:** Day 5

#### Performance & Reliability
- [ ] **3.12** Test connector latency & response time
  - **Owner:** MCP Integration Lead
  - **Target:** < 2 min for complex queries, < 30 sec for cached
  - **Estimated Time:** 3 hours
  - **Deadline:** Day 5

- [ ] **3.13** Test connector failover & error handling
  - **Owner:** MCP Integration Lead
  - **Test Cases:** Connector unavailable, timeout, invalid ID
  - **Estimated Time:** 3 hours
  - **Deadline:** Day 5

#### Documentation
- [ ] **3.14** Document connector setup & troubleshooting
  - **Owner:** MCP Integration Lead
  - **Output:** Connector troubleshooting guide, known issues
  - **Estimated Time:** 4 hours
  - **Deadline:** End of Week 5

**MCP Integration Total Time:** ~56 hours (~1.5 weeks for 1 person)

---

### Phase 4: Orchestrator & Sub-Agent Testing (Weeks 6-7) – 0% Complete

#### Unit Testing (Per Sub-Agent)
- [ ] **4.1** Test Purview Product Expert scenarios
  - [ ] Query known issues
  - [ ] Diagnose product bug
  - [ ] Assess feature readiness
  - [ ] Detect systemic issue
  - **Owner:** Purview Product Expert Owner
  - **Estimated Time:** 6 hours

- [ ] **4.2** Test Support Case Manager scenarios
  - [ ] Retrieve at-risk cases
  - [ ] Flag SLA breach
  - [ ] Trend analysis
  - [ ] Escalation recommendation
  - **Owner:** Support Case Manager Owner
  - **Estimated Time:** 6 hours

- [ ] **4.3** Test Escalation Manager scenarios
  - [ ] Retrieve incident details
  - [ ] Assess customer impact
  - [ ] Detect systemic incident
  - [ ] Recommend escalation path
  - **Owner:** Escalation Manager Owner
  - **Estimated Time:** 6 hours

- [ ] **4.4** Test Work Item Manager scenarios
  - [ ] Retrieve bug status
  - [ ] Link case to ADO
  - [ ] Assess blocker impact
  - [ ] Recommend priority
  - **Owner:** Work Item Manager Owner
  - **Estimated Time:** 6 hours

- [ ] **4.5** Test Program Onboarding Manager scenarios
  - [ ] Check cohort status
  - [ ] Validate go-live readiness
  - [ ] Flag blocker
  - [ ] Activate comms template
  - **Owner:** Program Onboarding Manager Owner
  - **Estimated Time:** 6 hours

- [ ] **4.6** Test Access & Role Manager scenarios
  - [ ] Assign role to new PM
  - [ ] Validate least-privilege
  - [ ] Troubleshoot access denial
  - [ ] Conduct access review
  - **Owner:** Access & Role Manager Owner
  - **Estimated Time:** 6 hours

- [ ] **4.7** Test Tenant Health Monitor scenarios
  - [ ] Aggregate per-tenant KPIs
  - [ ] Detect adoption anomaly
  - [ ] Roll up cohort health
  - [ ] Alert on tenant risk
  - **Owner:** Tenant Health Monitor Owner
  - **Estimated Time:** 6 hours

- [ ] **4.8** Test Contacts & Escalation Finder scenarios
  - [ ] Find PG lead
  - [ ] Find CSS manager
  - [ ] Route escalation
  - [ ] Validate contact currency
  - **Owner:** Contacts & Escalation Finder Owner
  - **Estimated Time:** 6 hours

#### Integration Testing (Multi-Agent Coordination)
- [ ] **4.9** Test orchestrator routing logic
  - [ ] Single-agent requests
  - [ ] Multi-agent coordination
  - [ ] Complex query analysis
  - **Owner:** All Sub-Agent Owners + Architect
  - **Estimated Time:** 8 hours

- [ ] **4.10** Test evidence collection & synthesis
  - [ ] Orchestrator aggregates findings from 3+ sub-agents
  - [ ] Validate citations (DFM #, ICM #, ADO #)
  - [ ] Check "why, evidence, next action" format
  - **Owner:** PHE PM + Architect
  - **Estimated Time:** 6 hours

- [ ] **4.11** Test escalation workflows end-to-end
  - [ ] SLA breach detection → escalation → contact routing
  - [ ] VIP customer issue → impact assessment → leadership notification
  - [ ] Systemic issue → multi-agent analysis → recommendation
  - **Owner:** Escalation Manager Owner + All Sub-Agent Owners
  - **Estimated Time:** 8 hours

#### Scenario Walkthroughs (10 Real-World Scenarios)
- [ ] **4.12** Scenario 1: "What's at SLA risk this week?"
  - **Agents Involved:** Support Case Manager, Escalation Manager, Tenant Health Monitor
  - **Owner:** Support Case Manager Owner
  - **Estimated Time:** 2 hours

- [ ] **4.13** Scenario 2: "Diagnose DFM case #123456"
  - **Agents Involved:** Support Case Manager, Purview Product Expert, Work Item Manager
  - **Owner:** Purview Product Expert Owner
  - **Estimated Time:** 2 hours

- [ ] **4.14** Scenario 3: "What's the status of MCS Alpha cohort?"
  - **Agents Involved:** Program Onboarding Manager, Tenant Health Monitor
  - **Owner:** Program Onboarding Manager Owner
  - **Estimated Time:** 2 hours

- [ ] **4.15** Scenario 4: "Is Tenant X at risk?"
  - **Agents Involved:** Tenant Health Monitor, Support Case Manager, Escalation Manager
  - **Owner:** Tenant Health Monitor Owner
  - **Estimated Time:** 2 hours

- [ ] **4.16** Scenario 5: "Who's the PG lead for DLP?"
  - **Agents Involved:** Contacts & Escalation Finder
  - **Owner:** Contacts & Escalation Finder Owner
  - **Estimated Time:** 1 hour

- [ ] **4.17** Scenario 6: "Set up access for new PM"
  - **Agents Involved:** Access & Role Manager
  - **Owner:** Access & Role Manager Owner
  - **Estimated Time:** 1 hour

- [ ] **4.18** Scenario 7: "When will ADO bug #999 be fixed?"
  - **Agents Involved:** Work Item Manager
  - **Owner:** Work Item Manager Owner
  - **Estimated Time:** 1 hour

- [ ] **4.19** Scenario 8: "Prepare go-live comms for MCS Beta"
  - **Agents Involved:** Program Onboarding Manager
  - **Owner:** Program Onboarding Manager Owner
  - **Estimated Time:** 2 hours

- [ ] **4.20** Scenario 9: "Assess impact of ICM incident #12345"
  - **Agents Involved:** Escalation Manager, Tenant Health Monitor, Contacts & Escalation Finder
  - **Owner:** Escalation Manager Owner
  - **Estimated Time:** 2 hours

- [ ] **4.21** Scenario 10: "Compare MCS Alpha vs. MCS Beta adoption"
  - **Agents Involved:** Tenant Health Monitor, Program Onboarding Manager
  - **Owner:** Tenant Health Monitor Owner
  - **Estimated Time:** 2 hours

#### User Acceptance Testing (UAT)
- [ ] **4.22** PHE PM UAT session
  - **Duration:** 4 hours
  - **Goal:** Validate orchestrator meets PM needs
  - **Owner:** PHE PM
  - **Deadline:** Week 7

- [ ] **4.23** Escalation Owner UAT session
  - **Duration:** 4 hours
  - **Goal:** Validate escalation workflows
  - **Owner:** Escalation Owner
  - **Deadline:** Week 7

- [ ] **4.24** CSS UAT session
  - **Duration:** 3 hours
  - **Goal:** Validate support case management
  - **Owner:** CSS Manager
  - **Deadline:** Week 7

- [ ] **4.25** Engineering UAT session
  - **Duration:** 3 hours
  - **Goal:** Validate work item tracking & deployment support
  - **Owner:** Engineering Lead
  - **Deadline:** Week 7

#### Feedback & Refinement
- [ ] **4.26** Collect UAT feedback
  - **Owner:** PHE PM
  - **Action:** Survey, interviews, bug reports
  - **Deadline:** End of Week 7

- [ ] **4.27** Prioritize feedback & create fix backlog
  - **Owner:** PHE PM + Architect
  - **Output:** Ranked list of fixes/enhancements
  - **Deadline:** End of Week 7

- [ ] **4.28** Implement critical fixes
  - **Owner:** MCP Integration Lead + Sub-Agent Owners
  - **Target:** Fix P0/P1 issues before production
  - **Deadline:** End of Week 7

**Testing Total Time:** ~100 hours (~2.5 weeks with team)

---

### Phase 5: Production Launch (Week 8) – 0% Complete

#### Pre-Launch Checklist
- [ ] **5.1** Final security review
  - [ ] PII redaction tested
  - [ ] Role-based access validated
  - [ ] No credentials hardcoded
  - **Owner:** Security / MCP Integration Lead
  - **Deadline:** Day 1

- [ ] **5.2** Final performance review
  - [ ] Response latency < 2 min
  - [ ] Connector uptime > 99%
  - [ ] No memory leaks
  - **Owner:** MCP Integration Lead
  - **Deadline:** Day 1

- [ ] **5.3** Backup & rollback plan
  - [ ] Document rollback procedure
  - [ ] Test rollback (dry run)
  - [ ] Identify rollback triggers
  - **Owner:** MCP Integration Lead + PHE PM
  - **Deadline:** Day 2

- [ ] **5.4** Monitoring & alerting setup
  - [ ] Deploy metrics dashboard
  - [ ] Configure SLA alerts
  - [ ] Set up on-call rotation
  - **Owner:** MCP Integration Lead + Ops
  - **Deadline:** Day 2

- [ ] **5.5** Documentation review
  - [ ] User guides up-to-date
  - [ ] Troubleshooting runbooks complete
  - [ ] Grounding docs indexed
  - **Owner:** Grounding Doc Lead
  - **Deadline:** Day 2

#### Team Training
- [ ] **5.6** Training Session 1: Orchestrator overview
  - **Audience:** All team members
  - **Duration:** 2 hours
  - **Content:** Capabilities, guardrails, common queries
  - **Owner:** PHE PM + Architect
  - **Deadline:** Day 3

- [ ] **5.7** Training Session 2: Sub-agent deep-dive
  - **Audience:** Sub-agent owners + power users
  - **Duration:** 2 hours
  - **Content:** Sub-agent responsibilities, data sources, scenarios
  - **Owner:** Sub-Agent Owners
  - **Deadline:** Day 3

- [ ] **5.8** Training materials
  - [ ] Quick reference card (1-pager)
  - [ ] Common query cheat sheet
  - [ ] Video walkthrough (optional)
  - **Owner:** PHE PM
  - **Deadline:** Day 3

#### Deployment
- [ ] **5.9** Deploy to production environment
  - **Owner:** MCP Integration Lead + Ops
  - **Method:** [Specify deployment method]
  - **Deadline:** Day 4

- [ ] **5.10** Smoke test in production
  - [ ] Test 5 common scenarios
  - [ ] Validate all connectors live
  - [ ] Check monitoring & alerts
  - **Owner:** MCP Integration Lead + Sub-Agent Owners
  - **Deadline:** Day 4

- [ ] **5.11** Go-live announcement
  - **Owner:** PHE PM
  - **Channel:** [Email, Slack, Teams]
  - **Content:** Capabilities, how to use, support contact
  - **Deadline:** Day 5

#### Post-Launch Monitoring
- [ ] **5.12** Week 1 daily standup
  - **Owner:** PHE PM
  - **Goal:** Monitor adoption, catch issues early
  - **Duration:** 15 min/day
  - **Deadline:** Days 5-9

- [ ] **5.13** Collect early feedback
  - **Owner:** PHE PM
  - **Method:** Survey, 1:1 interviews
  - **Deadline:** End of Week 1

- [ ] **5.14** 30-day health check
  - [ ] Review KPIs (escalation accuracy, response latency, etc.)
  - [ ] Identify improvement opportunities
  - [ ] Plan iteration 2
  - **Owner:** PHE PM + All Sub-Agent Owners
  - **Deadline:** 30 days post-launch

**Production Launch Total Time:** ~40 hours (~1 week with team)

---

## 📊 Summary by Phase

| Phase | Duration | Effort (Hours) | Status |
|-------|----------|----------------|--------|
| **Phase 1: Review & Approval** | 1 week | ~40 | ⏳ To Do |
| **Phase 2: Grounding Docs** | 2-3 weeks | ~189 | ⏳ To Do |
| **Phase 3: MCP Integration** | 1 week | ~56 | ⏳ To Do |
| **Phase 4: Testing & UAT** | 2 weeks | ~100 | ⏳ To Do |
| **Phase 5: Production Launch** | 1 week | ~40 | ⏳ To Do |
| **TOTAL** | **7-8 weeks** | **~425 hours** | **0% Complete** |

---

## 🎯 Critical Path Items (Must Complete First)

### Week 1 (CRITICAL)
1. Get leadership sign-off
2. Assign 8 sub-agent owners + grounding doc lead + MCP integration lead
3. Begin high-priority grounding docs:
   - purview_product_architecture.md
   - purview_known_issues.md
   - mcs_ic_cohort_registry.md
   - pg_css_contacts.md

### Weeks 2-4 (HIGH PRIORITY)
1. Complete all Domain 1-4 grounding docs (34 files)
2. Begin MCP connector configuration (parallel)

### Week 5 (HIGH PRIORITY)
1. Complete MCP integration & testing
2. Complete Domain 5-6 grounding docs (remaining 10 files)

### Weeks 6-7 (MEDIUM PRIORITY)
1. Complete testing & UAT
2. Refine based on feedback

### Week 8 (GO-LIVE)
1. Train team
2. Deploy to production
3. Monitor & iterate

---

## 📈 Success Metrics to Track

### Quality Metrics (Track Post-Launch)
- [ ] Escalation accuracy: > 95% (track weekly)
- [ ] At-risk detection: > 90% (track weekly)
- [ ] Response latency: < 2 min (track daily)
- [ ] False positive rate: < 10% (track weekly)
- [ ] PII compliance: 0 violations (track daily)
- [ ] Contact accuracy: > 99% (track weekly)

### Adoption Metrics (Track Post-Launch)
- [ ] User satisfaction: > 80% (survey monthly)
- [ ] Workflow coverage: > 80% (audit quarterly)
- [ ] Time savings: > 50% (measure at 30 days)
- [ ] Active users: track daily

---

## 🚨 Risks & Blockers

### Current Risks
- [ ] **RISK:** Grounding doc population takes longer than expected
  - **Mitigation:** Prioritize critical docs, accept 80% complete at launch
  - **Owner:** Grounding Doc Lead

- [ ] **RISK:** MCP connectors have latency/reliability issues
  - **Mitigation:** Implement caching, fallback to manual queries
  - **Owner:** MCP Integration Lead

- [ ] **RISK:** Team capacity (2-3 FTE for 8 weeks) not available
  - **Mitigation:** Extend timeline or reduce scope (defer Domain 6)
  - **Owner:** PHE PM

- [ ] **RISK:** User adoption low due to training/awareness gap
  - **Mitigation:** Multiple training sessions, quick reference materials
  - **Owner:** PHE PM

- [ ] **RISK:** PII compliance violation during testing
  - **Mitigation:** Test redaction early, involve security team
  - **Owner:** Security / MCP Integration Lead

---

## 📞 Escalation & Support

### Issue Escalation Path
1. **Sub-Agent Owner** → PHE PM (for sub-agent scope issues)
2. **MCP Integration Lead** → Engineering Lead (for connector issues)
3. **Grounding Doc Lead** → PHE PM (for content blockers)
4. **PHE PM** → Leadership (for budget/resource issues)

### Status Reporting
- [ ] Weekly status report to leadership (email)
- [ ] Bi-weekly team standup (30 min)
- [ ] Slack channel for async updates: [TBD]

---

## 📝 Notes & Assumptions

1. **Assumption:** 2-3 FTE available for 8 weeks (175-260 hours/person)
2. **Assumption:** MCP connectors are production-ready (minimal custom dev)
3. **Assumption:** Grounding doc content is available (not starting from scratch)
4. **Assumption:** Team has access to DFM, ICM, ADO, Kusto
5. **Assumption:** Security/compliance approval obtained

---

## ✅ Next Immediate Actions (This Week)

1. [ ] Schedule kickoff meeting with PHE leadership (1 hour)
2. [ ] Share EXECUTIVE_BRIEFING.md with decision-makers
3. [ ] Share QUICK_START.md with entire team
4. [ ] Assign 8 sub-agent owners + 2 leads (grounding doc, MCP integration)
5. [ ] Create Slack/Teams channel for project updates
6. [ ] Begin populating 3 critical grounding docs (product architecture, cohort registry, contacts)

**Owner:** [Your Name]  
**Deadline:** End of this week

---

**Last Updated:** February 4, 2026  
**Total To-Do Items:** 114+  
**Status:** ⏳ 0% Complete, Ready to Start  
**Timeline:** 7-8 weeks to production
