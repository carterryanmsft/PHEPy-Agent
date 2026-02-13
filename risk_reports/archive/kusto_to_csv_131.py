#!/usr/bin/env python3
"""
Write Kusto query JSON result directly to CSV (all 131 cases)
Then call report generator
"""
import json
import csv
import subprocess
from pathlib import Path

# Read the Kusto JSON result from the query I just executed
KUSTO_JSON = """INSERT_JSON_HERE"""

def main():
    # Parse the result
    result = json.loads(KUSTO_JSON)
    cases = result['data']
    
    print(f"✓ Loaded {len(cases)} cases from Kusto")
    
    # Write to CSV
    csv_path = Path("data/production_full_cases.csv")
    csv_path.parent.mkdir(exist_ok=True)
    
    # Get field names from first case
    fieldnames = list(cases[0].keys())
    
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cases)
    
    print(f"✓ Saved {len(cases)} cases to {csv_path}")
    
    # Generate report
    print("\nGenerating report...")
    result = subprocess.run([
        "python",
        "scripts/ic_mcs_risk_report_generator.py",
        str(csv_path),
        "IC_MCS_Production_Report_131.htm"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ SUCCESS: Report generated")
        print(result.stdout)
    else:
        print(f"✗ ERROR: Report generation failed")
        print(result.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
