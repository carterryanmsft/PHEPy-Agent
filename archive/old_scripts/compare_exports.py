import pandas as pd

# Load files
export = pd.read_csv('export (9).csv')
current = pd.read_csv('data/production_full_cases.csv')

print(f"Export CSV: {len(export)} cases")
print(f"Current production: {len(current)} cases")
print(f"\nExport unique: {export['ServiceRequestNumber'].nunique()}")
print(f"Current unique: {current['ServiceRequestNumber'].nunique()}")

# Compare case lists
export_cases = set(export['ServiceRequestNumber'])
current_cases = set(current['ServiceRequestNumber'])

missing = export_cases - current_cases
extra = current_cases - export_cases

print(f"\n=== COMPARISON ===")
print(f"Missing from current data: {len(missing)}")
print(f"Extra in current data: {len(extra)}")

if missing:
    print(f"\nSample missing cases:")
    for case in sorted(list(missing))[:10]:
        case_data = export[export['ServiceRequestNumber'] == case].iloc[0]
        print(f"  {case}: {case_data['TopParentName']} - Risk {case_data['RiskScore']}")

if extra:
    print(f"\nSample extra cases:")
    for case in sorted(list(extra))[:10]:
        case_data = current[current['ServiceRequestNumber'] == case].iloc[0]
        print(f"  {case}: {case_data['TopParentName']} - Risk {case_data['RiskScore']}")

# Compare risk scores for matching cases
matching = export_cases.intersection(current_cases)
print(f"\n=== MATCHING CASES: {len(matching)} ===")

if len(matching) > 0:
    export_match = export[export['ServiceRequestNumber'].isin(matching)].set_index('ServiceRequestNumber')
    current_match = current[current['ServiceRequestNumber'].isin(matching)].set_index('ServiceRequestNumber')
    
    risk_diff = (export_match['RiskScore'] - current_match['RiskScore']).abs()
    mismatched_risk = risk_diff[risk_diff > 0]
    
    print(f"Cases with different risk scores: {len(mismatched_risk)}")
    if len(mismatched_risk) > 0:
        print("\nSample risk mismatches:")
        for case in list(mismatched_risk.index)[:5]:
            print(f"  {case}: Export={export_match.loc[case, 'RiskScore']}, Current={current_match.loc[case, 'RiskScore']}")
