#!/usr/bin/env python3
"""
Convert Kusto JSON result to CSV for report generation
Save this in risk_reports/ directory
Run: python kusto_to_csv.py
Then manually copy/paste the Kusto JSON when prompted
"""
import json
import csv
import sys

print("Paste the Kusto JSON result and press Enter, then Ctrl+Z (Windows) or Ctrl+D (Unix):")
print()

# Read from stdin
json_text = sys.stdin.read()

try:
    kusto_result = json.loads(json_text)
    cases = kusto_result.get('data', [])
    
    if not cases:
        print("ERROR: No cases found in JSON")
        sys.exit(1)
    
    print(f"\nFound {len(cases)} cases")
    
    # Write to CSV
    output_file = 'data/production_cases_131.csv'
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if cases:
            fields = list(cases[0].keys())
            writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(cases)
    
    print(f"✓ Created {output_file} with {len(cases)} cases")
    print(f"\nNext step: Run the report generator:")
    print(f"python ic_mcs_risk_report_generator.py {output_file} IC_MCS_Production_Report_131.htm icm.csv")
    
except json.JSONDecodeError as e:
    print(f"ERROR: Invalid JSON - {e}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
