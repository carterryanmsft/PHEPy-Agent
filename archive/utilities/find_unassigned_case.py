import pandas as pd

cases = pd.read_csv('risk_reports/data/ic_cases.csv')

# Find case with ICM 737553612
case_with_unassigned = cases[cases['RelatedICM_Id'].str.contains('737553612', na=False)]

if len(case_with_unassigned) > 0:
    print('✅ Case with UNASSIGNED ICM 737553612 found:')
    print(case_with_unassigned[['ServiceRequestNumber','TopParentName','RelatedICM_Id']].to_string(index=False))
else:
    print('⚠️  ICM 737553612 not found in cases')
