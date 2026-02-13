"""
Extract all ICM IDs from IC/MCS customer cases to search in Azure DevOps
"""
import pandas as pd
import json

# Load production cases
cases_df = pd.read_csv('data/production_full_cases.csv')

# Extract all unique ICM IDs from IC/MCS cases
all_icm_ids = set()
icm_to_customer = {}

for _, case in cases_df.iterrows():
    if pd.notna(case['RelatedICM_Id']) and case['RelatedICM_Id']:
        icm_ids = str(case['RelatedICM_Id']).replace(',', ';').split(';')
        for icm_id in icm_ids:
            icm_id = icm_id.strip()
            if icm_id:
                try:
                    icm_int = int(icm_id)
                    all_icm_ids.add(icm_int)
                    
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
print('ICM IDs FOR AZURE DEVOPS SEARCH')
print('=' * 100)

print(f'\nTotal Unique ICM IDs: {len(all_icm_ids)}')

# Sort by ICM ID
sorted_icms = sorted(all_icm_ids)

# Show some samples
print(f'\nSample ICM IDs (first 20):')
for icm_id in sorted_icms[:20]:
    customers = [c['Customer'] for c in icm_to_customer[icm_id]]
    unique_customers = list(set(customers))
    print(f'  {icm_id}: {", ".join(unique_customers[:3])}{"..." if len(unique_customers) > 3 else ""}')

# Save for ADO search
output = {
    'icm_ids': sorted_icms,
    'icm_to_customer': {str(k): v for k, v in icm_to_customer.items()},
    'total_icms': len(all_icm_ids)
}

with open('data/icm_ids_for_ado_search.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f'\n✓ Saved to: data/icm_ids_for_ado_search.json')

# Generate ICM URL patterns for search
print(f'\n' + '=' * 100)
print('ICM URL PATTERNS')
print('=' * 100)
print('\nWill search for bugs with hyperlinks matching these patterns:')
print('  https://portal.microsofticm.com/imp/v3//incidents/details/{ICM_ID}/home')
print('  https://portal.microsofticm.com/imp/v5/incidents/details/{ICM_ID}/home')

print('\n' + '=' * 100)
