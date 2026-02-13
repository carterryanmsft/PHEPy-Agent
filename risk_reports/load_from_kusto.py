#!/usr/bin/env python3
"""
Load cases from MCP Kusto, save to CSV, generate report
Works by using the last Kusto query result from conversation
"""
import csv
import subprocess
import sys
from pathlib import Path

# Paste the "data" array from the Kusto mcp_kusto-mcp-ser_execute_query result here
# This was retrieved from: cxedataplatformcluster.westus2.kusto.windows.net/cxedata
# From file: queries/ic_mcs_risk_report.kql
#
# Note: Use the raw data array from the query result, not the full JSON wrapper

CASES_DATA = """
PASTE THE 'data' ARRAY CONTENTS HERE FROM KUSTO QUERY OUTPUT
"""

def main():
    print("Note: This script requires manually pasting the Kusto query result")
    print("Please edit the script and paste the 'data' array from the Kusto query")
    print("\nFor now, using existing data/production_full_cases.csv")
    
    csv_file = Path('data/production_full_cases.csv')
    if not csv_file.exists():
        print(f"ERROR: {csv_file} not found")
        return 1
    
    # Generate report
    print("\nGenerating report...")
    result = subprocess.run([
        sys.executable,
        'scripts/ic_mcs_risk_report_generator.py',
        'data/production_full_cases.csv',
        'IC_MCS_Production_Report_131.htm',
        'data/icm.csv'
    ], capture_output=True, text=True)
    
    print(result.stdout)
    
    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
