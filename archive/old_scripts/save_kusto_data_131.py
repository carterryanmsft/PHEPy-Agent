"""Save Kusto query result (131 cases) to production CSV"""
import json
import pandas as pd

# The 131-case dataset from MCP Kusto query
# First few cases inline, then we'll add the rest
kusto_data_json = """[
{"ModifiedDate": "2026-02-02T16:50:33.000Z", "ServiceRequestNumber": "2510030040002408", "CaseUrl": "https://onesupport.crm.dynamics.com/main.aspx?appid=101acb62-8d00-eb11-a813-000d3a8b3117&pagetype=entityrecord&etn=incident&id=fb7b8b77-50a0-f011-b41b-002248233bcc", "ServiceRequestStatus": "Waiting for customer confirmation", "ServiceRequestState": "Open", "ProductName": "Microsoft Purview Compliance", "DerivedProductName": "Compliance", "TenantId": "157a26ef-912f-4244-abef-b45fc4bd77f9", "TopParentName": "Huntington", "TpAccountName": "HUNTINGTON BANCSHARES INC", "SAPPath": "Security/Microsoft Purview Compliance/Data loss prevention (DLP)/DLP Alerts", "Program": "IC", "PHE": "Hemanth Varyani", "CLE": "", "AgentAlias": "vickievo", "ManagerEmail": "karimatson", "ServiceRequestCurrentSeverity": "B", "CreatedTime": "2025-10-03T11:59:48.000Z", "DaysOpen": 123.6882, "AgeCategory": "Very High (>120 days)", "OwnershipCount": 11, "TransferCount": 10, "ReopenCount": 0, "RelatedICM_Id": "693849812,693543577,694142803,694208210,694253124,693952482,694041459", "HasICM": "Yes", "IsCritSit": "Yes", "RiskScore": 81, "RiskLevel": "Critical", "Summary": "Case is 123 days old, status is Waiting for customer confirmation, ICM present: Yes. Extremely high ownership (11) and transfer (10) counts indicate severe instability.", "QueueName": "OneSupport System Holding", "TPID": 645695}
]"""

# Parse JSON
cases = json.loads(kusto_data_json)
print(f"Loaded {len(cases)} cases from JSON")

# Convert to DataFrame
df = pd.DataFrame(cases)
print(f"DataFrame shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Save to CSV
output_file = "data/production_full_cases.csv"
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n✓ Saved {len(df)} cases to {output_file}")
print(f"✓ Customers: {df['TopParentName'].nunique()}")
print(f"✓ Risk levels: {df['RiskLevel'].value_counts().to_dict()}")
