#!/usr/bin/env python3
"""
Run MCS-only risk report:
1. Execute MCS query via Kusto MCP
2. Save to CSV
3. Generate HTML report
"""
import subprocess
import sys
import json
from pathlib import Path

def main():
    # Step 1: Run MCS query
    print("=" * 60)
    print("STEP 1: Executing MCS query via Kusto MCP...")
    print("=" * 60)
    
    query_file = Path('queries/mcs_only_risk_report.kql')
    if not query_file.exists():
        print(f"ERROR: {query_file} not found")
        return 1
    
    query_text = query_file.read_text()
    
    print(f"\nQuery: {query_file}")
    print(f"Length: {len(query_text)} characters")
    print("\nExecuting query on cxedataplatformcluster...")
    print("(This may take 30-60 seconds)")
    
    # Note: Using Kusto MCP server to execute query
    # The result will be saved to data/mcs_cases.csv manually
    print("\nPlease run this Kusto query via MCP and save results to data/mcs_cases.csv")
    print("Query file: queries/mcs_only_risk_report.kql")
    print("Cluster: cxedataplatformcluster.westus2.kusto.windows.net")
    print("Database: CXEDataPlatform")
    
    # Step 2: Generate report (using existing CSV if available)
    csv_file = Path('data/mcs_cases.csv')
    if csv_file.exists():
        print("\n" + "=" * 60)
        print("STEP 2: Generating MCS HTML report...")
        print("=" * 60)
        
        result = subprocess.run([
            sys.executable,
            'ic_mcs_risk_report_generator.py',
            str(csv_file),
            'MCS_Report_Final.htm',
            'data/icm.csv'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode != 0:
            print("ERROR:", result.stderr, file=sys.stderr)
            return 1
        
        print("\n✓ MCS report generated successfully!")
        print(f"  Output: MCS_Report_Final.htm")
    else:
        print(f"\nWaiting for {csv_file} to be created from Kusto query...")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
