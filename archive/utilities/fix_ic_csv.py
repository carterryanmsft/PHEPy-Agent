#!/usr/bin/env python3
"""
Add missing columns to IC cases CSV
"""
import pandas as pd
from pathlib import Path

# Load the CSV
csv_file = Path('c:/Users/carterryan/OneDrive - Microsoft/PHEPy/risk_reports/data/ic_cases.csv')
df = pd.read_csv(csv_file)

print(f'Current columns: {list(df.columns)}')

# Add Program column (all IC cases)
df['Program'] = 'IC'

# Add Summary column
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

# Also add DerivedProductName and ProductName if missing
if 'ProductName' not in df.columns:
    df['ProductName'] = 'Microsoft Purview Compliance'
if 'DerivedProductName' not in df.columns:
    df['DerivedProductName'] = 'Compliance'
if 'TpAccountName' not in df.columns:
    df['TpAccountName'] = df['TopParentName']

# Save back to CSV
df.to_csv(csv_file, index=False)

print(f'\n✅ Added Program, Summary, and other missing columns')
print(f'   Total cases: {len(df)}')
print(f'   Total columns: {len(df.columns)}')
print(f'   New columns: {list(df.columns)}')
