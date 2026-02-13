"""
Combine JSON chunks into the final kusto_result_131.json file.
This script merges all the part files into a single JSON.
"""
import json
from pathlib import Path

def combine_chunks():
    """Combine all JSON chunk files into final result."""
    data_dir = Path(__file__).parent / "data"
    
    # Find all part files
    part_files = sorted(data_dir.glob("kusto_131_part*.json"))
    
    if not part_files:
        print("❌ No part files found!")
        print(f"   Looking in: {data_dir}")
        return False
    
    print(f"📦 Found {len(part_files)} chunk files")
    
    # Read and combine all parts
    all_cases = []
    for part_file in part_files:
        print(f"   Reading {part_file.name}...")
        with open(part_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'data' in data:
                all_cases.extend(data['data'])
            else:
                # Assume it's just an array of cases
                all_cases.extend(data)
    
    # Create final structure
    final_data = {
        "name": "PrimaryResult",
        "data": all_cases
    }
    
    # Save combined file
    output_file = data_dir / "kusto_result_131.json"
    print(f"\n💾 Saving combined file...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2)
    
    print(f"✅ SUCCESS! Created {output_file}")
    print(f"   Total cases: {len(all_cases)}")
    
    # Cleanup - optionally remove part files
    cleanup = input("\n🧹 Remove chunk files? (y/N): ").strip().lower()
    if cleanup == 'y':
        for part_file in part_files:
            part_file.unlink()
            print(f"   Deleted {part_file.name}")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Kusto Data Chunk Combiner")
    print("=" * 60)
    success = combine_chunks()
    exit(0 if success else 1)
