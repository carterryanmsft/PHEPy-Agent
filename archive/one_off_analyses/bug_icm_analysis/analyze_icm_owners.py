"""
Check ICM data for SCIM Escalation Management and save to CSV
"""
import json
import pandas as pd

# Read ICM data
with open('risk_reports/data/icm_owners_raw.json', 'r', encoding='utf-8') as f:
    content = f.read()
    # Remove the "Query results: " prefix if present
    if content.startswith('Query results: '):
        content = content.replace('Query results: ', '', 1)
    data = json.loads(content)

# Handle both wrapped and unwrapped JSON
if isinstance(data, dict) and 'data' in data:
    icm_df = pd.DataFrame(data['data'])
else:
    icm_df = pd.DataFrame(data)

print('='*60)
print('ICM OWNERSHIP ANALYSIS')
print('='*60)

print(f'\nTotal ICMs: {len(icm_df)}')

# Check for SCIM Escalation Management
scim_icms = icm_df[icm_df['OwningTenantName'] == 'SCIM Escalation Management']
print(f'\n🚨 ICMs owned by SCIM Escalation Management: {len(scim_icms)}')

if len(scim_icms) > 0:
    print('\nSCIM ICMs that should be filtered:')
    print(scim_icms[['IncidentId', 'OwningTenantName', 'OwningTeamName', 'IcmOwner', 'IcmStatus']].to_string(index=False))
    print('\n⚠️  These ICMs should cause their cases to be EXCLUDED from the report!')

# Show owner distribution
print(f'\n📊 ICM Owner Distribution (Top 10):')
print(icm_df['OwningTenantName'].value_counts().head(10))

# Save to CSV for report generator
icm_df.to_csv('risk_reports/data/icm_owners.csv', index=False)
print(f'\n✅ Saved ICM data to: risk_reports/data/icm_owners.csv')
