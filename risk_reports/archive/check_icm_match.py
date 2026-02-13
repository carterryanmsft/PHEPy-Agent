import pandas as pd

# Load case data
df_cases = pd.read_csv('../data/production_full_cases.csv')
# Load ICM data
df_icm = pd.read_csv('data/icm.csv')

print('Checking ICM data match...')
print(f'Cases with ICMs: {len(df_cases[df_cases["HasICM"] == "Yes"])}')
print(f'ICM data available: {len(df_icm)}')

# Check if any case ICMs match our ICM data
icm_ids_in_data = set(df_icm['IncidentId'].astype(str))
print(f'\nICM IDs in icm.csv: {len(icm_ids_in_data)} total')
print(f'Sample: {sorted(list(icm_ids_in_data))[:5]}')

# Find cases that have ICMs in our data
cases_with_data = []
for idx, row in df_cases.iterrows():
    icm_field = row['RelatedICM_Id']
    if pd.notna(icm_field):
        icms = [icm.strip() for icm in str(icm_field).replace(';', ',').split(',')]
        for icm in icms:
            if icm in icm_ids_in_data:
                cases_with_data.append({
                    'Case': row['ServiceRequestNumber'],
                    'Customer': row['TopParentName'],
                    'ICM': icm,
                    'All_ICMs': icm_field
                })
                break

print(f'\nCases that SHOULD show ICM owner/status: {len(cases_with_data)}')
if cases_with_data:
    print('\nThese cases have ICM data:')
    for item in cases_with_data[:10]:
        icm_info = df_icm[df_icm['IncidentId'] == int(item['ICM'])].iloc[0]
        print(f"  {item['Case']} ({item['Customer']}): ICM {item['ICM']}")
        print(f"    Owner: {icm_info['IcmOwner']}, Status: {icm_info['IcmStatus']}")
