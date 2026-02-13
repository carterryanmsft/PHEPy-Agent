# ICM Query Execution Instructions

## Expanded By-Design Analysis - 180 Days

**Generated:** 2026-02-11 10:34:41  
**Scope:** Last 180 days  
**Resolution Type:** By Design (ALL prevention types)  
**Teams:** 15 MIP/DLP/Encryption teams

## Teams Included

### Labeling & Classification
- Sensitivity Labels
- Classification

### DLP (All Workloads)
- DLP (Generic)
- DLP Alerts
- DLP Endpoint
- DLP Exchange
- DLP SharePoint OneDrive
- DLP Teams

### Information Protection & Encryption
- Information Protection
- Encryption
- RMS (Rights Management Service)
- AIP (Azure Information Protection)

### Auto Labeling
- Server Side Auto Labeling

## Query Files

All query files are in this directory. Each file is named:
`[TeamName]_by_design_180days.kql`

## Execution Options

### Option 1: GitHub Copilot with ICM MCP (Recommended)

Ask Copilot:
```
Please execute all KQL queries in:
sub_agents/icm_agent/queries/expanded_by_design_180days/

Use ICM MCP with:
- Cluster: https://icmcluster.kusto.windows.net
- Database: IcMDataWarehouse

Save combined results to:
sub_agents/icm_agent/data/expanded_by_design_180days_results.json
```

### Option 2: Kusto Explorer

1. Open Kusto Explorer
2. Connect: https://icmcluster.kusto.windows.net
3. Database: IcMDataWarehouse
4. Execute each .kql file
5. Export as JSON and combine

### Option 3: ICM Portal Advanced Search

Use these filters:
- owning_team_id IN (teams listed above)
- how_fixed = "By Design"
- created_date >= now() - 180d
- Export results

## Expected Data

Each ICM should include:
- ID
- Title
- Description/Summary
- Severity
- Status
- Owning Team
- Created Date
- Modified Date
- How Fixed (should be "By Design")
- Prevention Type (if available)
- Customer Name
- Source

## Next Steps

After gathering data, run:
```bash
python analyze_expanded_by_design.py
```

This will generate:
1. Comprehensive documentation gap analysis
2. Prevention type breakdown
3. Theme identification across all By-Design types
4. Executive summary report (using approved format)
