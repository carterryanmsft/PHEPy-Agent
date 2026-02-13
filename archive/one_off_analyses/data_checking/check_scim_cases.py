import pandas as pd

df = pd.read_csv('risk_reports/data/ic_cases.csv')

print('='*60)
print('CHECKING FOR SCIM ESCALATION MANAGEMENT CASES')
print('='*60)

# Check SAPPath for SCIM
scim_in_path = df[df['SAPPath'].str.contains('SCIM', case=False, na=False)]
print(f'\nCases with SCIM in SAPPath: {len(scim_in_path)}')
if len(scim_in_path) > 0:
    print(scim_in_path[['ServiceRequestNumber', 'TopParentName', 'SAPPath']].to_string(index=False))

# Check if any cases should have been filtered by ICM ownership
print('\n' + '='*60)
print('ICM OWNER POPULATION CHECK')
print('='*60)

has_icm = df[df['HasICM'] == 'Yes']
print(f'\nCases with ICM: {len(has_icm)}')
print(f'\nSample cases needing ICM owner lookup:')
print(has_icm[['ServiceRequestNumber', 'TopParentName', 'RelatedICM_Id']].head(10).to_string(index=False))
