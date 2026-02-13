"""
Analyze all user-provided bug IDs and their connection to IC/MCS customers
"""
import pandas as pd
import json

# User-provided bug IDs
target_bugs = [
    "4397651", "4900202", "5000554", "5086097", "5359703", "5746145", 
    "5794140", "5968930", "6254385", "6305634", "6330464", "6707273", 
    "6771602", "6794267", "6821575", "6879829", "6902454"
]

# Read the ICM query results
with open(r'c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\08a9d21f-9c04-4a6b-ab5a-c4fd011fc61f\toolu_01HjemowfgR5JWvdXzkAaDGB__vscode-1770399796715\content.txt', 'r') as f:
    content = f.read()
    start_idx = content.find('"data": [')
    end_idx = content.rfind(']')
    json_str = '{' + content[start_idx:end_idx+1] + '}'
    icm_bug_data = json.loads(json_str)

# Load production cases
cases_df = pd.read_csv('data/production_full_cases.csv')

# Extract all ICM IDs from cases
case_icms = set()
icm_to_case = {}
for _, case in cases_df.iterrows():
    if pd.notna(case['RelatedICM_Id']) and case['RelatedICM_Id']:
        icm_ids = str(case['RelatedICM_Id']).replace(',', ';').split(';')
        for icm_id in icm_ids:
            icm_id = icm_id.strip()
            if icm_id:
                try:
                    icm_int = int(icm_id)
                    case_icms.add(icm_int)
                    if icm_int not in icm_to_case:
                        icm_to_case[icm_int] = []
                    icm_to_case[icm_int].append({
                        'Customer': case['TopParentName'],
                        'Program': case['Program'],
                        'CaseNumber': case['ServiceRequestNumber'],
                        'RiskScore': case['RiskScore'],
                        'Status': case['ServiceRequestStatus']
                    })
                except ValueError:
                    pass

print('=' * 100)
print('BUG ANALYSIS: USER-PROVIDED LIST vs IC/MCS CUSTOMERS')
print('=' * 100)

# Analyze each bug
bugs_found_in_icm = {}
bugs_not_found = []

for bug_data in icm_bug_data['data']:
    bug_id = bug_data['ExternalId']
    if bug_id not in bugs_found_in_icm:
        bugs_found_in_icm[bug_id] = {
            'ExternalId': bug_id,
            'Status': bug_data['Status'],
            'Owner': bug_data['Owner'].split('<')[0].strip(),
            'Description': bug_data['Description'],
            'ICMs': [],
            'LinkedToICMCS': False,
            'Customers': []
        }
    
    icm_id = bug_data['IncidentId']
    bugs_found_in_icm[bug_id]['ICMs'].append(icm_id)
    
    # Check if this ICM is linked to IC/MCS customers
    if icm_id in icm_to_case:
        bugs_found_in_icm[bug_id]['LinkedToICMCS'] = True
        for case_info in icm_to_case[icm_id]:
            bugs_found_in_icm[bug_id]['Customers'].append(case_info)

# Find bugs not in ICM at all
for bug_id in target_bugs:
    if bug_id not in bugs_found_in_icm:
        bugs_not_found.append(bug_id)

# Summary
print(f'\n[SUMMARY]')
print(f'  Total Bugs Requested: {len(target_bugs)}')
print(f'  Found in ICM: {len(bugs_found_in_icm)}')
print(f'  NOT Found in ICM: {len(bugs_not_found)}')

linked_count = sum(1 for b in bugs_found_in_icm.values() if b['LinkedToICMCS'])
not_linked_count = len(bugs_found_in_icm) - linked_count

print(f'\n  Of those found in ICM:')
print(f'    ✓ Linked to IC/MCS Customers: {linked_count}')
print(f'    ✗ NOT Linked to IC/MCS Customers: {not_linked_count}')

# Show bugs NOT linked to IC/MCS
print('\n' + '=' * 100)
print('❌ BUGS FOUND IN ICM BUT NOT LINKED TO IC/MCS CUSTOMERS')
print('=' * 100)

not_linked_bugs = [b for b in bugs_found_in_icm.values() if not b['LinkedToICMCS']]
for bug in sorted(not_linked_bugs, key=lambda x: x['ExternalId']):
    print(f'\nBug {bug["ExternalId"]} ({bug["Status"]})')
    print(f'  Owner: {bug["Owner"]}')
    print(f'  Description: {bug["Description"][:80]}...')
    print(f'  Linked to ICMs: {", ".join(str(i) for i in bug["ICMs"][:5])}{"..." if len(bug["ICMs"]) > 5 else ""}')
    print(f'  Link: https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug["ExternalId"]}')
    print(f'  ⚠️  These ICMs are NOT in your IC/MCS customer cases')

# Show bugs linked to IC/MCS
print('\n' + '=' * 100)
print('✅ BUGS LINKED TO IC/MCS CUSTOMERS')
print('=' * 100)

linked_bugs = [b for b in bugs_found_in_icm.values() if b['LinkedToICMCS']]
for bug in sorted(linked_bugs, key=lambda x: x['ExternalId']):
    print(f'\nBug {bug["ExternalId"]} ({bug["Status"]})')
    print(f'  Owner: {bug["Owner"]}')
    print(f'  Description: {bug["Description"][:80]}...')
    
    # Get unique customers
    customers = {}
    for cust in bug['Customers']:
        cust_name = cust['Customer']
        if cust_name not in customers:
            customers[cust_name] = {
                'Program': cust['Program'],
                'Cases': []
            }
        customers[cust_name]['Cases'].append(cust['CaseNumber'])
    
    print(f'  Customers ({len(customers)}):')
    for cust_name, cust_data in customers.items():
        cases_str = ', '.join(str(c) for c in cust_data['Cases'][:3])
        if len(cust_data['Cases']) > 3:
            cases_str += f' +{len(cust_data["Cases"]) - 3} more'
        print(f'    - {cust_name} ({cust_data["Program"]}): {cases_str}')
    
    print(f'  Link: https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug["ExternalId"]}')

# Show bugs NOT found in ICM at all
if bugs_not_found:
    print('\n' + '=' * 100)
    print('🔍 BUGS NOT FOUND IN ICM DATABASE')
    print('=' * 100)
    print(f'\nThese {len(bugs_not_found)} bug IDs do not exist in the ICM IncidentBugs table:')
    for bug_id in sorted(bugs_not_found):
        print(f'  • Bug {bug_id}')
        print(f'    Link: https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug_id}')
    print('\n⚠️  These bugs may:')
    print('   - Not be linked to any ICM incidents')
    print('   - Be in a different Azure DevOps project')
    print('   - Have been deleted or archived')

# Save analysis
output = {
    'summary': {
        'total_requested': len(target_bugs),
        'found_in_icm': len(bugs_found_in_icm),
        'not_found_in_icm': len(bugs_not_found),
        'linked_to_ic_mcs': linked_count,
        'not_linked_to_ic_mcs': not_linked_count
    },
    'bugs_linked_to_ic_mcs': [b for b in bugs_found_in_icm.values() if b['LinkedToICMCS']],
    'bugs_not_linked': [b for b in bugs_found_in_icm.values() if not b['LinkedToICMCS']],
    'bugs_not_found': bugs_not_found
}

with open('data/bug_linkage_analysis.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)

print('\n' + '=' * 100)
print(f'✓ Analysis saved to: data/bug_linkage_analysis.json')
print('=' * 100)
