import pandas as pd

# Load case data
cases = pd.read_csv('../data/production_full_cases.csv')
# Load ICM data
icm = pd.read_csv('data/icm.csv')

# Get all ICMs from cases
cases_with_icms = cases[cases['RelatedICM_Id'].notna()].copy()
print(f"Total cases with ICMs: {len(cases_with_icms)}")

# Parse all ICM IDs from cases
all_case_icms = set()
for icm_ids in cases_with_icms['RelatedICM_Id']:
    if pd.notna(icm_ids):
        icm_ids_str = str(icm_ids).replace(',', ';')
        for icm_id in icm_ids_str.split(';'):
            if icm_id.strip():
                try:
                    all_case_icms.add(int(icm_id.strip()))
                except:
                    pass

print(f"Unique ICMs in cases: {len(all_case_icms)}")
print(f"ICMs in icm.csv: {len(icm)}")

# Check which case ICMs are NOT in icm.csv
icm_ids_set = set(icm['IncidentId'].values)
missing_icms = all_case_icms - icm_ids_set
if missing_icms:
    print(f"\n⚠️ WARNING: {len(missing_icms)} ICMs in cases but NOT in icm.csv:")
    print(sorted(list(missing_icms))[:10])

# Check ICM owners
icm_dict = icm.set_index('IncidentId')['IcmOwner'].to_dict()
print(f"\nICMs with owners in icm.csv: {icm['IcmOwner'].notna().sum()}")

# Sample a few cases and show their ICM owner lookup
print("\n=== Sample Case ICM Owner Lookup ===")
for idx, row in cases_with_icms.head(10).iterrows():
    icm_ids = str(row['RelatedICM_Id']).replace(',', ';').split(';')
    case_id = row['ServiceRequestNumber']
    print(f"\nCase {case_id}:")
    print(f"  ICM IDs: {row['RelatedICM_Id']}")
    for icm_id_str in icm_ids:
        if icm_id_str.strip():
            try:
                icm_id = int(icm_id_str.strip())
                owner = icm_dict.get(icm_id, 'NOT_IN_DICT')
                if pd.isna(owner):
                    owner = 'NO_OWNER'
                print(f"    {icm_id}: {owner}")
            except:
                print(f"    {icm_id_str}: PARSE_ERROR")
