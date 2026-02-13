"""
Convert MCP Kusto query result to CSV
Usage: Pass JSON result as argument or stdin
"""
import pandas as pd
import json
import sys

def convert_to_csv(json_data):
    """Convert MCP query result JSON to CSV"""
    
    # Parse if string
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    # Extract the data array
    if isinstance(data, dict) and 'data' in data:
        cases = data['data']
    elif isinstance(data, list):
        cases = data
    else:
        raise ValueError("Unexpected JSON structure")
    
    # Convert to DataFrame
    df = pd.DataFrame(cases)
    
    # Save to CSV
    output_path = 'data/production_full_cases.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"✓ SUCCESS: Saved {len(df)} cases to {output_path}")
    print(f"  Customers: {df['TopParentName'].nunique()}")
    print(f"  Risk levels: {df['RiskLevel'].value_counts().to_dict()}")
    
    return len(df)

if __name__ == "__main__":
    # This will be called with the MCP result
    print("Ready to convert MCP query result to CSV...")
