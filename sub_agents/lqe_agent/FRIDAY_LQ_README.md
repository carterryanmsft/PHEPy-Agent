# Friday Night Low Quality Escalation Analysis

## Overview
Specialized weekly analysis workflow for identifying and organizing **unassigned low quality escalations** from the past 7 days, designed for Friday night runs.

## Purpose
Identify escalations that:
- Were closed in the last 7 days
- Are marked as low quality (EscalationQuality != "All Data Provided")
- Have **blank/no reviewer assignment**
- Are not false positives

## Organization Structure
Escalations are organized by two dimensions:

### 1. Originating Region
- **Americas** - US, North America
- **EMEA** - Europe, Middle East, Africa
- **APAC** - Asia Pacific
- **LATAM** - Latin America
- **Unknown** - Unable to determine

### 2. Feature Area
- **MIP/DLP** - Microsoft Information Protection / Data Loss Prevention
- **DLM** - Data Lifecycle Management / Retention
- **eDiscovery** - Electronic Discovery
- **Compliance** - Compliance and Records Management
- **Other** - Other feature areas
- **Unknown** - Not specified

## How to Run

### Option 1: With Pre-loaded Data
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"
python run_friday_lq_analysis.py --data-file data/friday_lq_20260205.json
```

### Option 2: Fresh Query Execution
1. Run the script without parameters to get the Kusto query:
```powershell
python run_friday_lq_analysis.py
```

2. Execute the query via MCP Kusto tool or Kusto Explorer:
   - **Cluster**: `https://icmcluster.kusto.windows.net`
   - **Database**: `IcMDataWarehouse`

3. Save results to: `data/friday_lq_YYYYMMDD.json`

4. Re-run with data file:
```powershell
python run_friday_lq_analysis.py --data-file data/friday_lq_20260205.json
```

## Output Files

### 1. JSON Report (`friday_reports/friday_lq_report_YYYYMMDD_HHMMSS.json`)
Comprehensive report with:
- Executive summary with counts by region and feature
- Full escalation details organized by region → feature area
- Reviewer instructions and next steps
- Metadata and filter criteria

### 2. CSV Export (`friday_reports/friday_lq_report_YYYYMMDD_HHMMSS.csv`)
Flat file with all escalations for easy filtering and sorting in Excel.

## Query Logic

The Kusto query filters for:
```
EscalationQuality != "All Data Provided"
AND (ReviewerName is empty OR ReviewerName == "")
AND (QualityReviewFalsePositive != "Yes" OR QualityReviewFalsePositive is empty)
AND ResolveDate > ago(7d)
```

Region mapping:
- Determined from `SourceOrigin` field
- Pattern matching for region keywords

Feature area mapping:
- Determined from `Feature Area` custom field
- Categorized into major product groups

## Reviewer Distribution

The report is intended for distribution to:
- Support leadership team (reviewers in `lq_escalation_config.json`)
- Regional managers for follow-up
- Feature area leads for quality coaching

## Scheduling

### Windows Task Scheduler
Create a scheduled task for Friday nights:
- **Trigger**: Weekly, every Friday at 8:00 PM
- **Action**: 
  ```
  Program: python.exe
  Arguments: run_friday_lq_analysis.py
  Start in: C:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents
  ```

### Manual Execution
Run anytime to get a snapshot of the last 7 days:
```powershell
cd sub_agents
python run_friday_lq_analysis.py --data-file data/latest_friday_data.json
```

## Next Steps After Report Generation

1. **Review the report** - Check summary statistics and regional breakdown
2. **Assign reviewers** - Update ICM with appropriate reviewer for each case
3. **Quality follow-up** - Contact escalation owners about quality issues
4. **Track trends** - Compare week-over-week to identify improvement areas
5. **Coaching** - Use data for targeted quality coaching sessions

## Configuration

Edit `lq_escalation_config.json` to:
- Add/remove reviewers
- Update reviewer contact information
- Set default reviewer assignments

## Files

- **run_friday_lq_analysis.py** - Main execution script
- **low_quality_escalation_agent.py** - Core analysis logic
- **lq_escalation_config.json** - Reviewer configuration
- **data/** - Cached query results
- **friday_reports/** - Generated reports

## Troubleshooting

**No data returned**:
- Check date filters in query
- Verify "All Data Provided" is the correct quality value
- Ensure ReviewerName field name is correct in ICM

**Region showing as Unknown**:
- Check SourceOrigin field values in ICM
- Update region mapping logic if needed

**Feature area not categorizing**:
- Check Feature Area custom field values
- Update feature area mapping in query

## Related Documentation
- [LQ_ESCALATION_README.md](LQ_ESCALATION_README.md) - Main LQE agent documentation
- [lq_escalation_config.json](lq_escalation_config.json) - Reviewer configuration
- [collect_lq_data.py](collect_lq_data.py) - Data collection helper

---
**Last Updated**: February 5, 2026  
**Author**: Carter Ryan
