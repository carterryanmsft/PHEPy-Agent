"""
Combine all JSON chunk files into the final kusto_result_131.json
Run this after all chunk files have been created.
"""
import json
from pathlib import Path

def combine_all_chunks():
    """Combine all chunk files into final Kusto result."""
    chunks_dir = Path(__file__).parent / "data" / "chunks"
    
    if not chunks_dir.exists():
        print(f"❌ Chunks directory not found: {chunks_dir}")
        return False
    
    # Find all chunk files
    chunk_files = sorted(chunks_dir.glob("chunk_*.json"))
    
    if not chunk_files:
        print(f"❌ No chunk files found in {chunks_dir}")
        return False
    
    print(f"📦 Found {len(chunk_files)} chunk files")
    print()
    
    all_cases = []
    for chunk_file in chunk_files:
        print(f"   Loading {chunk_file.name}...", end=" ")
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunk_data = json.load(f)
            if isinstance(chunk_data, list):
                all_cases.extend(chunk_data)
                print(f"✓ ({len(chunk_data)} cases)")
            else:
                print("⚠️ Invalid format")
    
    print()
    print(f"📊 Total cases loaded: {len(all_cases)}")
    
    # Create final Kusto result structure
    final_result = {
        "name": "PrimaryResult",
        "data": all_cases
    }
    
    # Save to final location
    output_file = Path(__file__).parent / "data" / "kusto_result_131.json"
    print(f"💾 Saving to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, indent=2)
    
    print()
    print("✅ SUCCESS! Combined all chunks")
    print(f"   Output: {output_file}")
    print(f"   Total cases: {len(all_cases)}")
    
    # Show risk distribution
    print()
    print("📊 Risk Level Distribution:")
    risk_counts = {}
    for case in all_cases:
        level = case.get('RiskLevel', 'Unknown')
        risk_counts[level] = risk_counts.get(level, 0) + 1
    
    for level in ['Critical', 'High', 'Medium', 'Low']:
        count = risk_counts.get(level, 0)
        print(f"   {level:8s}: {count:3d} cases")
    
    print()
    print("▶️  Next steps:")
    print("   1. python write_all_cases.py data\\kusto_result_131.json")
    print("   2. python ic_mcs_risk_report_generator.py data\\production_full_cases.csv FINAL_REPORT.htm data\\icm.csv")
    
    return True

if __name__ == "__main__":
    print("=" * 70)
    print("IC/MCS Risk Report - Chunk Combiner")
    print("=" * 70)
    print()
    
    success = combine_all_chunks()
    exit(0 if success else 1)
