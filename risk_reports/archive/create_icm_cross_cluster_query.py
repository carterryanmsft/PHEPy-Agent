import sys

# Read ICM IDs
with open('data/icm_ids_to_query.txt', 'r') as f:
    icm_ids = [line.strip() for line in f if line.strip()]

print(f'Creating ICM query for {len(icm_ids)} ICMs using cross-cluster syntax...')

# Format for Kusto IN clause - all as integers
icm_ids_str = ', '.join(icm_ids)

# Create the cross-cluster query
query = f"""cluster('icmcluster').database('IcmDataWarehouse').Incident
| where IncidentId in ({icm_ids_str})
| project IncidentId, Severity, OwningContactAlias, Status
| order by IncidentId asc
"""

print(query)
print(f'\nQuery ready for {len(icm_ids)} ICMs')
