"""
Batch Process ICM Details Fetching

Manages batch fetching of ICM details with progress tracking and error handling

Author: Carter Ryan
Created: February 11, 2026
"""

import json
import time
from pathlib import Path
from datetime import datetime


def load_icm_ids():
    """Load all ICM IDs to fetch"""
    ids_file = Path(__file__).parent / "data" / "icms_to_fetch.txt"
    
    with open(ids_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def load_existing_details():
    """Load any previously fetched details"""
    details_file = Path(__file__).parent / "data" / "expanded_by_design_icm_details.json"
    
    if details_file.exists():
        with open(details_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {}


def save_icm_details(all_details):
    """Save ICM details periodically"""
    output_file = Path(__file__).parent / "data" / "expanded_by_design_icm_details.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_details, f, indent=2)
    
    return output_file


def parse_icm_temp_file(temp_file_path):
    """Parse ICM details from temp file"""
    try:
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"   ❌ Error parsing {temp_file_path}: {e}")
        return None


def find_icm_temp_files():
    """Find all temp files with ICM details from current session"""
    temp_dir = Path(r"c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\0b3a52cb-5056-42f6-b403-95846ca4b223")
    
    # Find all content.json files from get_incident_details_by_id calls
    temp_files = []
    for folder in temp_dir.glob("toolu_*__vscode-*"):
        content_file = folder / "content.json"
        if content_file.exists():
            temp_files.append(content_file)
    
    # Sort by modification time (newest first)
    temp_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    
    return temp_files


def extract_icm_id_from_data(data):
    """Extract ICM ID from response data"""
    if isinstance(data, dict):
        return data.get('id') or data.get('incidentId') or data.get('Id')
    return None


def main():
    print("="*80)
    print("BATCH PROCESSING ICM DETAILS FROM TEMP FILES")
    print("="*80)
    print()
    
    # Load existing details
    all_details = load_existing_details()
    initial_count = len(all_details)
    
    print(f"💾 Starting with {initial_count} previously saved ICMs")
    print()
    
    # Find temp files
    temp_files = find_icm_temp_files()
    print(f"🔍 Found {len(temp_files)} temp files to process")
    print()
    
    # Process each temp file
    newly_added = 0
    errors = 0
    
    for i, temp_file in enumerate(temp_files, 1):
        data = parse_icm_temp_file(temp_file)
        
        if data:
            icm_id = extract_icm_id_from_data(data)
            
            if icm_id:
                if str(icm_id) not in all_details:
                    all_details[str(icm_id)] = data
                    newly_added += 1
                    print(f"   ✅ [{i}/{len(temp_files)}] Added ICM {icm_id}")
                else:
                    print(f"   ⏭️  [{i}/{len(temp_files)}] ICM {icm_id} already exists")
            else:
                print(f"   ⚠️  [{i}/{len(temp_files)}] Could not extract ICM ID from {temp_file.name}")
        else:
            errors += 1
            print(f"   ❌ [{i}/{len(temp_files)}] Failed to parse {temp_file.name}")
    
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"📊 Total ICMs in database: {len(all_details)}")
    print(f"✅ Newly added: {newly_added}")
    print(f"❌ Errors: {errors}")
    print()
    
    # Save updated details
    if newly_added > 0:
        output_file = save_icm_details(all_details)
        print(f"💾 Saved to: {output_file}")
        print()
    
    # Check progress
    target_icms = load_icm_ids()
    remaining = [icm_id for icm_id in target_icms if str(icm_id) not in all_details]
    
    print(f"📈 Progress: {len(all_details)}/{len(target_icms)} ICMs fetched")
    print(f"⏳ Remaining: {len(remaining)} ICMs")
    print()
    
    if remaining:
        print("🔍 Next ICMs to fetch (first 10):")
        for icm_id in remaining[:10]:
            print(f"   {icm_id}")
        if len(remaining) > 10:
            print(f"   ... and {len(remaining) - 10} more")
    else:
        print("🎉 All ICMs fetched successfully!")
    
    print()


if __name__ == "__main__":
    main()
