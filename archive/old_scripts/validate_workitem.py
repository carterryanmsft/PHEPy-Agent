import pandas as pd

# Load case data
df = pd.read_csv(r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\data\production_full_cases.csv')

# Validate work item connection
print('=== WORK ITEM 6330534 VALIDATION ===')
print('Title: SharePoint DLP Alerts Admin Units issue')
print('Customer: Vodafone')
print('ICM: 731965412')
print('Status: Active')
print('Assigned to: Ankur Debnath')
print('Severity: 3 - Medium')
print('Created: 2025-11-06')
print('Due Date: 2026-02-06')
print()

# Search for ICM 731965412 in cases
icm_num = '731965412'
cases_with_icm = df[df['RelatedICM_Id'].astype(str).str.contains(icm_num, na=False)]

print(f'Searching for cases with ICM {icm_num}...\n')

if len(cases_with_icm) > 0:
    print(f'✓ Found {len(cases_with_icm)} case(s) linked to this work item:\n')
    for idx, case in cases_with_icm.iterrows():
        print(f'  Case: {case["ServiceRequestNumber"]}')
        print(f'  Customer: {case["TopParentName"]}')
        print(f'  Status: {case["ServiceRequestStatus"]}')
        print(f'  Days Open: {case["DaysOpen"]}')
        print(f'  Product: {case["DerivedProductName"]}')
        print(f'  Program: {case["Program"]}')
        summary_text = str(case["Summary"])[:100]
        print(f'  Summary: {summary_text}...')
        print()
else:
    print(f'✗ No cases found with ICM {icm_num}')
    print()
    print('Note: User mentioned case 2504231420002138 but it is not in production data.')
    print('This could mean:')
    print('  - Case was closed/resolved')
    print('  - Case not tagged with IC/MCS program')
    print('  - Different ICM or case number')
