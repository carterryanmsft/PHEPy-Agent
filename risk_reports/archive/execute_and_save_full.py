"""
Execute full IC/MCS Kusto query and save to JSON
Then generate complete risk report
"""
import json
import subprocess
import sys
from pathlib import Path

print("This script needs the MCP Kusto query result.")
print("Please run the following Kusto query and save the result:")
print("\nCluster: https://cxedataplatformcluster.westus2.kusto.windows.net")
print("Database: cxedata")
print("Max rows: 200")
print("\nQuery is in: risk_reports/queries/ic_mcs_risk_report.kql")
print("\nThe query result should be saved to: risk_reports/data/all_131_cases.json")
print("\nAfter saving the JSON, run this script again to generate the HTML report.")

# Check if JSON file exists
risk_reports_dir = Path(__file__).parent
data_dir = risk_reports_dir / "data"
json_file = data_dir / "all_131_cases.json"

if not json_file.exists():
    print(f"\n✗ JSON file not found: {json_file}")
    print("Please save the Kusto query result first.")
    sys.exit(1)

print(f"\n✓ Found JSON file: {json_file}")

# Convert JSON to CSV
print("\nConverting JSON to CSV...")
convert_script = risk_reports_dir.parent / "convert_mcp_to_csv.py"
csv_output = data_dir / "production_full_131.csv"

result = subprocess.run(
    [sys.executable, str(convert_script), str(json_file), str(csv_output)],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"✗ Error converting to CSV:")
    print(result.stderr)
    sys.exit(1)

print(f"✓ CSV created: {csv_output}")

# Generate HTML report
print("\nGenerating HTML report...")
generator_script = risk_reports_dir / "ic_mcs_risk_report_generator.py"
html_output = risk_reports_dir / "IC_MCS_Production_Report_ALL_131.htm"
icm_file = data_dir / "icm.csv"

result = subprocess.run(
    [
        sys.executable,
        str(generator_script),
        str(csv_output),
        str(html_output),
        str(icm_file)
    ],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print(f"\n✓ Report generated: {html_output}")
    print(result.stdout)
else:
    print(f"✗ Error generating report:")
    print(result.stderr)
    sys.exit(1)

print("\n✓ Complete! Opening report...")
subprocess.run(["cmd", "/c", "start", str(html_output)], shell=True)
