"""
Save all 131 IC/MCS cases directly from Kusto query result
This receives the data from stdin and processes it through write_all_cases
"""
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, 'c:/Users/carterryan/OneDrive - Microsoft/PHEPy')
from write_all_cases import write_cases_to_csv

def process_kusto_result(kusto_json_str):
    """
    Takes the Kusto query result JSON string and processes it
    """
    print("Processing Kusto query result...")
    
    # Parse the JSON
    kusto_data = json.loads(kusto_json_str)
    
    case_count = len(kusto_data.get('data', []))
    print(f"Received {case_count} cases from Kusto query")
    
    # Call write_cases_to_csv with the json_data parameter
    output_file = "data/production_full_cases.csv"
    print(f"\nConverting to CSV: {output_file}")
    
    write_cases_to_csv(json_data=kusto_data, output_csv_path=output_file)
    
    print(f"\n✓ Successfully processed all {case_count} cases")
    print(f"✓ CSV saved to: {output_file}")
    
    return output_file

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Read from file
        input_file = sys.argv[1]
        print(f"Reading from file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            kusto_json = f.read()
    else:
        # Read from stdin
        print("Reading from stdin...")
        kusto_json = sys.stdin.read()
    
    process_kusto_result(kusto_json)
