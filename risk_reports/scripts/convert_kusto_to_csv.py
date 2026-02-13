import json
import csv
import sys

# Since we have the Kusto query result, we'll generate CSV from it
# This script reads from a JSON file and converts to CSV

input_file = sys.argv[1] if len(sys.argv) > 1 else "production_cases_131.json"
output_file = sys.argv[2] if len(sys.argv) > 2 else "production_cases_131.csv"

print(f"Converting {input_file} to {output_file}...")

# Load the JSON result
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract the cases from the query result
cases = data.get('data', [])
print(f"Found {len(cases)} cases in the query result")

if len(cases) == 0:
    print("ERROR: No cases found in the JSON file!")
    sys.exit(1)

# Get all field names from the first case
fieldnames = list(cases[0].keys())
print(f"Fields: {', '.join(fieldnames)}")

# Write to CSV
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cases)

print(f"✓ Successfully converted {len(cases)} cases to {output_file}")
print(f"  Top risks: {', '.join([f\"{c['TopParentName']} ({c['RiskScore']})\" for c in cases[:5]])}")
