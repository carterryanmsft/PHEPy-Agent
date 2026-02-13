import pandas as pd

icm = pd.read_csv('risk_reports/data/icm_owners.csv')

print('='*60)
print('CHECKING FOR ACTIVE UNASSIGNED ICMs')
print('='*60)

# Check for ACTIVE ICMs with no owner
active_unassigned = icm[(icm['IcmStatus']=='ACTIVE') & ((icm['IcmOwner']=='') | (icm['IcmOwner'].isna()))]

print(f'\n🔴 ACTIVE ICMs with no owner: {len(active_unassigned)}')

if len(active_unassigned) > 0:
    print('\nThese will be flagged as UNASSIGNED in red:')
    print(active_unassigned[['IncidentId','IcmOwner','IcmStatus','OwningTenantName','OwningTeamName']].to_string(index=False))
else:
    print('\n✅ All ACTIVE ICMs have owners assigned')

# Also show all ACTIVE ICMs
active_icms = icm[icm['IcmStatus']=='ACTIVE']
print(f'\n📊 Total ACTIVE ICMs: {len(active_icms)}')
if len(active_icms) > 0:
    print('\nAll ACTIVE ICMs:')
    print(active_icms[['IncidentId','IcmOwner','IcmStatus','OwningTenantName']].to_string(index=False))
