"""
Fetch ADO bugs and extract ICM hyperlinks to map to IC/MCS customers
"""
import json
import pandas as pd
import re

# Load IC/MCS ICM data
with open('data/icm_ids_for_ado_search.json', 'r') as f:
    icm_data = json.load(f)

ic_mcs_icm_ids = set(icm_data['icm_ids'])
icm_to_customer = {int(k): v for k, v in icm_data['icm_to_customer'].items()}

print('=' * 100)
print('ADO BUGS LINKED TO IC/MCS CUSTOMER ICMS')
print('=' * 100)
print(f'\nSearching for bugs with hyperlinks to {len(ic_mcs_icm_ids)} IC/MCS ICM incidents')

# Process the search results
with open(r'c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\08a9d21f-9c04-4a6b-ab5a-c4fd011fc61f\toolu_015M3XnnUAeVRVA6uxuQoipW__vscode-1770399796729\content.json', 'r', encoding='utf-8') as f:
    search_results = json.load(f)

bugs_to_fetch = [result['fields']['system.id'] for result in search_results['results']]

print(f'\nFound {len(bugs_to_fetch)} Customer Escalation bugs to check')
print(f'\nBugs: {", ".join(bugs_to_fetch[:20])}{"..." if len(bugs_to_fetch) > 20 else ""}')

# Save list for batch processing
with open('data/ado_bugs_to_fetch.json', 'w') as f:
    json.dump({'bug_ids': bugs_to_fetch}, f, indent=2)

print(f'\n✓ Saved {len(bugs_to_fetch)} bug IDs to: data/ado_bugs_to_fetch.json')
print(f'\nNext: Will fetch full details with relations for these bugs using ADO MCP')
print('=' * 100)
