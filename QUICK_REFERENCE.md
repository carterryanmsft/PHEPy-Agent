# ⚡ Quick Reference Card

**PHEPy Workspace** | Copy-Paste Ready Prompts

---

## 🎯 Most Common Actions

### Incident Investigation
```
Get full details for ICM 21000000887894 including timeline and customer impact
```

```
Find all ICMs for Purview SensitivityLabels team in the last 7 days with severity P0 or P1
```

```
For ICM X: query Kusto for matching errors in the 24h before incident, then create ADO tracking bug
```

### Customer Health Check
```
Generate IC/MCS production risk report with current health status
```

```
Query Kusto for all errors affecting tenant XYZ in the last 48 hours
```

```
Compare telemetry for my top 5 customers against baseline and flag anomalies
```

### Work Item Management
```
Show me all open bugs assigned to me in ADO
```

```
Create bug for sensitivity label deletion issue, link to ICM 693849812, assign to current sprint
```

```
Search ADO for work items mentioning "auto-labeling" across all projects
```

### Data Analysis
```
Execute purview_analysis/queries/SensitivityLabels_analysis.kql and summarize key findings
```

```
List all tables in PurviewTelemetry database with schema details
```

```
Run these 3 queries in parallel: [query1.kql, query2.kql, query3.kql] and create combined report
```

---

## 🔄 Workflow Templates

### New ICM Response
```
New P0 ICM workflow:
1. Get incident details and affected customers
2. Query Kusto for error patterns in incident timeframe
3. Find similar historical ICMs
4. Create ADO bug with pre-populated context
5. Get on-call team contact info
6. Generate triage brief with recommendations
```

### Weekly Health Review
```
Generate weekly Purview health report:
1. Query ICM for all new incidents this week
2. Run Kusto analytics for error rates by product area
3. Check ADO for bug fix deployment status
4. Calculate per-customer risk scores
5. Create executive summary with trends
6. Save to reports/ folder
```

### Root Cause Analysis
```
Investigate issue X:
1. Collect evidence from Kusto telemetry
2. Check for related ICMs and support cases in ADO
3. Analyze code changes in timeframe
4. Correlate deployment timeline with errors
5. Identify root cause and contributing factors
6. Generate RCA document with recommendations
7. Update TSG in wiki
```

---

## 🧠 Sub-Agent Quick Calls

### Product Expert Mode
```
Act as Purview Product Expert and explain how sensitivity label inheritance works in SharePoint Online
```

### Escalation Manager Mode
```
Act as Escalation Manager and coordinate response for P0 ICM including DRI assignment and stakeholder notifications
```

### Kusto Expert Mode
```
Act as Kusto Expert and build optimized query to correlate errors across PurviewTelemetry, ICMEvents, and CustomerData tables
```

---

## 📊 Ready-to-Use Queries

### Top Errors This Week
```
Query Kusto for top 10 error signatures in Purview this week with affected customer count
```

### Feature Adoption
```
Analyze sensitivity label adoption trends over last 90 days by customer segment
```

### SLA Tracking
```
Show all support cases at risk of missing SLA with days until breach
```

### Team Performance
```
Calculate average ICM resolution time by Purview team for last quarter
```

---

## 🎭 Situation-Specific Prompts

### Customer Called With Issue
```
Customer Fabrikam reports [symptom]:
- Check their tenant health in Kusto
- Find any open ICMs affecting them
- Review recent support cases
- Generate troubleshooting action plan
```

### Planning Sprint Work
```
Sprint planning assistance:
- List all bugs in backlog prioritized by customer impact
- Show dependencies between work items
- Calculate team velocity from last 3 sprints
- Recommend sprint commitment
```

### Preparing for Executive Review
```
Executive briefing for next week:
- Summarize ICM trends vs last quarter
- Highlight top customer pain points
- Show progress on key initiatives
- Identify upcoming risks
- Generate PowerPoint-ready slides
```

### Responding to Escalation
```
High-visibility escalation response:
- Full customer impact analysis
- Timeline of events with evidence
- Identified root cause and fix status
- Communication plan for stakeholders
- Lessons learned and preventive actions
```

---

## 💡 Pro Tips

### Chaining Operations
Good: "Get ICM details, then query Kusto"
Better: "For ICM X: get details, query related telemetry, find similar incidents, and create analysis report"

### Being Specific
Good: "Show recent ICMs"
Better: "Show P0/P1 ICMs for Purview teams created in last 72 hours with customer impact >1000 users"

### Leveraging Context
Good: "Create a bug"
Better: "Using the analysis we just did, create ADO bug with summary, repro steps, and links to evidence"

### Parallel Execution
Good: Run 5 queries one at a time
Better: "Execute these 5 queries in parallel and generate combined dashboard"

---

## 🔍 Discovery Prompts

### Learn What's Available
```
What MCP agents do I have configured and what can each one do?
```

```
Show me all available Kusto queries in my workspace with descriptions
```

```
List all sub-agents and their specializations
```

### Explore Data
```
What tables are available in my Kusto cluster and what's in them?
```

```
Show me sample data from ICMIncidents table to understand the schema
```

```
What queries have I run recently and can we build on those results?
```

### Find Examples
```
Show me example prompts for [specific task]
```

```
How would I [accomplish goal] using my MCP setup?
```

```
What's the most sophisticated workflow you can orchestrate for [scenario]?
```

---

## 🚨 Emergency Quick Actions

### P0 Incident
```
URGENT: New P0 ICM [ID] - full war room setup now
```

### Customer Down
```
CRITICAL: Customer [name] is down - immediate health assessment and escalation
```

### Data Needed Fast
```
FAST: Need telemetry for tenant [ID] last 24h - quick export to CSV
```

---

## 📞 Contact & Team Info

### Find People
```
Get on-call contact for Purview SensitivityLabels team
```

```
Find escalation path for Azure AD integration issue
```

```
Who are the SMEs that resolved ICMs similar to [ID]?
```

---

## 📁 File Operations

### Save Results
```
Save this analysis to reports/ with timestamp and summary
```

### Export Data
```
Export query results to CSV for Power BI import
```

### Update Documentation
```
Update TSG wiki page with this resolution and add validation query
```

---

## 🔄 Continuous Improvement

### Get Weekly Suggestions
```
Suggest a continuous improvement activity for this week
```

```
Show me my continuous improvement progress
```

### After Completing Work
```
I just finished [task/incident]. Any continuous improvement suggestions?
```

```
Help me do a 5-minute reflection on today's work
```

### When Frustrated
```
This workflow is annoying. Help me improve it
```

```
What friction points can I eliminate?
```

### On Fridays
```
What's my continuous improvement win this week?
```

### Documentation & Process
```
Help me document [process]
```

```
Create a checklist for [recurring task]
```

```
Guide me through a 5 Whys analysis on [recurring issue]
```

**Full guide:** [CONTINUOUS_IMPROVEMENT_QUICK_REFERENCE.md](CONTINUOUS_IMPROVEMENT_QUICK_REFERENCE.md)

---

## 🎯 Copy-Paste Examples by Role

### Product Engineer
```
Morning standup brief: ICMs overnight, customer health status, bugs in current sprint
```

### Support Escalation Manager
```
All P1+ incidents requiring attention, with impact assessment and recommended actions
```

### Program Manager
```
FY26 planning data: historical trends, capacity analysis, investment recommendations
```

### Data Analyst
```
Deep dive: [product feature] adoption, errors, customer feedback correlation
```

---

## 🔗 Quick Links to Resources

- **All Guides**: See [INDEX.md](INDEX.md)
- **Getting Started**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Full Capabilities**: [ADVANCED_CAPABILITIES.md](ADVANCED_CAPABILITIES.md)
- **Capability Matrix**: [CAPABILITY_MATRIX.md](CAPABILITY_MATRIX.md)
- **Continuous Improvement**: [CONTINUOUS_IMPROVEMENT_QUICK_REFERENCE.md](CONTINUOUS_IMPROVEMENT_QUICK_REFERENCE.md)
- **KQL Queries**: [purview_analysis/queries/](purview_analysis/queries/)
- **Sub-Agents**: [sub_agents/](sub_agents/)

---

**Bookmark this page for instant access to your most-used prompts! 📌**

Last updated: February 4, 2026
