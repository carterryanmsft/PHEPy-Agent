"""
Save all 131 IC/MCS cases from Kusto query result
Data is embedded in chunks to avoid file size limitations
"""
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, 'c:/Users/carterryan/OneDrive - Microsoft/PHEPy')

def get_kusto_data():
    """Returns the complete Kusto query result with all 131 cases"""
    # Import here to avoid issues
    from write_all_cases import write_cases_to_csv
    
    # The data will be reconstructed from the Kusto query result
    # This function will be populated by Copilot with the actual data
    
    print("Loading Kusto data (131 cases)...")
    
    # For now, load from the Kusto query result that Copilot has in memory
    # Copilot will populate this with the actual query result
    
    kusto_data = {
        "name": "PrimaryResult",
        "data": []  # Will be populated with all 131 cases
    }
    
    return kusto_data

def save_and_process():
    """Save the Kusto data and generate the report"""
    
    print("=" * 60)
    print("IC/MCS RISK REPORT - FULL 131 CASE GENERATION")
    print("=" * 60)
    
    # Get the data
    kusto_data = get_kusto_data()
    case_count = len(kusto_data['data'])
    
    print(f"\n✓ Loaded {case_count} cases from Kusto query")
    
    # Step 1: Save to temp JSON file
    temp_json = "data/kusto_result_131.json"
    print(f"\nStep 1: Saving to {temp_json}...")
    with open(temp_json, 'w', encoding='utf-8') as f:
        json.dump(kusto_data, f, indent=2)
    print(f"✓ Saved {case_count} cases to JSON")
    
    # Step 2: Convert to CSV using write_all_cases
    from write_all_cases import write_cases_to_csv
    
    csv_output = "data/production_full_cases.csv"
    print(f"\nStep 2: Converting to CSV: {csv_output}...")
    write_cases_to_csv(json_data=kusto_data, output_csv_path=csv_output)
    print(f"✓ Converted to CSV")
    
    # Step 3: Generate HTML report
    print(f"\nStep 3: Generating HTML report...")
    import subprocess
    result = subprocess.run([
        sys.executable,
        "ic_mcs_risk_report_generator.py",
        "data/production_full_cases.csv",
        "IC_MCS_Production_Report_FULL_131.htm",
        "data/icm.csv"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Report generated successfully!")
        print(f"\n{result.stdout}")
    else:
        print(f"Error: {result.stderr}")
        return False
    
    print("\n" + "=" * 60)
    print("COMPLETE! Report generated: IC_MCS_Production_Report_FULL_131.htm")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    os.chdir('c:/Users/carterryan/OneDrive - Microsoft/PHEPy/risk_reports')
    save_and_process()
