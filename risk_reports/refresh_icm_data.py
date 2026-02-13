"""
Refresh ICM data with fresh export
Run after executing GET_ALL_135_ICMS.kql and saving results to data/icm_fresh.csv
"""
import pandas as pd
import sys

print("=" * 70)
print("ICM DATA REFRESH")
print("=" * 70)

# Check if fresh ICM data exists
try:
    icm_fresh = pd.read_csv('data/icm_fresh.csv')
    print(f"\n✓ Found fresh ICM data: {len(icm_fresh)} ICMs")
    
    # Rename columns to match expected format
    column_mapping = {
        'IncidentId': 'IncidentId',
        'Severity': 'IcmSeverity',
        'OwningContactAlias': 'IcmOwner',
        'Status': 'IcmStatus'
    }
    
    icm_fresh = icm_fresh.rename(columns=column_mapping)
    
    # Save to icm.csv
    icm_fresh.to_csv('data/icm.csv', index=False)
    print(f"✓ Saved to data/icm.csv")
    
    print(f"\nStatus breakdown:")
    print(icm_fresh['IcmStatus'].value_counts())
    
    print(f"\n✓ ICM data refreshed successfully!")
    print(f"\nNext step: Regenerate report with:")
    print(f"  python ic_mcs_risk_report_generator.py ..\\data\\production_full_cases.csv IC_MCS_COMPLETE_REPORT.htm data\\icm.csv")
    
except FileNotFoundError:
    print("\n❌ ERROR: data/icm_fresh.csv not found")
    print("\nPlease:")
    print("1. Open Kusto Explorer")
    print("2. Run queries/GET_ALL_135_ICMS.kql")
    print("3. Export results to data/icm_fresh.csv")
    print("4. Run this script again")
    sys.exit(1)

print("=" * 70)
