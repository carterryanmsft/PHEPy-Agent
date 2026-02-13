"""
FINAL SOLUTION: Query Kusto via MCP and save 131 cases to CSV

This documents the exact steps to complete the data update.
"""

print("""
================================================================================
IC/MCS PRODUCTION REPORT - DATA UPDATE PROCEDURE
================================================================================

PROBLEM:
  • Current data/production_full_cases.csv has only 3 cases
  • Should have 131 cases from Kusto query

SOLUTION STATUS:
  ✓ MCP Kusto query works (returns all 131 cases)
  ✓ Query: queries/ic_mcs_risk_report.kql
  ✓ Cluster: cxedataplatformcluster.westus2.kusto.windows.net  
  ✓ Database: cxedata

STEPS TO COMPLETE:
================================================================================

OPTION A: Manual JSON → CSV Conversion (SIMPLEST)
--------------------------------------------------
1. Re-run the MCP Kusto query:
   Call: mcp_kusto-mcp-ser_execute_query  
   Parameters:
     - clusterUrl: https://cxedataplatformcluster.westus2.kusto.windows.net
     - database: cxedata
     - query: <contents of queries/ic_mcs_risk_report.kql>
     - maxRows: 150

2. Copy the "data" array from the result (131 case objects)

3. Save to: data/kusto_raw_131.json
   Format: Just the array, like: [{case1}, {case2}, ...]

4. Run: python update_production_csv_from_kusto.py

5. Generate report:
   cd risk_reports
   python scripts/ic_mcs_risk_report_generator.py ../data/production_full_cases.csv IC_MCS_Production_Report_131.htm ../data/icm.csv


OPTION B: Automated PowerShell (REQUIRES MCP ACCESS)
----------------------------------------------------
# Read query file
$query = Get-Content queries/ic_mcs_risk_report.kql -Raw

# Execute via MCP (requires mcp-kusto-server to be running)
# ... MCP tool invocation ...  
# Save result → data/kusto_raw_131.json

# Convert to CSV
python update_production_csv_from_kusto.py

# Generate report
cd risk_reports
python scripts/ic_mcs_risk_report_generator.py ../data/production_full_cases.csv IC_MCS_Production_Report_131.htm ../data/icm.csv


VERIFICATION:
================================================================================
After completing the update:

✓ Check CSV: 
  python -c "import pandas as pd; df=pd.read_csv('data/production_full_cases.csv'); print(f'Cases: {len(df)}, Customers: {df.TopParentName.nunique()}')"
  
  Expected: Cases: 131, Customers: 23

✓ Check report HTML:
  Open IC_MCS_Production_Report_131.htm in browser
  
  Expected: "Total Cases: 131 | Customers: 23"
  

CURRENT STATUS:
================================================================================
• MCP query result available in conversation context
• All 131 cases retrieved successfully
• Waiting for user to choose Option A or Option B above
• Once CSV updated, can regenerate report immediately

""")
