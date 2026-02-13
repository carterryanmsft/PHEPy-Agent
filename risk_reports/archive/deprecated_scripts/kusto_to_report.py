"""
One-command Kusto to Report Generator
Accepts Kusto JSON via stdin and generates the full HTML report
"""
import sys
import json
import csv
import subprocess
from pathlib import Path

def main():
    # Read JSON from stdin
    print("Reading Kusto query result from stdin...", file=sys.stderr)
    input_data = sys.stdin.read()
    
    if not input_data.strip():
        print("ERROR: No data received on stdin", file=sys.stderr)
        sys.exit(1)
    
    # Parse JSON
    try:
        data = json.loads(input_data)
        cases = data.get('data', data) if isinstance(data, dict) else data
        print(f"✓ Parsed {len(cases)} cases from JSON", file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Write to CSV
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    csv_path = data_dir / "production_cases_full.csv"
    
    if not cases:
        print("ERROR: No cases found in data", file=sys.stderr)
        sys.exit(1)
    
    fieldnames = list(cases[0].keys())
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(cases)
    
    print(f"✓ Wrote {len(cases)} cases to {csv_path}", file=sys.stderr)
    
    # Generate report
    report_path = script_dir.parent.parent / "IC_MCS_Production_Report_131.htm"
    icm_path = data_dir / "icm.csv"
    generator_path = script_dir / "ic_mcs_risk_report_generator.py"
    
    print(f"✓ Generating HTML report...", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, str(generator_path), str(csv_path), str(report_path), str(icm_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✓ SUCCESS: Report generated at {report_path}", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        return 0
    else:
        print(f"ERROR: Report generation failed", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
