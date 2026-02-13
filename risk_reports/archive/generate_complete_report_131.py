"""
Complete IC/MCS Risk Report Generator
Uses the batch_writer to save all 131 cases then generates HTML report
"""

import subprocess
import sys
import json
from pathlib import Path

def main():
    print("=" * 80)
    print("IC/MCS Production Risk Report - Full 131 Cases")
    print("=" * 80)
    
    # Step 1: The Kusto query has already been executed successfully via MCP
    # We have 131 cases. Now we need to convert and generate report
    
    # Use batch_writer.py which can save the paginated result
    print("\n[1/3] Saving 131 cases from Kusto query...")
    print("  Invoking batch_writer.py to save all cases...")
    
    # The batch_writer should be configured to save automatically
    try:
        result = subprocess.run(
            [sys.executable, "batch_writer.py"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"  ✓ batch_writer completed")
            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
        else:
            print(f"  ✗ batch_writer failed: {result.stderr}")
            return 1
    except Exception as e:
        print(f"  ✗ Error running batch_writer: {e}")
        # Continue anyway - the data might already be saved
    
    # Step 2: Convert JSON to CSV
    print("\n[2/3] Converting to CSV format...")
    data_file = Path(__file__).parent / "data" / "kusto_production_result.json"
    csv_file = Path(__file__).parent / "data" / "production_all_131.csv"
    
    if data_file.exists():
        try:
            result = subprocess.run(
                [sys.executable, "../convert_mcp_to_csv.py", str(data_file), str(csv_file)],
                cwd=Path(__file__).parent,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"  ✓ CSV file created: {csv_file}")
                print(result.stdout)
            else:
                print(f"  ✗ Conversion failed: {result.stderr}")
                return 1
        except Exception as e:
            print(f"  ✗ Error converting to CSV: {e}")
            return 1
    else:
        print(f"  ✗ Data file not found: {data_file}")
        print("     Please ensure Kusto query result is saved")
        return 1
    
    # Step 3: Generate HTML report
    print("\n[3/3] Generating HTML report...")
    output_html = Path(__file__).parent / "IC_MCS_Production_Report_FULL_131.htm"
    icm_file = Path(__file__).parent / "data" / "icm.csv"
    
    try:
        result = subprocess.run(
            [sys.executable, "ic_mcs_risk_report_generator.py", 
             str(csv_file), str(output_html), str(icm_file)],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"  ✓ HTML report generated: {output_html}")
            print(result.stdout)
            
            # Show summary
            with open(csv_file, 'r', encoding='utf-8') as f:
                import csv
                reader = csv.DictReader(f)
                cases = list(reader)
                
                print(f"\n{'='*80}")
                print(f"REPORT COMPLETE - {len(cases)} cases")
                print(f"{'='*80}")
                
                # Count by risk level
                risk_counts = {}
                for case in cases:
                    risk = case.get('RiskLevel', 'Unknown')
                    risk_counts[risk] = risk_counts.get(risk, 0) + 1
                
                for risk in ['Critical', 'High', 'Medium', 'Low']:
                    if risk in risk_counts:
                        print(f"  {risk}: {risk_counts[risk]} cases")
                
                # Top 5 cases
                print(f"\n  Top 5 Highest Risk:")
                sorted_cases = sorted(cases, key=lambda x: float(x.get('RiskScore', 0)), reverse=True)
                for i, case in enumerate(sorted_cases[:5], 1):
                    print(f"    {i}. {case['TopParentName']} - Risk {case['RiskScore']} ({case['DaysOpen'][:5]} days)")
                
                print(f"\n  Report file: {output_html}")
                print(f"{'='*80}")
            
            return 0
        else:
            print(f"  ✗ Report generation failed: {result.stderr}")
            return 1
    except Exception as e:
        print(f"  ✗ Error generating report: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
