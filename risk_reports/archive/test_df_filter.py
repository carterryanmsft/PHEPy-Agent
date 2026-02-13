import pandas as pd

# Simulate the exact flow
df = pd.DataFrame([{
    'ServiceRequestNumber': '2510030040002408',
    'RelatedICM_Id': '693849812,693543577,694142803,694208210,694253124,693952482,694041459'
}])

print("BEFORE filtering:")
print(df['RelatedICM_Id'])

# Load ICM and build dict
icm_df = pd.read_csv('data/icm.csv')
icm_df['IcmOwner'] = icm_df['IcmOwner'].replace('', pd.NA)
icm_dict = icm_df.set_index('IncidentId')[['IcmOwner', 'IcmSeverity', 'IcmStatus']].to_dict('index')

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

# Apply filter
df['RelatedICM_Id'] = df['RelatedICM_Id'].apply(filter_icm_ids)

print("\nAFTER filtering:")
print(df['RelatedICM_Id'])

# Now iterate like the report does
for _, row in df.iterrows():
    print(f"\nIn row iteration:")
    print(f"  row['RelatedICM_Id'] = {row['RelatedICM_Id']}")
