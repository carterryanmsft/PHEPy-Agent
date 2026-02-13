import pandas as pd

print("=== STEP-BY-STEP TRACE ===\n")

# Step 1: Load ICM data
print("STEP 1: Load ICM CSV")
icm_df = pd.read_csv('data/icm.csv')
print(f"Loaded {len(icm_df)} ICMs")
print(f"Columns: {icm_df.columns.tolist()}")

# Step 2: Replace empty strings with NaN
print("\nSTEP 2: Replace empty strings with pd.NA")
icm_df['IcmOwner'] = icm_df['IcmOwner'].replace('', pd.NA)
print(f"ICMs with NaN owners after replace: {icm_df['IcmOwner'].isna().sum()}")

# Step 3: Build dict
print("\nSTEP 3: Build ICM dictionary")
icm_dict = icm_df.set_index('IncidentId')[['IcmOwner', 'IcmSeverity', 'IcmStatus']].to_dict('index')
print(f"Dict has {len(icm_dict)} entries")

# Step 4: Test with specific ICMs
print("\nSTEP 4: Test lookups for case with ICMs: 704668547,51000000859513")
test_icm_ids = "704668547,51000000859513"

# Simulate get_icm_data
def get_icm_data(icm_ids_str, field):
    if pd.isna(icm_ids_str) or not str(icm_ids_str).strip():
        return None
    icm_ids_str = str(icm_ids_str).replace(',', ';')
    icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
    if icm_ids:
        # First, look for an ACTIVE ICM with data
        for icm_id_str in icm_ids:
            try:
                icm_id = int(icm_id_str)
                if icm_id in icm_dict:
                    if icm_dict[icm_id].get('IcmStatus') == 'ACTIVE':
                        value = icm_dict[icm_id].get(field)
                        print(f"  Checking ACTIVE ICM {icm_id}: {field}={value}, pd.notna={pd.notna(value)}")
                        if pd.notna(value) and str(value).strip():
                            return value
            except (ValueError, KeyError) as e:
                print(f"  Error with {icm_id_str}: {e}")
        # If no ACTIVE with data, return first available
        for icm_id_str in icm_ids:
            try:
                icm_id = int(icm_id_str)
                if icm_id in icm_dict:
                    value = icm_dict[icm_id].get(field)
                    print(f"  Checking ICM {icm_id}: {field}={value}, pd.notna={pd.notna(value)}")
                    if pd.notna(value) and str(value).strip():
                        return value
            except (ValueError, KeyError) as e:
                print(f"  Error with {icm_id_str}: {e}")
    return None

owner = get_icm_data(test_icm_ids, 'IcmOwner')
status = get_icm_data(test_icm_ids, 'IcmStatus')

print(f"\nRESULT: Owner={owner}, Status={status}")

# Step 5: Simulate display logic
print("\nSTEP 5: Simulate display logic")
has_icm_data = True
row_icm_owner = owner
row_icm_status = status

icm_owner_display = 'N/A'
if has_icm_data and test_icm_ids.strip():
    # Get owner value, handling all edge cases
    owner_value = ''
    raw_owner = row_icm_owner
    # Check if it's actually a value
    if pd.notna(raw_owner):
        owner_str = str(raw_owner).strip()
        print(f"  raw_owner={raw_owner}, owner_str='{owner_str}'")
        # Filter out 'nan', 'None', empty strings
        if owner_str and owner_str.lower() not in ['nan', 'none', 'null']:
            owner_value = owner_str
            print(f"  owner_value set to: '{owner_value}'")
    
    # Get status value
    icm_status = ''
    raw_status = row_icm_status
    if pd.notna(raw_status):
        status_str = str(raw_status).strip()
        if status_str and status_str.lower() not in ['nan', 'none', 'null']:
            icm_status = status_str
            print(f"  icm_status set to: '{icm_status}'")
    
    # Display logic
    if owner_value:
        icm_owner_display = owner_value
        print(f"  Display: Owner exists -> '{icm_owner_display}'")
    elif icm_status == 'ACTIVE':
        icm_owner_display = '<span class="icm-unassigned">Unassigned</span>'
        print(f"  Display: ACTIVE without owner -> Unassigned")
    else:
        print(f"  Display: No owner, not ACTIVE -> N/A")

print(f"\nFINAL: icm_owner_display = '{icm_owner_display}'")
