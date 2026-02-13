import pandas as pd
import json

# Simulate the full report generator logic
print("=== SIMULATING FULL REPORT GENERATOR ===\n")

# Load case data - using small sample for testing
cases_data = [
    {
        "ServiceRequestNumber": "2510270040012508",
        "RelatedICM_Id": "704668547,51000000859513",
        "TopParentName": "Huntington",
        "DaysOpen": 99.0,
        "RiskScore": 75
    }
]
df = pd.DataFrame(cases_data)
print("Initial case data:")
print(df[['ServiceRequestNumber', 'RelatedICM_Id']])

# Load ICM data
icm_df = pd.read_csv('data/icm.csv')
print(f"\n Loaded {len(icm_df)} ICMs")
icm_df['IcmOwner'] = icm_df['IcmOwner'].replace('', pd.NA)
icm_dict = icm_df.set_index('IncidentId')[['IcmOwner', 'IcmSeverity', 'IcmStatus']].to_dict('index')
has_icm_data = True

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

# Filter RelatedICM_Id
print("\nFiltering RelatedICM_Id...")
df['RelatedICM_Id'] = df['RelatedICM_Id'].apply(filter_icm_ids)
print("After filtering:")
print(df[['ServiceRequestNumber', 'RelatedICM_Id']])

# get_icm_data function
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

# Apply ICM lookups
print("\nApplying ICM lookups...")
df['IcmOwner'] = df['RelatedICM_Id'].apply(lambda x: get_icm_data(x, 'IcmOwner'))
df['IcmStatus'] = df['RelatedICM_Id'].apply(lambda x: get_icm_data(x, 'IcmStatus'))

print("After ICM lookups:")
print(df[['ServiceRequestNumber', 'RelatedICM_Id', 'IcmOwner', 'IcmStatus']])

# Now simulate the display logic for a row
print("\n=== SIMULATING DISPLAY LOGIC ===")
row = df.iloc[0]

icm_owner_display = 'N/A'
if has_icm_data and not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip():
    owner_value = ''
    if 'IcmOwner' in df.columns:
        raw_owner = row['IcmOwner']
        if pd.notna(raw_owner):
            owner_str = str(raw_owner).strip()
            if owner_str and owner_str.lower() not in ['nan', 'none', 'null']:
                owner_value = owner_str
                print(f"owner_value = '{owner_value}'")
    
    icm_status = ''
    if 'IcmStatus' in df.columns:
        raw_status = row['IcmStatus']
        if pd.notna(raw_status):
            status_str = str(raw_status).strip()
            if status_str and status_str.lower() not in ['nan', 'none', 'null']:
                icm_status = status_str
                print(f"icm_status = '{icm_status}'")
    
    if owner_value:
        icm_owner_display = owner_value
    elif icm_status == 'ACTIVE':
        icm_owner_display = '<span class="icm-unassigned">Unassigned</span>'

print(f"\nFINAL icm_owner_display = '{icm_owner_display}'")
