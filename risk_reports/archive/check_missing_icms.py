import pandas as pd

# Load cases
df = pd.read_csv('../data/production_full_cases.csv')

# Load existing ICM data
icm_df = pd.read_csv('data/icm.csv')
existing_icms = set(icm_df['IncidentId'].tolist())

# Extract all ICMs from cases
all_icms = set()
for icm_str in df['RelatedICM_Id'].dropna():
    for icm in str(icm_str).replace(',', ' ').split():
        icm = icm.strip()
        if icm.isdigit():
            all_icms.add(int(icm))

# Find missing
missing = all_icms - existing_icms

print(f"Total unique ICMs in cases: {len(all_icms)}")
print(f"ICMs in icm.csv: {len(existing_icms)}")
print(f"Missing ICMs: {len(missing)}")
print(f"\nMissing ICM IDs:")
for icm in sorted(missing):
    print(f"  {icm}")
