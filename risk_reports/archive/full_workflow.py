"""
Complete End-to-End IC/MCS Risk Report Workflow
Executes all steps: Kusto queries → Data processing → Report generation
"""

import subprocess
import sys
import json
from pathlib import Path

def run_step(step_name, command, description):
    """Execute a workflow step"""
    print(f"\n{'='*80}")
    print(f"STEP: {step_name}")
    print(f"{'='*80}")
    print(f"Description: {description}")
    print(f"Command: {command}\n")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ FAILED: {step_name}")
        print(f"Error: {result.stderr}")
        return False
    
    print(result.stdout)
    print(f"✓ COMPLETED: {step_name}")
    return True

def main():
    """Run complete workflow"""
    print("="*80)
    print("IC/MCS RISK REPORT - COMPLETE WORKFLOW")
    print("="*80)
    print("This will execute:")
    print("1. Query Kusto for IC/MCS cases (118 expected)")
    print("2. Extract ICM IDs from cases")
    print("3. Query ICM cluster for ICM details with filtering")
    print("4. Generate separate IC and MCS HTML reports")
    print("="*80)
    
    # Note: Steps 1-3 require manual execution via MCP Kusto tool
    # This script handles step 4 automatically
    
    print("\n⚠️  PREREQUISITE STEPS (Execute manually via Copilot):")
    print("   1. Run case query via mcp_kusto-mcp-ser_execute_query")
    print("   2. Save results to data/kusto_result_131.json")
    print("   3. Run python update_production_csv_from_kusto.py")
    print("   4. Extract ICM IDs and query ICM cluster")
    print("   5. Save ICM results to risk_reports/data/icm.csv")
    
    print("\n▶️  AUTOMATED STEPS:")
    
    # Check if prerequisites are met
    case_file = Path("../data/production_full_cases.csv")
    icm_file = Path("data/icm.csv")
    
    if not case_file.exists():
        print(f"❌ Missing: {case_file}")
        print("   Run case query and save to CSV first")
        return False
    
    if not icm_file.exists():
        print(f"❌ Missing: {icm_file}")
        print("   Run ICM query and save to CSV first")
        return False
    
    # Count records
    import pandas as pd
    cases_df = pd.read_csv(case_file)
    icm_df = pd.read_csv(icm_file)
    
    print(f"\n✓ Found case data: {len(cases_df)} cases")
    print(f"✓ Found ICM data: {len(icm_df)} ICMs")
    
    if len(cases_df) < 100:
        print(f"\n⚠️  WARNING: Only {len(cases_df)} cases found, expected ~118")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    
    # Step 4: Generate reports
    success = run_step(
        "4. Generate IC/MCS Reports",
        "python ic_mcs_risk_report_generator.py ../data/production_full_cases.csv IC_MCS_PRODUCTION data/icm.csv",
        "Generate separate IC and MCS HTML reports with all enhancements"
    )
    
    if not success:
        return False
    
    print("\n" + "="*80)
    print("WORKFLOW COMPLETE ✓")
    print("="*80)
    print(f"Generated reports:")
    print(f"  - IC_MCS_PRODUCTION_IC.htm (Intensive Care)")
    print(f"  - IC_MCS_PRODUCTION_MCS.htm (Mission Critical Support)")
    print("="*80)
    
    # Open IC report
    print("\nOpening IC report...")
    subprocess.run("Invoke-Item IC_MCS_PRODUCTION_IC.htm", shell=True)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
