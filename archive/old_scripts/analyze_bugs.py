import pandas as pd
import csv

# Bug summary from ICM database
bugs_summary = {
    # Batch 1 - Bugs from first query
    616515906: {'BugId': 2245477, 'ExternalId': '5806337', 'Status': 'Active', 'Owner': 'Deepak Kasera', 'Desc': 'MCE Discrepancy in SIT detection'},
    659601256: {'BugId': 2341494, 'ExternalId': '5995267', 'Status': 'Active', 'Owner': 'Manshi Mishra', 'Desc': 'Missing DPA logs for Barclays'},
    675908430: {'BugId': 2444294, 'ExternalId': '2755112', 'Status': 'Done', 'Owner': 'Kartik Mahajan', 'Desc': 'Labels V Next SetLabel fix'},
    681780305: {'BugId': 2462495, 'ExternalId': '6254385', 'Status': 'Active', 'Owner': 'Yamuna J K', 'Desc': 'Morgan Stanley EDM token separators'},
    703334015: {'BugId': 2473589, 'ExternalId': '6306283', 'Status': 'New', 'Owner': 'Karthik Kandasamy', 'Desc': 'DLP Missing Key Info in Audit Logs'},
    712466636: {'BugId': 2463321, 'ExternalId': '6281633', 'Status': 'New', 'Owner': 'Karthik Kandasamy', 'Desc': 'Policy rename feature not working'},
    717527954: {'BugId': 2547359, 'ExternalId': '6771882', 'Status': 'New', 'Owner': 'Manshi Mishra', 'Desc': 'DLP EXO True file type detection'},
    # Batch 2 - Bugs from second query
    718445455: {'BugId': 2587444, 'ExternalId': '60605756', 'Status': 'Resolved', 'Owner': 'Aman Jha', 'Desc': 'DLP User scoping map preparation fails'},
    718828407: {'BugId': 2647484, 'ExternalId': '6927933', 'Status': 'New', 'Owner': 'Pavel Garmashov', 'Desc': 'DPS Cache Key Collision Causes False Positives'},
    719005833: {'BugId': 2604893, 'ExternalId': '6831758', 'Status': 'Active', 'Owner': 'Lillian Meng', 'Desc': 'Search: Increase support for large tenant wide SPO queries'},
    721235722: {'BugId': 2576070, 'ExternalId': '6794267', 'Status': 'New', 'Owner': 'Monica Aripaka', 'Desc': 'DLP Policy authoring experience permission issues'},
    726565549: {'BugId': 2596747, 'ExternalId': '6821575', 'Status': 'New', 'Owner': 'Mansi Agrawal', 'Desc': 'DLP SPO MatchedSITAndSurroundingcontext shows actual SIT'},
    728619885: {'BugId': 2617845, 'ExternalId': '6868007', 'Status': 'New', 'Owner': 'Nitin Kumar Maharana', 'Desc': 'Publish Hold Policy Scope Status in batches'},
    731474122: {'BugId': 2226345, 'ExternalId': '4744455', 'Status': 'Closed', 'Owner': 'Vishu Chhabra', 'Desc': 'Message only evaluation not working for OWA policy tips'},
    731622085: {'BugId': 2639826, 'ExternalId': '6902454', 'Status': 'New', 'Owner': 'Tomas Fonseca', 'Desc': 'Batch Infra: Improve Search job performance'},
}

print('=== ICM BUGS FOUND FOR CASES WAITING FOR PRODUCT TEAM ===')
print(f'Total ICMs with bugs: {len(bugs_summary)}')

# Count statuses
status_counts = {}
for bug in bugs_summary.values():
    status = bug['Status']
    status_counts[status] = status_counts.get(status, 0) + 1

status_str = ', '.join([f'{count} {status}' for status, count in sorted(status_counts.items())])
print(f'Status: {status_str}\n')

# Create CSV with ADO links
with open(r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\data\icm_bugs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['IncidentId', 'BugId', 'ExternalId', 'Status', 'Owner', 'Description', 'AdoLink'])
    for icm, bug in bugs_summary.items():
        ado_link = f"https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug['BugId']}"
        writer.writerow([icm, bug['BugId'], bug['ExternalId'], bug['Status'], bug['Owner'], bug['Desc'], ado_link])
        print(f"ICM {icm}: Bug {bug['BugId']} ({bug['ExternalId']})")
        print(f"  Status: {bug['Status']} | Owner: {bug['Owner']}")
        print(f"  {bug['Desc']}")
        print(f"  ADO: {ado_link}\n")

print('✓ Saved to icm_bugs.csv')

# Now link bugs to cases
df = pd.read_csv(r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\data\production_full_cases.csv')
print(f'\n=== MATCHING BUGS TO CASES ===')
print(f'Total cases in CSV: {len(df)}')

# Find cases with these ICMs
for icm, bug in bugs_summary.items():
    matching_cases = df[df['RelatedICM_Id'].astype(str).str.contains(str(icm), na=False)]
    if len(matching_cases) > 0:
        for _, case in matching_cases.iterrows():
            print(f"\nCase {case['ServiceRequestNumber']} - {case['TopParentName']}")
            print(f"  ICM {icm}: {bug['Desc']}")
            print(f"  Bug Status: {bug['Status']} | Owner: {bug['Owner']}")
            print(f"  Case Status: {case['ServiceRequestStatus']}")
    else:
        print(f"\nNo cases found for ICM {icm}")
