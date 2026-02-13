import json
import sys

# This script will read JSON from stdin and save it to a file
# Usage: echo '{"data": [...]}' | python save_query_result.py output.json

if len(sys.argv) < 2:
    print("Usage: python save_query_result.py <output_file>")
    sys.exit(1)

output_file = sys.argv[1]

# Read from stdin
input_data = sys.stdin.read()

# Parse and validate JSON
try:
    data = json.loads(input_data)
    print(f"✓ Parsed JSON successfully")
    
    # Check if it's a Kusto result with 'data' field
    if 'data' in data:
        case_count = len(data['data'])
        print(f"✓ Found {case_count} cases in result")
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved to {output_file}")
    
except json.JSONDecodeError as e:
    print(f"✗ JSON parse error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
