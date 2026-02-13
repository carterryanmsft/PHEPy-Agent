"""
Analyze bugs linked to IC and MCS customer incidents from ICM query results
"""
import json

# Read the bug results
with open(r'c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\08a9d21f-9c04-4a6b-ab5a-c4fd011fc61f\toolu_01RgKsEHkdiAS16jS7K359Rn__vscode-1770399796706\content.txt', 'r') as f:
    content = f.read()
    
# Parse JSON to find unique bugs
start_idx = content.find('"data": [')
end_idx = content.rfind(']')
json_str = '{' + content[start_idx:end_idx+1] + '}'
data = json.loads(json_str)

bugs = {}
for bug in data['data']:
    bug_key = f"{bug['ExternalId']}"
    if bug_key not in bugs:
        bugs[bug_key] = {
            'ExternalId': bug['ExternalId'],
            'Status': bug['Status'],
            'Owner': bug['Owner'],
            'Description': bug['Description'],
            'IncidentIds': set(),
            'Type': bug['Type'],
            'Source': bug['Source'],
            'CreatedDate': bug['CreatedDate'],
            'ModifiedDate': bug['ModifiedDate']
        }
    bugs[bug_key]['IncidentIds'].add(bug['IncidentId'])

# Summary
print('=' * 80)
print('IC/MCS BUGS FROM ICM SUMMARY')
print('=' * 80)
print(f'Total Unique Bugs: {len(bugs)}')
print(f'Total Bug-Incident Links: {len(data["data"])}')

# Count by status
status_counts = {}
for bug in bugs.values():
    status = bug['Status']
    status_counts[status] = status_counts.get(status, 0) + 1

print(f'\nBugs by Status:')
for status, count in sorted(status_counts.items()):
    print(f'  {status}: {count}')

# Count by source
source_counts = {}
for bug in bugs.values():
    source = bug['Source']
    source_counts[source] = source_counts.get(source, 0) + 1

print(f'\nBugs by Source:')
for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
    print(f'  {source}: {count}')

# Convert sets to lists for JSON
bugs_for_export = []
for bug in bugs.values():
    bug_copy = bug.copy()
    bug_copy['IncidentIds'] = sorted(list(bug['IncidentIds']))
    bug_copy['ICM_Count'] = len(bug_copy['IncidentIds'])
    bugs_for_export.append(bug_copy)

# Save summary
with open('data/ic_mcs_bugs_from_icm.json', 'w') as f:
    json.dump(bugs_for_export, f, indent=2)

print(f'\n✓ Saved detailed summary to: data/ic_mcs_bugs_from_icm.json')

# Top 15 bugs by incident count
print(f'\n' + '=' * 80)
print('TOP 15 BUGS (by ICM count)')
print('=' * 80)
sorted_bugs = sorted(bugs_for_export, key=lambda x: x['ICM_Count'], reverse=True)[:15]
for i, bug in enumerate(sorted_bugs, 1):
    icm_count = bug['ICM_Count']
    print(f"\n{i}. Bug {bug['ExternalId']} - Status: {bug['Status']} - ICMs: {icm_count}")
    print(f"   Source: {bug['Source']}")
    print(f"   Owner: {bug['Owner'].split('<')[0].strip()}")
    print(f"   Description: {bug['Description'][:100]}...")
    print(f"   Link: https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug['ExternalId']}")

# Open bugs only
print(f'\n' + '=' * 80)
print('OPEN BUGS (Active or New)')
print('=' * 80)
open_bugs = [b for b in sorted_bugs if b['Status'] in ['Active', 'New']]
print(f'Total Open Bugs: {len([b for b in bugs_for_export if b["Status"] in ["Active", "New"]])}')
for i, bug in enumerate(open_bugs[:10], 1):
    icm_count = bug['ICM_Count']
    print(f"\n{i}. Bug {bug['ExternalId']} - Status: {bug['Status']} - ICMs: {icm_count}")
    print(f"   Owner: {bug['Owner'].split('<')[0].strip()}")
    print(f"   Description: {bug['Description'][:80]}...")
    print(f"   Link: https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug['ExternalId']}")

print('\n' + '=' * 80)
print('ANALYSIS COMPLETE!')
print('=' * 80)
