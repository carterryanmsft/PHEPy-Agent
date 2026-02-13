import json
import csv
import sys

# Read the Kusto JSON output from stdin (will be piped from PowerShell)
kusto_json = sys.stdin.read()
data = json.loads(kusto_json)

# Extract cases from the result
cases = data.get('data', [])

if not cases:
    print("ERROR: No cases found in Kusto result", file=sys.stderr)
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
