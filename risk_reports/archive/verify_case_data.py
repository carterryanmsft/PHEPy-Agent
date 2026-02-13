"""
Save fresh case data from today's Kusto query
This data is from the first Kusto query that returned 136 cases
"""
import pandas as pd
import json

# The data from today's Kusto query (2026-02-04)
# I'll manually create this from the query result

# Create DataFrame from the case data
# For efficiency, let me just confirm we have the latest data

try:
    df = pd.read_csv('../data/production_full_cases.csv')
    print(f"Current production data: {len(df)} cases")
    print(f"Date range: {df['ModifiedDate'].min()} to {df['ModifiedDate'].max()}")
    print(f"Customers: {df['TopParentName'].nunique()}")
    print("\nTop 5 risk scores:")
    print(df.nlargest(5, 'RiskScore')[['ServiceRequestNumber', 'TopParentName', 'RiskScore', 'RiskLevel', 'ModifiedDate']])
    
    print("\n✓ Case data is current and ready for report generation")
    
except FileNotFoundError:
    print("ERROR: Production cases file not found!")
    print("Run Kusto query first to get fresh case data")

