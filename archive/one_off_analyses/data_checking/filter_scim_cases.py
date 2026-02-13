"""
Filter out cases with SCIM Escalation Management ICMs
"""
import pandas as pd

# Read current IC cases
df = pd.read_csv('risk_reports/data/ic_cases.csv')
print(f'Starting with {len(df)} cases')

# Read ICM owner data
icm_df = pd.read_csv('risk_reports/data/icm_owners.csv')

# Get SCIM ICM IDs
scim_icms = icm_df[icm_df['OwningTenantName'] == 'SCIM Escalation Management']['IncidentId'].astype(str).tolist()
print(f'\nSCIM ICM IDs to filter: {scim_icms}')

# Find cases with SCIM ICMs
cases_with_scim = []
for idx, row in df.iterrows():
    icm_str = str(row['RelatedICM_Id'])
    if icm_str and icm_str != 'nan' and icm_str != '':
        # Split ICM IDs
        icm_ids = [x.strip() for x in icm_str.split(',')]
        # Check if ANY ICM is SCIM
        if any(icm_id in scim_icms for icm_id in icm_ids):
            cases_with_scim.append(row['ServiceRequestNumber'])
            print(f'\n🚫 Filtering case {row["ServiceRequestNumber"]} ({row["TopParentName"]})')
            print(f'   Has SCIM ICM(s): {icm_str}')

print(f'\n📊 Summary:')
print(f'   Cases with SCIM ICMs: {len(cases_with_scim)}')
print(f'   Cases after filtering: {len(df) - len(cases_with_scim)}')

# Remove cases with SCIM ICMs
df_filtered = df[~df['ServiceRequestNumber'].isin(cases_with_scim)]

# Save filtered data
df_filtered.to_csv('risk_reports/data/ic_cases.csv', index=False)
print(f'\n✅ Saved {len(df_filtered)} cases to: risk_reports/data/ic_cases.csv')

# Show risk distribution after filtering
print(f'\n📊 Risk Level Distribution (after SCIM filtering):')
print(df_filtered['RiskLevel'].value_counts())

print(f'\n🚨 Top 5 Highest Risk Cases (after SCIM filtering):')
top5 = df_filtered.nlargest(5, 'RiskScore')[['ServiceRequestNumber', 'TopParentName', 'RiskScore', 'DaysOpen']]
for _, row in top5.iterrows():
    print(f'   {row["ServiceRequestNumber"]}: {row["TopParentName"]} - Risk {row["RiskScore"]}, {int(row["DaysOpen"])} days')
