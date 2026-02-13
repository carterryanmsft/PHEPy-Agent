# 🎯 PHEPy Capability Matrix

**Quick Reference** | What Can Your Workspace Do?

---

## 📊 Capability Overview

| Category | Capability | Example Use Case | MCP Agents Used |
|----------|-----------|------------------|-----------------|
| **Incident Management** | ICM Details & History | Get full context for escalation | ICM |
| **Incident Management** | Bulk ICM Analysis | Analyze 620 sensitivity label ICMs | ICM + Kusto |
| **Incident Management** | Customer Impact Assessment | Calculate affected tenant count | ICM |
| **Incident Management** | Similar Incident Detection | Find related ICMs by pattern | ICM + Kusto |
| **Incident Management** | On-Call Scheduling | Get team rotation and contacts | ICM |
| **Incident Management** | Predictive Alerting | Detect ICM patterns before they happen | ICM + Kusto + ADO |
| | | | |
| **Support Case Management** | DFM Case Tracking | Monitor SLA and at-risk cases | ADO O365 |
| **Support Case Management** | Case-ICM Correlation | Link support cases to incidents | ADO + ICM |
| **Support Case Management** | Customer Journey Mapping | Track customer across all systems | ADO + ICM + Kusto |
| | | | |
| **Work Item Tracking** | Bug & Feature Management | Track product backlog | ADO ASIM + ADO O365 |
| **Work Item Tracking** | Cross-Project Linking | Connect bugs to ICMs and cases | ADO + ICM |
| **Work Item Tracking** | Sprint Planning & Velocity | Analyze team capacity | ADO |
| **Work Item Tracking** | Artifact Linking | Connect code, builds, tests | ADO ASIM |
| **Work Item Tracking** | Wiki Documentation | Create/update TSGs and runbooks | ADO O365 |
| | | | |
| **Code & Deployment** | Branch Management | Create branches for fixes | ADO ASIM |
| **Code & Deployment** | Pull Request Workflow | Create, review, merge PRs | ADO ASIM |
| **Code & Deployment** | Pipeline Execution | Run builds and deployments | ADO O365 |
| **Code & Deployment** | Test Plan Tracking | Manage test suites and results | ADO O365 |
| **Code & Deployment** | Code Review Comments | Reply to PR feedback | ADO ASIM |
| | | | |
| **Data Analytics** | KQL Query Execution | Run telemetry analysis | Kusto |
| **Data Analytics** | Multi-Table Joins | Correlate across data sources | Kusto |
| **Data Analytics** | Time-Series Analysis | Detect trends and anomalies | Kusto |
| **Data Analytics** | Table Schema Discovery | Explore database structure | Kusto |
| **Data Analytics** | 22 Pre-Built Queries | Product-specific analysis | Kusto |
| | | | |
| **Customer Health** | Tenant Health Checks | Monitor IC/MCS customers | Kusto + ICM |
| **Customer Health** | Risk Report Generation | Identify at-risk customers | Kusto + ICM + ADO |
| **Customer Health** | Proactive Monitoring | Detect issues before escalation | Kusto |
| **Customer Health** | Comparative Analysis | Benchmark tenant performance | Kusto |
| | | | |
| **Product Analysis** | Feature Adoption Tracking | Measure usage patterns | Kusto |
| **Product Analysis** | Error Pattern Detection | Find recurring issues | Kusto + ICM |
| **Product Analysis** | By-Design Filtering | Distinguish bugs from features | Kusto |
| **Product Analysis** | Cross-Team Summary | All Purview teams overview | Kusto + ADO |
| | | | |
| **Automation** | Multi-Agent Orchestration | Chain complex workflows | ALL |
| **Automation** | Scheduled Monitoring | Continuous health checks | Kusto + ICM |
| **Automation** | Auto-Work Item Creation | Generate tracking bugs | ADO + ICM |
| **Automation** | Alert Routing | Smart notification delivery | ALL |
| | | | |
| **Knowledge Management** | TSG Generation | Create troubleshooting guides | ADO Wiki + ICM |
| **Knowledge Management** | SharePoint Integration | Team documentation access | SharePoint |
| **Knowledge Management** | Historical Analysis | Learn from past incidents | ICM + ADO + Kusto |
| **Knowledge Management** | Best Practice Capture | Document successful patterns | ADO Wiki |
| | | | |
| **Reporting** | Executive Briefings | High-level impact summaries | ALL |
| **Reporting** | Operational Dashboards | Real-time health metrics | Kusto |
| **Reporting** | Trend Analysis | Historical pattern reports | Kusto + ICM |
| **Reporting** | Custom Visualizations | Data export for Power BI | Kusto |

---

## 🎭 Sub-Agent Capabilities

| Sub-Agent | Primary Function | Key Actions | When to Use |
|-----------|------------------|-------------|-------------|
| **Purview Product Expert** | Product knowledge & architecture | Explain features, debug behavior, design solutions | Need deep product understanding |
| **Support Case Manager** | DFM case lifecycle | Track SLAs, link cases, at-risk detection | Managing customer support |
| **Escalation Manager** | ICM incident coordination | Triage, impact assessment, DRI assignment | High-severity incidents |
| **Kusto Expert** | Data query & analysis | Write KQL, optimize queries, interpret results | Need data insights |
| **Work Item Manager** | ADO tracking & planning | Create epics, link items, sprint planning | Development tracking |
| **Tenant Health Monitor** | Customer environment health | Run diagnostics, detect anomalies, recommend fixes | Proactive monitoring |
| **Program Onboarding Manager** | Customer onboarding | Create plans, track milestones, generate checklists | New customer setup |
| **Contacts & Escalation Finder** | Contact lookup | Find team members, escalation paths, account teams | Need to reach people |
| **Access & Role Manager** | Permission management | Verify access, request elevation, audit usage | Security & compliance |

---

## 🔄 Workflow Patterns

### Pattern 1: Reactive Incident Response
```
New ICM → Get Details → Query Telemetry → Find Similar → Link ADO Bug → Generate Brief
Agents: ICM → Kusto → ICM → ADO → ALL
```

### Pattern 2: Proactive Health Monitoring
```
Schedule → Query Metrics → Detect Anomalies → Predict Risk → Alert Team → Create Work Item
Agents: Kusto → Kusto → Kusto → ADO → ALL
```

### Pattern 3: Customer Lifecycle Management
```
Onboard → Monitor Health → Track Cases → Correlate ICMs → Risk Report → Executive Review
Agents: ADO → Kusto → ADO → ICM → Kusto + ADO → SharePoint
```

### Pattern 4: Product Development Integration
```
Bug Report → Create Branch → Link ICM → Write Tests → Deploy → Validate → Update TSG
Agents: ADO → ADO ASIM → ICM + ADO → ADO → ADO → Kusto → ADO Wiki
```

### Pattern 5: Knowledge Discovery
```
Research Topic → Search Wiki → Query Historical Data → Find Patterns → Document Findings → Share
Agents: ADO Wiki → Kusto → Kusto → ADO Wiki → SharePoint
```

---

## 💡 Capability Combinations

### 🔥 High-Impact Combos

1. **ICM + Kusto + ADO**
   - Full incident investigation with automated tracking
   - "For ICM X: query telemetry, find root cause, create fix tracking bug"

2. **Kusto + ADO Wiki**
   - Data-driven documentation
   - "Query common errors, generate TSG with sample queries embedded"

3. **ICM + ADO + SharePoint**
   - Executive communication pipeline
   - "Analyze incidents, generate brief, upload to team site"

4. **Kusto (Multi-Query) + ADO**
   - Comprehensive health dashboard
   - "Run 10 product queries in parallel, create summary work item"

5. **All Agents + Sub-Agent Specialist**
   - Expert-level orchestration
   - "Act as Escalation Manager: coordinate full incident response using all tools"

---

## 🎯 Complexity Levels

### ⚡ Simple (Single Agent)
- Get ICM details
- Run one Kusto query
- Create ADO work item
- Search wiki

### 🔥 Moderate (2-3 Agents)
- ICM analysis with telemetry
- Create bug linked to ICM
- Query and document in wiki

### 🚀 Advanced (3-5 Agents)
- Full incident pipeline
- Multi-source correlation
- Automated report generation

### 💎 Expert (All Agents + Logic)
- Predictive monitoring
- Autonomous response
- Strategic planning

---

## 📊 Data Flow Map

```
                    ┌─────────────┐
                    │   USER      │
                    │   PROMPT    │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
       ┌────▼───┐     ┌───▼────┐    ┌───▼────┐
       │  ICM   │     │  ADO   │    │ KUSTO  │
       │ Server │◄───►│ Server │◄──►│ Server │
       └────┬───┘     └───┬────┘    └───┬────┘
            │             │              │
            └──────┬──────┴──────┬───────┘
                   │             │
              ┌────▼───┐    ┌───▼────┐
              │ Sub-   │    │SharePt │
              │ Agents │    │ Site   │
              └────┬───┘    └───┬────┘
                   │             │
                   └──────┬──────┘
                          │
                   ┌──────▼──────┐
                   │  ANALYSIS   │
                   │   REPORT    │
                   │   OUTPUT    │
                   └─────────────┘
```

---

## 🎓 Skill Progression

### Beginner
- Single-system queries
- Basic prompts from GETTING_STARTED.md
- Understanding MCP capabilities

### Intermediate  
- Multi-system workflows
- Using sub-agents
- Custom query development

### Advanced
- Orchestrated pipelines
- Predictive analytics
- Automated monitoring

### Expert
- Custom agent development
- Strategic AI operations
- Enterprise integration

---

## 🚀 Quick Capability Checker

**Want to know if something is possible? Ask:**

- "Can you [action] using [data source]?"
- "How would I [accomplish task] with my MCP setup?"
- "Show me examples of [workflow type]"
- "What's the most advanced thing you can do with [scenario]?"

**99% of the time, the answer is YES! Try it!** 🎉
