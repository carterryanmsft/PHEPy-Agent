#!/usr/bin/env python3
"""
Automated IC/MCS Risk Report Generator
Executes Kusto query, converts to CSV, and generates HTML report
"""

import pandas as pd
import subprocess
import json
import sys
import os

def run_kusto_query():
    """Run the Kusto query using the MCP tool and return results."""
    print("📊 Executing Kusto query...")
    
    # Since we can't directly call the MCP tool from Python,
    # we'll use the query results that were already fetched
    # This script expects query_results.json to exist
    
    if os.path.exists('query_results.json'):
        with open('query_results.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Loaded {len(data.get('data', []))} cases from cache")
        return data
    else:
        print("❌ query_results.json not found")
        print("Please run the Kusto query first and save results as query_results.json")
        return None

def convert_to_csv(data, output_file='production_cases.csv'):
    """Convert JSON query results to CSV."""
    print(f"📝 Converting to CSV: {output_file}")
    
    rows = data.get('data', [])
    if not rows:
        print("❌ No data to convert")
        return False
    
    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✓ Created {output_file} with {len(df)} cases")
    return True

def generate_html_report(csv_file, icm_file='icm.csv', output_html='IC_MCS_Production_Report.htm'):
    """Generate the HTML report."""
    print(f"🎨 Generating HTML report: {output_html}")
    
    cmd = [
        'python',
        'ic_mcs_risk_report_generator.py',
        csv_file,
        output_html,
        icm_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Report generated: {output_html}")
        print(result.stdout)
        return True
    else:
        print(f"❌ Error generating report:")
        print(result.stderr)
        return False

def main():
    print("\n" + "="*60)
    print("  IC/MCS Automated Production Report Generator")
    print("="*60 + "\n")
    
    # Step 1: Get query results
    data = run_kusto_query()
    if not data:
        print("\n❌ Failed to get query data")
        print("\nTo fix this, save the Kusto query results as 'query_results.json'")
        return 1
    
    # Step 2: Convert to CSV
    if not convert_to_csv(data):
        return 1
    
    # Step 3: Generate HTML report
    if not generate_html_report('production_cases.csv'):
        return 1
    
    print("\n" + "="*60)
    print("✓ Production report generated successfully!")
    print("="*60)
    print("\nReport: IC_MCS_Production_Report.htm")
    print(f"Cases: {len(data.get('data', []))}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
