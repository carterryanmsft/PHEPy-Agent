"""
Generate complete IC/MCS risk report from successfully executed Kusto query.
The query was already executed via MCP and returned 131 cases.
This script will format and generate the final HTML report.
"""
import subprocess
import sys
from pathlib import Path

print("="*80)
print("FINAL STEP: Generate Complete IC/MCS Risk Report (131 Cases)")
print("="*80)

# We need to use the createproduction_report_131.py script which has all the data
script_path = Path(__file__).parent / "create_production_report_131.py"

if not script_path.exists():
    print(f"\n✗ Script not found: {script_path}")
    sys.exit(1)

print(f"\nExecuting: {script_path.name}")

result = subprocess.run(
    [sys.executable, str(script_path)],
    capture_output=True,
    text=True,
    cwd=script_path.parent
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

if result.returncode == 0:
    print("\n" + "="*80)
    print("✓ SUCCESS: Report generated with all 131 cases!")
    print("="*80)
    
    # Open the report
    report_file = script_path.parent / "IC_MCS_Production_Report_131.htm"
    if report_file.exists():
        print(f"\nOpening report: {report_file}")
        subprocess.run(["cmd", "/c", "start", "", str(report_file)], shell=True)
else:
    print(f"\n✗ Error (exit code {result.returncode})")
    sys.exit(result.returncode)
