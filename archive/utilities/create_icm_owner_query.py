"""
Extract ICM ownership data for IC cases
"""
import pandas as pd
import json

# Read the IC cases
df = pd.read_csv('risk_reports/data/ic_cases.csv')

# Get all unique ICM IDs
icm_ids = []
for icm_str in df['RelatedICM_Id'].dropna():
    if str(icm_str).strip() and str(icm_str) != '':
        # Split by comma and clean
        ids = [x.strip() for x in str(icm_str).split(',') if x.strip()]
        icm_ids.extend(ids)

icm_ids = list(set(icm_ids))
print(f'Found {len(icm_ids)} unique ICM IDs')
print(f'\nSample ICM IDs: {icm_ids[:10]}')

# Create Kusto query to get ICM ownership
query = f"""
let ICMIds = datatable(IncidentId:long)
[
"""

# Add ICM IDs
for icm_id in sorted(icm_ids):
    try:
        query += f"    {int(icm_id)},\n"
    except ValueError:
        print(f'Skipping invalid ICM ID: {icm_id}')

query += """];
cluster('icmcluster').database('IcmDataWarehouse').Incidents
| where IncidentId in (ICMIds)
| summarize arg_max(ModifiedDate, *) by IncidentId
| join kind=leftouter (
    cluster('icmcluster').database('IcmDataWarehouse').IncidentBugs
    | where IncidentId in (ICMIds)
    | where IsTombstoned == false
    | summarize 
        BugIds = strcat_array(make_set(BugId), ','),
        BugExternalIds = strcat_array(make_set(ExternalId), ','),
        BugDescriptions = strcat_array(make_set(Description), '; '),
        BugStatuses = strcat_array(make_set(Status), ',')
    by IncidentId
) on IncidentId
| project 
    IncidentId,
    IcmOwner = OwningContactAlias,
    IcmStatus = Status,
    IcmSeverity = Severity,
    OwningTenantName,
    OwningTeamName,
    Title,
    ModifiedDate,
    BugIds,
    BugExternalIds,
    BugDescriptions,
    BugStatuses
| order by IncidentId asc
"""

# Save query to file
with open('risk_reports/queries/get_icm_owners.kql', 'w', encoding='utf-8') as f:
    f.write(query)

print(f'\n✅ Query saved to: risk_reports/queries/get_icm_owners.kql')
print(f'Run this query using the Kusto MCP server to get ICM ownership data')
