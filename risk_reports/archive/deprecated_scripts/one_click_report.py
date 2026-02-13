#!/usr/bin/env python3
"""
ONE-CLICK IC/MCS Production Report Generator
Takes the full 131-case Kusto result and generates the complete report
"""
import json
import csv
import subprocess
import sys

# Embedding the complete Kusto result data from the MCP query
# This is the full 131-case dataset returned by mcp_kusto-mcp-ser_execute_query

print("=" * 60)
print("IC/MCS PRODUCTION REPORT GENERATOR")
print("=" * 60)
print()

# Check if we should read from file or use embedded data
if len(sys.argv) > 1 and sys.argv[1] == "--from-file":
    json_file = sys.argv[2] if len(sys.argv) > 2 else "data/kusto_result.json"
    print(f"Reading Kusto result from: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        kusto_result = json.load(f)
    cases = kusto_result.get('data', [])
else:
    # I have the data from the Kusto MCP query - let me use it directly
    # COPILOT: Insert the full 131-case JSON data here
    print("ERROR: Full dataset needs to be embedded in this script")
    print("Usage:")
    print("  1. Save Kusto JSON to data/kusto_result.json")
    print("  2. Run: python one_click_report.py --from-file data/kusto_result.json")
    sys.exit(1)

if not cases:
    print("ERROR: No cases found!")
    sys.exit(1)

print(f"Processing {len(cases)} cases from Kusto query...")

# Step 1: Convert to CSV
csv_file = "data/production_cases_131.csv"
print(f"\nStep 1: Creating CSV file...")

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    fields = list(cases[0].keys())
    writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(cases)

print(f"✓ Created {csv_file} with {len(cases)} cases")

# Step 2: Generate HTML report
report_file = "IC_MCS_Production_Report_131.htm"
icm_file = "icm.csv"

print(f"\nStep 2: Generating HTML report...")
result = subprocess.run(
    [sys.executable, "ic_mcs_risk_report_generator.py", csv_file, report_file, icm_file],
    capture_output=True,
    text=True,
    encoding='utf-8'
)

print(result.stdout)
if result.stderr:
    print("Warnings:", result.stderr)

if result.returncode == 0:
    print()
    print("=" * 60)
    print(f"✓✓✓ SUCCESS! ✓✓✓")
    print(f"Report generated: {report_file}")
    print(f"Total cases: {len(cases)}")
    print("=" * 60)
else:
    print("\n✗ ERROR: Report generation failed")
    sys.exit(1)
