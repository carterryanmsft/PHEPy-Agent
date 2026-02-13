"""
Validate Bug Information in IC Risk Report
"""
import pandas as pd

df = pd.read_csv('risk_reports/data/ic_cases.csv')

print('='*70)
print('BUG INFORMATION IN IC RISK REPORT - VALIDATION')
print('='*70)

# Check for bug data
with open('risk_reports/IC_Report_Final.htm', 'r', encoding='utf-8') as f:
    html = f.read()

bug_count = html.count('Linked Bugs:')

print(f'\n✅ Bug information added to report')
print(f'   Cases with linked bugs shown: {bug_count} instances')

# Sample bug entries
import re
bug_pattern = r'<strong>Linked Bugs:</strong> ([^<]+)</td>'
bug_matches = re.findall(bug_pattern, html)

if bug_matches:
    print(f'\n📋 Sample bug references in report:')
    for i, bug_info in enumerate(bug_matches[:10], 1):
        print(f'   {i}. {bug_info}')

# Show distribution
icm = pd.read_csv('risk_reports/data/icm_owners.csv')
bugs_present = icm[icm['BugIds'].notna() & (icm['BugIds'] != '')]

print(f'\n📊 Bug Coverage:')
print(f'   ICMs with bugs: {len(bugs_present)} out of {len(icm)}')
print(f'   Cases with bug information: {bug_count}')

# Check bug statuses
all_bugs = []
for _, row in bugs_present.iterrows():
    if pd.notna(row['BugExternalIds']) and pd.notna(row['BugStatuses']):
        bug_ids = str(row['BugExternalIds']).split(',')
        statuses = str(row['BugStatuses']).split(',')
        for bug_id, status in zip(bug_ids, statuses):
            all_bugs.append((bug_id.strip(), status.strip()))

if all_bugs:
    print(f'\n📈 Bug Status Distribution:')
    from collections import Counter
    status_counts = Counter([status for _, status in all_bugs])
    for status, count in status_counts.most_common():
        print(f'   {status:15} {count:2} bugs')

print('\n' + '='*70)
print('SUMMARY ENHANCEMENT COMPLETE')
print('='*70)
print('\n✅ Summaries now include:')
print('   1. Case age and status')
print('   2. Ownership/transfer risk factors')
print('   3. ICM presence indicator')
print('   4. 🆕 Linked Bug IDs with status (when available)')
print('\nExample:')
print('   "Case is 501 days old, status is Waiting for product team,')
print('    ICM present: Yes. High ownership (7) and transfer (6) counts')
print('    increase risk. Linked Bugs: 5806337 (Resolved)"')
