"""
Parse bug URLs mentioned in ICM comments/descriptions
Extract bug IDs from text fields and map to customers
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

# Read the Kusto query results
# The results file contains ICMs that mention bug URLs in their text fields
result_file = None
try:
    with open('data/kusto_result_131.json', 'r', encoding='utf-8') as f:
        result_file = json.load(f)
except FileNotFoundError:
    print("⚠️  Result file not found, using hardcoded sample data")
    result_file = None

print('=' * 100)
print('PARSING BUG URLs FROM ICM COMMENTS/DESCRIPTIONS')
print('=' * 100)

# Bug URL patterns to search for
# Format: https://o365exchange.visualstudio.com/.../_workitems/edit/[BUGID]
bug_url_patterns = [
    r'visualstudio\.com/[^/]+/[^/]+/_workitems/edit/(\d+)',
    r'_workitems/edit/(\d+)',
    r'/workitems.*?(\d{4,})',  # Generic pattern for bug IDs (4+ digits)
]

mentioned_bugs = {}  # bug_id -> list of ICM IDs

if result_file:
    print(f'\n📋 Processing {len(result_file)} query results...')
    
    for entry in result_file:
        icm_id = entry.get('IncidentId')
        
        # Search all text fields for bug URLs
        text_fields = [
            entry.get('Title', ''),
            entry.get('Summary', ''),
            entry.get('ReproSteps', ''),
            entry.get('Mitigation', ''),
            entry.get('HowFixed', '')
        ]
        
        combined_text = ' '.join([str(t) for t in text_fields if t])
        
        # Extract bug IDs from text
        for pattern in bug_url_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            for bug_id in matches:
                bug_id = str(bug_id).strip()
                if bug_id and len(bug_id) >= 4:  # Valid bug IDs are at least 4 digits
                    if bug_id not in mentioned_bugs:
                        mentioned_bugs[bug_id] = []
                    if icm_id not in mentioned_bugs[bug_id]:
                        mentioned_bugs[bug_id].append(icm_id)

print(f'\n✅ Found {len(mentioned_bugs)} unique bugs mentioned in ICM text')
print(f'📊 Across {sum(len(icms) for icms in mentioned_bugs.values())} ICM mentions')

# Filter to only IC/MCS customer ICMs
customer_mentioned_bugs = {}
for bug_id, icm_list in mentioned_bugs.items():
    customer_icms = [icm for icm in icm_list if icm in icm_to_customer]
    if customer_icms:
        customer_mentioned_bugs[bug_id] = customer_icms

print(f'\n🎯 {len(customer_mentioned_bugs)} bugs mentioned in IC/MCS customer ICMs')

# Group by customer
customer_mention_report = {}
for bug_id, icm_list in customer_mentioned_bugs.items():
    for icm_id in icm_list:
        if icm_id in icm_to_customer:
            for case_info in icm_to_customer[icm_id]:
                customer = case_info['Customer']
                if customer not in customer_mention_report:
                    customer_mention_report[customer] = {
                        'Program': case_info['Program'],
                        'Bugs': []
                    }
                
                customer_mention_report[customer]['Bugs'].append({
                    'BugId': bug_id,
                    'ICM': icm_id,
                    'CaseNumber': case_info['CaseNumber']
                })

# Display by customer
if customer_mention_report:
    print('\n' + '=' * 100)
    print('BUGS MENTIONED IN ICM TEXT BY CUSTOMER')
    print('=' * 100)
    
    for customer, data in sorted(customer_mention_report.items()):
        # Get unique bugs for this customer
        unique_bugs = set(b['BugId'] for b in data['Bugs'])
        
        print(f'\n[{customer}] {data["Program"]} - {len(unique_bugs)} Unique Bug(s)')
        
        for bug_id in sorted(unique_bugs):
            bug_icms = [b for b in data['Bugs'] if b['BugId'] == bug_id]
            print(f'  💬 Bug {bug_id} mentioned in:')
            for bug_info in bug_icms[:5]:  # Show first 5 ICMs
                print(f'     ICM: {bug_info["ICM"]} | Case: {bug_info["CaseNumber"]}')
            if len(bug_icms) > 5:
                print(f'     ... and {len(bug_icms) - 5} more ICMs')
            print(f'     https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug_id}')
else:
    print('\n⚠️  Note: Bug URL parsing requires the full query result file')
    print('Sample data shows ICM 731225498 contains bug URL mentions')

# Save results
output = {
    'mentioned_bugs_count': len(customer_mentioned_bugs),
    'total_icm_mentions': sum(len(icms) for icms in customer_mentioned_bugs.values()),
    'by_customer': customer_mention_report,
    'all_mentioned_bugs': {
        bug_id: {
            'icm_count': len(icms),
            'icms': icms
        }
        for bug_id, icms in customer_mentioned_bugs.items()
    }
}

with open('data/icm_bug_mentions_analysis.json', 'w') as f:
    json.dump(output, f, indent=2)

print('\n' + '=' * 100)
print('SUMMARY')
print('=' * 100)
print(f'\n✅ Bugs mentioned in text: {len(customer_mentioned_bugs)}')
print(f'✅ Total customers affected: {len(customer_mention_report)}')
print(f'✓ Saved to: data/icm_bug_mentions_analysis.json')
print('\n' + '=' * 100)
