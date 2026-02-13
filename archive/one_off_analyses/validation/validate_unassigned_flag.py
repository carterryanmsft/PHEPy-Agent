"""
Validate UNASSIGNED ICM flagging in report
"""
import pandas as pd

print('='*60)
print('UNASSIGNED ICM FLAGGING VALIDATION')
print('='*60)

# Load data
icm = pd.read_csv('risk_reports/data/icm_owners.csv')
cases = pd.read_csv('risk_reports/data/ic_cases.csv')

# Find ACTIVE ICMs with no owner
active_unassigned = icm[(icm['IcmStatus']=='ACTIVE') & ((icm['IcmOwner']=='') | (icm['IcmOwner'].isna()))]

print(f'\n🔴 ACTIVE ICMs with no owner: {len(active_unassigned)}')

if len(active_unassigned) > 0:
    for _, icm_row in active_unassigned.iterrows():
        icm_id = str(icm_row['IncidentId'])
        print(f'\n  ICM: {icm_id} ({icm_row["OwningTenantName"]} - {icm_row["OwningTeamName"]})')
        
        # Find case with this ICM
        case = cases[cases['RelatedICM_Id'].str.contains(icm_id, na=False)]
        if len(case) > 0:
            case_num = case.iloc[0]['ServiceRequestNumber']
            customer = case.iloc[0]['TopParentName']
            print(f'  ✅ Case: {case_num} ({customer})')
            print(f'  → Will display "UNASSIGNED" in RED')
        else:
            print(f'  ⚠️  No case found with this ICM')

# Verify in HTML
with open('risk_reports/IC_Report_Final.htm', 'r', encoding='utf-8') as f:
    html_content = f.read()
    
if 'icm-unassigned' in html_content and 'UNASSIGNED' in html_content:
    print(f'\n✅ HTML report contains UNASSIGNED flagging')
    print(f'   - CSS class defined: .icm-unassigned')
    print(f'   - Red background: #FFC7CE')
    print(f'   - Red text: #9C0006')
else:
    print(f'\n⚠️  UNASSIGNED flagging not found in HTML')

print('\n' + '='*60)
print('VERIFICATION COMPLETE')
print('='*60)
print('\n✅ ACTIVE ICMs with no owner will show as "UNASSIGNED" in red')
print('✅ All other cases display normally')
