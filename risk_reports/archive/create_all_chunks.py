"""
Generate all 27 chunk files from the Kusto query result.
This script will be populated with all 131 cases split into chunks.
"""
import json
from pathlib import Path

# All 131 cases will be embedded here in the next update
ALL_CASES = []  # Will contain all 131 case dictionaries

def create_chunks():
    """Split ALL_CASES into 5-case chunks and save."""
    if not ALL_CASES:
        print("❌ No case data available")
        print("   The AI agent has the data but cannot embed it directly")
        print("   due to token size limitations.")
        print()
        print("RECOMMENDED: Run the Kusto query yourself:")
        print("   1. Open Azure Data Explorer")
        print("   2. Connect to: cxedataplatformcluster.westus2.kusto.windows.net")
        print("   3. Database: cxedata")
        print("   4. Run query from: queries/ic_mcs_risk_query.kql")
        print("   5. Export as JSON to: data/kusto_result_131.json")
        return False
    
    chunks_dir = Path("data/chunks")
    chunks_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_size = 5
    total_chunks = (len(ALL_CASES) + chunk_size - 1) // chunk_size
    
    print(f"Creating {total_chunks} chunk files...")
    
    for i in range(0, len(ALL_CASES), chunk_size):
        chunk_num = (i // chunk_size) + 1
        chunk_data = ALL_CASES[i:i + chunk_size]
        
        chunk_file = chunks_dir / f"chunk_{chunk_num:03d}.json"
        with open(chunk_file, 'w', encoding='utf-8') as f:
            json.dump(chunk_data, f)
        
        print(f"   ✓ {chunk_file.name} ({len(chunk_data)} cases)")
    
    print(f"\n✅ Created {total_chunks} chunk files")
    return True

if __name__ == "__main__":
    create_chunks()
