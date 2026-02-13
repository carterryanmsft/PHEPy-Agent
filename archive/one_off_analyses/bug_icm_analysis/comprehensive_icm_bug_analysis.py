"""
Comprehensive analysis of bugs linked to IC/MCS customer ICMs
Finds bugs in two ways:
1. Bugs linked as repair items in IncidentBugs table
2. Bug URLs mentioned in ICM comments/descriptions
"""
import json
import pandas as pd
import re

# Load customer case data
cases_df = pd.read_csv('data/production_full_cases.csv')

# Create ICM to customer mapping
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
                        'CaseNumber': case['ServiceRequestNumber'],
                        'RiskScore': case['RiskScore'],
                        'Status': case['ServiceRequestStatus']
                    })
                except ValueError:
                    pass

print('=' * 100)
print('BUGS LINKED TO IC/MCS CUSTOMER ICMS')
print('=' * 100)

# Method 1: Bugs from IncidentBugs table (repair items)
repair_item_bugs = {
    703334015: {'bug_id': '6306283', 'status': 'New', 'count': 44},
    681780305: {'bug_id': '6254385', 'status': 'Active/New', 'count': 40},
    616515906: {'bug_id': '5806337', 'status': 'Closed', 'count': 31},
    659601256: {'bug_id': '5995267', 'status': 'Closed', 'count': 16},
    718445455: {'bug_id': '60605756', 'status': 'Resolved/Active', 'count': 13},
    721235722: {'bug_id': '6794267', 'status': 'New', 'count': 9},
    675908430: {'bug_id': '2755112', 'status': 'Done', 'count': 9},
    712466636: {'bug_id': '6281633', 'status': 'Closed', 'count': 7},
    701554955: {'bug_id': '6296924', 'status': 'Resolved/New', 'count': 7},
    718828407: {'bug_id': '6927933', 'status': 'Closed', 'count': 6},
    680275765: {'bug_id': '21227', 'status': 'Removed', 'count': 2}
}

print('\n' + '=' * 100)
print('METHOD 1: BUGS LINKED AS REPAIR ITEMS (from IncidentBugs table)')
print('=' * 100)
print(f'\nFound {len(repair_item_bugs)} ICMs with bugs linked as repair items\n')

# Group by customer
customer_repair_bugs = {}
for icm_id, bug_info in repair_item_bugs.items():
    if icm_id in icm_to_customer:
        for case_info in icm_to_customer[icm_id]:
            customer = case_info['Customer']
            if customer not in customer_repair_bugs:
                customer_repair_bugs[customer] = {
                    'Program': case_info['Program'],
                    'Bugs': []
                }
            
            customer_repair_bugs[customer]['Bugs'].append({
                'ICM': icm_id,
                'BugId': bug_info['bug_id'],
                'Status': bug_info['status'],
             'LinkCount': bug_info['count'],
                'CaseNumber': case_info['CaseNumber']
            })

# Display by customer
for customer, data in sorted(customer_repair_bugs.items()):
    print(f'\n[{customer}] {data["Program"]} - {len(data["Bugs"])} Bug(s)')
    
    # Get unique bugs
    unique_bugs = {}
    for bug in data['Bugs']:
        if bug['BugId'] not in unique_bugs:
            unique_bugs[bug['BugId']] = bug
    
    for bug_id, bug in unique_bugs.items():
        print(f'  🔗 Bug {bug["BugId"]} ({bug["Status"]})')
        print(f'     ICM: {bug["ICM"]} | Case: {bug["CaseNumber"]} | Links: {bug["LinkCount"]}')
        print(f'     https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug_id}')

# Summary stats
print('\n' + '=' * 100)
print('REPAIR ITEM STATS')
print('=' * 100)

total_bugs = len(set(bug['bug_id'] for bug in repair_item_bugs.values()))
total_customers = len(customer_repair_bugs)

print(f'\n📊 Total Unique Bugs as Repair Items: {total_bugs}')
print(f'📊 Total IC/MCS Customers: {total_customers}')

ic_customers = [c for c, d in customer_repair_bugs.items() if d['Program'] == 'IC']
mcs_customers = [c for c, d in customer_repair_bugs.items() if d['Program'] == 'MCS']

print(f'\n  IC Customers: {len(ic_customers)}')
for customer in ic_customers:
    bug_count = len(set(b['BugId'] for b in customer_repair_bugs[customer]['Bugs']))
    print(f'    - {customer}: {bug_count} bug(s)')

print(f'\n  MCS Customers: {len(mcs_customers)}')
for customer in mcs_customers:
    bug_count = len(set(b['BugId'] for b in customer_repair_bugs[customer]['Bugs']))
    print(f'    - {customer}: {bug_count} bug(s)')

# Method 2: Bug URLs mentioned in comments (from earlier query)
print('\n' + '=' * 100)
print('METHOD 2: BUG URLs MENTIONED IN ICM COMMENTS/DESCRIPTIONS')
print('=' * 100)
print(f'\nFound multiple ICMs that mention bug URLs in their comments')
print(f'⚠️  Note: Text extraction needed to parse actual bug IDs from URLs')
print(f'Sample ICMs with bug mentions:')
print(f'  • ICM 731225498 - State of WA - Mentions bug URLs in Summary')
print(f'  • Additional ICMs found in query results (1900+ entries)')

# Save comprehensive results
output = {
    'repair_item_bugs': {
        'total_bugs': total_bugs,
        'total_icms': len(repair_item_bugs),
        'total_customers': total_customers,
        'by_customer': customer_repair_bugs,
        'raw_data': repair_item_bugs
    },
    'summary': {
        'method_1_bugs': total_bugs,
        'method_1_icms': len(repair_item_bugs),
        'method_1_customers': total_customers,
        'method_2_note': 'Additional bug mentions found in ICM comments - requires text parsing'
    }
}

with open('data/comprehensive_icm_bug_analysis.json', 'w') as f:
    json.dump(output, f, indent=2)

print('\n' + '=' * 100)
print('COMPLETE MAPPING')
print('=' * 100)

# Create final comprehensive list
all_bug_icm_mappings = []
for icm_id, bug_info in repair_item_bugs.items():
    if icm_id in icm_to_customer:
        customers = list(set(c['Customer'] for c in icm_to_customer[icm_id]))
        programs = list(set(c['Program'] for c in icm_to_customer[icm_id]))
        cases = [c['CaseNumber'] for c in icm_to_customer[icm_id]]
        
        all_bug_icm_mappings.append({
            'ICM': icm_id,
            'Bug': bug_info['bug_id'],
            'Status': bug_info['status'],
            'Customers': customers,
            'Programs': programs,
            'Cases': cases,
            'LinkCount': bug_info['count'],
            'BugURL': f"https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug_info['bug_id']}"
        })

print(f'\n✅ Complete: {len(all_bug_icm_mappings)} Bug-ICM-Customer mappings')
print(f'✓ Saved to: data/comprehensive_icm_bug_analysis.json')

# Show final summary table
print('\n' + '=' * 100)
print('FINAL SUMMARY TABLE')
print('=' * 100)
print(f'\n{"Bug ID":<15} {"Status":<20} {"ICM":<15} {"Customer":<20} {"Program":<10}')
print('-' * 100)

for mapping in sorted(all_bug_icm_mappings, key=lambda x: (x['Programs'][0], x['Customers'][0])):
    bug_id = mapping['Bug']
    status = mapping['Status'][:18]
    icm = str(mapping['ICM'])
    customer = mapping['Customers'][0][:18] if mapping['Customers'] else 'N/A'
    program = mapping['Programs'][0] if mapping['Programs'] else 'N/A'
    
    print(f'{bug_id:<15} {status:<20} {icm:<15} {customer:<20} {program:<10}')

print('\n' + '=' * 100)
