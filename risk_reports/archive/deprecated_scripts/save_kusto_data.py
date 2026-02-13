# Script to execute Kusto query and save results
# This will be populated with the actual query result from the MCP tool

import json

# Placeholder - will be replaced with actual query result
query_result = {"name": "PrimaryResult", "data": []}

# Save to file
output_file = "production_cases_131.json"

try:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(query_result, f, indent=2, ensure_ascii=False)
    
    case_count = len(query_result.get('data', []))
    print(f"✓ Saved {case_count} cases to {output_file}")
    
except Exception as e:
    print(f"✗ Error saving file: {e}")
