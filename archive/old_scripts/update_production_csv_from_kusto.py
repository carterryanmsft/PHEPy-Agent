"""
SOLUTION: Update production_full_cases.csv with 131 cases from Kusto

CURRENT STATUS:
- MCP Kusto query SUCCESSFUL: Retrieved all 131 cases
- Data available in conversation context
- Need to extract and save to data/production_full_cases.csv

APPROACH:
Since the MCP query result (131 cases) is too large to embed directly in a Python script,
the solution is to re-execute the MCP query one more time and pipe the result directly
to a file, then convert it.

STEPS TO COMPLETE:
1. Execute MCP Kusto query again (via agent): mcp_kusto-mcp-ser_execute_query
2. Save the "data" array from result to: data/kusto_raw_131.json
3. Run this script to convert JSON → CSV

Once you have kusto_raw_131.json with the 131-case data array, run:
  python update_production_csv_from_kusto.py
"""

import json
import pandas as pd
from pathlib import Path

def update_csv_from_kusto_json():
    """Convert Kusto JSON (131 cases) to production CSV"""
    
    json_file = Path("data/kusto_raw_131.json")
    csv_file = Path("data/production_full_cases.csv")
    
    print("IC/MCS Production Report - Data Update Tool")
    print("=" * 60)
    
    if not json_file.exists():
        print(f"❌ ERROR: {json_file} not found")
        print("\nPlease save the MCP Kusto query result 'data' array to:")
        print(f"  {json_file.absolute()}")
        print("\nThe data array should contain all 131 case objects.")
        return False
    
    # Load JSON
    print(f"\n[1/3] Loading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        cases = json.load(f)
    
    if isinstance(cases, dict) and 'data' in cases:
        cases = cases['data']
    
    print(f"✓ Loaded {len(cases)} cases")
    
    # Convert to DataFrame
    print(f"\n[2/3] Converting to DataFrame...")
    df = pd.DataFrame(cases)
    print(f"✓ DataFrame shape: {df.shape}")
    print(f"✓ Columns: {len(df.columns)}")
    
    # Verify expected structure
    required_cols = ['ServiceRequestNumber', 'TopParentName', 'RiskScore', 'RiskLevel', 'HasICM', 'DaysOpen']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"❌ ERROR: Missing columns: {missing}")
        return False
    
    # Show summary
    print(f"\n[3/3] Data Summary:")
    print(f"  Cases: {len(df)}")
    print(f"  Customers: {df['TopParentName'].nunique()}")
    print(f"  Risk levels: {df['RiskLevel'].value_counts().to_dict()}")
    print(f"  Date range: {df['DaysOpen'].min():.0f} - {df['DaysOpen'].max():.0f} days")
    print(f"  ICMs present: {(df['HasICM'] == 'Yes').sum()} cases")
    
    # Save to CSV
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ SUCCESS: Saved {len(df)} cases to {csv_file}")
    print(f"✓ Previous: 3 cases → Now: {len(df)} cases (100% complete)")
    
    return True

if __name__ == "__main__":
    success = update_csv_from_kusto_json()
    
    if success:
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("Run the report generator:")
        print("  cd risk_reports")
        print("  python scripts/ic_mcs_risk_report_generator.py ^")
        print("         ../data/production_full_cases.csv ^")
        print("         IC_MCS_Production_Report_131.htm ^")
        print("         ../data/icm.csv")
        print("\nExpected output: Report with 131 cases across 23 customers")
    else:
        print("\n" + "="*60)
        print("REQUIRED ACTION:")
        print("="*60)
        print("Save the MCP Kusto query result to data/kusto_raw_131.json")
        print("\nThe result should be the 'data' array from:")
        print("  mcp_kusto-mcp-ser_execute_query(...)")
        print(f"\nExpected: Array of 131 case objects with fields like:")
        print("  ServiceRequestNumber, TopParentName, RiskScore, etc.")
