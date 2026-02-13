#!/usr/bin/env python3
"""
Direct Kusto Connection - IC/MCS Risk Report Generator
Uses Azure Kusto SDK to query directly (no MCP dependency)
Requires: pip install azure-kusto-data azure-identity
"""
import csv
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def query_kusto_direct():
    """Query Kusto directly using Azure SDK"""
    print("=" * 80)
    print("IC/MCS RISK REPORT - DIRECT KUSTO CONNECTION")
    print("=" * 80)
    
    try:
        from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
        from azure.identity import DefaultAzureCredential
    except ImportError:
        print("\n✗ ERROR: Azure Kusto SDK not installed")
        print("\nPlease install required packages:")
        print("  pip install azure-kusto-data azure-identity")
        return None
    
    # Configuration
    cluster_url = "https://cxedataplatformcluster.westus2.kusto.windows.net"
    database = "cxedata"
    query_file = "queries/ic_mcs_risk_report.kql"
    
    print(f"\n[1/4] Reading query from {query_file}...")
    query_path = Path(query_file)
    if not query_path.exists():
        print(f"ERROR: Query file not found: {query_file}")
        return None
    
    with open(query_path, 'r', encoding='utf-8') as f:
        query = f.read()
    
    print(f"✓ Loaded query ({len(query)} characters)")
    
    print(f"\n[2/4] Connecting to Kusto...")
    print(f"  Cluster: {cluster_url}")
    print(f"  Database: {database}")
    print(f"  Auth: Azure Default Credentials")
    
    try:
        # Build connection string with Azure CLI authentication
        kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster_url)
        client = KustoClient(kcsb)
        
        print("✓ Connected successfully")
        print("\n[3/4] Executing query...")
        
        # Execute query
        response = client.execute(database, query)
        
        # Convert to list of dicts
        results = []
        primary_table = response.primary_results[0]
        
        for row in primary_table:
            row_dict = {}
            for col_idx, col in enumerate(primary_table.columns):
                row_dict[col.column_name] = row[col_idx]
            results.append(row_dict)
        
        print(f"✓ Query completed: {len(results)} cases retrieved")
        
        return {
            'name': 'PrimaryResult',
            'data': results
        }
        
    except Exception as e:
        print(f"\n✗ ERROR: Failed to query Kusto")
        print(f"  {type(e).__name__}: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure you're logged in: az login")
        print("  2. Verify cluster access permissions")
        print("  3. Check network connectivity")
        return None

def save_to_csv(kusto_result, output_csv):
    """Convert Kusto result to CSV"""
    if not kusto_result or 'data' not in kusto_result:
        return False
    
    data = kusto_result['data']
    if not data:
        print("ERROR: No data to save")
        return False
    
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = list(data[0].keys())
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\n✓ Saved {len(data)} cases to {output_csv}")
    return True

def generate_report(csv_file, output_html, icm_csv):
    """Generate HTML report"""
    print(f"\n[4/4] Generating HTML report...")
    
    if not Path(csv_file).exists():
        print(f"ERROR: CSV not found: {csv_file}")
        return False
    
    cmd = [sys.executable, 'scripts/ic_mcs_risk_report_generator.py', csv_file, output_html]
    if Path(icm_csv).exists():
        cmd.append(icm_csv)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print("ERROR:", result.stderr, file=sys.stderr)
        return False
    
    print(f"\n{'=' * 80}")
    print("✓ SUCCESS: Report generated")
    print(f"{'=' * 80}")
    print(f"\nReport: {output_html}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

def main():
    # Configuration
    output_csv = "data/production_full_cases.csv"
    output_html = "IC_MCS_Production_Report_131.htm"
    icm_csv = "data/icm.csv"
    
    try:
        # Query Kusto
        result = query_kusto_direct()
        if not result:
            return 1
        
        # Save to CSV
        if not save_to_csv(result, output_csv):
            return 1
        
        # Generate report
        if not generate_report(output_csv, output_html, icm_csv):
            return 1
        
        return 0
        
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
