# ICM Agent - Theme-Based Analysis & Impact Tracking

## Overview

The ICM Agent now generates **themes** from by-design incidents by clustering similar issues together, then provides queries to track the related ICM impact for each theme. This helps identify:

- **Common design limitations** affecting multiple customers
- **Related incidents** that share root causes
- **Broader impact** of specific design decisions
- **Priority areas** for documentation or product improvements

---

## How Theme Generation Works

### 1. Keyword Extraction
The agent extracts key terms from incident titles, filtering out common words to identify meaningful patterns:

```
"Sensitivity label not visible in File Explorer details view"
→ Keywords: ["sensitivity", "label", "visible", "file", "explorer"]
```

### 2. Theme Clustering
Incidents with overlapping keywords are grouped into themes:

```
Theme: "Label / Sensitivity / Visible"
├── Sensitivity label not visible in File Explorer (45 incidents)
├── Label missing in Outlook web access (29 incidents)
└── Label watermark not appearing in printed documents (18 incidents)
```

### 3. Impact Aggregation
For each theme, the agent calculates:
- Total incident count across all related issues
- Unique customer count affected by theme
- Sample incident IDs for deeper analysis

---

## Theme Analysis Output

### Report Sections

#### 1. Theme Cards
Visual cards showing:
- **Theme Name** (top 3 keywords from clustered incidents)
- **Total Incidents** (sum across all issues in theme)
- **Unique Issue Types** (distinct problems in theme)
- **Customers Affected** (unique customer count)
- **Related Incidents** (top 5 specific issues with counts)

#### 2. ICM Impact Queries
For each theme, the agent generates KQL queries to retrieve:
- Incident details (ID, title, severity)
- Customer impact (names, regions, user counts)
- Resolution metrics (time to resolve, impact duration)
- Affected services and features

---

## Usage Example

### Step 1: Run Analysis
```bash
cd sub_agents/icm_agent
python icm_agent.py --from-file data/by_design_results.json
```

### Step 2: Review Themes
Open the generated HTML report to see:
```
🎯 Label / Sensitivity / Visible
   Total Incidents: 92
   Unique Issues: 3
   Customers Affected: 76

   Related Incidents:
   - Sensitivity label not visible in File Explorer
     📊 45 incidents | 👥 32 customers | 🔄 Recurring
```

### Step 3: Query Related ICM Impact
Navigate to `queries/theme_impacts/` to find generated queries:
```
theme_Label_Sensitivity_Visible_impact.kql
```

Execute this query in Kusto Explorer to see full ICM details for incidents in this theme.

---

## Key Benefits

### 🎯 Pattern Recognition
Automatically identifies common themes across hundreds of by-design incidents without manual review.

### 📊 Impact Quantification
Shows the **cumulative effect** of design decisions across multiple related issues.

### 🔍 Root Cause Analysis
Groups incidents by shared characteristics, making it easier to identify systemic issues.

### 📝 Documentation Priorities
Highlights themes affecting the most customers, helping prioritize documentation work.

### 🔗 Cross-Incident Correlation
Links related issues that might otherwise be analyzed in isolation.

---

## Theme Report Structure

```html
ICM "By Design" Analysis Report
├── Summary Metrics
│   ├── Total Incidents: 312
│   ├── Unique Issues: 12
│   ├── Customers Affected: 238
│   ├── Critical Doc Gaps: 7
│   └── Themes Identified: 5
│
├── By-Design Themes & Related ICM Impact
│   ├── Theme 1: Label / Sensitivity / Visible
│   │   ├── Stats (incidents, issues, customers)
│   │   └── Related Incidents (top 5)
│   │
│   ├── Theme 2: Auto-Label / Policy / Apply
│   │   └── ...
│   └── ...
│
├── Top Issues Requiring Documentation
│   └── (Individual incident list)
│
└── Recommendations
    └── (Prioritized action items)
```

---

## Sample Theme Analysis

### Theme: "Label / Sensitivity / Visible"

**Total Impact:**
- 92 total incidents
- 76 unique customers affected
- 3 distinct issue types

**Related Issues:**
1. **Sensitivity label not visible in File Explorer**
   - 45 incidents, 32 customers
   - Persistent over 166 days
   - Action: Document File Explorer column setup

2. **Label missing in Outlook web access**
   - 29 incidents, 21 customers
   - Persistent over 135 days
   - Action: Update OWA documentation

3. **Label watermark not appearing in printed docs**
   - 18 incidents, 14 customers
   - Persistent over 89 days
   - Action: Clarify print behavior

**Recommended Actions:**
1. Create unified "Label Visibility Troubleshooting" guide
2. Add FAQ section covering all three scenarios
3. Update product documentation with limitations
4. Consider UX improvements for better visibility

---

## ICM Impact Query Details

### What the Queries Return

For each theme, the generated query retrieves:

```kql
Incidents
| where IncidentId in (sample_incident_ids)
| project 
    IncidentId,
    Title,
    Severity,
    CustomerName,
    CreateDate,
    ResolveDate,
    ImpactedUserCount,
    ImpactedServices,
    Region
| extend 
    ResolutionTime_Hours,
    ImpactDuration_Hours
```

### Use Cases
- **Customer reach-outs:** Identify all affected customers for proactive communication
- **Impact assessment:** Quantify total user impact across theme
- **Service correlation:** See which services are most affected
- **Regional analysis:** Identify geographic patterns
- **Resolution patterns:** Track how similar issues were resolved

---

## Advanced Features

### Theme Customization
Edit `icm_agent.py` to adjust:
- Keyword extraction logic (`_extract_keywords`)
- Theme clustering algorithm (`generate_themes`)
- Priority thresholds for highlighting themes

### Theme-Specific Queries
The agent automatically generates one query per theme:
- Saves to `queries/theme_impacts/`
- Includes theme metadata in file header
- Ready to execute in Kusto Explorer or via MCP

### Integration with Other Agents
- **Purview Product Expert:** Link themes to known product limitations
- **Work Item Manager:** Create ADO work items per theme
- **Documentation Team:** Generate documentation roadmap from themes

---

## Best Practices

### 1. Theme Naming
- Names are auto-generated from top keywords
- Edit query files to add more descriptive names if needed

### 2. Sample Size
- Agent uses max 10 sample incidents per theme for impact queries
- Adjust in `export_theme_impact_queries()` if needed

### 3. Theme Refinement
- Review themes in HTML report
- Merge similar themes manually if clustering is too granular
- Split broad themes if they cover unrelated issues

### 4. Regular Analysis
- Run weekly to track emerging themes
- Compare theme evolution over time
- Identify new patterns early

---

## Troubleshooting

### Too Many Themes
**Cause:** Low keyword overlap between incidents  
**Solution:** Increase keyword extraction count or adjust clustering logic

### Themes Too Broad
**Cause:** Common keywords grouping unrelated issues  
**Solution:** Add more stop words to filter generic terms

### Missing Impact Data
**Cause:** Sample incident IDs not found in Incidents table  
**Solution:** Verify incident IDs exist and are accessible

---

## File Locations

```
sub_agents/icm_agent/
├── icm_agent.py              # Contains theme generation logic
├── data/
│   └── *.json                # Input data files
├── reports/
│   └── icm_analysis_*.html   # Theme-based reports
└── queries/
    └── theme_impacts/        # Generated ICM impact queries
        ├── theme_*.kql
        └── ...
```

---

## Example Workflow

### 1. Extract By-Design Data
```bash
# Generate query
python icm_agent.py --days 180

# Execute in Kusto, save results
# Save to data/by_design_results.json
```

### 2. Run Theme Analysis
```bash
python icm_agent.py --from-file data/by_design_results.json
```

### 3. Review Themes
Open: `reports/icm_analysis_<timestamp>.html`

### 4. Query Theme Impact
```bash
# In Kusto Explorer, execute:
queries/theme_impacts/theme_Label_Sensitivity_Visible_impact.kql
```

### 5. Take Action
Based on themes:
- Update documentation for top themes
- File DCRs for product improvements
- Reach out to affected customers
- Create proactive communication plan

---

## Future Enhancements

- **ML-based clustering:** Use embeddings for better theme detection
- **Trend tracking:** Compare themes month-over-month
- **Auto-documentation:** Generate draft docs from themes
- **Customer segmentation:** Break down themes by customer type/size
- **Service correlation:** Identify service-specific theme patterns

---

**Last Updated:** February 5, 2026  
**Version:** 2.0 (Theme-based analysis added)
