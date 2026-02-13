import pandas as pd

icm = pd.read_csv('risk_reports/data/icm_owners.csv')

print('='*70)
print('BUG INFORMATION IN ICM DATA')
print('='*70)

print('\nColumns:', icm.columns.tolist())

if 'BugIds' in icm.columns:
    bugs_present = icm[icm['BugIds'].notna() & (icm['BugIds'] != '')]
    print(f'\n✅ ICMs with linked bugs: {len(bugs_present)} out of {len(icm)}')
    
    if len(bugs_present) > 0:
        print('\n📋 Sample ICMs with bugs:')
        for _, row in bugs_present.head(10).iterrows():
            print(f'\nICM {row["IncidentId"]}:')
            print(f'  Bug IDs: {row["BugExternalIds"]}')
            print(f'  Bug Status: {row["BugStatuses"]}')
            if pd.notna(row['BugDescriptions']):
                desc = str(row['BugDescriptions'])[:100]
                print(f'  Description: {desc}...')
    else:
        print('\n⚠️  No bugs found in ICM data')
else:
    print('\n⚠️  BugIds column not found in CSV')
