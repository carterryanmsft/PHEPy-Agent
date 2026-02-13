import pandas as pd
from datetime import datetime

# IC-only case data from Kusto query (Feb 5, 2026)
# Query: Only IC (Intensive Care) customers
print("Saving IC-only cases to CSV...")

# Using the truncated query result - need to run full query again
print("Please run the full Kusto query again to get all IC cases")
print("Query returned 20 cases, but may have more beyond maxRows limit")
print("\nFor now, filtering existing production_full_cases.csv to IC only...")

# Load existing data and filter to IC only
df = pd.read_csv(r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\data\production_full_cases.csv')
print(f"Original data: {len(df)} cases")

# Filter to IC program only
ic_df = df[df['Program'] == 'IC'].copy()
print(f"IC-only data: {len(ic_df)} cases")

# Save IC-only data
ic_df.to_csv(r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\data\production_ic_only.csv', index=False)
print(f"✓ Saved {len(ic_df)} IC cases to production_ic_only.csv")

# Show summary
print(f"\nIC Customers: {ic_df['TopParentName'].nunique()}")
print(f"IC Cases by customer:")
customer_counts = ic_df.groupby('TopParentName').size().sort_values(ascending=False)
for customer, count in customer_counts.items():
    print(f"  {customer}: {count}")
