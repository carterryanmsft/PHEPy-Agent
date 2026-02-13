#!/usr/bin/env python3
"""
Analyze IC Risk Report Results
"""
import json
from collections import Counter
from pathlib import Path

# Read the query results
result_file = Path(r"c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\c53a391a-f578-4281-ab4f-61aa3c57bff7\toolu_01TLrS6D7fCvLJirrxQedqj8__vscode-1770399796315\content.txt")

with open(result_file, 'r', encoding='utf-8') as f:
    content = f.read()
    if content.startswith('Query results:'):
        content = content.replace('Query results:', '').strip()
    data = json.loads(content)

cases = data['data']

# Save to data folder
output_file = Path("data/ic_risk_report_results.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f'✅ Saved to: {output_file}')
print(f'\n📊 IC RISK REPORT SUMMARY')
print('='*70)
print(f'\nTotal High-Risk Cases (20+ days old): {len(cases)}')

print(f'\n🎯 Risk Level Breakdown:')
risk_levels = Counter(c['RiskLevel'] for c in cases)
for level in sorted(risk_levels.keys()):
    print(f'  {level}: {risk_levels[level]}')

print(f'\n🏢 Cases by Customer:')
customers = Counter(c['TopParentName'] for c in cases)
for customer, count in customers.most_common():
    print(f'  {customer}: {count}')

print(f'\n👥 Cases by PHE:')
phes = Counter(c['PHE'] for c in cases if c['PHE'])
for phe, count in phes.most_common():
    print(f'  {phe}: {count}')

print(f'\n🚨 TOP 5 HIGHEST RISK CASES:')
sorted_cases = sorted(cases, key=lambda x: x['RiskScore'], reverse=True)
for case in sorted_cases[:5]:
    print(f'\n  Case: {case["ServiceRequestNumber"]} | Risk: {case["RiskScore"]} ({case["RiskLevel"]})')
    print(f'  Customer: {case["TopParentName"]} | PHE: {case["PHE"]}')
    print(f'  Age: {int(case["DaysOpen"])} days | Status: {case["ServiceRequestStatus"]}')
    print(f'  {case["Summary"][:100]}...')

avg_age = sum(c['DaysOpen'] for c in cases) / len(cases)
max_age = max(c['DaysOpen'] for c in cases)
print(f'\n📈 Age Statistics:')
print(f'  Average Age: {avg_age:.1f} days')
print(f'  Oldest Case: {int(max_age)} days')

with_icm = len([c for c in cases if c['HasICM'] == 'Yes'])
print(f'\n🔥 Cases with ICM Escalations: {with_icm}')

# Age category breakdown
print(f'\n📊 Age Category Distribution:')
age_cats = Counter(c['AgeCategory'] for c in cases)
for cat in ['Critical (>180 days)', 'Very High (>120 days)', 'High (>90 days)', 'Elevated (>60 days)', 'Moderate (>30 days)', 'Recent (20-30 days)']:
    if cat in age_cats:
        print(f'  {cat}: {age_cats[cat]}')

print()
