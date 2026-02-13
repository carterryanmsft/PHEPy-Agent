"""
Process Azure DevOps search results to find bugs with IC/MCS customer ICM hyperlinks
"""
import json
import pandas as pd
import re

# Load ICM IDs for IC/MCS customers
with open('data/icm_ids_for_ado_search.json', 'r') as f:
    icm_data = json.load(f)

ic_mcs_icm_ids = set(icm_data['icm_ids'])
icm_to_customer = {int(k): v for k, v in icm_data['icm_to_customer'].items()}

print('=' * 100)
print('PROCESSING ADO SEARCH RESULTS FOR IC/MCS ICM LINKS')
print('=' * 100)
print(f'\nLooking for bugs linked to {len(ic_mcs_icm_ids)} IC/MCS customer ICM incidents')

# Load ADO search results
with open(r'c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\08a9d21f-9c04-4a6b-ab5a-c4fd011fc61f\toolu_01LRfmvrc5hePviEijbUC59s__vscode-1770399796722\content.json', 'r', encoding='utf-8') as f:
    search_results = json.load(f)

print(f'\nTotal bugs found in search: {search_results["count"]}')
print(f'Processing first {len(search_results["results"])} results...')

# Extract work item IDs that might have ICM links
work_item_ids = []
potential_matches = {}

icm_url_pattern = re.compile(r'microsofticm\.com/imp/v[35]/incidents/details/(\d+)')

for result in search_results['results']:
    work_item_id = result['fields']['system.id']
    title = result['fields'].get('system.title', '')
    
    # Check if title or highlights contain ICM URLs
    all_text = title
    
    if 'hits' in result:
        for hit in result['hits']:
            if 'highlights' in hit:
                for highlight in hit['highlights']:
                    all_text += ' ' + highlight
    
    # Find all ICM IDs in the text
    icm_matches = icm_url_pattern.findall(all_text)
    
    if icm_matches:
        icm_ids_in_bug = [int(m) for m in icm_matches]
        
        # Check if any match our IC/MCS ICMs
        matching_icms = [icm for icm in icm_ids_in_bug if icm in ic_mcs_icm_ids]
        
        if matching_icms:
            work_item_ids.append(work_item_id)
            potential_matches[work_item_id] = {
                'title': title,
                'state': result['fields'].get('system.state'),
                'tags': result['fields'].get('system.tags', ''),
                'icm_ids': matching_icms
            }

print(f'\n✓ Found {len(work_item_ids)} bugs with potential IC/MCS ICM links')

# Save work item IDs for detailed fetch
output = {
    'work_item_ids': work_item_ids,
    'potential_matches': potential_matches,
    'total_found': len(work_item_ids)
}

with open('data/ado_bugs_with_icms.json', 'w') as f:
    json.dump(output, f, indent=2)

# Show summary
print(f'\n' + '=' * 100)
print('POTENTIAL MATCHES (Sample - First 20)')
print('=' * 100)

for work_item_id, info in list(potential_matches.items())[:20]:
    icm_ids_str = ', '.join(str(i) for i in info['icm_ids'][:5])
    if len(info['icm_ids']) > 5:
        icm_ids_str += f' +{len(info["icm_ids"]) - 5} more'
    
    print(f'\n[{work_item_id}] {info["state"]} - {info.get("tags", "No tags")}')
    print(f'  {info["title"][:90]}...')
    print(f'  ICMs: {icm_ids_str}')
    
    # Show customers
    customers = set()
    for icm_id in info['icm_ids']:
        if icm_id in icm_to_customer:
            for case in icm_to_customer[icm_id]:
                customers.add(f"{case['Customer']} ({case['Program']})")
    
    if customers:
        print(f'  Customers: {", ".join(list(customers)[:3])}')

print(f'\n✓ Saved to: data/ado_bugs_with_icms.json')
print(f'\nNext: Will fetch full details with hyperlinks for these {len(work_item_ids)} bugs')
print('=' * 100)
