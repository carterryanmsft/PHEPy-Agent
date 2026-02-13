"""
Extract ICM IDs from fresh case data and save case data and ICM list for querying
"""
import json
import pandas as pd

# Read the Kusto result from the MCP tool (we'll pass this as argument)
def extract_icm_ids(cases_data):
    """Extract unique ICM IDs from case data"""
    all_icm_ids = set()
    
    for case in cases_data:
        icm_field = case.get('RelatedICM_Id', '')
        if icm_field:
            # Split by comma or semicolon
            icm_ids = [icm.strip() for icm in icm_field.replace(';', ',').split(',')]
            all_icm_ids.update([icm for icm in icm_ids if icm])
    
    return sorted(list(all_icm_ids))

def save_case_data(cases_data, output_file):
    """Save case data to CSV"""
    df = pd.DataFrame(cases_data)
    
    # Remove duplicates based on ServiceRequestNumber and DerivedProductName
    df_unique = df.drop_duplicates(subset=['ServiceRequestNumber', 'DerivedProductName'], keep='first')
    
    print(f"Total cases from Kusto: {len(df)}")
    print(f"Unique cases (after dedup): {len(df_unique)}")
    
    df_unique.to_csv(output_file, index=False)
    print(f"Saved {len(df_unique)} unique cases to {output_file}")
    
    return df_unique

# This will be called with the data from Kusto
if __name__ == "__main__":
    print("This script is intended to be called programmatically")
    print("Pass case data to extract_icm_ids() and save_case_data()")
