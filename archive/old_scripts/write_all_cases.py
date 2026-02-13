"""
Write all 131 production cases from MCP Kusto query to CSV
Processes the complete dataset and generates the production_full_cases.csv file
"""

import pandas as pd
import json
from pathlib import Path

# This will be populated with the MCP query result
# For now, we'll read from the temp file or process directly
def write_cases_to_csv(json_file_path=None, json_data=None):
    """
    Convert MCP query result to CSV
    
    Args:
        json_file_path: Path to JSON file with MCP result
        json_data: Direct JSON data (dict or str)
    """
    if json_file_path:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif json_data:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
    else:
        raise ValueError("Must provide either json_file_path or json_data")
    
    # Extract the cases array
    if 'data' in data:
        cases = data['data']
    elif isinstance(data, list):
        cases = data
    else:
        raise ValueError("Unexpected data structure")
    
    # Convert to DataFrame
    df = pd.DataFrame(cases)
    
    # Ensure data directory exists
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)
    
    # Write to CSV
    output_file = output_dir / 'production_full_cases.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    # Generate report
    print(f"✓ Successfully wrote {len(df)} cases to {output_file}")
    print(f"\nData Summary:")
    print(f"  • Total Cases: {len(df)}")
    print(f"  • Unique Customers: {df['TopParentName'].nunique()}")
    print(f"  • Columns: {len(df.columns)}")
    
    if 'RiskLevel' in df.columns:
        risk_dist = df['RiskLevel'].value_counts().to_dict()
        print(f"\nRisk Distribution:")
        for level in ['Critical', 'High', 'Medium', 'Low']:
            count = risk_dist.get(level, 0)
            print(f"  • {level}: {count}")
    
    return df

if __name__ == "__main__":
    import sys
    
    # Check for command line argument
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        print(f"Reading from {json_file}...")
        df = write_cases_to_csv(json_file_path=json_file)
    else:
        # Check if temp JSON file exists from the MCP query
        temp_file = Path('temp_data.json')
        
        if temp_file.exists():
            print(f"Reading from {temp_file}...")
            df = write_cases_to_csv(json_file_path=temp_file)
        else:
            print("ERROR: No temp_data.json found.")
            print("\nTo use this script:")
            print("1. Save the MCP query result to 'temp_data.json'")
            print("2. Run: python write_all_cases.py [json_file]")
            print("\nAlternatively, modify this script to include the JSON data directly.")
