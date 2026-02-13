# MIP/DLP By-Design Analysis - Workflow Summary

**Generated:** February 11, 2026  
**Status:** Phase 1 Complete - Queries Generated  
**Next Phase:** ICM Query Execution Required

---

## 🎯 Objective

Analyze by-design escalations in MIP/DLP areas (encryption, labeling, DLP) for the last 90 days to:
1. Identify common themes and patterns
2. Assess documentation gaps on learn.microsoft.com
3. Generate actionable recommendations for content improvements

---

## ✅ Phase 1: Complete - Query Generation

### What Was Created

#### 1. KQL Queries for ICM Analysis
Three queries generated for MIP/DLP teams analyzing by-design incidents:

- **Sensitivity Labels (Labeling)**
  - File: `queries/mip_dlp_analysis/SensitivityLabels_by_design_90days.kql`
  - Team: PURVIEW\SensitivityLabels

- **DLP (Data Loss Prevention)**
  - File: `queries/mip_dlp_analysis/DLP_by_design_90days.kql`
  - Team: PURVIEW\DLP

- **Information Protection (Encryption/MIP)**
  - File: `queries/mip_dlp_analysis/InformationProtection_by_design_90days.kql`
  - Team: PURVIEW\InformationProtection

#### 2. Analysis Scripts
Created three Python scripts for end-to-end workflow:

1. **analyze_mip_dlp_by_design.py** - Query generation (✅ Complete)
2. **analyze_mip_dlp_themes.py** - Theme clustering analysis
3. **generate_doc_gap_analysis.py** - Documentation gap detection

#### 3. Instructions
- `data/ICM_QUERY_INSTRUCTIONS.md` - Detailed execution instructions

---

## 🔄 Phase 2: ICM Query Execution (Required Next)

### Option A: Manual Kusto Explorer Execution

**Requirements:**
- Access to Kusto Explorer with ICM permissions
- Cluster: https://icmcluster.kusto.windows.net
- Database: IcMDataWarehouse

**Steps:**
1. Open each query file in Kusto Explorer:
   - `queries/mip_dlp_analysis/SensitivityLabels_by_design_90days.kql`
   - `queries/mip_dlp_analysis/DLP_by_design_90days.kql`
   - `queries/mip_dlp_analysis/InformationProtection_by_design_90days.kql`

2. Execute each query and export results as JSON

3. Combine all three result sets into a single JSON array

4. Save combined results to:
   `data/mip_dlp_by_design_results.json`

**Expected Format:**
```json
[
  {
    "Title": "Sensitivity label not visible in File Explorer",
    "Count": 45,
    "FirstSeen": "2025-11-15T10:30:00Z",
    "LastSeen": "2026-02-03T14:22:00Z",
    "SampleIncidents": [728221759, 729445123, 730112456],
    "AffectedCustomers": 32,
    "SeverityBreakdown": {"2": 5, "3": 30, "4": 10},
    "DaysBetween": 80,
    "IsRecurring": "Yes"
  },
  ...
]
```

### Option B: ICM MCP Server (Authentication Required)

The Kusto MCP server needs proper authentication configured:
- Verify MCP server connection in `mcp.json`
- Ensure Azure AD authentication is configured
- May require ICM data access permissions

---

## 📊 Phase 3: Theme Analysis (Automated)

Once query results are saved, run:

```bash
cd sub_agents/icm_agent
python analyze_mip_dlp_themes.py
```

**This will:**
- Load ICM query results
- Cluster similar incidents into themes based on keywords
- Calculate impact metrics (incident count, customer count)
- Generate HTML report with visualizations
- Export theme-specific KQL queries for deeper analysis
- Save themes to `data/mip_dlp_themes.json`

**Output:**
- HTML report in `reports/` folder
- Theme impact queries in `queries/theme_impacts/`
- JSON summary in `data/mip_dlp_themes.json`

---

## 📝 Phase 4: Documentation Gap Analysis (Automated)

After theme analysis completes, run:

```bash
cd sub_agents/icm_agent
python generate_doc_gap_analysis.py
```

**This will:**
- Load identified themes
- Generate Purview Product Expert review prompts for each theme
- Create comprehensive markdown report
- Include prioritization (CRITICAL/HIGH/MEDIUM/LOW)
- Save context for expert agent review

**Output:**
- Markdown report: `reports/mip_dlp_doc_gap_analysis_[timestamp].md`
- Expert context: `data/purview_expert_context.json`

---

## 🔍 Phase 5: Expert Review (Manual/Agent-Assisted)

### Manual Review
Open the generated report and manually assess each theme for:
- Whether behavior is truly by-design vs product gap
- Existing documentation on learn.microsoft.com
- Content recommendations
- Priority assessment

### Agent-Assisted Review
Invoke Purview Product Expert agent:

```
Please review the documentation gap analysis in 
sub_agents/icm_agent/data/purview_expert_context.json
and provide your assessment for each theme.
```

**Expert will assess:**
1. Is this truly by-design or a product gap?
2. Does documentation exist on learn.microsoft.com?
3. What specific content should be created/updated?
4. What should customers be told?
5. Priority level for documentation work

---

## 📈 Expected Outcomes

### Deliverables
1. **Theme Analysis Report** (HTML)
   - Visual cards showing theme impact
   - Incident counts and customer impact
   - Related ICM patterns

2. **Documentation Gap Analysis** (Markdown)
   - Prioritized list of documentation needs
   - Specific recommendations per theme
   - Customer communication strategies

3. **Expert Assessment** (Generated by Product Expert)
   - learn.microsoft.com content gaps identified
   - Specific article recommendations
   - Priority-based action plan

### Success Metrics
- Number of themes identified
- Customer impact quantification
- Documentation gaps discovered
- Actionable recommendations generated

---

## 🚀 Quick Start Commands

```bash
# Step 1: Generate queries (✅ COMPLETE)
python analyze_mip_dlp_by_design.py

# Step 2: Execute queries manually in Kusto Explorer
# Save results to: data/mip_dlp_by_design_results.json

# Step 3: Analyze themes
python analyze_mip_dlp_themes.py

# Step 4: Generate documentation gap analysis
python generate_doc_gap_analysis.py

# Step 5: Review with Product Expert
# Open reports/mip_dlp_doc_gap_analysis_[timestamp].md
```

---

## 📂 File Structure

```
sub_agents/icm_agent/
├── analyze_mip_dlp_by_design.py      ✅ Created
├── analyze_mip_dlp_themes.py         ✅ Created
├── generate_doc_gap_analysis.py      ✅ Created
├── queries/
│   └── mip_dlp_analysis/
│       ├── SensitivityLabels_by_design_90days.kql    ✅ Generated
│       ├── DLP_by_design_90days.kql                  ✅ Generated
│       └── InformationProtection_by_design_90days.kql ✅ Generated
├── data/
│   ├── ICM_QUERY_INSTRUCTIONS.md                     ✅ Created
│   ├── mip_dlp_by_design_results.json                ⏳ Needs execution
│   ├── mip_dlp_themes.json                           ⏳ Pending
│   └── purview_expert_context.json                   ⏳ Pending
└── reports/
    ├── [HTML theme report]                            ⏳ Pending
    └── mip_dlp_doc_gap_analysis_[timestamp].md       ⏳ Pending
```

---

## 🔧 Troubleshooting

### Kusto Authentication Issues
- Ensure you have ICM data access permissions
- Try running queries in Kusto Explorer manually
- Contact ICM admin for access if needed

### MCP Server Connection
- Verify `mcp.json` configuration
- Check Kusto MCP server is running
- Ensure Azure AD authentication is configured

### Missing Data Files
- Verify query execution completed successfully
- Check JSON format matches expected structure
- Ensure all three team queries are combined

---

## 📞 Support

For assistance with:
- **ICM Queries:** See `data/ICM_QUERY_INSTRUCTIONS.md`
- **Theme Analysis:** See `sub_agents/icm_agent/THEME_ANALYSIS_GUIDE.md`
- **Product Expert:** See `sub_agents/purview_product_expert/AGENT_INSTRUCTIONS.md`

---

## ✨ What's Next

1. **Immediate:** Execute ICM queries in Kusto Explorer
2. **After data collection:** Run theme analysis
3. **After themes identified:** Run documentation gap analysis
4. **Final step:** Expert review and action planning

---

*Generated by PHEPy ICM Agent - February 11, 2026*
