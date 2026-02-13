import pandas as pd

# Load and simulate the report generator logic
cases = pd.read_csv('../data/production_full_cases.csv')
icm = pd.read_csv('data/icm.csv')

# Simulate ICM loading
icm['IcmOwner'] = icm['IcmOwner'].replace('', pd.NA)
icm_dict = icm.set_index('IncidentId')[['IcmOwner', 'IcmSeverity', 'IcmStatus']].to_dict('index')

print(f"ICM dict has {len(icm_dict)} entries")

# Filter function
def filter_icm_ids(icm_ids_str):
    if pd.isna(icm_ids_str) or not str(icm_ids_str).strip():
        return ''
    icm_ids_str = str(icm_ids_str).replace(',', ';')
    icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
    valid_icms = []
    for icm_id_str in icm_ids:
        try:
            icm_id = int(icm_id_str)
            if icm_id in icm_dict:
                valid_icms.append(str(icm_id))
        except (ValueError, KeyError):
            pass
    return ','.join(valid_icms) if valid_icms else ''

# Test with the problematic case
test_case = cases[cases['ServiceRequestNumber'] == '2510030040002408'].iloc[0]
print(f"\nCase: {test_case['ServiceRequestNumber']}")
print(f"Original ICMs: {test_case['RelatedICM_Id']}")

filtered = filter_icm_ids(test_case['RelatedICM_Id'])
print(f"Filtered ICMs: {filtered}")

original_icms = str(test_case['RelatedICM_Id']).split(',')
filtered_icms = filtered.split(',') if filtered else []

print(f"\nOriginal count: {len(original_icms)}")
print(f"Filtered count: {len(filtered_icms)}")
print(f"Removed: {set(original_icms) - set(filtered_icms)}")

# Test owner lookup on filtered
def get_icm_data(icm_ids_str, field):
    if pd.isna(icm_ids_str) or not str(icm_ids_str).strip():
        return None
    icm_ids_str = str(icm_ids_str).replace(',', ';')
    icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
    if icm_ids:
        for icm_id_str in icm_ids:
            try:
                icm_id = int(icm_id_str)
                if icm_id in icm_dict:
                    if icm_dict[icm_id].get('IcmStatus') == 'ACTIVE':
                        value = icm_dict[icm_id].get(field)
                        if pd.notna(value) and str(value).strip():
                            return value
            except (ValueError, KeyError):
                pass
        for icm_id_str in icm_ids:
            try:
                icm_id = int(icm_id_str)
                if icm_id in icm_dict:
                    value = icm_dict[icm_id].get(field)
                    if pd.notna(value) and str(value).strip():
                        return value
            except (ValueError, KeyError):
                pass
    return None

owner = get_icm_data(filtered, 'IcmOwner')
status = get_icm_data(filtered, 'IcmStatus')
print(f"\nOwner from filtered: {owner}")
print(f"Status from filtered: {status}")
