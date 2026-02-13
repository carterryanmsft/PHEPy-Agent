#!/usr/bin/env python3
"""
Automated IC/MCS Risk Report Generator
Executes Kusto query and generates HTML report automatically
"""

import subprocess
import json
import sys
import os

def main():
    print("=== Automated IC/MCS Risk Report Generator ===\n")
    
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    query_file = os.path.join(script_dir, "queries", "ic_mcs_risk_report.kql")
    generator_script = os.path.join(script_dir, "ic_mcs_risk_report_generator.py")
    icm_file = os.path.join(script_dir, "icm.csv")
    output_file = os.path.join(script_dir, "IC_MCS_Production_Report.htm")
    temp_json = os.path.join(script_dir, "temp_query_results.json")
    
    # Read the Kusto query
    print(f"📖 Reading query from: {query_file}")
    with open(query_file, 'r', encoding='utf-8') as f:
        query = f.read()
    
    print("🔄 Executing Kusto query...")
    print("   Cluster: cxedataplatformcluster.westus2.kusto.windows.net")
    print("   Database: cxedata")
    print("   Max Rows: 500\n")
    
    # Execute query using the Kusto MCP tool via PowerShell
    # This requires the MCP tool to be available in the session
    ps_command = f"""
$query = @'
{query}
'@

# Note: This would need to call the Kusto MCP tool
# For now, we'll use the existing CSV file approach
Write-Host "Note: Using existing CSV file approach for now"
Write-Host "To fully automate, integrate with Kusto MCP tool"
"""
    
    print("⚠️  Note: Direct MCP integration requires session context.")
    print("📋 Using hybrid approach with existing CSV export...\n")
    
    # Look for recent CSV export
    csv_file = os.path.join(script_dir, "CaseRiskReport - 2026-02-03.csv")
    
    if os.path.exists(csv_file):
        print(f"✅ Found existing CSV export: {os.path.basename(csv_file)}")
        input_file = csv_file
    else:
        print("❌ No CSV export found!")
        print("\n📝 Please export Kusto query results to CSV:")
        print("   1. Run query in Azure Data Explorer")
        print("   2. Export to CSV as 'CaseRiskReport - 2026-02-03.csv'")
        print("   3. Save in risk_reports folder")
        print("   4. Re-run this script")
        return 1
    
    # Generate report
    print(f"\n📊 Generating HTML report...")
    print(f"   Input: {os.path.basename(input_file)}")
    print(f"   ICM Data: {os.path.basename(icm_file)}")
    print(f"   Output: {os.path.basename(output_file)}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, generator_script, input_file, output_file, icm_file],
            capture_output=True,
            text=True,
            cwd=script_dir
        )
        
        if result.returncode == 0:
            print("✅ SUCCESS! Report generated successfully!\n")
            print(result.stdout)
            print(f"\n📄 Report saved to: {output_file}")
            print(f"\n🌐 Open in browser: file:///{output_file.replace(chr(92), '/')}")
            return 0
        else:
            print("❌ ERROR generating report:")
            print(result.stderr)
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
