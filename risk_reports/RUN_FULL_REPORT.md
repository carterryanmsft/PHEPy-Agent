# ONE-SHOT AUTOMATED IC/MCS RISK REPORT

## The Problem We Solved
The Kusto MCP tool returns data in memory, but we need it saved to a file. We went in circles trying different save approaches.

## The Solution
A **single command** that:
1. Queries Kusto for all 131 cases
2. Saves the result immediately
3. Converts to CSV
4. Generates the HTML report

## How to Run

Simply ask Copilot:

```
"Execute the full IC/MCS risk report with all 131 cases"
```

Copilot will:
1. Query Kusto using `mcp_kusto-mcp-ser_execute_query` 
2. Immediately save the JSON result to `data/kusto_result_131.json`
3. Convert to CSV using `write_all_cases.py`
4. Generate report using `ic_mcs_risk_report_generator.py`

## Output
- **Report File**: `IC_MCS_Production_Report_FULL_131.htm`
- **Contains**: All 131 cases across 23 customers
- **Distribution**: 2 Critical, 7 High, 36 Medium, 86 Low
- **Features**: ICM enrichment, risk scoring, color coding

## Why This Works
The automation happens in the conversation - Copilot queries Kusto, captures the result, and chains the processing scripts together in one flow. No manual copy/paste needed!

##Status
✓ Report generator: WORKING (all 3 bugs fixed)
✓ ICM enrichment: WORKING (owners, status, highlighting)
✓ Kusto query: WORKING (returns all 131 cases)  
✓ File I/O: WORKING (OneDrive confirmed not an issue)
✓ ONE-SHOT PROCESS: **READY TO USE**
