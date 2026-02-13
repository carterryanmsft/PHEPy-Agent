"""
Save all 118 cases from Kusto query result to production CSV
This script takes the JSON output from mcp_kusto query and saves it to CSV format
"""
import pandas as pd
import json
from pathlib import Path

def save_kusto_results_to_csv(query_result_json):
    """
    Convert Kusto query result JSON to CSV
    
    Args:
        query_result_json: The JSON result from mcp_kusto-mcp-ser_execute_query
    """
    
    # Parse the query result
    if isinstance(query_result_json, str):
        data = json.loads(query_result_json)
    else:
        data = query_result_json
    
    # Extract the case data
    # Query result structure: {"name": "PrimaryResult", "data": [{case1}, {case2}, ...]}
    if 'data' in data:
        cases = data['data']
    else:
        cases = data
    
    # Convert to DataFrame
    df = pd.DataFrame(cases)
    
    print(f"📊 Loaded {len(df)} cases from Kusto query")
    print(f"✓ Columns: {len(df.columns)}")
    print(f"✓ Programs: {df['Program'].value_counts().to_dict()}")
    print(f"✓ Top customers by case count:")
    print(df['TopParentName'].value_counts().head(5))
    
    # Save to production CSV
    output_path = Path(__file__).parent.parent / 'data' / 'production_full_cases.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ SUCCESS: Saved {len(df)} cases to {output_path}")
    print(f"Previous: 10 cases → Now: {len(df)} cases")
    
    return df

# For manual execution, you would call:
# save_kusto_results_to_csv(query_result_json)

if __name__ == "__main__":
    print("="*70)
    print("KUSTO DATA SAVER - Ready to process 118 cases")
    print("="*70)
    print("\nUsage:")
    print("1. Execute Kusto query to get 118 IC/MCS cases")
    print("2. Pass the JSON result to save_kusto_results_to_csv()")
    print("3. CSV will be saved to data/production_full_cases.csv")
    print("\nAlternatively, paste the query result JSON below and run this script.")
