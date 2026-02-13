import pandas as pd

print("=== DIAGNOSING ICM OWNER ISSUE ===\n")

# Load case data
cases = pd.read_csv('../data/production_full_cases.csv')
print(f"Cases loaded: {len(cases)}")
print(f"Cases with ICMs: {cases['RelatedICM_Id'].notna().sum()}")

# Load ICM data
icm = pd.read_csv('data/icm.csv')
print(f"\nICM data loaded: {len(icm)}")
print(f"ICM columns: {icm.columns.tolist()}")

# Check for empty strings
empty_owners = (icm['IcmOwner'] == '').sum()
print(f"Empty string owners: {empty_owners}")
na_owners = icm['IcmOwner'].isna().sum()
print(f"NA owners: {na_owners}")

# Sample ICM data
print("\n=== Sample ICM Data (first 10 rows) ===")
print(icm[['IncidentId', 'IcmOwner', 'IcmStatus']].head(10))

# Now simulate the join logic
icm['IcmOwner'] = icm['IcmOwner'].replace('', pd.NA)
icm_dict = icm.set_index('IncidentId')[['IcmOwner', 'IcmSeverity', 'IcmStatus']].to_dict('index')

# Test with a specific case
test_case = cases[cases['RelatedICM_Id'].notna()].iloc[0]
print(f"\n=== Testing Case: {test_case['ServiceRequestNumber']} ===")
print(f"RelatedICM_Id: {test_case['RelatedICM_Id']}")

icm_ids = str(test_case['RelatedICM_Id']).replace(',', ';').split(';')
for icm_id_str in icm_ids[:3]:  # First 3 ICMs
    icm_id_str = icm_id_str.strip()
    if icm_id_str:
        try:
            icm_id = int(icm_id_str)
            if icm_id in icm_dict:
                icm_data = icm_dict[icm_id]
                print(f"\nICM {icm_id}:")
                print(f"  Owner: {icm_data.get('IcmOwner')} (type: {type(icm_data.get('IcmOwner'))})")
                print(f"  Status: {icm_data.get('IcmStatus')}")
                
                # Test pd.notna
                owner_val = icm_data.get('IcmOwner')
                print(f"  pd.notna(owner): {pd.notna(owner_val)}")
                if pd.notna(owner_val):
                    print(f"  str(owner): '{str(owner_val)}'")
                    print(f"  str(owner).strip(): '{str(owner_val).strip()}'")
            else:
                print(f"\nICM {icm_id}: NOT IN DICT")
        except Exception as e:
            print(f"\nICM {icm_id_str}: ERROR - {e}")
