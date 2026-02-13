import json
import csv
import sys

# Read the Kusto query result from stdin (it will be in JSON format)
input_data = sys.stdin.read()
data = json.loads(input_data)

# Extract cases array from the result
cases = data['data']

if not cases:
    print("ERROR: No cases found in data!")
    sys.exit(1)

# Get all field names from the first case
fieldnames = list(cases[0].keys())

# Write to CSV
output_file = 'production_cases_131.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cases)

print(f"SUCCESS: Converted {len(cases)} cases to {output_file}")
print(f"Fields: {', '.join(fieldnames[:5])}... ({len(fieldnames)} total)")
