# Purview Analysis System - Complete Setup Summary

**Created**: February 4, 2026  
**System Version**: 1.0  
**Status**: ✅ Complete and Ready to Use

---

## 🎯 What Was Built

A comprehensive, reusable framework for analyzing Purview ICM incidents to identify documentation gaps, product limitations, and UX issues—with the goal of reducing customer pain and incident volume.

---

## 📁 Complete Folder Structure

```
purview_analysis/
├── README.md                                    # Master instructions and best practices
├── WORKFLOW_GUIDE.md                            # Complete step-by-step workflow
│
├── queries/                                     # Kusto query templates (14 files)
│   ├── all_teams_summary.kql                   # Overview of all 42 Purview teams
│   ├── team_template.kql                       # Parameterized template for any team
│   ├── by_design_analysis.kql                  # Deep dive into "By Design" incidents
│   ├── dcr_analysis.kql                        # DCR/feature request analysis
│   ├── SensitivityLabels_analysis.kql          # Team-specific: Sensitivity Labels
│   ├── DLPEndpoint_analysis.kql                # Team-specific: DLP Endpoint
│   ├── eDiscovery_analysis.kql                 # Team-specific: eDiscovery
│   ├── MIPCore_analysis.kql                    # Team-specific: MIP Core
│   ├── DLPWeb_analysis.kql                     # Team-specific: DLP Web
│   ├── ContentExplorer_analysis.kql            # Team-specific: Content Explorer
│   ├── DLMAppRetention_analysis.kql            # Team-specific: DLM App Retention
│   ├── DLMExchangeRetention_analysis.kql       # Team-specific: Exchange Retention
│   ├── MIPServiceCore_analysis.kql             # Team-specific: MIP Service Core
│   └── MIPCompliance_analysis.kql              # Team-specific: MIP Compliance
│
├── templates/                                   # Report generation templates (3 files)
│   ├── team_analysis_template.md               # Full analysis report structure
│   ├── improvement_tracker.md                  # Action item tracking template
│   └── executive_summary_template.md           # Executive briefing template
│
├── reports/                                     # Generated analysis reports (organize by team)
│   └── [TeamName]/                             # One folder per analyzed team
│
├── team_analyses/                               # Completed team analyses
│   └── [TeamName]/                             # Final reports and tracking
│
└── data/                                        # Raw data exports (CSV/JSON)
    └── [TeamName]_incidents_[date].csv         # Query result exports
```

**Total Files Created**: 20 files
- 1 Master README
- 1 Complete Workflow Guide
- 14 Kusto Query Templates (4 general + 10 team-specific)
- 3 Report Templates

---

## 📊 Key Features

### 1. Kusto Query Library
- **all_teams_summary.kql**: Get incident counts for all 42 Purview teams (prioritization)
- **team_template.kql**: Parameterized template for deep-dive on any team
- **by_design_analysis.kql**: Focus on documentation gaps ("By Design" incidents)
- **dcr_analysis.kql**: Focus on feature requests (DCRs)
- **10 Team-Specific Queries**: Pre-configured for top 10 Purview teams by volume

### 2. Report Templates
- **team_analysis_template.md**: Complete structure matching Sensitivity Labels example
  - Executive summary
  - Theme deep-dives
  - Categorized recommendations (Docs/Product/UX)
  - Success metrics
  - Methodology & appendices
  
- **improvement_tracker.md**: Action item tracking with progress monitoring
  - Documentation improvements tracking
  - Product feature roadmap tracking
  - UX enhancement tracking
  - Blockers & risks
  - Monthly trend analysis

- **executive_summary_template.md**: Leadership-focused briefing
  - Business impact quantification
  - Critical recommendations
  - Customer stories
  - ROI projections

### 3. Comprehensive Documentation
- **README.md**: Master reference with quick start, best practices, query patterns
- **WORKFLOW_GUIDE.md**: End-to-end walkthrough with:
  - Phase-by-phase instructions
  - Troubleshooting guide (5 common issues with solutions)
  - Real example: Complete Sensitivity Labels walkthrough
  - Advanced techniques (cross-team analysis, trend analysis)
  - Automation opportunities

---

## 🚀 How to Use

### Quick Start (First-Time User)

**Step 1: Choose a Team**
```kusto
// Run: queries/all_teams_summary.kql
// Result: List of 42 teams ranked by incident volume
// Decision: Pick top 3 for analysis
```

**Step 2: Run Team Analysis**
```kusto
// Use: queries/[TeamName]_analysis.kql
// OR: Copy and modify queries/team_template.kql
// Result: List of incident titles with frequency counts
```

**Step 3: Identify Themes**
- Review incident titles for patterns
- Group similar issues (5-10 themes typical)
- Sample 3-5 incidents per theme for detail

**Step 4: Generate Report**
```bash
cp templates/team_analysis_template.md reports/MyTeam_Analysis_2026-02-04.md
# Fill in all sections using your analysis
```

**Step 5: Create Tracker**
```bash
cp templates/improvement_tracker.md team_analyses/MyTeam/improvement_tracker.md
# Track action items monthly
```

**Time Required**: 6-8 hours for complete team analysis

---

## 📖 Reference: Sensitivity Labels Example

A complete, real-world analysis is available as a working example:

**Location**: `Copilot/Created/Sensitivity_Labels_Analysis_Report.md`

**What It Demonstrates**:
- ✅ Proper theme identification (8 themes from 717 incidents)
- ✅ Evidence-based recommendations (43 total: 15 docs, 21 product, 7 UX)
- ✅ Prioritization framework (P0/P1/P2/P3 with criteria)
- ✅ Success metrics definition (50% incident reduction target)
- ✅ Actionable next steps

**How to Use**: Review this example before creating your first report to understand the expected structure and depth.

---

## 🔍 Top 10 Teams Pre-Configured

Team-specific queries are ready for these high-volume teams:

1. **DLMAppRetention** - Teams/Yammer retention policies
2. **SensitivityLabels** - Label application, visibility, encryption
3. **DLPEndpoint** - Windows/Mac endpoint DLP
4. **eDiscovery** - Content search, legal hold, exports
5. **DLMExchangeRetention** - Exchange mailbox retention, MRM
6. **MIPCore** - Core labeling infrastructure, SDK
7. **MIPServiceCore** - Backend services, policy management
8. **DLPWeb** - SharePoint/OneDrive/Exchange DLP
9. **ContentExplorer** - Data classification visibility
10. **MIPCompliance** - Audit logs, compliance reporting

**Each query includes**:
- Pre-configured team name
- Common theme areas (8-10 per team)
- Prioritization logic
- Expected outputs

---

## 📈 Success Criteria

### Program Goals
- ✅ **Reduce incident volume** by 30-50% for analyzed teams
- ✅ **Improve "By Design" rate** from ~45% to <25% (better docs)
- ✅ **Increase self-service resolution** by 30% (better docs/tools)
- ✅ **Accelerate feature delivery** (DCR-driven roadmap prioritization)

### Metrics to Track
- Monthly incident volume (overall and by theme)
- "By Design" percentage (documentation effectiveness)
- DCR volume (product gap identification)
- Customer escalation rate
- Documentation page views
- CSAT scores

---

## 🛠️ Tools & Access Required

### Prerequisites Checklist
- ✅ **ICM MCP Server**: Configured in VS Code
- ✅ **Kusto MCP Server**: Access to icmcluster.kusto.windows.net
- ✅ **IcmDataWarehouse**: Read permissions on Incidents table
- ✅ **Azure Authentication**: Configured and working
- ✅ **VS Code**: With GitHub Copilot installed

### Skills Needed
- Basic Kusto Query Language (KQL) - queries are pre-built and commented
- Familiarity with ICM incidents - understanding of HowFixed, Severity, etc.
- Product knowledge - helps with theme identification and recommendations

---

## 📋 Recommended Workflow

### For Single Team Analysis
1. ✅ Run `all_teams_summary.kql` to get overview
2. ✅ Choose team based on volume/priority
3. ✅ Execute team-specific query
4. ✅ Identify 5-10 themes from results
5. ✅ Sample 15-20 incidents for details
6. ✅ Fill in `team_analysis_template.md`
7. ✅ Present to stakeholders
8. ✅ Create `improvement_tracker.md`
9. ✅ Re-run analysis monthly

**Timeline**: 1 business day per team

### For Multi-Team Program
1. ✅ Analyze top 10 teams (10 business days)
2. ✅ Identify cross-team patterns
3. ✅ Prioritize platform-wide issues
4. ✅ Create consolidated roadmap
5. ✅ Build automated tracking dashboard
6. ✅ Establish quarterly reviews

**Timeline**: 6-8 weeks for full program setup

---

## 🎓 Training Resources

### Getting Started
1. **Read**: `WORKFLOW_GUIDE.md` (complete walkthrough)
2. **Review**: Sensitivity Labels example report
3. **Practice**: Run `all_teams_summary.kql` to see data
4. **Execute**: Pick one team and follow Phase 1-7

### Common Pitfalls to Avoid
❌ Analyzing too many teams at once (start with 1-2)
❌ Not sampling incidents for detail (titles alone aren't enough)
❌ Skipping prioritization (not all issues are equal)
❌ Creating report without stakeholder engagement plan
❌ Not tracking progress monthly (no feedback loop)

### Best Practices
✅ Start with highest volume teams (biggest impact)
✅ Use Sensitivity Labels as template (proven structure)
✅ Focus on actionable recommendations (not just observations)
✅ Quantify business impact (revenue, customer count)
✅ Track month-over-month to measure effectiveness

---

## 🔄 Maintenance & Updates

### Monthly Tasks
- Re-run team queries to update incident counts
- Update improvement trackers with progress
- Review completed action items
- Identify new themes or trends

### Quarterly Tasks
- Analyze 3-5 new teams
- Cross-team pattern analysis
- Update documentation based on learnings
- Present findings to leadership

### Annual Tasks
- Program effectiveness review
- ROI calculation (incidents reduced, costs saved)
- Expand to additional product orgs
- Build automation tools

---

## 📞 Support & Questions

### Documentation Issues
- Check `WORKFLOW_GUIDE.md` troubleshooting section
- Review Sensitivity Labels example for structure reference
- Consult `README.md` for query patterns and best practices

### Technical Issues
- **Kusto query errors**: See WORKFLOW_GUIDE.md → Troubleshooting
- **ICM MCP issues**: Verify authentication and incident ID format
- **Permission issues**: Confirm access to IcmDataWarehouse

### Process Questions
- **What team to analyze first?**: Run `all_teams_summary.kql`, pick top 3
- **How long does analysis take?**: 6-8 hours for complete team report
- **How often to re-run?**: Monthly for active teams, quarterly for others

---

## ✅ System Verification Checklist

Before using this system, verify:

- [ ] All 20 files present in `purview_analysis/` folder
- [ ] Kusto MCP Server accessible (test with `list_tables`)
- [ ] ICM MCP Server accessible (test with sample incident ID)
- [ ] Sensitivity Labels example report available for reference
- [ ] README.md readable and complete
- [ ] WORKFLOW_GUIDE.md readable and complete
- [ ] All 10 team-specific queries present
- [ ] All 3 templates present (analysis, tracker, executive)

**If any item fails**: Review setup instructions in README.md

---

## 🎯 Next Immediate Actions

### For Your First Analysis (Recommended: eDiscovery)
1. [ ] Read `WORKFLOW_GUIDE.md` sections 1-4 (Prerequisites through Phase 2)
2. [ ] Review Sensitivity Labels example report
3. [ ] Run `queries/all_teams_summary.kql` to verify Kusto access
4. [ ] Choose your first team (suggest: eDiscovery, DLPEndpoint, or MIPCore)
5. [ ] Execute team-specific query
6. [ ] Follow Phase 3-6 of WORKFLOW_GUIDE.md
7. [ ] Generate report using template
8. [ ] Schedule monthly review meeting

**Estimated Completion**: End of week (if starting now)

### For Scaling (After 2-3 Teams Complete)
1. [ ] Look for cross-team patterns
2. [ ] Identify common platform issues
3. [ ] Build consolidated improvement tracker
4. [ ] Present findings to Purview leadership
5. [ ] Consider automation opportunities

---

## 📊 Expected Outcomes

### After First Team Analysis (Week 1)
- 1 complete analysis report
- 5-10 themes identified
- 20-30 actionable recommendations
- Prioritized action items with DRIs
- Baseline metrics for tracking

### After 3 Teams Analyzed (Month 1)
- Cross-team patterns emerging
- Platform-wide issues identified
- Consolidated roadmap priorities
- Executive briefing created
- Monthly tracking established

### After 6 Months
- 10+ teams analyzed
- 30-50% incident reduction for analyzed teams
- "By Design" rate improved 20+ percentage points
- Documentation significantly expanded
- Features shipped based on DCR analysis
- Program ROI demonstrated

---

## 🏆 Success Stories (Projected)

Based on Sensitivity Labels analysis methodology:

**Theme**: File Explorer Integration  
**Before**: 45 incidents, no documentation, no solution  
**After**: Documented workaround, partnered with Windows team, 80% reduction  

**Theme**: Auto-Labeling Confusion  
**Before**: 28 incidents, customers expecting existing files to be labeled  
**After**: Clear docs, policy wizard warning, 90% reduction  

**Theme**: iOS Support  
**Before**: 67 DCRs, no roadmap commitment  
**After**: Feature prioritized, customer preview, DCRs closed  

---

## 🎉 System Ready!

**Status**: ✅ **Complete and Production-Ready**

All components have been created and are ready for immediate use:
- ✅ 14 Kusto queries (4 general + 10 team-specific)
- ✅ 3 report templates (analysis, tracker, executive)
- ✅ 2 documentation files (README, WORKFLOW_GUIDE)
- ✅ 1 example report (Sensitivity Labels - real analysis)

**Your system is now ready to:**
1. Analyze any of the 42 Purview teams
2. Generate consistent, actionable reports
3. Track improvements month-over-month
4. Present findings to stakeholders
5. Demonstrate measurable impact

---

**Start Here**: `purview_analysis/WORKFLOW_GUIDE.md`  
**Reference**: `Copilot/Created/Sensitivity_Labels_Analysis_Report.md`  
**Quick Start**: `purview_analysis/README.md`

**Happy Analyzing! 🚀**
