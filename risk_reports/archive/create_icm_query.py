# Read ICM IDs and create Kusto query
with open('data/icm_ids_to_query.txt', 'r') as f:
    icm_ids = [line.strip() for line in f if line.strip()]

print(f'Creating Kusto query for {len(icm_ids)} ICMs...')

# Format for Kusto IN clause
formatted_ids = []
for icm_id in icm_ids:
    if icm_id.isdigit():
        formatted_ids.append(icm_id)
    else:
        formatted_ids.append(f'"{icm_id}"')

ids_str = ', '.join(formatted_ids)

query = f"""IcMDataWarehouse_Snapshot
| where IncidentId in ({ids_str})
| project IncidentId, Severity, Status, OwningContactAlias, Title, CreateDate, ModifiedDate
| order by IncidentId asc"""

# Save query
with open('queries/icm_data_query.kql', 'w') as f:
    f.write(query)

print(f'✓ Saved query to queries/icm_data_query.kql')
print(f'  Query will fetch data for {len(icm_ids)} ICMs')
print(f'\nQuery preview (first 200 chars):')
print(query[:200] + '...')
