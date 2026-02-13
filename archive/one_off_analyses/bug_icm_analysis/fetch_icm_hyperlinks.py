"""
Fetch hyperlinks from IC/MCS customer bugs and map to ICM incidents
"""
import json
import re

# IC/MCS bugs to fetch (from previous analysis)
ic_mcs_bug_ids = [3563451, 4000625, 4676229, 5166846, 5174195, 5193520, 5379952]

print('=' * 100)
print('FETCHING ICM HYPERLINKS FROM IC/MCS CUSTOMER BUGS')
print('=' * 100)
print(f'\nFetching {len(ic_mcs_bug_ids)} bugs with relations...')

# This will be populated by the ADO MCP calls
bugs_with_icm_links = []

# Save the list for the fetch script
with open('data/bugs_to_fetch_with_relations.json', 'w') as f:
    json.dump({'bug_ids': ic_mcs_bug_ids}, f, indent=2)

print(f'✓ Saved bug IDs to: data/bugs_to_fetch_with_relations.json')
print('\nNext: Fetching each bug individually with expand=relations...')
print('=' * 100)
