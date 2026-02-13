"""
Show Barclays case details with PHE and agent assignments
"""
import pandas as pd

# Load cases
df = pd.read_csv('data/production_full_cases.csv')

# Filter Barclays cases
barclays = df[df['TopParentName'].str.contains('Barclays', case=False, na=False)]

print('=' * 120)
print('BARCLAYS CASES - PHE AND AGENT ASSIGNMENTS')
print('=' * 120)
print(f'\nTotal Cases: {len(barclays)}')
print(f'Program: {barclays["Program"].iloc[0] if not barclays.empty else "N/A"}')

# Get unique PHEs
phe_values = barclays['PHE'].dropna().unique()
print(f'PHE: {", ".join(phe_values) if len(phe_values) > 0 else "Not assigned"}')

# Show case details
print('\n' + '=' * 120)
print('CASE DETAILS:')
print('=' * 120)

for idx, row in barclays.iterrows():
    print(f'\n📋 Case: {row["ServiceRequestNumber"]}')
    print(f'   Status: {row["ServiceRequestStatus"]}')
    print(f'   Days Open: {row["DaysOpen"]:.1f}')
    print(f'   Risk Score: {row["RiskScore"]} ({row["RiskLevel"]})')
    print(f'   PHE: {row["PHE"] if pd.notna(row["PHE"]) else "Not assigned"}')
    print(f'   Agent: {row["AgentAlias"]}')
    print(f'   Manager: {row["ManagerEmail"]}')
    if pd.notna(row['RelatedICM_Id']):
        print(f'   ICM: {row["RelatedICM_Id"]}')

print('\n' + '=' * 120)

# Summary by agent
print('\n📊 CASES BY AGENT:')
print('=' * 120)
agent_summary = barclays.groupby('AgentAlias').agg({
    'ServiceRequestNumber': 'count',
    'DaysOpen': 'mean',
    'RiskScore': 'mean'
}).round(1)
agent_summary.columns = ['Cases', 'Avg Days Open', 'Avg Risk Score']
print(agent_summary.to_string())

print('\n' + '=' * 120)

# Summary by status
print('\n📊 CASES BY STATUS:')
print('=' * 120)
status_summary = barclays.groupby('ServiceRequestStatus').agg({
    'ServiceRequestNumber': 'count',
    'DaysOpen': 'mean'
}).round(1)
status_summary.columns = ['Count', 'Avg Days Open']
print(status_summary.to_string())

print('=' * 120)
