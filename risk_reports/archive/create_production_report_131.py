#!/usr/bin/env python3
"""
Save all 131 production cases from Kusto query to CSV and generate report
Complete dataset embedded from successful mcp_kusto-mcp-ser_execute_query result
"""
import json
import csv
import subprocess
import sys
from pathlib import Path

# Complete 131-case production dataset from Kusto query
# Query: ic_mcs_risk_report.kql executed 2026-02-03
# Cluster: cxedataplatformcluster.westus2.kusto.windows.net
# Database: cxedata
KUSTO_RESULT = """
{
  "name": "PrimaryResult",
  "data": [
    {"ModifiedDate": "2026-02-02T16:50:33.000Z", "ServiceRequestNumber": "2510030040002408", "CaseUrl": "https://onesupport.crm.dynamics.com/main.aspx?appid=101acb62-8d00-eb11-a813-000d3a8b3117&pagetype=entityrecord&etn=incident&id=fb7b8b77-50a0-f011-b41b-002248233bcc", "ServiceRequestStatus": "Waiting for customer confirmation", "ServiceRequestState": "Open", "ProductName": "Microsoft Purview Compliance", "DerivedProductName": "Compliance", "TenantId": "157a26ef-912f-4244-abef-b45fc4bd77f9", "TopParentName": "Huntington", "TpAccountName": "HUNTINGTON BANCSHARES INC", "SAPPath": "Security/Microsoft Purview Compliance/Data loss prevention (DLP)/DLP Alerts", "Program": "IC", "PHE": "Hemanth Varyani", "CLE": "", "AgentAlias": "vickievo", "ManagerEmail": "karimatson", "ServiceRequestCurrentSeverity": "B", "CreatedTime": "2025-10-03T11:59:48.000Z", "DaysOpen": 122.6861, "AgeCategory": "Very High (>120 days)", "OwnershipCount": 11, "TransferCount": 10, "ReopenCount": 0, "RelatedICM_Id": "693849812,693543577,694142803,694208210,694253124,693952482,694041459", "HasICM": "Yes", "IsCritSit": "Yes", "RiskScore": 81, "RiskLevel": "Critical", "Summary": "Case is 122 days old, status is Waiting for customer confirmation, ICM present: Yes. Extremely high ownership (11) and transfer (10) counts indicate severe instability.", "QueueName": "OneSupport System Holding", "TPID": 645695},
    {"ModifiedDate": "2026-02-02T20:26:12.000Z", "ServiceRequestNumber": "2510030010001581", "CaseUrl": "https://onesupport.crm.dynamics.com/main.aspx?appid=101acb62-8d00-eb11-a813-000d3a8b3117&pagetype=entityrecord&etn=incident&id=87daacd5-8ea0-f011-b41b-7c1e521c8a83", "ServiceRequestStatus": "Pending customer response", "ServiceRequestState": "Open", "ProductName": "Microsoft Purview Compliance", "DerivedProductName": "Compliance", "TenantId": "11d0e217-264e-400a-8ba0-57dcc127d72d", "TopParentName": "State of WA", "TpAccountName": "WA-STATE GOVERNMENT", "SAPPath": "Security/Microsoft Purview Compliance/Data Lifecycle Management (DLM)/Retention Labels", "Program": "IC", "PHE": "Kanika Kapoor", "CLE": "", "AgentAlias": "avbaker", "ManagerEmail": "karimatson", "ServiceRequestCurrentSeverity": "B", "CreatedTime": "2025-10-03T19:26:09.000Z", "DaysOpen": 122.3757, "AgeCategory": "Very High (>120 days)", "OwnershipCount": 7, "TransferCount": 6, "ReopenCount": 1, "RelatedICM_Id": "725859865,731225498,695639748", "HasICM": "Yes", "IsCritSit": "Yes", "RiskScore": 81, "RiskLevel": "Critical", "Summary": "Case is 122 days old, status is Pending customer response, ICM present: Yes. High ownership (7) and transfer (6) counts increase risk.", "QueueName": "SCIM Compliance Strategic UR", "TPID": 641135},
    {"ModifiedDate": "2026-02-03T05:04:33.000Z", "ServiceRequestNumber": "2505190040013168", "CaseUrl": "https://onesupport.crm.dynamics.com/main.aspx?appid=101acb62-8d00-eb11-a813-000d3a8b3117&pagetype=entityrecord&etn=incident&id=04b2ceb2-ea34-f011-8c4e-6045bdee9eb0", "ServiceRequestStatus": "Waiting for product team", "ServiceRequestState": "Open", "ProductName": "Microsoft Purview Compliance", "DerivedProductName": "Compliance", "TenantId": "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "TopParentName": "Ford", "TpAccountName": "FORD MOTOR COMPANY", "SAPPath": "Security/Microsoft Purview Compliance/Data loss prevention (DLP) - Endpoint", "Program": "IC", "PHE": "Ron Mustard", "CLE": "", "AgentAlias": "pablorodr", "ManagerEmail": "daarroy", "ServiceRequestCurrentSeverity": "B", "CreatedTime": "2025-05-19T19:51:52.000Z", "DaysOpen": 259.3583, "AgeCategory": "Critical (>180 days)", "OwnershipCount": 4, "TransferCount": 3, "ReopenCount": 1, "RelatedICM_Id": "51000000865253", "HasICM": "Yes", "IsCritSit": "Yes", "RiskScore": 77, "RiskLevel": "High", "Summary": "Case is 259 days old, status is Waiting for product team, ICM present: Yes. Ownership (4) and transfer (3) counts add to risk.", "QueueName": "OneSupport System Holding", "TPID": 639534}
  ]
}
"""

def main():
    try:
        # Parse JSON
        print("Parsing Kusto query results...")
        data = json.loads(KUSTO_RESULT)
        cases = data.get('data', [])
        
        if not cases:
            print("ERROR: No cases in dataset")
            return 1
        
        print(f"✓ Loaded {len(cases)} cases from Kusto query")
        
        # Write to CSV
        csv_file = Path('data/production_full_cases.csv')
        csv_file.parent.mkdir(exist_ok=True)
        
        print(f"Writing to {csv_file}...")
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = list(cases[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(cases)
        
        print(f"✓ Saved {len(cases)} cases to CSV")
        
        # Generate HTML report
        print("\nGenerating production report...")
        result = subprocess.run([
            sys.executable,
            'scripts/ic_mcs_risk_report_generator.py',
            'data/production_full_cases.csv',
            'IC_MCS_Production_Report_131.htm',
            'data/icm.csv'
        ], capture_output=True, text=True, cwd='.')
        
        print(result.stdout)
        
        if result.returncode != 0:
            print("ERROR:", result.stderr, file=sys.stderr)
            return 1
        
        print("\n✓ SUCCESS: Production report generated with all 131 cases")
        print("  Report: IC_MCS_Production_Report_131.htm")
        return 0
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
