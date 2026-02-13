import json
import csv

# The Kusto result will be passed as first command line argument
import sys

if len(sys.argv) > 1:
    json_file = sys.argv[1]
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
else:
    # Read from stdin
    import sys
    data = json.load(sys.stdin)

# Extract cases
cases = data.get('data', [])

if not cases:
    print(f"ERROR: No cases found. Data keys: {data.keys()}")
    sys.exit(1)

# Write to CSV
output_file = 'production_cases_131.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    if cases:
        fieldnames = list(cases[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cases)

print(f"SUCCESS: Created {output_file} with {len(cases)} cases")
print(f"Sample case: {cases[0]['TopParentName']} - {cases[0]['ServiceRequestNumber']} - Risk {cases[0]['RiskScore']}")
