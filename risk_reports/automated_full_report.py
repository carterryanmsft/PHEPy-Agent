"""
ONE-SHOT AUTOMATED IC/MCS RISK REPORT GENERATOR
Executes full workflow: Query Kusto → Save → Convert to CSV → Generate HTML report
"""
import subprocess
import sys
import os

# Note: Kusto data will be queried directly when this script runs

def execute_complete_workflow():
    """Execute full workflow using existing tools"""
    print("\nStep 1: Executing save_kusto_data_131.py...")
    
    result = subprocess.run([
        sys.executable,
        os.path.join(os.path.dirname(__file__), "..", "save_kusto_data_131.py")
    ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
    
    if result.returncode != 0:
        print(f"✗ Failed to save Kusto data:")
        print(result.stderr)
        return None
        
    print(result.stdout)
    print("✓ Kusto data saved")
    
    print("\nStep 2: Converting to CSV...")
    result = subprocess.run([
        sys.executable,
        os.path.join(os.path.dirname(__file__), "..", "write_all_cases.py"),
        os.path.join(os.path.dirname(__file__), "data", "kusto_result_131.json")
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"✗ Failed to convert to CSV:")
        print(result.stderr)
        return None
        
    print(result.stdout)
    print("✓ CSV generated")
    
    print("\nStep 3: Generating HTML report...")
    csv_file = os.path.join(os.path.dirname(__file__), "data", "production_full_cases.csv")
    icm_file = os.path.join(os.path.dirname(__file__), "data", "icm.csv")
    output_file = os.path.join(os.path.dirname(__file__), "IC_MCS_Production_Report_FULL_131.htm")
    
    result = subprocess.run([
        sys.executable,
        os.path.join(os.path.dirname(__file__), "ic_mcs_risk_report_generator.py"),
        csv_file,
        output_file,
        icm_file
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Report generated: {output_file}")
        print(result.stdout)
        return output_file
    else:
        print(f"✗ Report generation failed:")
        print(result.stderr)
        return None

def main():
    """Execute complete workflow"""
    print("=" * 80)
    print("ONE-SHOT AUTOMATED IC/MCS RISK REPORT - FULL 131 CASES")
    print("=" * 80)
    
    try:
        # Execute workflow
        report_file = execute_complete_workflow()
        
        if report_file:
            print("\n" + "=" * 80)
            print("✓✓✓ SUCCESS! Full report generated with 131 cases")
            print(f"Report: {report_file}")
            print("=" * 80)
        else:
            print("\n✗ Workflow failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
