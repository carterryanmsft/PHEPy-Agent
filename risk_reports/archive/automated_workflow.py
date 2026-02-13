"""
Automated IC/MCS Risk Report Generation Workflow
Runs end-to-end: Query Kusto -> Extract ICMs -> Query ICM data -> Generate report
"""
import json
import pandas as pd
import sys
from pathlib import Path

def save_cases_and_extract_icms(cases_json_str, output_cases_file, output_icm_list_file):
    """
    Save case data to CSV and extract unique ICM IDs
    
    Args:
        cases_json_str: JSON string of case data from Kusto
        output_cases_file: Path to save cases CSV
        output_icm_list_file: Path to save ICM IDs list
    
    Returns:
        tuple: (number of cases saved, list of ICM IDs)
    """
    # Parse JSON
    cases_data = json.loads(cases_json_str)
    
    # Convert to DataFrame
    df = pd.DataFrame(cases_data)
    
    # Remove duplicates (same case can appear twice with different DerivedProductName)
    df_unique = df.drop_duplicates(subset=['ServiceRequestNumber', 'DerivedProductName'], keep='first')
    
    print(f"Total cases from Kusto: {len(df)}")
    print(f"Unique cases after dedup: {len(df_unique)}")
    
    # Save to CSV
    df_unique.to_csv(output_cases_file, index=False)
    print(f"✓ Saved {len(df_unique)} cases to {output_cases_file}")
    
    # Extract ICM IDs
    all_icm_ids = set()
    for icm_field in df_unique['RelatedICM_Id'].dropna():
        if icm_field:
            # Split by comma or semicolon and clean
            icm_ids = [icm.strip() for icm in str(icm_field).replace(';', ',').split(',')]
            all_icm_ids.update([icm for icm in icm_ids if icm])
    
    icm_list = sorted(list(all_icm_ids))
    print(f"✓ Found {len(icm_list)} unique ICM IDs")
    
    # Save ICM list
    with open(output_icm_list_file, 'w') as f:
        f.write('\n'.join(icm_list))
    print(f"✓ Saved ICM list to {output_icm_list_file}")
    
    return len(df_unique), icm_list

def create_icm_query(icm_ids):
    """
    Create Kusto query to fetch ICM data
    
    Args:
        icm_ids: List of ICM IDs
    
    Returns:
        str: Kusto query
    """
    # Format ICM IDs for IN clause
    icm_ids_formatted = ', '.join([f'"{icm_id}"' if not icm_id.isdigit() else icm_id for icm_id in icm_ids])
    
    query = f"""
IcMDataWarehouse_Snapshot
| where IncidentId in ({icm_ids_formatted})
| project IncidentId, Severity, Status, OwningTeamId, OwningContactAlias, Title, CreateDate, ModifiedDate
| order by IncidentId asc
"""
    return query

if __name__ == "__main__":
    print("=" * 60)
    print("IC/MCS Risk Report - Automated Workflow")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage: python automated_workflow.py <cases_json_file>")
        print("\nThis script will:")
        print("  1. Load case data from JSON file")
        print("  2. Save unique cases to production_full_cases.csv")
        print("  3. Extract ICM IDs and save to icm_ids.txt")
        print("  4. Generate ICM query to icm_query.kql")
        print("\nNext steps (to be automated):")
        print("  5. Execute ICM query in Kusto")
        print("  6. Save ICM data to data/icm.csv")
        print("  7. Run report generator")
        sys.exit(1)
    
    # Paths
    cases_json_file = sys.argv[1]
    output_dir = Path(__file__).parent
    data_dir = output_dir / 'data'
    output_dir.mkdir(exist_ok=True)
    data_dir.mkdir(exist_ok=True)
    
    cases_output = data_dir.parent / 'data' / 'production_full_cases.csv'
    icm_list_output = output_dir / 'icm_ids.txt'
    icm_query_output = output_dir / 'queries' / 'icm_query.kql'
    icm_query_output.parent.mkdir(exist_ok=True)
    
    # Step 1: Load and process cases
    print("\n[Step 1] Processing case data...")
    with open(cases_json_file, 'r') as f:
        cases_json = f.read()
    
    num_cases, icm_ids = save_cases_and_extract_icms(
        cases_json,
        cases_output,
        icm_list_output
    )
    
    # Step 2: Create ICM query
    print(f"\n[Step 2] Creating ICM query for {len(icm_ids)} ICMs...")
    icm_query = create_icm_query(icm_ids)
    
    with open(icm_query_output, 'w') as f:
        f.write(icm_query)
    print(f"✓ Saved ICM query to {icm_query_output}")
    
    print("\n" + "=" * 60)
    print("WORKFLOW STATUS")
    print("=" * 60)
    print(f"✓ Cases saved: {num_cases}")
    print(f"✓ ICM IDs extracted: {len(icm_ids)}")
    print(f"✓ ICM query generated: {icm_query_output}")
    print("\nNext: Execute ICM query in Kusto to get ICM owner/status data")
    print("=" * 60)
