"""
Process MCP Kusto query result and write to CSV
Accepts JSON via stdin or from the query result stored in memory
"""

import pandas as pd
import sys
import json

# Read JSON from stdin or use embedded data
if not sys.stdin.isatty():
    # Read from stdin
    json_str = sys.stdin.read()
    data = json.loads(json_str)
else:
    print("Waiting for JSON input via stdin...")
    print("Usage: echo '{...}' | python process_mcp_result.py")
    sys.exit(1)

# Extract cases
if 'data' in data:
    cases = data['data']
elif isinstance(data, list):
    cases = data
else:
    print(f"ERROR: Unexpected data structure: {type(data)}")
    sys.exit(1)

# Convert to DataFrame
df = pd.DataFrame(cases)

# Write to CSV
output_file = 'data/production_full_cases.csv'
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
print(f"✓ Successfully wrote {len(df)} cases to {output_file}")
print(f"  • Unique Customers: {df['TopParentName'].nunique()}")

if 'RiskLevel' in df.columns:
    risk_dist = df['RiskLevel'].value_counts().to_dict()
    print(f"  • Critical: {risk_dist.get('Critical', 0)}, High: {risk_dist.get('High', 0)}, Medium: {risk_dist.get('Medium', 0)}, Low: {risk_dist.get('Low', 0)}")
