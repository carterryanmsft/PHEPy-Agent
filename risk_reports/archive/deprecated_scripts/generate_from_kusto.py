#!/usr/bin/env python3
"""
Generate IC/MCS Risk Report directly from Kusto JSON result
"""
import json
import sys
import subprocess
import os

def main():
    # Read the Kusto JSON result (passed as argument or from file)
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        with open(json_file, 'r', encoding='utf-8') as f:
            kusto_result = json.load(f)
    else:
        print("Usage: python generate_from_kusto.py <kusto_json_file>")
        sys.exit(1)
    
    # Extract the data array from Kusto result
    cases = kusto_result.get('data', [])
    
    print(f"Processing {len(cases)} cases from Kusto query...")
    
    # Convert to CSV format expected by the report generator
    csv_file = "production_cases_131.csv"
    
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        # Write header - all field names from the query
        fields = list(cases[0].keys()) if cases else []
        f.write(','.join([f'"{field}"' for field in fields]) + '\n')
        
        # Write data rows
        for case in cases:
            row = []
            for field in fields:
                value = case.get(field, '')
                # Handle None values
                if value is None:
                    value = ''
                # Convert to string and escape quotes
                value_str = str(value).replace('"', '""')
                row.append(f'"{value_str}"')
            f.write(','.join(row) + '\n')
    
    print(f"Created CSV with {len(cases)} cases: {csv_file}")
    
    # Now run the report generator
    report_file = "../IC_MCS_Production_Report_131.htm"
    icm_file = "../icm.csv"
    
    print(f"\nGenerating report: {report_file}")
    
    # Change to parent directory and run generator
    os.chdir('..')
    result = subprocess.run([
        sys.executable,
        "ic_mcs_risk_report_generator.py",
        f"data/{csv_file}",
        report_file,
        "icm.csv"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)
    
    if result.returncode == 0:
        print(f"\n✓ SUCCESS: Report generated with all {len(cases)} cases!")
    else:
        print(f"\n✗ ERROR: Report generation failed with return code {result.returncode}")
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
