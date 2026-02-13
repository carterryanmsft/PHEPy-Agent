"""
Match specific bug work items to MCS/IC customers
"""
import json
import pandas as pd
import os
from collections import defaultdict

# Bug IDs to match
BUG_IDS = [
    4397651, 4900202, 5008054, 5086097, 5359703, 5748145, 5794140, 5968930,
    6254385, 6330464, 6330534, 6707273, 6771882, 6794267, 6821575, 6879829,
    6902454, 5806337, 5800277, 6254385, 5565986
]

print('=' * 100)
print(f'MATCHING {len(set(BUG_IDS))} BUGS TO MCS/IC CUSTOMERS')
print('=' * 100)

# Load IC/MCS customer cases
cases_df = pd.read_csv('data/production_full_cases.csv')

# Get unique IC/MCS customers
ic_mcs_customers = cases_df['TopParentName'].unique()
ic_mcs_customer_set = set([c.upper() for c in ic_mcs_customers])

# Create customer name variations for better matching
customer_variations = {}
for customer in ic_mcs_customers:
    customer_upper = customer.upper()
    variations = [customer_upper]
    
    # Add common abbreviations and variations
    if 'MUFJ' in customer_upper or 'MITSUBISHI' in customer_upper:
        variations.extend(['MUFJ', 'MITSUBISHI', 'MITSUBISHI UFJ'])
    elif 'FORD' in customer_upper:
        variations.extend(['FORD', 'FORD MOTOR', 'FORD MOTOR COMPANY'])
    elif 'HUNTINGTON' in customer_upper:
        variations.extend(['HUNTINGTON', 'HUNTINGTON BANK'])
    elif 'BHP' in customer_upper:
        variations.append('BHP')
    elif 'STATE OF WA' in customer_upper or 'WASHINGTON' in customer_upper:
        variations.extend(['STATE OF WA', 'WASHINGTON', 'WA-STATE'])
    
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

# Try to load existing bug data
bugs_data = {}
data_sources = [
    'data/ado_bugs_with_icms.json',
    'data/bug_linkage_analysis.json',
    'data/comprehensive_icm_bug_analysis.json'
]

for data_file in data_sources:
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for bug in data:
                        if 'id' in bug or 'BugId' in bug or 'ExternalId' in bug:
                            bug_id = bug.get('id') or bug.get('BugId') or bug.get('ExternalId')
                            if bug_id and int(bug_id) in BUG_IDS:
                                bugs_data[int(bug_id)] = bug
                elif isinstance(data, dict):
                    # Handle different data structures
                    if 'bugs' in data:
                        for bug in data['bugs']:
                            bug_id = bug.get('id') or bug.get('BugId')
                            if bug_id and int(bug_id) in BUG_IDS:
                                bugs_data[int(bug_id)] = bug
        except Exception as e:
            print(f'Warning: Could not load {data_file}: {e}')

# Analyze bugs
results = {
    'matched_bugs': [],
    'unmatched_bugs': [],
    'summary': {
        'total_bugs': len(set(BUG_IDS)),
        'matched_count': 0,
        'unmatched_count': 0,
        'ic_customers': set(),
        'mcs_customers': set()
    }
}

for bug_id in sorted(set(BUG_IDS)):
    bug_entry = {
        'BugId': bug_id,
        'Link': f'https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug_id}',
        'Customers': [],
        'MatchMethod': []
    }
    
    # Check if we have bug data
    if bug_id in bugs_data:
        bug_data = bugs_data[bug_id]
        bug_entry['Title'] = bug_data.get('title') or bug_data.get('Description') or 'N/A'
        bug_entry['Status'] = bug_data.get('state') or bug_data.get('Status') or 'Unknown'
        bug_entry['Tags'] = bug_data.get('tags', '')
        
        # Method 1: Check tags and title for customer names
        tags_upper = str(bug_entry['Tags']).upper()
        title_upper = str(bug_entry['Title']).upper()
        
        matched_by_name = set()
        for customer, variations in customer_variations.items():
            for variation in variations:
                if variation in tags_upper or variation in title_upper:
                    program = cases_df[cases_df['TopParentName'] == customer]['Program'].iloc[0]
                    matched_by_name.add((customer, program))
                    bug_entry['MatchMethod'].append(f'Name match: {variation}')
                    break
        
        # Method 2: Check ICM links
        icm_ids = []
        if 'icm_ids' in bug_data:
            icm_ids = bug_data['icm_ids']
        elif 'ICMIds' in bug_data:
            icm_ids = bug_data['ICMIds']
        elif 'IncidentIds' in bug_data:
            icm_ids = bug_data['IncidentIds']
        
        matched_by_icm = set()
        for icm_id in icm_ids:
            try:
                icm_int = int(icm_id)
                if icm_int in icm_to_customer:
                    for case_info in icm_to_customer[icm_int]:
                        matched_by_icm.add((case_info['Customer'], case_info['Program']))
                        bug_entry['MatchMethod'].append(f'ICM link: {icm_int}')
            except (ValueError, TypeError):
                pass
        
        # Combine matches
        all_matches = matched_by_name.union(matched_by_icm)
        
        for customer, program in all_matches:
            bug_entry['Customers'].append({
                'Customer': customer,
                'Program': program
            })
            
            if program == 'IC':
                results['summary']['ic_customers'].add(customer)
            else:
                results['summary']['mcs_customers'].add(customer)
    
    else:
        bug_entry['Title'] = 'Data not available - needs ADO query'
        bug_entry['Status'] = 'Unknown'
        bug_entry['Note'] = 'Bug data not found in local cache'
    
    if bug_entry['Customers']:
        results['matched_bugs'].append(bug_entry)
        results['summary']['matched_count'] += 1
    else:
        results['unmatched_bugs'].append(bug_entry)
        results['summary']['unmatched_count'] += 1

# Print report
print(f'\n✅ Bugs Matched to IC/MCS Customers: {results["summary"]["matched_count"]}')
print(f'❌ Bugs NOT Matched (or data unavailable): {results["summary"]["unmatched_count"]}')
print(f'📊 IC Customers: {len(results["summary"]["ic_customers"])}')
print(f'📊 MCS Customers: {len(results["summary"]["mcs_customers"])}')

print('\n' + '=' * 100)
print('MATCHED BUGS')
print('=' * 100)

for bug in results['matched_bugs']:
    print(f'\n[Bug {bug["BugId"]}] {bug.get("Status", "Unknown")}')
    print(f'  Title: {bug.get("Title", "N/A")[:80]}')
    print(f'  Customers:')
    for cust in bug['Customers']:
        print(f'    - {cust["Customer"]} ({cust["Program"]})')
    if bug.get('MatchMethod'):
        print(f'  Match Method: {", ".join(bug["MatchMethod"][:2])}')
    print(f'  Link: {bug["Link"]}')

print('\n' + '=' * 100)
print('UNMATCHED OR DATA UNAVAILABLE')
print('=' * 100)

for bug in results['unmatched_bugs']:
    print(f'\n[Bug {bug["BugId"]}]')
    print(f'  Status: {bug.get("Status", "Unknown")}')
    if 'Note' in bug:
        print(f'  Note: {bug["Note"]}')
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
            'Status': bug.get('Status', 'Unknown'),
            'Program': cust['Program'],
            'Link': bug['Link']
        })

# Sort by program and customer name
sorted_customers = sorted(customer_bugs.items(), 
                         key=lambda x: (customer_bugs[x[0]][0]['Program'], x[0]))

for customer, bugs in sorted_customers:
    program = bugs[0]['Program']
    print(f'\n{customer} ({program}) - {len(bugs)} bugs:')
    for bug in bugs:
        print(f'  - Bug {bug["BugId"]} [{bug["Status"]}]: {bug["Link"]}')

# Save results
output_file = 'data/bug_customer_matches.json'
results['summary']['ic_customers'] = list(results['summary']['ic_customers'])
results['summary']['mcs_customers'] = list(results['summary']['mcs_customers'])

with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f'\n✅ Results saved to: {output_file}')
print('=' * 100)
