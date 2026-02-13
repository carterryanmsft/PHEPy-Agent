"""
Process all fetched bugs and extract ICM hyperlinks
"""
import json
import re
import pandas as pd
from pathlib import Path

# Load IC/MCS customer data
cases_df = pd.read_csv('data/production_full_cases.csv')
icm_to_customer = {}

for _, case in cases_df.iterrows():
    if pd.notna(case['RelatedICM_Id']) and case['RelatedICM_Id']:
        icm_ids = str(case['RelatedICM_Id']).replace(',', ';').split(';')
        for icm_id in icm_ids:
            icm_id = icm_id.strip()
            if icm_id:
                try:
                    icm_int = int(icm_id)
                    if icm_int not in icm_to_customer:
                        icm_to_customer[icm_int] = []
                    icm_to_customer[icm_int].append({
                        'Customer': case['TopParentName'],
                        'Program': case['Program'],
                        'CaseNumber': case['ServiceRequestNumber']
                    })
                except ValueError:
                    pass

# Bug data files from ADO MCP
bug_files = [
    ('4676229', r'toolu_01Dy9bWFspPj8aJ7vg1X1QwS__vscode-1770399796743'),
    ('5166846', r'toolu_018pBXuiAH6hmsB9d9vjXVrD__vscode-1770399796744'),
    ('5174195', r'toolu_01UL2znDJqSzCuf2qrvK4RTH__vscode-1770399796745'),
    ('5193520', r'toolu_01QhU7m6L7yThpDbtNdJoDtL__vscode-1770399796746'),
    ('5379952', r'toolu_01WvyTQhQTg8nZDUsU2YiFng__vscode-1770399796747'),
    ('4000625', r'toolu_0157JNWFZGHXJAF19vwg3si6__vscode-1770399796748')
]

base_path = r'c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\08a9d21f-9c04-4a6b-ab5a-c4fd011fc61f'

icm_url_pattern = re.compile(r'microsofticm\.com/imp/v[35]/+incidents/details/(\d+)')

print('=' * 100)
print('EXTRACTING ICM HYPERLINKS FROM ADO BUGS')
print('=' * 100)

bugs_with_icm_links = []

for bug_id, file_code in bug_files:
    file_path = Path(base_path) / file_code / 'content.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            bug_data = json.load(f)
        
        bug_info = {
            'bug_id': bug_id,
            'title': bug_data.get('fields', {}).get('System.Title', 'Unknown'),
            'state': bug_data.get('fields', {}).get('System.State', 'Unknown'),
            'tags': bug_data.get('fields', {}).get('System.Tags', ''),
            'icm_links': [],
            'ic_mcs_customers': []
        }
        
        # Extract ICM links from relations
        if 'relations' in bug_data:
            for relation in bug_data['relations']:
                if relation.get('rel') == 'Hyperlink':
                    url = relation.get('url', '')
                    matches = icm_url_pattern.findall(url)
                    if matches:
                        for icm_id_str in matches:
                            icm_id = int(icm_id_str)
                            bug_info['icm_links'].append({
                                'icm_id': icm_id,
                                'url': url
                            })
                            
                            # Check if this ICM is linked to IC/MCS customers
                            if icm_id in icm_to_customer:
                                for cust in icm_to_customer[icm_id]:
                                    bug_info['ic_mcs_customers'].append(cust)
        
        bugs_with_icm_links.append(bug_info)
        
        print(f'\n[Bug {bug_id}] {bug_info["state"]}')
        print(f'  Title: {bug_info["title"][:80]}...')
        print(f'  ICM Links: {len(bug_info["icm_links"])}')
        if bug_info['ic_mcs_customers']:
            customers = set(c['Customer'] for c in bug_info['ic_mcs_customers'])
            print(f'  IC/MCS Customers: {", ".join(customers)}')
        else:
            print(f'  ⚠️  ICMs not in IC/MCS customer cases')
        
    except Exception as e:
        print(f'\n❌ Error processing bug {bug_id}: {e}')

# Also process bug 3563451 which we fetched earlier
file_path_3563451 = Path(base_path) / 'toolu_01JeKVyCerqCcrgS7ikd3EjC__vscode-1770399796734' / 'content.json'
try:
    with open(file_path_3563451, 'r', encoding='utf-8') as f:
        bug_data = json.load(f)
    
    bug_info = {
        'bug_id': '3563451',
        'title': bug_data.get('fields', {}).get('System.Title', 'Unknown'),
        'state': bug_data.get('fields', {}).get('System.State', 'Unknown'),
        'tags': bug_data.get('fields', {}).get('System.Tags', ''),
        'icm_links': [],
        'ic_mcs_customers': []
    }
    
    if 'relations' in bug_data:
        for relation in bug_data['relations']:
            if relation.get('rel') == 'Hyperlink':
                url = relation.get('url', '')
                matches = icm_url_pattern.findall(url)
                if matches:
                    for icm_id_str in matches:
                        icm_id = int(icm_id_str)
                        bug_info['icm_links'].append({
                            'icm_id': icm_id,
                            'url': url
                        })
                        
                        if icm_id in icm_to_customer:
                            for cust in icm_to_customer[icm_id]:
                                bug_info['ic_mcs_customers'].append(cust)
    
    bugs_with_icm_links.append(bug_info)
    
    print(f'\n[Bug 3563451] {bug_info["state"]}')
    print(f'  Title: {bug_info["title"][:80]}...')
    print(f'  ICM Links: {len(bug_info["icm_links"])}')
    if bug_info['ic_mcs_customers']:
        customers = set(c['Customer'] for c in bug_info['ic_mcs_customers'])
        print(f'  IC/MCS Customers: {", ".join(customers)}')
    else:
        print(f'  ⚠️  ICMs not in IC/MCS customer cases')
        
except Exception as e:
    print(f'\n❌ Error processing bug 3563451: {e}')

# Summary
print('\n' + '=' * 100)
print('SUMMARY')
print('=' * 100)

bugs_linked = [b for b in bugs_with_icm_links if b['ic_mcs_customers']]
bugs_not_linked = [b for b in bugs_with_icm_links if not b['ic_mcs_customers']]

print(f'\n✅ Bugs with IC/MCS Customer ICMs: {len(bugs_linked)}')
print(f'❌ Bugs with ICMs NOT in IC/MCS cases: {len(bugs_not_linked)}')

total_icms = sum(len(b['icm_links']) for b in bugs_with_icm_links)
linked_icms = sum(len(b['icm_links']) for b in bugs_linked if b['ic_mcs_customers'])

print(f'\n📊 Total ICM Hyperlinks Found: {total_icms}')
print(f'📊 ICMs Linked to IC/MCS: {linked_icms}')

# Detailed breakdown
print('\n' + '=' * 100)
print('BUGS WITH IC/MCS CUSTOMER ICMS')
print('=' * 100)

for bug in bugs_linked:
    print(f'\n[Bug {bug["bug_id"]}] {bug["state"]}')
    print(f'  {bug["title"][:80]}...')
    
    # Get unique customers
    customers_dict = {}
    for cust in bug['ic_mcs_customers']:
        cust_name = cust['Customer']
        if cust_name not in customers_dict:
            customers_dict[cust_name] = {
                'Program': cust['Program'],
                'Cases': []
            }
        customers_dict[cust_name]['Cases'].append(cust['CaseNumber'])
    
    print(f'  Customers: {len(customers_dict)}')
    for cust_name, cust_data in customers_dict.items():
        cases_str = ', '.join(cust_data['Cases'][:2])
        if len(cust_data['Cases']) > 2:
            cases_str += f' +{len(cust_data["Cases"]) - 2} more'
        print(f'    - {cust_name} ({cust_data["Program"]}): {cases_str}')
    
    print(f'  ICMs: {", ".join(str(link["icm_id"]) for link in bug["icm_links"][:5])}')
    print(f'  Link: https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug["bug_id"]}')

if bugs_not_linked:
    print('\n' + '=' * 100)
    print('BUGS WITH ICMS NOT IN IC/MCS CUSTOMER CASES')
    print('=' * 100)
    
    for bug in bugs_not_linked:
        print(f'\n[Bug {bug["bug_id"]}] {bug["state"]}')
        print(f'  {bug["title"][:80]}...')
        if bug['icm_links']:
            print(f'  ICMs: {", ".join(str(link["icm_id"]) for link in bug["icm_links"][:5])}')
        print(f'  ⚠️  These ICMs are not in your IC/MCS customer case data')

# Save results
output = {
    'bugs_with_ic_mcs_links': bugs_linked,
    'bugs_without_ic_mcs_links': bugs_not_linked,
    'summary': {
        'total_bugs': len(bugs_with_icm_links),
        'bugs_with_ic_mcs': len(bugs_linked),
        'bugs_without_ic_mcs': len(bugs_not_linked),
        'total_icm_links': total_icms,
        'ic_mcs_icm_links': linked_icms
    }
}

with open('data/ado_bugs_icm_hyperlinks_final.json', 'w') as f:
    json.dump(output, f, indent=2)

print('\n' + '=' * 100)
print(f'✓ Analysis saved to: data/ado_bugs_icm_hyperlinks_final.json')
print('=' * 100)
