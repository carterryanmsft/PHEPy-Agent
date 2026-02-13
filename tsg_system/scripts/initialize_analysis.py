"""
Initialize TSG Gap Analysis with Sample Dataset
Demonstrates the workflow with the incidents already retrieved
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from batch_icm_retriever import BatchICMRetriever

# Sample incident IDs from previous retrieval
SAMPLE_INCIDENT_IDS = [
    51000000879655,  # Sensitivity label migration RFC
    51000000879746,  # Encryption label issues in OWA/New Outlook
    51000000879362,  # DCR for file scanning limits
    741203392,       # Office legacy file format labeling issues
    51000000878019,  # General Password SIT detection issues
    51000000877201,  # Missing CapexApproved Orders
]

def initialize_sample_dataset():
    """Initialize retriever with sample incident IDs"""
    print("Initializing TSG Gap Analysis with sample dataset...")
    print(f"Sample size: {len(SAMPLE_INCIDENT_IDS)} incidents")
    print()
    
    retriever = BatchICMRetriever()
    retriever.set_incident_ids(SAMPLE_INCIDENT_IDS)
    
    print("✓ Sample dataset initialized")
    print()
    print("Next steps:")
    print("1. Retrieve details for these incidents using MCP")
    print("2. Save each incident with retriever.save_incident()")
    print("3. Run TSG gap analysis")
    print()
    
    # Show next batch to retrieve
    next_batch = retriever.get_next_batch(batch_size=6)
    print("Incidents to retrieve:")
    for iid in next_batch:
        print(f"  mcp_icm_mcp_eng_get_incident_details_by_id(incidentId={iid})")
    
    return retriever


def initialize_full_dataset(incident_ids: list):
    """Initialize retriever with full dataset from Kusto query"""
    print(f"Initializing TSG Gap Analysis with {len(incident_ids)} incidents...")
    
    retriever = BatchICMRetriever()
    retriever.set_incident_ids(incident_ids)
    
    print("✓ Full dataset initialized")
    retriever.print_status()
    
    # Show first batch
    next_batch = retriever.get_next_batch(batch_size=10)
    print("\nFirst batch to retrieve:")
    for i, iid in enumerate(next_batch[:5], 1):
        print(f"  {i}. {iid}")
    if len(next_batch) > 5:
        print(f"  ... and {len(next_batch) - 5} more")
    
    return retriever


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize TSG Gap Analysis")
    parser.add_argument('--mode', choices=['sample', 'full'], default='sample',
                       help='Initialize with sample or full dataset')
    parser.add_argument('--ids-file', help='JSON file with incident IDs for full mode')
    
    args = parser.parse_args()
    
    if args.mode == 'sample':
        initialize_sample_dataset()
    elif args.mode == 'full':
        if not args.ids_file:
            print("Error: --ids-file required for full mode")
            sys.exit(1)
        
        import json
        with open(args.ids_file, 'r') as f:
            data = json.load(f)
            incident_ids = data.get('incident_ids', [])
        
        initialize_full_dataset(incident_ids)
