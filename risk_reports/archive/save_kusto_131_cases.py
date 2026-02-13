"""
Save all 131 Kusto cases from Copilot query directly to JSON
"""
import json
import sys

# This is a placeholder - Copilot will need to embed the actual query result here
kusto_data = {
    "name": "PrimaryResult",
    "data": []  # Copilot: Replace with full query result
}

def save_kusto_data(output_file):
    """Save the Kusto query result to a JSON file"""
    print(f"Saving {len(kusto_data['data'])} cases to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(kusto_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Successfully saved {len(kusto_data['data'])} cases")
    
    # Summary
    case_count = len(kusto_data['data'])
    customers = set(case['TopParentName'] for case in kusto_data['data'])
    risk_levels = {}
    for case in kusto_data['data']:
        level = case['RiskLevel']
        risk_levels[level] = risk_levels.get(level, 0) + 1
    
    print(f"\nSummary:")
    print(f"  • Total Cases: {case_count}")
    print(f"  • Unique Customers: {len(customers)}")
    print(f"\nRisk Distribution:")
    for level in ['Critical', 'High', 'Medium', 'Low']:
        count = risk_levels.get(level, 0)
        print(f"  • {level}: {count}")

if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "data/kusto_result_131.json"
    save_kusto_data(output)
