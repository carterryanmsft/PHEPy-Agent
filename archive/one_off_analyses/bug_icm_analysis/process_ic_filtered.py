#!/usr/bin/env python3
"""
Process IC query results (excluding SCIM Escalation Management)
"""
import json
import pandas as pd
from pathlib import Path
from collections import Counter
import sys

# Load the JSON results
if len(sys.argv) > 1:
    result_file = Path(sys.argv[1])
else:
    result_file = Path(r"c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\c53a391a-f578-4281-ab4f-61aa3c57bff7\toolu_0182gt5FhqB4fGj7ZAGWWCtw__vscode-1770399796343\content.txt")

with open(result_file, 'r', encoding='utf-8') as f:
    content = f.read()
    if content.startswith('Query results:'):
        content = content.replace('Query results:', '').strip()
    data = json.loads(content)

cases = data['data']

print(f'Query returned: {len(cases)} cases (excluding SCIM Escalation Management)')

# Convert to DataFrame
df = pd.DataFrame(cases)

# Calculate Risk Score
def calculate_risk_score(row):
    score = 0
    days_open = row['DaysOpen']
    
    # Age/Status factor (0-56 points) - increased by 40%
    if days_open > 180: score += 56
    elif days_open > 120: score += 49
    elif days_open > 90: score += 42
    elif days_open > 60: score += 35
    elif days_open > 30: score += 28
    else: score += 14
    
    # Ownership changes (0-20 points)
    ownership = row['OwnershipCount']
    if ownership > 20: score += 20
    elif ownership > 10: score += 15
    elif ownership > 5: score += 10
    elif ownership > 2: score += 5
    
    # Transfer count (0-15 points)
    transfers = row['TransferCount']
    if transfers > 20: score += 15
    elif transfers > 10: score += 12
    elif transfers > 5: score += 8
    elif transfers > 2: score += 4
    
    # Idle period (0-15 points)
    idle = row['DaysSinceUpdate']
    if idle > 30: score += 15
    elif idle > 21: score += 12
    elif idle > 14: score += 8
    elif idle > 7: score += 4
    
    # Reopen count (0-10 points)
    reopens = row['ReopenCount']
    if reopens >= 3: score += 10
    elif reopens == 2: score += 7
    elif reopens == 1: score += 5
    
    # ICM presence (0-10 points)
    if row['HasICM'] == 'Yes': score += 10
    
    # Severity (0-5 points)
    sev = row['ServiceRequestCurrentSeverity']
    if sev in ['1', 'A', 'Critical']: score += 5
    elif sev in ['2', 'B', 'High']: score += 3
    
    # CritSit boost
    if row['IsCritSit'] == 'Yes': score += 10
    
    return min(score, 100)

df['RiskScore'] = df.apply(calculate_risk_score, axis=1)

# Add risk level - ANY CASE OVER 90 DAYS IS CRITICAL
def get_risk_level(row):
    days_open = row['DaysOpen']
    score = row['RiskScore']
    
    # FORCE Critical for any case over 90 days old
    if days_open > 90:
        return 'Critical'
    elif score >= 80:
        return 'Critical'
    elif score >= 60:
        return 'High'
    elif score >= 40:
        return 'Medium'
    else:
        return 'Low'

df['RiskLevel'] = df.apply(get_risk_level, axis=1)

# Add age category
def get_age_category(days):
    if days > 180: return 'Critical (>180 days)'
    elif days > 120: return 'Very High (>120 days)'
    elif days > 90: return 'High (>90 days)'
    elif days > 60: return 'Elevated (>60 days)'
    elif days > 30: return 'Moderate (>30 days)'
    else: return 'Recent (20-30 days)'

df['AgeCategory'] = df['DaysOpen'].apply(get_age_category)

# Add Program
df['Program'] = 'IC'

# Add Summary
def create_summary(row):
    days = int(row['DaysOpen'])
    status = row['ServiceRequestStatus']
    has_icm = row['HasICM']
    ownership = row['OwnershipCount']
    transfers = row['TransferCount']
    
    summary = f"Case is {days} days old, status is {status}, ICM present: {has_icm}. "
    
    if ownership > 10:
        summary += f"Extremely high ownership ({ownership}) and transfer ({transfers}) counts indicate severe instability."
    elif ownership > 5:
        summary += f"High ownership ({ownership}) and transfer ({transfers}) counts increase risk."
    elif ownership > 2:
        summary += f"Ownership ({ownership}) and transfer ({transfers}) counts add to risk."
    else:
        summary += "No major additional risk factors."
    
    return summary

df['Summary'] = df.apply(create_summary, axis=1)

# Add other required fields
df['ProductName'] = 'Microsoft Purview Compliance'
df['DerivedProductName'] = 'Compliance'
df['TpAccountName'] = df['TopParentName']

# Save to CSV
csv_file = Path('c:/Users/carterryan/OneDrive - Microsoft/PHEPy/risk_reports/data/ic_cases.csv')
df.to_csv(csv_file, index=False)

# Save JSON backup
json_file = Path('c:/Users/carterryan/OneDrive - Microsoft/PHEPy/data/ic_risk_report_filtered.json')
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f'✅ Saved {len(df)} cases to CSV (filtered to exclude SCIM Escalation Management)')
print(f'   CSV: {csv_file}')
print(f'   JSON: {json_file}')

print(f'\n📊 Risk Level Distribution:')
print(df['RiskLevel'].value_counts().to_string())

print(f'\n🏢 Cases by Customer (Top 10):')
customers = Counter(df['TopParentName'])
for customer, count in customers.most_common(10):
    print(f'   {customer}: {count}')

print(f'\n🚨 Top 5 Highest Risk Cases:')
top5 = df.nlargest(5, 'RiskScore')[['ServiceRequestNumber', 'TopParentName', 'RiskScore', 'DaysOpen']]
for _, row in top5.iterrows():
    print(f'   {row["ServiceRequestNumber"]}: {row["TopParentName"]} - Risk {row["RiskScore"]}, {int(row["DaysOpen"])} days')
