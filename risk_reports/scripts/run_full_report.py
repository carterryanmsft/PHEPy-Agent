"""
Automated IC/MCS Risk Report Generation
Executes full production query via Kusto MCP and generates HTML report
"""
import json
import subprocess
import sys

# The Kusto query JSON results from MCP tool are passed in via stdin
# This script processes the JSON and calls the report generator

print("🚀 IC/MCS Risk Report - Full Automation")
print("=" * 60)

# Read JSON data from stdin (passed from query execution)
print("\n📥 Reading query results...")
input_data = sys.stdin.read()

try:
    data = json.loads(input_data)
    
    # Extract the cases from the MCP query result
    if 'data' in data:
        cases = data['data']
    else:
        cases = data
    
    case_count = len(cases)
    print(f"✅ Loaded {case_count} cases from query")
    
    # Save to temporary JSON file
    temp_file = "production_cases_131.json"
    with open(temp_file, 'w') as f:
        json.dump(cases, f, indent=2)
    print(f"💾 Saved cases to {temp_file}")
    
    # Generate report using the existing report generator
    print("\n📊 Generating HTML report...")
    result = subprocess.run([
        sys.executable,
        "ic_mcs_risk_report_generator.py",
        temp_file,
        "IC_MCS_Production_Report.htm",
        "icm.csv"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"\n✅ SUCCESS! Report generated:")
        print(result.stdout)
        print("\n" + "=" * 60)
        print("📄 Report: IC_MCS_Production_Report.htm")
        print("=" * 60)
    else:
        print(f"\n❌ Error generating report:")
        print(result.stderr)
        sys.exit(1)
        
except json.JSONDecodeError as e:
    print(f"❌ Error parsing JSON: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
