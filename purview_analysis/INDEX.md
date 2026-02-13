# Purview ICM Analysis System - Navigation Index

**Welcome!** This index helps you quickly find the right resource for your task.

---

## 🚀 Quick Navigation

### I want to...

**→ Get started with my first analysis**
- Start here: [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Complete step-by-step instructions
- Review example: `../Copilot/Created/Sensitivity_Labels_Analysis_Report.md`

**→ Understand what this system does**
- Read: [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md) - Complete overview
- Read: [README.md](README.md) - Quick reference and best practices

**→ Run a Kusto query**
- Overview of all teams: [queries/all_teams_summary.kql](queries/all_teams_summary.kql)
- Deep dive template: [queries/team_template.kql](queries/team_template.kql)
- Team-specific: See [Kusto Queries](#kusto-queries) section below

**→ Generate a report**
- Full analysis: [templates/team_analysis_template.md](templates/team_analysis_template.md)
- Executive summary: [templates/executive_summary_template.md](templates/executive_summary_template.md)
- Track progress: [templates/improvement_tracker.md](templates/improvement_tracker.md)

**→ Troubleshoot an issue**
- Check: [WORKFLOW_GUIDE.md - Troubleshooting Section](WORKFLOW_GUIDE.md#troubleshooting-guide)
- Common issues: Query 400 errors, duplicates, timeouts, team not found

**→ Learn from a real example**
- Review: `../Copilot/Created/Sensitivity_Labels_Analysis_Report.md`
- Demonstrates: 8 themes, 717 incidents, complete recommendations

---

## 📂 File Organization

### Core Documentation (Read First)
| File | Purpose | When to Use |
|------|---------|-------------|
| [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md) | Complete system overview | First-time setup, understanding scope |
| [README.md](README.md) | Quick reference, best practices | During analysis, query help |
| [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) | Step-by-step instructions | Performing analysis, troubleshooting |
| [INDEX.md](INDEX.md) | This file - navigation | Finding the right resource |

### Kusto Queries

#### General Purpose Queries
| File | Purpose | Use Case |
|------|---------|----------|
| [queries/all_teams_summary.kql](queries/all_teams_summary.kql) | List all 42 Purview teams | Prioritization, discovery |
| [queries/team_template.kql](queries/team_template.kql) | Parameterized template | Any team analysis |
| [queries/by_design_analysis.kql](queries/by_design_analysis.kql) | "By Design" deep dive | Documentation gaps |
| [queries/dcr_analysis.kql](queries/dcr_analysis.kql) | Feature request analysis | Product roadmap input |

#### Team-Specific Queries (Pre-Configured)
| File | Team | Known Themes |
|------|------|--------------|
| [queries/SensitivityLabels_analysis.kql](queries/SensitivityLabels_analysis.kql) | Sensitivity Labels | Cross-app, File Explorer, DKE, auto-labeling |
| [queries/DLPEndpoint_analysis.kql](queries/DLPEndpoint_analysis.kql) | DLP Endpoint | Policy conflicts, printer, USB, Mac support |
| [queries/eDiscovery_analysis.kql](queries/eDiscovery_analysis.kql) | eDiscovery | Content search, legal hold, exports |
| [queries/MIPCore_analysis.kql](queries/MIPCore_analysis.kql) | MIP Core | Service reliability, API, SDK |
| [queries/DLPWeb_analysis.kql](queries/DLPWeb_analysis.kql) | DLP Web | Policy tips, false positives, SharePoint/Exchange |
| [queries/ContentExplorer_analysis.kql](queries/ContentExplorer_analysis.kql) | Content Explorer | Data refresh, filtering, permissions |
| [queries/DLMAppRetention_analysis.kql](queries/DLMAppRetention_analysis.kql) | DLM App Retention | Teams/Yammer retention, policy conflicts |
| [queries/DLMExchangeRetention_analysis.kql](queries/DLMExchangeRetention_analysis.kql) | Exchange Retention | MRM, archive policies, journaling |
| [queries/MIPServiceCore_analysis.kql](queries/MIPServiceCore_analysis.kql) | MIP Service Core | Service health, policy sync, licensing |
| [queries/MIPCompliance_analysis.kql](queries/MIPCompliance_analysis.kql) | MIP Compliance | Audit logs, alerts, reporting |

### Report Templates

| File | Purpose | Output |
|------|---------|--------|
| [templates/team_analysis_template.md](templates/team_analysis_template.md) | Complete analysis report | 10-15 page detailed analysis |
| [templates/executive_summary_template.md](templates/executive_summary_template.md) | Leadership briefing | 3-5 page executive summary |
| [templates/improvement_tracker.md](templates/improvement_tracker.md) | Action item tracking | Living document (monthly updates) |

---

## 🎯 Common Workflows

### Workflow 1: First-Time Analysis (eDiscovery Example)

```bash
# Step 1: Verify access
Run: queries/all_teams_summary.kql
Expected: List of 42 teams with incident counts

# Step 2: Choose team
Decision: eDiscovery (high volume, strategic importance)

# Step 3: Run team query
Run: queries/eDiscovery_analysis.kql
Expected: ~50 unique incident titles with counts

# Step 4: Identify themes
Manual: Review titles, group into 5-10 themes
Expected: Content search, legal hold, exports, permissions, etc.

# Step 5: Sample incidents
Tool: mcp_icm_mcp_eng_get_incident_context
Count: 3-5 per theme (15-20 total)

# Step 6: Generate report
Copy: templates/team_analysis_template.md → reports/eDiscovery_Analysis_2026-02-04.md
Fill: All sections based on analysis

# Step 7: Create tracker
Copy: templates/improvement_tracker.md → team_analyses/eDiscovery/improvement_tracker.md
```

**Time Required**: 6-8 hours

---

### Workflow 2: Monthly Progress Update

```bash
# Step 1: Re-run team query
Run: queries/[TeamName]_analysis.kql
Compare: Current results vs. last month

# Step 2: Calculate trends
Metric: Total incidents (% change)
Metric: "By Design" rate (% change)
Metric: DCR volume (new requests)

# Step 3: Update tracker
File: team_analyses/[TeamName]/improvement_tracker.md
Update: Completed items, metrics, blockers

# Step 4: Monthly review meeting
Agenda: Progress, trends, priorities, next steps
Duration: 30 minutes
```

**Time Required**: 1-2 hours

---

### Workflow 3: Executive Presentation

```bash
# Step 1: Generate executive summary
Copy: templates/executive_summary_template.md
Fill: Business impact, top 3 themes, recommendations

# Step 2: Extract key metrics
From: team_analysis_template.md
Include: Incident counts, customer impact, cost savings

# Step 3: Create slides
Tool: PowerPoint (optional)
Slides: 5-7 slides covering TL;DR, findings, recommendations

# Step 4: Present findings
Audience: PM, Engineering Lead, Leadership
Duration: 15-30 minutes
```

**Time Required**: 2-3 hours

---

## 📚 Learning Path

### Beginner (Week 1)
1. ✅ Read: [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md) - Understand what this is
2. ✅ Read: [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) Sections 1-4 - Prerequisites, workflow overview
3. ✅ Review: Sensitivity Labels example report
4. ✅ Run: `queries/all_teams_summary.kql` - Verify Kusto access
5. ✅ Practice: Run one team-specific query, review results

### Intermediate (Week 2-4)
1. ✅ Complete: First full team analysis (choose from pre-configured teams)
2. ✅ Generate: Complete report using template
3. ✅ Create: Improvement tracker
4. ✅ Present: Findings to stakeholders
5. ✅ Schedule: Monthly review

### Advanced (Month 2-3)
1. ✅ Analyze: 3-5 additional teams
2. ✅ Identify: Cross-team patterns
3. ✅ Build: Consolidated roadmap
4. ✅ Automate: Monthly query execution
5. ✅ Measure: Program ROI (incident reduction, cost savings)

---

## 🔍 Finding Information

### Query-Related Questions
- **"Which query should I use?"** → See [Kusto Queries](#kusto-queries) table above
- **"How do I modify a query?"** → [README.md - Query Patterns](README.md#query-patterns)
- **"Query is failing"** → [WORKFLOW_GUIDE.md - Troubleshooting](WORKFLOW_GUIDE.md#troubleshooting-guide)

### Report-Related Questions
- **"What should my report include?"** → [templates/team_analysis_template.md](templates/team_analysis_template.md)
- **"How do I identify themes?"** → [WORKFLOW_GUIDE.md - Phase 3](WORKFLOW_GUIDE.md#phase-3-theme-identification-1-2-hours)
- **"How do I prioritize?"** → [README.md - Prioritization Criteria](README.md#prioritization-criteria)

### Process Questions
- **"Where do I start?"** → [WORKFLOW_GUIDE.md - Quick Start](WORKFLOW_GUIDE.md#quick-start-guide)
- **"How long will this take?"** → See [Common Workflows](#common-workflows) above
- **"What's the expected outcome?"** → [SYSTEM_SUMMARY.md - Expected Outcomes](SYSTEM_SUMMARY.md#expected-outcomes)

---

## 🎓 Reference Examples

### Real-World Analysis
**Sensitivity Labels Team** (717 incidents, 6 months)
- Location: `../Copilot/Created/Sensitivity_Labels_Analysis_Report.md`
- Themes: 8 identified
- Recommendations: 43 total (15 docs, 21 product, 7 UX)
- Target: 50% incident reduction in 6 months

**What to Learn From It**:
- ✅ How to structure theme sections
- ✅ How to write evidence-based recommendations
- ✅ How to prioritize (P0/P1/P2/P3)
- ✅ How to define success metrics

---

## 🛠️ Tools & Resources

### Required Tools
- **Kusto MCP Server**: `mcp_kusto-mcp-ser_execute_query`
- **ICM MCP Server**: `mcp_icm_mcp_eng_get_incident_context`
- **VS Code**: With GitHub Copilot

### Data Sources
- **Kusto Cluster**: https://icmcluster.kusto.windows.net
- **Database**: IcmDataWarehouse
- **Table**: Incidents
- **ICM Portal**: https://portal.microsofticm.com

### External Resources
- **KQL Reference**: https://learn.microsoft.com/kusto/query
- **Purview Docs**: https://learn.microsoft.com/purview

---

## ✅ Pre-Flight Checklist

Before starting your first analysis:

- [ ] Kusto MCP Server configured and working
- [ ] ICM MCP Server configured and working
- [ ] Azure authentication successful
- [ ] Can access IcmDataWarehouse.Incidents table
- [ ] All 20 files present in purview_analysis/ folder
- [ ] Read SYSTEM_SUMMARY.md
- [ ] Read WORKFLOW_GUIDE.md sections 1-4
- [ ] Reviewed Sensitivity Labels example report

**If any item unchecked**: Resolve before proceeding

---

## 📞 Getting Help

### Documentation
- **General questions**: [README.md](README.md)
- **Step-by-step help**: [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
- **System overview**: [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md)

### Troubleshooting
- **Query errors**: [WORKFLOW_GUIDE.md - Troubleshooting](WORKFLOW_GUIDE.md#troubleshooting-guide)
- **Common issues**: Covers 5 most frequent problems with solutions

### Example Reference
- **Working example**: `../Copilot/Created/Sensitivity_Labels_Analysis_Report.md`
- **Shows**: Complete analysis from start to finish

---

## 🎯 Quick Links

| Need | Link |
|------|------|
| 🚀 **Get Started** | [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) |
| 📖 **System Overview** | [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md) |
| 🔍 **Query Reference** | [README.md](README.md) |
| 📊 **Report Template** | [templates/team_analysis_template.md](templates/team_analysis_template.md) |
| 🎓 **Real Example** | `../Copilot/Created/Sensitivity_Labels_Analysis_Report.md` |
| 🛠️ **Troubleshooting** | [WORKFLOW_GUIDE.md - Troubleshooting](WORKFLOW_GUIDE.md#troubleshooting-guide) |

---

**Ready to begin?** → [WORKFLOW_GUIDE.md - Quick Start](WORKFLOW_GUIDE.md#quick-start-guide)

**Version**: 1.0 | **Last Updated**: February 4, 2026
