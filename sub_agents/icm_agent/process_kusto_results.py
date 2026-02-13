"""
Process Kusto Results and Fetch ICM Details

Extracts unique ICM IDs from Kusto results and fetches detailed information

Author: Carter Ryan
Created: February 11, 2026
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def extract_unique_icm_ids(kusto_results_file):
    """Extract unique ICM IDs from Kusto results"""
    
    print("📂 Reading Kusto results...")
    with open(kusto_results_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse JSON
    start_idx = content.find('{')
    if start_idx == -1:
        print("❌ No JSON found in file")
        return []
    
    data = json.loads(content[start_idx:])
    
    # Extract unique ICM IDs
    icm_ids = set()
    for row in data.get('data', []):
        icm_id = row.get('IncidentId')
        if icm_id:
            icm_ids.add(icm_id)
    
    return sorted(list(icm_ids), reverse=True)


def main():
    print("="*80)
    print("PROCESSING KUSTO RESULTS - EXTRACTING ICM IDS")
    print("="*80)
    print()
    
    # Get the most recent Kusto results file
    temp_dir = Path(r"c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\0b3a52cb-5056-42f6-b403-95846ca4b223")
    
    kusto_files = list(temp_dir.glob("toolu_*__vscode-*/content.txt"))
    if not kusto_files:
        print("❌ No Kusto results found")
        return
    
    # Get most recent
    kusto_file = max(kusto_files, key=lambda p: p.stat().st_mtime)
    print(f"Using: {kusto_file.name}")
    print()
    
    # Extract ICM IDs
    icm_ids = extract_unique_icm_ids(kusto_file)
    
    print(f"✅ Found {len(icm_ids)} unique ICM IDs")
    print()
    
    # Save ICM IDs
    output_file = Path(__file__).parent / "data" / "expanded_by_design_icm_ids.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        for icm_id in icm_ids:
            f.write(f"{icm_id}\n")
    
    print(f"💾 Saved ICM IDs to: {output_file}")
    print()
    
    # Show sample
    print("📋 Sample ICM IDs (first 20):")
    for icm_id in icm_ids[:20]:
        print(f"   {icm_id}")
    
    if len(icm_ids) > 20:
        print(f"   ... and {len(icm_ids) - 20} more")
    
    print()
    print("="*80)
    print("✅ READY TO FETCH DETAILS")
    print("="*80)
    print()
    print(f"📊 Total ICMs to analyze: {len(icm_ids)}")
    print()
    print("⚠️  Note: Fetching details for this many ICMs may take significant time.")
    print("   Consider running in batches if needed.")
    print()
    print("Next step: Run fetch script to get details via ICM MCP")
    print()


if __name__ == "__main__":
    main()
