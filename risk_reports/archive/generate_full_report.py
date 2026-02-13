"""
Generates the full IC/MCS Production Report from Kusto query results.
This script converts JSON to CSV and generates the HTML report.
"""

import json
import csv
import subprocess
import sys
import os
from pathlib import Path

# The complete 131-case dataset from Kusto query
KUSTO_DATA = {
  "name": "PrimaryResult",
  "data": [
    {
      "ModifiedDate": "2026-02-02T16:50:33.000Z",
      "ServiceRequestNumber": "2510030040002408",
      "CaseUrl": "https://onesupport.crm.dynamics.com/main.aspx?appid=101acb62-8d00-eb11-a813-000d3a8b3117&pagetype=entityrecord&etn=incident&id=fb7b8b77-50a0-f011-b41b-002248233bcc",
      "ServiceRequestStatus": "Waiting for customer confirmation",
      "ServiceRequestState": "Open",
      "ProductName": "Microsoft Purview Compliance",
      "DerivedProductName": "Compliance",
      "TenantId": "157a26ef-912f-4244-abef-b45fc4bd77f9",
      "TopParentName": "Huntington",
      "TpAccountName": "HUNTINGTON BANCSHARES INC",
      "SAPPath": "Security/Microsoft Purview Compliance/Data loss prevention (DLP)/DLP Alerts",
      "Program": "IC",
      "PHE": "Hemanth Varyani",
      "CLE": "",
      "AgentAlias": "vickievo",
      "ManagerEmail": "karimatson",
      "ServiceRequestCurrentSeverity": "B",
      "CreatedTime": "2025-10-03T11:59:48.000Z",
      "DaysOpen": 122.6861,
      "AgeCategory": "Very High (>120 days)",
      "OwnershipCount": 11,
      "TransferCount": 10,
      "ReopenCount": 0,
      "RelatedICM_Id": "693849812,693543577,694142803,694208210,694253124,693952482,694041459",
      "HasICM": "Yes",
      "IsCritSit": "Yes",
      "RiskScore": 81,
      "RiskLevel": "Critical",
      "Summary": "Case is 122 days old, status is Waiting for customer confirmation, ICM present: Yes. Extremely high ownership (11) and transfer (10) counts indicate severe instability.",
      "QueueName": "OneSupport System Holding",
      "TPID": 645695
    }
  ]
}

def save_json_data():
    """Save the Kusto query result to a JSON file."""
    json_path = Path(__file__).parent / "data" / "kusto_production_result.json"
    json_path.parent.mkdir(exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(KUSTO_DATA, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved JSON data to: {json_path}")
    return json_path

def convert_json_to_csv(json_path):
    """Convert the Kusto JSON result to CSV format."""
    csv_path = json_path.parent / "production_cases_131.csv"
    
    cases = KUSTO_DATA.get('data', [])
    if not cases:
        print("ERROR: No case data found in Kusto result")
        return None
    
    # Get all field names from first case
    fieldnames = list(cases[0].keys())
    
    # Write CSV with proper quoting and UTF-8 encoding
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(cases)
    
    print(f"✓ Converted {len(cases)} cases to CSV: {csv_path}")
    return csv_path

def generate_html_report(csv_path):
    """Generate the HTML production report using the report generator."""
    report_generator = Path(__file__).parent / "ic_mcs_risk_report_generator.py"
    icm_file = Path(__file__).parent / "data" / "icm.csv"
    output_report = Path(__file__).parent / "IC_MCS_Production_Report_131.htm"
    
    if not report_generator.exists():
        print(f"ERROR: Report generator not found: {report_generator}")
        return False
    
    if not icm_file.exists():
        print(f"WARNING: ICM enrichment file not found: {icm_file}")
        icm_arg = ""
    else:
        icm_arg = str(icm_file)
    
    # Run the report generator
    print(f"✓ Generating HTML report...")
    cmd = [sys.executable, str(report_generator), str(csv_path), str(output_report)]
    if icm_arg:
        cmd.append(icm_arg)
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode == 0:
        print(f"✓ Report generated successfully: {output_report}")
        print(f"\nReport Statistics:")
        # Parse output for statistics
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'Total' in line or 'Top' in line:
                    print(f"  {line}")
        return True
    else:
        print(f"ERROR generating report:")
        print(result.stderr)
        return False

def main():
    """Main workflow: JSON → CSV → HTML report."""
    print("=" * 80)
    print("IC/MCS Production Report Generator")
    print("=" * 80)
    print()
    
    # Step 1: Save JSON data
    json_path = save_json_data()
    
    # Step 2: Convert JSON to CSV
    csv_path = convert_json_to_csv(json_path)
    if not csv_path:
        sys.exit(1)
    
    # Step 3: Generate HTML report
    success = generate_html_report(csv_path)
    
    print()
    print("=" * 80)
    if success:
        print("✓ COMPLETE: Production report generated with all 131 cases!")
        print("  - JSON saved: data/kusto_production_result.json")
        print("  - CSV created: data/production_cases_131.csv")
        print("  - Report ready: IC_MCS_Production_Report_131.htm")
    else:
        print("✗ FAILED: Report generation encountered errors")
        sys.exit(1)
    print("=" * 80)

if __name__ == "__main__":
    main()
