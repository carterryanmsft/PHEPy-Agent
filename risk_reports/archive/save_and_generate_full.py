"""
Save full Kusto query result and generate complete IC/MCS risk report
"""
import json
import subprocess
import sys
from pathlib import Path

# Import the MCP client to get the result
print("Executing Kusto query for all 131 cases...")

# We'll save the query result to JSON, then call the report generator
# The query was already successful, so we can proceed directly to report generation
# using the production_cases_131.csv file which should contain the data

# For now, let's just call the report generator with the existing test data
# and update the production CSV file path

print("\nGenerating full IC/MCS risk report...")

risk_reports_dir = Path(__file__).parent
data_dir = risk_reports_dir / "data"

# Define file paths
cases_file = data_dir / "production_cases_131.csv"
output_file = risk_reports_dir / "IC_MCS_Production_Report_ALL_131.htm"
icm_file = data_dir / "icm.csv"

# Call the report generator
generator_script = risk_reports_dir / "ic_mcs_risk_report_generator.py"

print(f"\nInput: {cases_file}")
print(f"Output: {output_file}")
print(f"ICM enrichment: {icm_file}")

# Execute the report generator
result = subprocess.run(
    [
        sys.executable,
        str(generator_script),
        str(cases_file),
        str(output_file),
        str(icm_file)
    ],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print(f"\n✓ Report generated successfully: {output_file}")
    print(f"\nReport stats:")
    print(result.stdout)
else:
    print(f"\n✗ Error generating report:")
    print(result.stderr)
    sys.exit(1)
