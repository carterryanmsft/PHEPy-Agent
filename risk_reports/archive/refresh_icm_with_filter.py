"""
Refresh ICM data with OwningService filter to exclude SCIM Escalation Management
Executes Kusto query against ICM cluster and updates local CSV
"""

import pandas as pd
import json
import sys
sys.path.append('..')

# Read case data to get all ICM IDs
cases = pd.read_csv('../data/production_full_cases.csv')
all_icm_ids = set()

for icm_ids_str in cases['RelatedICM_Id'].dropna():
    icm_ids_str = str(icm_ids_str).replace(',', ';')
    for icm_id in icm_ids_str.split(';'):
        if icm_id.strip():
            try:
                all_icm_ids.add(int(icm_id.strip()))
            except:
                pass

icm_list = sorted(list(all_icm_ids))
print(f"Found {len(icm_list)} unique ICMs in cases")

# Format as Kusto query
icm_ids_formatted = ', '.join(str(id) for id in icm_list)

query = f"""cluster('icmcluster').database('IcmDataWarehouse').Incidents
| where IncidentId in ({icm_ids_formatted})
| summarize arg_max(ModifiedDate, *) by IncidentId
| where OwningService !contains "SCIM Escalation Management"
| project IncidentId, Severity, OwningContactAlias, Status
| order by IncidentId asc"""

print("\n" + "="*80)
print("KUSTO QUERY TO EXECUTE:")
print("="*80)
print(query)
print("="*80)
print("\nCopy this query and execute in Kusto Explorer or use the mcp_kusto tool")
print("Cluster: icmcluster")
print("Database: IcmDataWarehouse")
