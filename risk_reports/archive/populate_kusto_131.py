"""
INSTRUCTIONS:
1. I will send you the 131-case JSON data in the next message
2. Copy it and replace the CASES_DATA variable below
3. Run this script: python populate_kusto_131.py
4. Then run the report generator
"""
import json
from pathlib import Path

# REPLACE THIS with the actual case data from the next message
CASES_DATA = [
    # Cases will be pasted here
]

def save_kusto_data():
    """Save the Kusto query results to JSON file."""
    output_file = Path("data/kusto_result_131.json")
    
    kusto_result = {
        "name": "PrimaryResult",
        "data": CASES_DATA
    }
    
    print(f"💾 Saving {len(CASES_DATA)} cases...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(kusto_result, f, indent=2)
    
    print(f"✅ SUCCESS! Saved to {output_file}")
    print(f"   Total cases: {len(CASES_DATA)}")
    
    # Verify the data
    print("\n📊 Data summary:")
    risk_levels = {}
    for case in CASES_DATA:
        level = case.get('RiskLevel', 'Unknown')
        risk_levels[level] = risk_levels.get(level, 0) + 1
    
    for level, count in sorted(risk_levels.items(), key=lambda x: {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}.get(x[0], 99)):
        print(f"   {level}: {count} cases")
    
    print("\n▶️ Next steps:")
    print("   1. python ..\\write_all_cases.py data\\kusto_result_131.json")
    print("   2. python ic_mcs_risk_report_generator.py data\\production_full_cases.csv FINAL.htm data\\icm.csv")

if __name__ == "__main__":
    if len(CASES_DATA) == 0:
        print("❌ ERROR: No case data found!")
        print("   Please paste the case data array into CASES_DATA variable")
        exit(1)
    
    save_kusto_data()
