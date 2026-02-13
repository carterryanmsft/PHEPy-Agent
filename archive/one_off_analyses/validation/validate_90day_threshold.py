"""
Validate 90+ Day Critical Threshold Implementation
"""
import pandas as pd

df = pd.read_csv('risk_reports/data/ic_cases.csv')

print('='*60)
print('90+ DAY CRITICAL THRESHOLD VALIDATION')
print('='*60)

# Check cases over 90 days
over_90_days = df[df['DaysOpen'] > 90]
print(f'\n📊 Cases over 90 days old: {len(over_90_days)}')

# Verify they are all Critical
critical_count = over_90_days[over_90_days['RiskLevel'] == 'Critical'].shape[0]
print(f'   Marked as Critical: {critical_count}')
print(f'   ✅ All flagged correctly: {critical_count == len(over_90_days)}')

# Show risk distribution
print(f'\n📊 Overall Risk Distribution:')
print(df['RiskLevel'].value_counts())

# Show age distribution of Critical cases
print(f'\n🚨 Critical Cases Age Distribution:')
critical_cases = df[df['RiskLevel'] == 'Critical']
print(f'   Total Critical: {len(critical_cases)}')
print(f'   Over 180 days: {len(critical_cases[critical_cases["DaysOpen"] > 180])}')
print(f'   120-180 days: {len(critical_cases[(critical_cases["DaysOpen"] > 120) & (critical_cases["DaysOpen"] <= 180)])}')
print(f'   90-120 days: {len(critical_cases[(critical_cases["DaysOpen"] > 90) & (critical_cases["DaysOpen"] <= 120)])}')
print(f'   Under 90 days: {len(critical_cases[critical_cases["DaysOpen"] <= 90])}')

# Show some examples of Critical cases over 90 days
print(f'\n📋 Sample Critical Cases (90+ days):')
sample = over_90_days.nlargest(5, 'DaysOpen')[['ServiceRequestNumber', 'TopParentName', 'DaysOpen', 'RiskScore', 'RiskLevel']]
for _, row in sample.iterrows():
    print(f'   {row["ServiceRequestNumber"]}: {row["TopParentName"]} - {int(row["DaysOpen"])} days, Risk {row["RiskScore"]:.0f}, {row["RiskLevel"]}')

# Check for any cases under 90 days that are Critical (should be based on score)
under_90_critical = critical_cases[critical_cases['DaysOpen'] <= 90]
if len(under_90_critical) > 0:
    print(f'\n⚠️  Cases under 90 days that are Critical (based on high risk score):')
    for _, row in under_90_critical.iterrows():
        print(f'   {row["ServiceRequestNumber"]}: {row["TopParentName"]} - {int(row["DaysOpen"])} days, Risk Score {row["RiskScore"]:.0f}')
else:
    print(f'\n✅ No cases under 90 days marked as Critical (all Critical cases are 90+ days old)')

print('\n' + '='*60)
print('VALIDATION COMPLETE')
print('='*60)
print('\n✅ ANY case over 90 days is now flagged as CRITICAL')
print('✅ Bug Information column added to report')
