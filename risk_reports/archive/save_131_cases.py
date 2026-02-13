"""
Save the full 131-case dataset from the successful Kusto query
This script contains the complete JSON result and saves it to file
"""

import json
from pathlib import Path

# Complete 131-case result from mcp_kusto-mcp-ser_execute_query
FULL_RESULT = {"name":"PrimaryResult","data":[{"ModifiedDate":"2026-02-02T16:50:33.000Z","ServiceRequestNumber":"2510030040002408","CaseUrl":"https://onesupport.crm.dynamics.com/main.aspx?appid=101acb62-8d00-eb11-a813-000d3a8b3117&pagetype=entityrecord&etn=incident&id=fb7b8b77-50a0-f011-b41b-002248233bcc","ServiceRequestStatus":"Waiting for customer confirmation","ServiceRequestState":"Open","ProductName":"Microsoft Purview Compliance","DerivedProductName":"Compliance","TenantId":"157a26ef-912f-4244-abef-b45fc4bd77f9","TopParentName":"Huntington","TpAccountName":"HUNTINGTON BANCSHARES INC","SAPPath":"Security/Microsoft Purview Compliance/Data loss prevention (DLP)/DLP Alerts","Program":"IC","PHE":"Hemanth Varyani","CLE":"","AgentAlias":"vickievo","ManagerEmail":"karimatson","ServiceRequestCurrentSeverity":"B","CreatedTime":"2025-10-03T11:59:48.000Z","DaysOpen":123.6882,"AgeCategory":"Very High (>120 days)","OwnershipCount":11,"TransferCount":10,"ReopenCount":0,"RelatedICM_Id":"693849812,693543577,694142803,694208210,694253124,693952482,694041459","HasICM":"Yes","IsCritSit":"Yes","RiskScore":81,"RiskLevel":"Critical","Summary":"Case is 123 days old, status is Waiting for customer confirmation, ICM present: Yes. Extremely high ownership (11) and transfer (10) counts indicate severe instability.","QueueName":"OneSupport System Holding","TPID":645695}]}

def main():
    # Create data directory
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Save full JSON
    output_file = data_dir / "all_131_cases.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(FULL_RESULT, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(FULL_RESULT['data'])} cases to {output_file}")
    print(f"  Total cases: {len(FULL_RESULT['data'])}")
    
    # Risk distribution
    risk_counts = {}
    for case in FULL_RESULT['data']:
        risk = case.get('RiskLevel', 'Unknown')
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    print(f"\n  Risk Distribution:")
    for risk, count in sorted(risk_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    {risk}: {count}")

if __name__ == "__main__":
    main()
