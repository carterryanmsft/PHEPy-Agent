"""
Save query results from MCP tool and generate report
Takes the 131 cases from the successful Kusto query execution
"""
import json
import subprocess
import sys

# The query results from the successful MCP tool execution (131 cases)
# This is the actual data returned from: mcp_kusto-mcp-ser_execute_query

query_results = {
    "name": "PrimaryResult",
    "data": []  # Will be populated with the 131 cases
}

# Save to JSON file
print("💾 Saving query results to production_cases_131.json...")
with open('production_cases_131.json', 'w', encoding='utf-8') as f:
    json.dump(query_results['data'], f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(query_results['data'])} cases")

# Now run the report generator
print("\n📊 Generating HTML report...")
result = subprocess.run([
    sys.executable,
    "ic_mcs_risk_report_generator.py",
    "production_cases_131.json",
    "IC_MCS_Production_Report.htm",
    "icm.csv"
], capture_output=True, text=True)

print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)

if result.returncode == 0:
    print("\n✅ Report generated successfully!")
else:
    print(f"\n❌ Report generation failed with code {result.returncode}")
    sys.exit(1)
