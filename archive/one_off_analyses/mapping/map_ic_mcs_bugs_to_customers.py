"""
Map bugs to specific IC/MCS customers
"""
import json
import pandas as pd

# Load production cases to get customer mappings
cases_df = pd.read_csv('data/production_full_cases.csv')

# Load bug summary from ICM
with open('data/ic_mcs_bugs_from_icm.json', 'r') as f:
    bugs = json.load(f)

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
                        'DaysOpen': case['DaysOpen'],
                        'Status': case['ServiceRequestStatus']
                    })
                except ValueError:
                    pass

# Map bugs to customers
customer_bugs = {}
bug_details = []

for bug in bugs:
    bug_entry = {
        'BugId': bug['ExternalId'],
        'Status': bug['Status'],
        'Description': bug['Description'],
        'Owner': bug['Owner'].split('<')[0].strip(),
        'Source': bug['Source'],
        'Customers': []
    }
    
    for icm_id in bug['IncidentIds']:
        if icm_id in icm_to_customer:
            for case_info in icm_to_customer[icm_id]:
                customer = case_info['Customer']
                program = case_info['Program']
                
                # Add to customer mapping
                if customer not in customer_bugs:
                    customer_bugs[customer] = {
                        'Program': program,
                        'Bugs': []
                    }
                
                bug_info = {
                    'BugId': bug['ExternalId'],
                    'Status': bug['Status'],
                    'ICM': icm_id,
                    'CaseNumber': case_info['CaseNumber'],
                    'Description': bug['Description'],
                    'Owner': bug['Owner'].split('<')[0].strip(),
                    'Link': f"https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug['ExternalId']}"
                }
                
                customer_bugs[customer]['Bugs'].append(bug_info)
                
                # Add to bug entry
                bug_entry['Customers'].append({
                    'Customer': customer,
                    'Program': program,
                    'CaseNumber': case_info['CaseNumber'],
                    'ICM': icm_id
                })
    
    bug_details.append(bug_entry)

# Print report
print('=' * 100)
print('IC/MCS BUGS BY CUSTOMER')
print('=' * 100)

# Sort by program (IC first, then MCS)
sorted_customers = sorted(customer_bugs.items(), key=lambda x: (x[1]['Program'], x[0]))

ic_customers = [(k, v) for k, v in sorted_customers if v['Program'] == 'IC']
mcs_customers = [(k, v) for k, v in sorted_customers if v['Program'] == 'MCS']

print(f'\nTotal IC Customers with Bugs: {len(ic_customers)}')
print(f'Total MCS Customers with Bugs: {len(mcs_customers)}')

print('\n' + '=' * 100)
print('IC (INCIDENT COMMANDER) CUSTOMERS')
print('=' * 100)

for customer, data in ic_customers:
    unique_bugs = {}
    for bug in data['Bugs']:
        if bug['BugId'] not in unique_bugs:
            unique_bugs[bug['BugId']] = bug
    
    print(f'\n[{customer}] - {len(unique_bugs)} Bug(s)')
    for bug_id, bug in unique_bugs.items():
        status_emoji = '🟢' if bug['Status'] == 'Closed' else '🔴' if bug['Status'] in ['Active', 'New'] else '🟡'
        print(f'  {status_emoji} Bug {bug["BugId"]} ({bug["Status"]})')
        print(f'     Case: {bug["CaseNumber"]} | ICM: {bug["ICM"]}')
        print(f'     Owner: {bug["Owner"]}')
        print(f'     {bug["Description"][:90]}...')
        print(f'     {bug["Link"]}')

print('\n' + '=' * 100)
print('MCS (MICROSOFT CONSULTING SERVICES) CUSTOMERS')
print('=' * 100)

for customer, data in mcs_customers:
    unique_bugs = {}
    for bug in data['Bugs']:
        if bug['BugId'] not in unique_bugs:
            unique_bugs[bug['BugId']] = bug
    
    print(f'\n[{customer}] - {len(unique_bugs)} Bug(s)')
    for bug_id, bug in unique_bugs.items():
        status_emoji = '🟢' if bug['Status'] == 'Closed' else '🔴' if bug['Status'] in ['Active', 'New'] else '🟡'
        print(f'  {status_emoji} Bug {bug["BugId"]} ({bug["Status"]})')
        print(f'     Case: {bug["CaseNumber"]} | ICM: {bug["ICM"]}')
        print(f'     Owner: {bug["Owner"]}')
        print(f'     {bug["Description"][:90]}...')
        print(f'     {bug["Link"]}')

# Summary stats
print('\n' + '=' * 100)
print('SUMMARY STATISTICS')
print('=' * 100)

total_ic_bugs = sum(len(set(b['BugId'] for b in data['Bugs'])) for c, data in ic_customers)
total_mcs_bugs = sum(len(set(b['BugId'] for b in data['Bugs'])) for c, data in mcs_customers)

print(f'\nIC Program:')
print(f'  Customers: {len(ic_customers)}')
print(f'  Unique Bugs: {total_ic_bugs}')

print(f'\nMCS Program:')
print(f'  Customers: {len(mcs_customers)}')
print(f'  Unique Bugs: {total_mcs_bugs}')

# Save mapping
export_data = {
    'customer_bugs': customer_bugs,
    'bug_details': bug_details,
    'summary': {
        'ic_customers': len(ic_customers),
        'mcs_customers': len(mcs_customers),
        'ic_bugs': total_ic_bugs,
        'mcs_bugs': total_mcs_bugs,
        'total_customers': len(customer_bugs),
        'total_unique_bugs': len(bugs)
    }
}

with open('data/ic_mcs_customer_bug_mapping.json', 'w') as f:
    json.dump(export_data, f, indent=2)

print(f'\n✓ Saved detailed mapping to: data/ic_mcs_customer_bug_mapping.json')
print('=' * 100)
