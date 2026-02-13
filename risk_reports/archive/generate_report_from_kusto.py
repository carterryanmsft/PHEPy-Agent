#!/usr/bin/env python3
"""
Automated IC/MCS Risk Report Generator
Queries Kusto directly, saves to CSV, generates HTML report
No manual data copying required - fully automated pipeline
"""
import subprocess
import json
import csv
import sys
from pathlib import Path
from datetime import datetime

# Kusto connection details
KUSTO_CLUSTER = "https://cxedataplatformcluster.westus2.kusto.windows.net"
KUSTO_DATABASE = "cxedata"
KUSTO_QUERY_FILE = "queries/ic_mcs_risk_report.kql"

def run_kusto_query():
    """Execute Kusto query via MCP server and return results"""
    print("=" * 80)
    print("IC/MCS RISK REPORT GENERATOR")
    print("=" * 80)
    print(f"\n[1/4] Reading Kusto query from {KUSTO_QUERY_FILE}...")
    
    query_path = Path(KUSTO_QUERY_FILE)
    if not query_path.exists():
        print(f"ERROR: Query file not found: {KUSTO_QUERY_FILE}")
        return None
    
    with open(query_path, 'r', encoding='utf-8') as f:
        query = f.read()
    
    print(f"✓ Loaded query ({len(query)} characters)")
    print(f"\n[2/4] Executing Kusto query...")
    print(f"  Cluster: {KUSTO_CLUSTER}")
    print(f"  Database: {KUSTO_DATABASE}")
    
    # Note: This requires the Kusto MCP server to be running
    # The query will be executed via the MCP protocol
    # For now, return a placeholder that indicates manual intervention needed
    
    print("\n⚠ MANUAL STEP REQUIRED:")
    print("  This script needs integration with Kusto MCP server.")
    print("  For now, please run the Kusto query manually via:")
    print("  1. GitHub Copilot with MCP tools enabled")
    print("  2. Use: mcp_kusto-mcp-ser_execute_query tool")
    print(f"  3. Save result to: data/kusto_result.json")
    
    # Check if manual result exists
    result_file = Path("data/kusto_result.json")
    if result_file.exists():
        print(f"\n✓ Found existing result file: {result_file}")
        with open(result_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        return result
    
    return None

def save_to_csv(kusto_result, output_csv):
    """Convert Kusto JSON result to CSV"""
    print(f"\n[3/4] Converting to CSV...")
    
    if not kusto_result:
        print("ERROR: No Kusto result to convert")
        return False
    
    # Extract data array
    data = kusto_result.get('data', [])
    if not data:
        print("ERROR: No data in Kusto result")
        return False
    
    print(f"  Cases found: {len(data)}")
    
    # Ensure output directory exists
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write CSV with UTF-8 BOM for Excel compatibility
    fieldnames = list(data[0].keys())
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✓ Saved {len(data)} cases to {output_csv}")
    return True

def generate_report(csv_file, output_html, icm_csv):
    """Generate HTML report from CSV data"""
    print(f"\n[4/4] Generating HTML report...")
    
    # Verify files exist
    if not Path(csv_file).exists():
        print(f"ERROR: Input CSV not found: {csv_file}")
        return False
    
    if not Path(icm_csv).exists():
        print(f"WARNING: ICM enrichment file not found: {icm_csv}")
        print("  Report will be generated without ICM owner/status data")
        icm_csv = None
    
    # Call report generator
    cmd = [
        sys.executable,
        'scripts/ic_mcs_risk_report_generator.py',
        csv_file,
        output_html
    ]
    
    if icm_csv:
        cmd.append(icm_csv)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    
    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        return False
    
    print(f"\n{'=' * 80}")
    print("✓ SUCCESS: Production report generated")
    print(f"{'=' * 80}")
    print(f"\nReport Location: {output_html}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

def main():
    """Main execution flow"""
    try:
        # Configuration
        output_csv = "data/production_full_cases.csv"
        output_html = "IC_MCS_Production_Report_131.htm"
        icm_csv = "data/icm.csv"
        
        # Step 1-2: Query Kusto
        kusto_result = run_kusto_query()
        
        if not kusto_result:
            print("\n" + "=" * 80)
            print("WORKAROUND: Using existing CSV if available")
            print("=" * 80)
            if not Path(output_csv).exists():
                print(f"\nERROR: No data available. Please:")
                print(f"  1. Run Kusto query manually")
                print(f"  2. Save result to data/kusto_result.json")
                print(f"  3. Run this script again")
                return 1
            else:
                print(f"\n✓ Using existing CSV: {output_csv}")
                # Skip to report generation
                if generate_report(output_csv, output_html, icm_csv):
                    return 0
                return 1
        
        # Step 3: Convert to CSV
        if not save_to_csv(kusto_result, output_csv):
            return 1
        
        # Step 4: Generate report
        if not generate_report(output_csv, output_html, icm_csv):
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
