import pandas as pd

df = pd.read_csv('risk_reports/data/ic_cases.csv')

print('HasICM column values:')
print(df['HasICM'].value_counts())

print('\nCases marked as having ICM:')
has_icm_cases = df[df['HasICM'] == 'Yes']
print(f'Count: {len(has_icm_cases)}')

if len(has_icm_cases) > 0:
    print('\nSample cases with HasICM=Yes:')
    print(has_icm_cases[['ServiceRequestNumber', 'RelatedICM_Id', 'HasICM']].head())
else:
    print('\n⚠️  No cases have ICM data populated (HasICM=Yes)')
    print('This explains why ICM IDs and owners are not showing in the report.')

print('\n' + '='*60)
print('DIAGNOSIS:')
print('='*60)
print('The Kusto query returned cases but RelatedICM_Id is empty.')
print('This could mean:')
print('1. These cases genuinely have no ICMs attached in OneSupport')
print('2. The GetSCIMIncidentV2 table does not populate RelatedICM_Id')
print('3. The query filtering removed ICM data inadvertently')
