"""
Complete Automated Workflow for IC/MCS Risk Report
This script is called by the AI agent with Kusto data passed in
"""
import json
import pandas as pd
import sys
from pathlib import Path

def run_complete_workflow(cases_json_data):
    """
    Run the complete workflow:
    1. Save cases to CSV (deduped)
    2. Extract unique ICM IDs
    3. Return ICM IDs for querying
    
    Args:
        cases_json_data: List of case dictionaries from Kusto
    
    Returns:
        tuple: (cases_df, icm_ids_list)
    """
    print("=" * 70)
    print("IC/MCS RISK REPORT - AUTOMATED WORKFLOW")
    print("=" * 70)
    
    # Step 1: Process cases
    print("\n[Step 1/4] Processing case data from Kusto...")
    df = pd.DataFrame(cases_json_data)
    print(f"  • Total cases from Kusto: {len(df)}")
    
    # Deduplicate (same case with different DerivedProductName)
    df_unique = df.drop_duplicates(subset=['ServiceRequestNumber', 'DerivedProductName'], keep='first')
    print(f"  • Unique cases after dedup: {len(df_unique)}")
    
    # Save to CSV
    output_file = Path('../data/production_full_cases.csv')
    output_file.parent.mkdir(exist_ok=True)
    df_unique.to_csv(output_file, index=False)
    print(f"  ✓ Saved cases to: {output_file}")
    
    # Step 2: Extract ICM IDs
    print("\n[Step 2/4] Extracting ICM IDs...")
    all_icm_ids = set()
    
    for icm_field in df_unique['RelatedICM_Id'].dropna():
        if icm_field and str(icm_field).strip():
            # Split by comma or semicolon
            icms = [icm.strip() for icm in str(icm_field).replace(';', ',').split(',')]
            all_icm_ids.update([icm for icm in icms if icm])
    
    icm_ids = sorted(list(all_icm_ids))
    print(f"  • Found {len(icm_ids)} unique ICM IDs in cases")
    
    # Save ICM IDs list
    icm_list_file = Path('data/icm_ids_to_query.txt')
    icm_list_file.parent.mkdir(exist_ok=True)
    with open(icm_list_file, 'w') as f:
        f.write('\n'.join(icm_ids))
    print(f"  ✓ Saved ICM list to: {icm_list_file}")
    
    return df_unique, icm_ids

def generate_icm_kusto_query(icm_ids):
    """Generate Kusto query for ICM data"""
    # Convert ICM IDs to proper format for Kusto IN clause
    formatted_ids = []
    for icm_id in icm_ids:
        # Check if it's numeric or string-based ICM ID
        if icm_id.isdigit():
            formatted_ids.append(icm_id)
        else:
            formatted_ids.append(f'"{icm_id}"')
    
    ids_str = ', '.join(formatted_ids)
    
    query = f"""// Query to get ICM owner and status information
// Run this in Kusto.Explorer against IcMDataWarehouse
IcMDataWarehouse_Snapshot
| where IncidentId in ({ids_str})
| project IncidentId, Severity, Status, OwningContactAlias, Title, CreateDate, ModifiedDate
| order by IncidentId asc
"""
    return query

if __name__ == "__main__":
    print("This script processes Kusto case data")
    print("Usage: Pass cases JSON data to run_complete_workflow()")
