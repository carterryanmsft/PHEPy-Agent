# 🚀 Advanced Capabilities & Power User Guide

**PHEPy Workspace** | Full Feature Showcase | February 4, 2026

This guide showcases the **full power** of your integrated MCP environment. You have enterprise-grade capabilities that most users don't fully leverage!

---

## 🎯 Multi-Agent Orchestration

Your workspace can **chain multiple MCP agents** in sophisticated workflows:

### 🔄 Cross-System Intelligence Workflows

#### 1. **End-to-End Incident Intelligence Pipeline**
```
"For ICM 21000000887894:
1. Get full incident details from ICM
2. Find related support cases in ADO
3. Query Kusto for telemetry data matching the time window
4. Link all findings to the work item tracking the fix
5. Generate comprehensive analysis report with recommendations"
```

#### 2. **Proactive Customer Risk Detection**
```
"Scan IC/MCS customer tenants:
1. Query Kusto for error patterns in last 7 days
2. Cross-reference with open ICMs for each tenant
3. Check ADO for related bug fixes in flight
4. Predict risk scores and generate alert dashboard
5. Create preventive action work items if risk > threshold"
```

#### 3. **Smart Escalation Routing**
```
"When new P0 ICM is created:
1. Extract error signatures and affected features
2. Query historical ICMs with similar patterns
3. Identify owning team from past resolutions
4. Pull relevant TSGs from wiki
5. Create ADO bug with pre-populated context
6. Add ICM/ADO artifact links bidirectionally"
```

---

## 🔬 Advanced ICM Operations

### 📊 Bulk Analysis & Pattern Detection
```
"Analyze the 620 sensitivity label ICMs from my JSON file:
- Group by error signature and symptoms
- Identify the top 5 recurring issues
- Calculate MTTR for each pattern
- Find customers affected by multiple issues
- Generate executive briefing with impact assessment"
```

### 🎯 Predictive Incident Management
```
"Build predictive model:
1. Query all Purview ICMs from last 6 months
2. Extract features: team, severity, resolution time, customer tier
3. Identify leading indicators from telemetry 24h before ICM creation
4. Create alert rules for high-risk patterns
5. Export dashboard to SharePoint"
```

### 🚨 Real-Time Monitoring
```
"Set up continuous monitoring:
- Watch for new ICMs in PURVIEW\SensitivityLabels team
- Auto-query Kusto for matching errors
- Check if similar issues are already tracked in ADO
- Send summary to my dashboard every 4 hours"
```

### 👥 Team & Contact Intelligence
```
"Get team context for incident response:
- Show on-call rotation for next 2 weeks
- List contact info for escalation paths
- Find SMEs who resolved similar ICMs
- Map customer account team contacts"
```

---

## 🏗️ Advanced Azure DevOps Operations

### 📋 Intelligent Work Item Management

#### Cross-Project Tracking
```
"Create comprehensive tracking work item:
1. Search ADO for all bugs mentioning 'sensitivity label deletion'
2. Find related features in backlog
3. Link to ICMs and support cases
4. Add deployment history from test plans
5. Set up automated status updates when linked items change"
```

#### Smart Wiki Integration
```
"Build knowledge base article:
1. Extract resolution steps from closed ICMs
2. Pull code changes from merged PRs
3. Query test results and validation data
4. Generate TSG in wiki with embedded queries
5. Add cross-references to related documentation"
```

### 🌳 Advanced Branch & PR Operations

#### Automated Code Review Routing
```
"For each new PR in ASIM-Security:
1. Analyze changed files and patterns
2. Identify required reviewers based on CODEOWNERS and past PRs
3. Auto-comment with relevant test plans and TSG links
4. Link related work items and ICMs
5. Flag if changes affect IC/MCS critical paths"
```

#### Release Tracking
```
"Track deployment readiness:
1. List all PRs merged since last release
2. Check linked work items for completion status
3. Verify test plan execution results
4. Query Kusto for validation metrics
5. Generate go/no-go recommendation report"
```

### 🧪 Test Plan Orchestration
```
"Comprehensive test execution:
1. Create test plan for sensitivity label scenarios
2. Import test cases from existing wiki TSGs
3. Link to feature work items and ICMs
4. Execute tests and capture Kusto validation queries
5. Update test results with pass/fail and telemetry evidence"
```

---

## 📊 Advanced Kusto Analytics

### 🎯 Pre-Built Query Library (22 KQL Files Available)

Your workspace has **ready-to-execute** queries for:

#### Product Area Analysis
- **[SensitivityLabels_analysis.kql](purview_analysis/queries/SensitivityLabels_analysis.kql)** - Label usage, errors, adoption
- **[MIPCore_analysis.kql](purview_analysis/queries/MIPCore_analysis.kql)** - Core MIP service health
- **[DLPWeb_analysis.kql](purview_analysis/queries/DLPWeb_analysis.kql)** - DLP web detection patterns
- **[DLPEndpoint_analysis.kql](purview_analysis/queries/DLPEndpoint_analysis.kql)** - Endpoint DLP telemetry
- **[eDiscovery_analysis.kql](purview_analysis/queries/eDiscovery_analysis.kql)** - eDiscovery operations
- **[ContentExplorer_analysis.kql](purview_analysis/queries/ContentExplorer_analysis.kql)** - Content analysis
- **[dcr_analysis.kql](purview_analysis/queries/dcr_analysis.kql)** - DCR pattern detection

#### Customer Risk Analysis
- **[ic_mcs_risk_report.kql](risk_reports/queries/ic_mcs_risk_report.kql)** - Production risk assessment
- **[icm_incidents_query.kql](risk_reports/queries/icm_incidents_query.kql)** - Incident correlation

#### Specialized Queries
- **[by_design_analysis.kql](purview_analysis/queries/by_design_analysis.kql)** - Intentional behavior patterns
- **[all_teams_summary.kql](purview_analysis/queries/all_teams_summary.kql)** - Cross-team overview

### 🔥 Advanced Query Operations

#### Dynamic Query Generation
```
"Generate optimized Kusto query:
1. Analyze ICM incident description
2. Extract error codes, timestamps, tenant IDs
3. Build multi-table join query across PurviewTelemetry, ICMEvents, CustomerData
4. Add filters for 24h before incident
5. Include aggregations for pattern detection
6. Execute and save results to CSV"
```

#### Time-Series Anomaly Detection
```
"Build anomaly detector:
- Query hourly error rates for last 90 days
- Calculate baseline and standard deviations
- Detect outliers and correlate with ICM creation times
- Visualize in Power BI-compatible format
- Alert when current rate exceeds 2 sigma"
```

#### Cross-Tenant Comparative Analysis
```
"Compare tenant health:
1. Query metrics for all IC/MCS tenants
2. Calculate per-tenant: error rate, feature adoption, support case count
3. Identify outliers and at-risk customers
4. Correlate with recent changes/deployments
5. Generate per-customer health scorecards"
```

---

## 🧠 Sub-Agent Specialization System

You have **9 specialized sub-agents** - each an expert in their domain:

### 1. 🎓 **Purview Product Expert**
```
"Act as Purview Product Expert and:
- Explain sensitivity label inheritance behavior
- Debug why auto-labeling policy isn't triggering
- Recommend architecture for hybrid deployment
- Review feature roadmap for customer ask"
```

### 2. 📞 **Support Case Manager**
```
"Act as Support Case Manager and:
- Find all open DFM cases for my customers
- Identify cases at risk of missing SLA
- Link support cases to product bugs
- Generate weekly case review report"
```

### 3. 🚨 **Escalation Manager**
```
"Act as Escalation Manager and:
- Triage this new P0 ICM and assign DRI
- Build escalation timeline with stakeholder notifications
- Calculate customer impact across tenants
- Coordinate with on-call team"
```

### 4. 📊 **Kusto Expert**
```
"Act as Kusto Expert and:
- Optimize this slow-running query
- Build a correlation query between 3 data sources
- Explain what this query result means
- Create scheduled query for daily monitoring"
```

### 5. 📝 **Work Item Manager**
```
"Act as Work Item Manager and:
- Create epic for multi-quarter initiative
- Break down into stories and tasks
- Link to test plans and deployment tracking
- Set up automated sprint burndown reporting"
```

### 6. 🏥 **Tenant Health Monitor**
```
"Act as Tenant Health Monitor and:
- Run comprehensive health check for tenant XYZ
- Compare against healthy baseline metrics
- Identify configuration drift or anomalies
- Generate remediation recommendations"
```

### 7. 📚 **Program Onboarding Manager**
```
"Act as Program Onboarding Manager and:
- Generate onboarding plan for new customer
- Create checklist of required artifacts
- Schedule touchpoints and reviews
- Track onboarding milestones"
```

### 8. 🔍 **Contacts & Escalation Finder**
```
"Act as Contacts Finder and:
- Look up customer account team for Contoso
- Find escalation path for Azure AD issue
- Get on-call contact for Exchange team
- Map stakeholder communication plan"
```

### 9. 🔐 **Access & Role Manager**
```
"Act as Access Role Manager and:
- Verify my permissions for customer tenant access
- Request elevated access for troubleshooting
- Document access used for compliance
- Audit access patterns across team"
```

---

## 🎭 Advanced Prompt Patterns

### 🔄 Chain-of-Thought Workflows

#### The "Detective" Pattern
```
"Investigate why customer Fabrikam is seeing label removal failures:

STEP 1 - Evidence Collection:
- Query Kusto for all label operations in last 48h
- Check for related ICMs or support cases
- Pull recent code changes from ADO

STEP 2 - Pattern Analysis:
- Correlate error signatures across data sources
- Identify commonalities (time, user type, file format)
- Compare against known issues in wiki

STEP 3 - Hypothesis Formation:
- List 3 most likely root causes
- Explain reasoning for each
- Identify confirming/refuting evidence

STEP 4 - Validation:
- Design targeted Kusto queries to test hypotheses
- Execute and analyze results
- Recommend next troubleshooting steps

STEP 5 - Resolution:
- If known issue, link to bug/fix timeline
- If new issue, create ICM with full context
- Document in TSG system for future reference"
```

#### The "Architect" Pattern
```
"Design comprehensive monitoring solution for Purview eDiscovery:

REQUIREMENTS ANALYSIS:
- What metrics matter most?
- What are current blind spots?
- What thresholds indicate problems?

DESIGN:
- Define Kusto queries for each metric
- Set up ICM correlation rules
- Create ADO work items for dashboard development
- Map alert routing to teams

IMPLEMENTATION PLAN:
- Break into phased work items
- Assign dependencies
- Create test plan
- Define success criteria

DEPLOYMENT:
- Generate deployment runbook in wiki
- Link to validation queries
- Create rollback procedures"
```

### 🎯 Conditional Logic Workflows

```
"Smart escalation handler:

IF new ICM created:
  THEN get incident details
  
  IF Severity = P0 OR Severity = P1:
    THEN:
      - Calculate customer impact
      - Get on-call team
      - Create ADO tracking bug
      - Query recent similar incidents
      - Pull relevant TSGs
      - Generate escalation brief
      
  IF customer in IC/MCS list:
    THEN:
      - Add to priority queue
      - Notify account team
      - Run tenant health check
      - Check for other open issues
      
  IF similar ICM resolved in last 30 days:
    THEN:
      - Retrieve resolution details
      - Suggest same approach
      - Link to previous work items"
```

---

## 🔗 SharePoint Integration (Bonus Capability!)

You have **SharePoint access** configured to CxE Security Care CEM team site!

### 📚 Knowledge Base Operations
```
"SharePoint Operations:
- Search team site for Purview runbooks
- Retrieve latest customer engagement templates
- Find contact lists and escalation matrices
- Pull team process documentation
- Access historical reports and presentations"
```

### 🔄 Bi-Directional Sync
```
"Create living documentation:
1. Query Kusto for current customer health metrics
2. Generate formatted report with charts
3. Upload to SharePoint team site
4. Update index page with latest report link
5. Schedule for daily automated refresh"
```

---

## 🎨 Advanced Use Cases

### 🏭 Production Monitoring Dashboard

```
"Build real-time production health dashboard:

DATA SOURCES:
- Kusto: Live error rates, latency p95/p99, success rates
- ICM: Active incidents, severity distribution, MTTR
- ADO: Bug backlog, sprint velocity, test pass rates
- SharePoint: Customer list, risk scores, engagement status

ANALYTICS:
- Detect anomalies in telemetry
- Correlate errors with recent deployments
- Predict future incidents using ML patterns
- Recommend proactive interventions

OUTPUTS:
- HTML dashboard updated every 15 min
- Alert emails for threshold violations
- Executive summary in SharePoint
- Automated work item creation for critical issues"
```

### 🔬 Root Cause Analysis Engine

```
"Automated RCA for ICM 693849812:

TIMELINE RECONSTRUCTION:
- Query Kusto for events ±6 hours from ICM creation
- Pull deployment history from ADO
- Check for correlated ICMs
- Map customer actions from audit logs

CORRELATION ANALYSIS:
- Statistical correlation between deployment and errors
- Pattern matching against historical RCAs
- Code change impact analysis from PRs
- Configuration drift detection

CAUSALITY DETERMINATION:
- Rank potential causes by evidence strength
- Eliminate ruled-out hypotheses
- Generate causal chain diagram
- Identify contributing factors vs root cause

REMEDIATION:
- Search for existing fixes in ADO
- Generate test plan for validation
- Create rollback procedure if needed
- Update TSG with new learnings"
```

### 📈 Strategic Planning Assistant

```
"FY26 Planning Analysis:

HISTORICAL PERFORMANCE:
- Analyze FY25 ICM trends by quarter
- Calculate team capacity and velocity
- Identify seasonal patterns
- Measure feature adoption curves

PREDICTIVE MODELING:
- Forecast FY26 support volume
- Estimate staffing needs
- Predict high-risk periods
- Project infrastructure scaling

INVESTMENT RECOMMENDATIONS:
- Identify top pain points from ICMs
- Calculate ROI of proposed improvements
- Prioritize TSG development areas
- Recommend automation opportunities

DELIVERABLE:
- Executive presentation in SharePoint
- Detailed backup analysis in wiki
- Tracked work items for initiatives
- Quarterly checkpoint queries"
```

---

## 💡 Power Tips & Hidden Features

### 🚀 Performance Optimization

1. **Parallel Queries**: Run independent Kusto queries simultaneously
```
"Execute these queries in parallel:
- Sensitivity label errors last 24h
- DLP policy violations last 24h  
- eDiscovery failures last 24h
Then generate combined health report"
```

2. **Query Result Caching**: Reference previously executed queries
```
"Using the ICM list from my last query, now find support cases for each"
```

3. **Incremental Analysis**: Build on previous results
```
"From the 620 sensitivity label ICMs we analyzed:
- Drill into the top error category
- Show detailed timeline
- Find code changes that might have caused it"
```

### 🔐 Security & Compliance

```
"Audit trail generation:
- Log all Kusto queries executed
- Track ICM access with justification
- Document customer data viewed
- Generate compliance report for security review"
```

### 📊 Data Export & Visualization

```
"Create executive briefing:
1. Execute multiple analytical queries
2. Export results to CSV/JSON
3. Generate charts and visualizations
4. Build PowerPoint-ready summary
5. Upload to SharePoint with access controls"
```

---

## 🎯 Challenge Prompts (Test Your Limits!)

Ready to push the boundaries? Try these advanced scenarios:

### 🧪 **The Super Query**
```
"Multi-dimensional analysis:
For each Purview product team (10 teams), for each month (last 12 months):
- ICM count by severity
- Average resolution time
- Customer impact score
- Related bug fix velocity
- Test coverage percentage
Generate heat map showing which team/month combinations need attention"
```

### 🔮 **The Predictor**
```
"Build early warning system:
- Identify telemetry signatures that precede ICMs
- Calculate lead time (how far in advance signals appear)
- Set up real-time monitoring for these signals
- Auto-create preventive work items when threshold hit
- Track prediction accuracy over time"
```

### 🎭 **The Orchestrator**
```
"End-to-end incident lifecycle automation:
- Monitor ICM API for new Purview incidents
- Auto-classify by symptom and severity
- Query relevant data sources
- Create ADO bug with pre-populated template
- Assign to appropriate team based on ML prediction
- Add links between all artifacts
- Generate initial triage brief
- Notify stakeholders via appropriate channels
- Track through resolution
- Generate lessons learned document
- Update TSG repository"
```

### 🏆 **The Time Traveler**
```
"Historical analysis & future projection:
- Analyze complete ICM history (all time)
- Identify trend inflection points
- Correlate with product launches, holidays, major updates
- Build forecasting model
- Predict next quarter's support load
- Recommend resource allocation
- Create risk mitigation plan"
```

---

## 🎓 Learning Path

### Level 1: Basic Operations (You are here)
- Single-system queries
- Basic ICM/ADO/Kusto operations
- Simple report generation

### Level 2: Cross-System Intelligence
- Multi-agent workflows
- Automated linking and correlation
- Template-based analysis

### Level 3: Advanced Orchestration
- Conditional logic workflows
- Real-time monitoring
- Predictive analytics

### Level 4: System Architect
- Custom sub-agent creation
- Automated pipelines
- Enterprise dashboards

### Level 5: AI Operations Master
- Full autonomous workflows
- Self-healing systems
- Strategic planning AI

---

## 🚀 Ready to Level Up?

Start with any prompt in this guide, or ask:

```
"Show me what you can do with [specific problem I'm facing]"
"Build me a workflow for [my use case]"
"Analyze [data source] and tell me something I don't know"
```

**Your MCP environment is an enterprise-grade intelligence platform. Use it like one! 🎉**
