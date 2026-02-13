"""
Fetch ICM Details for Expanded By-Design Analysis

Batch fetches ICM details via MCP for 180-day By-Design dataset

Author: Carter Ryan
Created: February 11, 2026
"""

import json
import time
from pathlib import Path
from datetime import datetime


def load_icm_ids():
    """Load ICM IDs from file"""
    ids_file = Path(__file__).parent / "data" / "expanded_by_design_icm_ids.txt"
    
    with open(ids_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def load_existing_details():
    """Load any previously fetched details to avoid re-fetching"""
    details_file = Path(__file__).parent / "data" / "expanded_by_design_icm_details.json"
    
    if details_file.exists():
        with open(details_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {}


def save_icm_details(all_details):
    """Save ICM details to file"""
    output_file = Path(__file__).parent / "data" / "expanded_by_design_icm_details.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_details, f, indent=2)
    
    return output_file


def main():
    print("="*80)
    print("FETCHING ICM DETAILS - EXPANDED BY-DESIGN DATASET")
    print("="*80)
    print()
    
    # Load ICM IDs
    icm_ids = load_icm_ids()
    print(f"📋 Loaded {len(icm_ids)} ICM IDs")
    print()
    
    # Load existing details
    existing_details = load_existing_details()
    print(f"💾 Found {len(existing_details)} previously fetched ICMs")
    print()
    
    # Filter to only fetch new ones
    icm_ids_to_fetch = [icm_id for icm_id in icm_ids if str(icm_id) not in existing_details]
    
    if not icm_ids_to_fetch:
        print("✅ All ICM details already fetched!")
        print(f"📊 Total ICMs with details: {len(existing_details)}")
        return
    
    print(f"🔍 Need to fetch {len(icm_ids_to_fetch)} new ICMs")
    print()
    
    # Save the list for MCP fetching
    fetch_list_file = Path(__file__).parent / "data" / "icms_to_fetch.txt"
    with open(fetch_list_file, 'w') as f:
        for icm_id in icm_ids_to_fetch:
            f.write(f"{icm_id}\n")
    
    print(f"💾 Saved fetch list to: {fetch_list_file}")
    print()
    print("="*80)
    print("NEXT STEPS")
    print("="*80)
    print()
    print("The agent will now fetch details for each ICM using the ICM MCP.")
    print(f"This will require {len(icm_ids_to_fetch)} individual MCP calls.")
    print()
    print("Progress will be shown as details are fetched.")
    print()


if __name__ == "__main__":
    main()
