"""
TSG Gap Analysis Workflow
Complete workflow for analyzing ICM incidents to identify TSG gaps
"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from tsg_gap_analyzer import TSGGapAnalyzer
from batch_icm_retriever import BatchICMRetriever


def run_tsg_gap_analysis():
    """Run complete TSG gap analysis workflow"""
    
    print("=" * 80)
    print("TSG GAP ANALYSIS WORKFLOW")
    print("=" * 80)
    print()
    
    # Step 1: Initialize retriever and check status
    print("Step 1: Checking ICM incident retrieval status...")
    retriever = BatchICMRetriever(output_dir="tsg_system/data")
    retriever.print_status()
    
    status = retriever.get_status()
    
    if status['remaining'] > 0:
        print(f"\n⚠️  {status['remaining']} incidents still need to be retrieved.")
        print("Run retrieve_next_batch() to continue data collection.")
        print()
        
        # Show what to do next
        next_batch = retriever.get_next_batch(batch_size=10)
        if next_batch:
            print("Next batch to retrieve:")
            print(f"  Incident IDs: {next_batch[:5]}{'...' if len(next_batch) > 5 else ''}")
            print(f"  Total in batch: {len(next_batch)}")
            print()
            print("Use these MCP tool calls:")
            for iid in next_batch[:3]:
                print(f"  mcp_icm_mcp_eng_get_incident_details_by_id(incidentId={iid})")
            if len(next_batch) > 3:
                print(f"  ... and {len(next_batch) - 3} more")
        
        return None
    
    # Step 2: Load all retrieved incidents
    print("Step 2: Loading retrieved incidents...")
    incidents = retriever.load_all_incidents()
    print(f"✓ Loaded {len(incidents)} incidents")
    print()
    
    # Step 3: Analyze for TSG gaps
    print("Step 3: Analyzing TSG gaps...")
    analyzer = TSGGapAnalyzer()
    
    for incident in incidents:
        tsg_data = analyzer.extract_tsg_data(incident)
        analyzer.add_incident(tsg_data)
    
    print(f"✓ Analyzed {len(analyzer.incidents)} incidents")
    print()
    
    # Step 4: Generate and save results
    print("Step 4: Generating analysis results...")
    
    results_file = "tsg_system/reports/tsg_gap_analysis.json"
    report_file = "tsg_system/reports/tsg_gap_report.md"
    
    analyzer.save_results(results_file)
    
    # Generate human-readable report
    report = analyzer.generate_report()
    Path(report_file).parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✓ Results saved to {results_file}")
    print(f"✓ Report saved to {report_file}")
    print()
    
    # Step 5: Display summary
    print("=" * 80)
    print(report)
    
    return analyzer.analyze_gaps()


def retrieve_next_batch(batch_size: int = 10):
    """Helper function to retrieve next batch of incidents"""
    retriever = BatchICMRetriever()
    batch = retriever.get_next_batch(batch_size)
    
    if not batch:
        print("✓ All incidents retrieved!")
        retriever.print_status()
        return []
    
    print(f"Next batch: {len(batch)} incidents")
    print(f"IDs: {batch}")
    print()
    print("Copy these incident IDs to retrieve with MCP:")
    for iid in batch:
        print(f"  {iid}")
    
    return batch


def process_retrieved_incidents(incident_list: list):
    """Process a list of retrieved incident dictionaries"""
    retriever = BatchICMRetriever()
    
    saved_count = 0
    for incident in incident_list:
        try:
            retriever.save_incident(incident)
            saved_count += 1
        except Exception as e:
            incident_id = incident.get('id', 'unknown')
            retriever.mark_failed(incident_id, str(e))
            print(f"Failed to save incident {incident_id}: {e}")
    
    print(f"\n✓ Saved {saved_count} incidents")
    retriever.print_status()


def quick_status():
    """Quick status check"""
    retriever = BatchICMRetriever()
    retriever.print_status()
    
    status = retriever.get_status()
    if status['retrieved'] > 0:
        print(f"Data file: {retriever.data_file}")
        print(f"Progress file: {retriever.progress_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="TSG Gap Analysis Workflow")
    parser.add_argument('--action', choices=['status', 'next-batch', 'analyze'], 
                       default='status', help='Action to perform')
    parser.add_argument('--batch-size', type=int, default=10, 
                       help='Batch size for retrieval')
    
    args = parser.parse_args()
    
    if args.action == 'status':
        quick_status()
    elif args.action == 'next-batch':
        retrieve_next_batch(args.batch_size)
    elif args.action == 'analyze':
        run_tsg_gap_analysis()
