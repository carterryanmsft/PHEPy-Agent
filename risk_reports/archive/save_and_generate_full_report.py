"""
Simple workflow: Query Kusto via MCP, save to CSV, generate HTML report
This bypasses OneDrive complexity by using straightforward file writes
"""

import sys
import json
import pandas as pd
from pathlib import Path

# The successful Kusto query returned 131 cases
# Rather than re-query, let's use the existing production_full_cases.csv and verify

def main():
    print("IC/MCS Risk Report Generator - Full 131 Cases\n")
    print("="*80)
    
    # Check current data
    csv_file = Path("data/production_full_cases.csv")
    
    if not csv_file.exists():
        print(f"❌ CSV file not found: {csv_file}")
        print("\nSolution: Run the Kusto query and save results to:")
        print(f"  {csv_file.absolute()}")
        return 1
    
    # Load and check
    df = pd.read_csv(csv_file)
    print(f"✓ Loaded CSV: {len(df)} cases")
    
    if len(df) < 131:
        print(f"\n⚠️  WARNING: Expected 131 cases, found {len(df)}")
        print("   The CSV file has incomplete data")
        print("\n   To get all 131 cases, you need to:")
        print("   1. Re-run the Kusto MCP query")
        print("   2. Save the JSON result to: data/kusto_result_131.json")
        print("   3. Convert to CSV")
    
    # Generate report with whatever data we have
    print(f"\n📊 Generating report with {len(df)} cases...")
    
    import subprocess
    result = subprocess.run([
        sys.executable, 
        "ic_mcs_risk_report_generator.py",
        "data/production_full_cases.csv",
        "IC_MCS_Production_Report_CURRENT.htm",
        "data/icm.csv"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Report generated: IC_MCS_Production_Report_CURRENT.htm")
        print(result.stdout)
        
        # Show summary
        risk_counts = df['RiskLevel'].value_counts().to_dict()
        print(f"\n{'='*80}")
        print(f"REPORT SUMMARY")
        print(f"{'='*80}")
        print(f"Total Cases: {len(df)}")
        print(f"Customers: {df['TopParentName'].nunique()}")
        print(f"\nRisk Distribution:")
        for risk in ['Critical', 'High', 'Medium', 'Low']:
            if risk in risk_counts:
                print(f"  {risk}: {risk_counts[risk]}")
        
        return 0
    else:
        print(f"❌ Report generation failed:")
        print(result.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
