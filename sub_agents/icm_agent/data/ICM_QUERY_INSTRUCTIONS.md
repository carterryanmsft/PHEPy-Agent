# ICM MCP Query Instructions for MIP/DLP By-Design Analysis

## Generated: 2026-02-11 09:39:39

## Query Details
- **Scope**: Last 90 days  
- **Teams**: Encryption, Labeling, DLP
- **Resolution Type**: By Design
- **Purpose**: Identify documentation gaps causing customer confusion

## Teams to Query

### 1. Sensitivity Labels (Labeling)
- Team: PURVIEW\SensitivityLabels
- Query File: `queries/mip_dlp_analysis/SensitivityLabels_by_design_90days.kql`

### 2. DLP  
- Team: PURVIEW\DLP
- Query File: `queries/mip_dlp_analysis/DLP_by_design_90days.kql`

### 3. Information Protection (Encryption/MIP)
- Team: PURVIEW\InformationProtection
- Query File: `queries/mip_dlp_analysis/InformationProtection_by_design_90days.kql`

## Using ICM MCP

### Option A: Use Kusto MCP Tool
```
Execute the KQL queries using the kusto-mcp tool with:
- Cluster: https://icmcluster.kusto.windows.net
- Database: IcMDataWarehouse
```

### Option B: Request via GitHub Copilot
Ask Copilot to execute the queries:
```
Please execute the MIP/DLP by-design ICM queries in 
sub_agents/icm_agent/queries/mip_dlp_analysis/ 
using the ICM MCP server and save the combined results to
sub_agents/icm_agent/data/mip_dlp_by_design_results.json
```

## Expected Output Format

Save all results as a single JSON array combining all three teams:

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

## Next Steps After Query Execution

1. ✓ Save combined results to `data/mip_dlp_by_design_results.json`
2. Run: `python analyze_mip_dlp_themes.py`
3. Run: `python generate_doc_gap_analysis.py`
4. Review: Generated HTML report and documentation recommendations
