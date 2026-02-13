"""
Match specific bug work items to MCS/IC customers using ADO data
"""
import json
import pandas as pd
from collections import defaultdict

# Load ADO bug data
with open('data/bugs_ado_data.json', 'r', encoding='utf-8') as f:
    bugs_ado = json.load(f)

# Load IC/MCS customer cases
cases_df = pd.read_csv('data/production_full_cases.csv')

# Get unique IC/MCS customers
ic_mcs_customers = cases_df['TopParentName'].unique()

# Create customer name variations for better matching
customer_variations = {}
for customer in ic_mcs_customers:
    customer_upper = customer.upper()
    variations = {customer_upper}
    
    # Add common abbreviations and variations
    if 'MUFJ' in customer_upper or 'MITSUBISHI' in customer_upper:
        variations.update(['MUFJ', 'MUFG', 'MITSUBISHI', 'MITSUBISHI UFJ', 'SMBC'])
    elif 'FORD' in customer_upper:
        variations.update(['FORD', 'FORD MOTOR', 'FORD MOTOR COMPANY'])
    elif 'HUNTINGTON' in customer_upper:
        variations.update(['HUNTINGTON', 'HUNTINGTON BANK'])
    elif 'NOVARTIS' in customer_upper:
        variations.add('NOVARTIS')
    elif 'MORGAN STANLEY' in customer_upper or 'MORGAN' in customer_upper:
        variations.update(['MORGAN STANLEY', 'MORGAN'])
    elif 'VODAFONE' in customer_upper:
        variations.add('VODAFONE')
    elif 'ADNOC' in customer_upper:
        variations.add('ADNOC')
    
    customer_variations[customer] = variations

# Create ICM to customer mapping
icm_to_customer = defaultdict(list)
for _, case in cases_df.iterrows():
    if pd.notna(case['RelatedICM_Id']) and case['RelatedICM_Id']:
        icm_ids = str(case['RelatedICM_Id']).replace(',', ';').split(';')
        for icm_id in icm_ids:
            icm_id = icm_id.strip()
            if icm_id:
                try:
                    icm_int = int(icm_id)
                    icm_to_customer[icm_int].append({
                        'Customer': case['TopParentName'],
                        'Program': case['Program'],
                        'CaseNumber': case['ServiceRequestNumber'],
                        'RiskScore': case['RiskScore'],
                        'Status': case['ServiceRequestStatus']
                    })
                except ValueError:
                    pass

print('=' * 100)
print(f'MATCHING {len(bugs_ado)} BUGS TO MCS/IC CUSTOMERS')
print('=' * 100)

# Analyze bugs
results = {
    'matched_bugs': [],
    'unmatched_bugs': [],
    'summary': {
        'total_bugs': len(bugs_ado),
        'matched_count': 0,
        'unmatched_count': 0,
        'ic_customers': set(),
        'mcs_customers': set()
    }
}

for bug in bugs_ado:
    bug_id = bug['id']
    bug_title = bug['fields'].get('System.Title', '')
    bug_state = bug['fields'].get('System.State', '')
    bug_tags = bug['fields'].get('System.Tags', '')
    
    bug_entry = {
        'BugId': bug_id,
        'Title': bug_title,
        'Status': bug_state,
        'Tags': bug_tags,
        'Link': f'https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug_id}',
        'Customers': [],
        'MatchMethod': []
    }
    
    # Method 1: Check tags and title for customer names
    tags_upper = bug_tags.upper()
    title_upper = bug_title.upper()
    
    matched_customers = set()
    for customer, variations in customer_variations.items():
        for variation in variations:
            if variation in tags_upper or variation in title_upper:
                program = cases_df[cases_df['TopParentName'] == customer]['Program'].iloc[0]
                matched_customers.add((customer, program, f'Name: {variation}'))
                break
    
    # Add matched customers to bug entry
    for customer, program, match_method in matched_customers:
        bug_entry['Customers'].append({
            'Customer': customer,
            'Program': program
        })
        bug_entry['MatchMethod'].append(match_method)
        
        if program == 'IC':
            results['summary']['ic_customers'].add(customer)
        else:
            results['summary']['mcs_customers'].add(customer)
    
    if bug_entry['Customers']:
        results['matched_bugs'].append(bug_entry)
        results['summary']['matched_count'] += 1
    else:
        results['unmatched_bugs'].append(bug_entry)
        results['summary']['unmatched_count'] += 1

# Print report
print(f'\n✅ Bugs Matched to IC/MCS Customers: {results["summary"]["matched_count"]}')
print(f'❌ Bugs NOT Matched: {results["summary"]["unmatched_count"]}')
print(f'📊 IC Customers: {len(results["summary"]["ic_customers"])}')
print(f'📊 MCS Customers: {len(results["summary"]["mcs_customers"])}')

print('\n' + '=' * 100)
print('MATCHED BUGS')
print('=' * 100)

for bug in results['matched_bugs']:
    print(f'\n[Bug {bug["BugId"]}] {bug["Status"]}')
    print(f'  Title: {bug["Title"][:100]}')
    print(f'  Customers:')
    for cust in bug['Customers']:
        print(f'    ✓ {cust["Customer"]} ({cust["Program"]})')
    if bug.get('MatchMethod'):
        print(f'  Match: {", ".join(bug["MatchMethod"][:3])}')
    print(f'  Link: {bug["Link"]}')

print('\n' + '=' * 100)
print('UNMATCHED BUGS (No IC/MCS Customer Found)')
print('=' * 100)

for bug in results['unmatched_bugs']:
    print(f'\n[Bug {bug["BugId"]}] {bug["Status"]}')
    print(f'  Title: {bug["Title"][:100]}')
    print(f'  Tags: {bug["Tags"][:100]}')
    print(f'  Link: {bug["Link"]}')

# Group by customer
print('\n' + '=' * 100)
print('BUGS BY CUSTOMER')
print('=' * 100)

customer_bugs = defaultdict(list)
for bug in results['matched_bugs']:
    for cust in bug['Customers']:
        customer_bugs[cust['Customer']].append({
            'BugId': bug['BugId'],
            'Status': bug['Status'],
            'Program': cust['Program'],
            'Title': bug['Title'],
            'Link': bug['Link']
        })

# Sort by program and customer name
sorted_customers = sorted(customer_bugs.items(), 
                         key=lambda x: (customer_bugs[x[0]][0]['Program'], x[0]))

for customer, bugs in sorted_customers:
    program = bugs[0]['Program']
    print(f'\n{customer} ({program}) - {len(bugs)} bug(s):')
    for bug in bugs:
        print(f'  • Bug {bug["BugId"]} [{bug["Status"]}]')
        print(f'    {bug["Title"][:80]}')
        print(f'    {bug["Link"]}')

# Save results
output_file = 'data/bug_customer_matches_final.json'
results['summary']['ic_customers'] = list(results['summary']['ic_customers'])
results['summary']['mcs_customers'] = list(results['summary']['mcs_customers'])

with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f'\n✅ Results saved to: {output_file}')
print('=' * 100)
