"""
Save MCP Kusto Query Results Directly to CSV
This script takes the 131-case dataset and saves it directly to CSV
"""

import csv
import sys

# The complete 131-case dataset from MCP Kusto query
# This will be populated by copying the data array from the MCP result
cases = [
    # Data will be inserted here
]

def save_to_csv(data, output_file='data/production_full_cases.csv'):
    """Save case data to CSV file"""
    if not data:
        print("❌ No data to save")
        return False
    
    # Get fieldnames from first case
    fieldnames = list(data[0].keys())
    
    try:
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        # Validate
        case_count = len(data)
        customers = len(set(case['TopParentName'] for case in data))
        risk_dist = {}
        for case in data:
            risk = case.get('RiskLevel', 'Unknown')
            risk_dist[risk] = risk_dist.get(risk, 0) + 1
        
        print(f"\n✓ SUCCESS: Saved {case_count} cases to {output_file}")
        print(f"✓ Customers: {customers}")
        print(f"✓ Risk Distribution: {risk_dist}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(cases) == 0:
        print("⚠ WARNING: cases array is empty")
        print("Please populate the 'cases' array with the data from the MCP query result")
        sys.exit(1)
    
    save_to_csv(cases)
