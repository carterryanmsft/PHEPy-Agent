"""
Convert Kusto JSON result to CSV and regenerate report
This script takes the Kusto query result (131 cases) and saves it to CSV,
then regenerates the IC/MCS Production Report
"""

import json
import pandas as pd
from pathlib import Path

# Kusto result from the query execution - paste the JSON data here
# For now, I'll use the MCP execute result directly
# You'll need to run the mcp_kusto-mcp-ser_execute_query tool first and 
# then this script will read from a temporary JSON file

def convert_kusto_to_csv():
    """Convert Kusto query result JSON to CSV format"""
    
    # Read the Kusto result from stdin or a temp file
    # For simplicity, we'll create it manually with the 131 cases
    
    print("=" * 80)
    print("KUSTO RESULT TO CSV CONVERTER")
    print("=" * 80)
    
    # Check if temp JSON file exists
    temp_json_path = Path("data/kusto_result_temp.json")
    if temp_json_path.exists():
        print(f"\n[1/3] Reading Kusto result from {temp_json_path}...")
        with open(temp_json_path, 'r', encoding='utf-8') as f:
            kusto_result = json.load(f)
        print(f"✓ Loaded {len(kusto_result['data'])} cases")
    else:
        print(f"\n✗ ERROR: {temp_json_path} not found")
        print("\nTo use this script:")
        print("1. Run the Kusto query via MCP tool")
        print("2. Save the result JSON to data/kusto_result_temp.json")
        print("3. Run this script again")
        return False
    
    # Convert to DataFrame
    print("\n[2/3] Converting to DataFrame...")
    df = pd.DataFrame(kusto_result['data'])
    print(f"✓ Created DataFrame with {len(df)} rows, {len(df.columns)} columns")
    
    # Save to CSV
    output_csv = Path("data/production_full_cases.csv")
    print(f"\n[3/3] Saving to {output_csv}...")
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"✓ Saved {len(df)} cases to CSV")
    
    # Display summary
    print("\n" + "=" * 80)
    print("CONVERSION COMPLETE")
    print("=" * 80)
    print(f"\nTotal Cases: {len(df)}")
    print(f"Unique Customers: {df['TopParentName'].nunique()}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nRisk Levels:")
    for level in ['Critical', 'High', 'Medium', 'Low']:
        count = len(df[df['RiskLevel'] == level])
        print(f"  {level}: {count}")
    
    print(f"\nNext step: Run the report generator:")
    print(f"  python scripts/ic_mcs_risk_report_generator.py data/production_full_cases.csv IC_MCS_Production_Report_131.htm data/icm.csv")
    
    return True

if __name__ == "__main__":
    convert_kusto_to_csv()
