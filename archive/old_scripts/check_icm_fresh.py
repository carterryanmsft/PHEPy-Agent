import pandas as pd

# Load data
df = pd.read_csv('data/production_full_cases.csv')
icm_df = pd.read_csv('risk_reports/data/icm.csv')

# Extract all ICMs from cases
all_icms = set()
for icm_str in df['RelatedICM_Id'].dropna():
    for icm in str(icm_str).replace(',', ' ').split():
        if icm.strip().isdigit():
            all_icms.add(int(icm.strip()))

existing_icms = set(icm_df['IncidentId'].tolist())
matching = all_icms.intersection(existing_icms)
missing = all_icms - existing_icms

print(f'Fresh export has {len(all_icms)} unique ICMs')
print(f'icm.csv has {len(existing_icms)} ICMs')
print(f'Missing from icm.csv: {len(missing)} ICMs')
print(f'Matching: {len(matching)} ICMs')

print(f'\nICMs in icm.csv that match fresh export cases:')
for icm_id in sorted(matching):
    icm_info = icm_df[icm_df['IncidentId']==icm_id].iloc[0]
    print(f'  {icm_id}: Owner={icm_info["IcmOwner"]}, Status={icm_info["IcmStatus"]}')

# Check if there are any ACTIVE ICMs
active_icms = icm_df[icm_df['IcmStatus']=='ACTIVE']
print(f'\nACTIVE ICMs in icm.csv: {len(active_icms)}')
if len(active_icms) > 0:
    print(active_icms[['IncidentId', 'IcmOwner', 'IcmStatus']])

# Check if those ACTIVE ICMs are in the fresh export
print(f'\nChecking if ACTIVE ICMs are in fresh export cases:')
for icm_id in active_icms['IncidentId']:
    cases_with_icm = df[df['RelatedICM_Id'].str.contains(str(icm_id), na=False)]
    if len(cases_with_icm) > 0:
        print(f'  ICM {icm_id} found in {len(cases_with_icm)} case(s):')
        for idx, case in cases_with_icm.iterrows():
            print(f'    {case["ServiceRequestNumber"]}: {case["TopParentName"]}')
    else:
        print(f'  ICM {icm_id}: NOT in fresh export')
