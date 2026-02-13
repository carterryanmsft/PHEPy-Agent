"""
Test Kusto Connection to ICM Cluster

This script tests the connection to the ICM Kusto cluster and runs
the low quality escalation query.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from low_quality_escalation_agent import LowQualityEscalationAgent
from lq_email_report_generator import EmailReportGenerator


def main():
    """Test Kusto connection and run analysis."""
    print("="*80)
    print("Testing ICM Kusto Connection")
    print("="*80)
    print()
    
    # Initialize agent (without passing a kusto_client - it will create its own)
    agent = LowQualityEscalationAgent()
    
    try:
        # Load escalations from ICM Kusto (last 30 days)
        print("Connecting to ICM Kusto cluster...")
        print("Cluster: https://icmcluster.kusto.windows.net")
        print("Database: IcMDataWarehouse")
        print()
        
        agent.load_escalations(days_back=30)
        
        # Show summary
        print("\n" + "="*80)
        print("QUERY RESULTS")
        print("="*80)
        
        stats = agent.generate_summary_stats()
        print(f"\nTotal Low Quality Escalations: {stats['total_escalations']}")
        print(f"Unique Escalation Owners: {stats['unique_owners']}")
        print(f"Teams Affected: {stats['teams_affected']}")
        
        print("\nBy Severity:")
        for severity, count in sorted(stats['by_severity'].items()):
            print(f"  Sev {severity}: {count}")
        
        print("\nTop 5 Teams:")
        for team, count in sorted(stats['by_team'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {team}: {count}")
        
        print("\nTop Quality Reasons:")
        for reason, count in sorted(stats['by_quality_reason'].items(), key=lambda x: x[1], reverse=True)[:5]:
            if reason:
                print(f"  {reason}: {count}")
        
        # Organize by owner
        organized = agent.organize_by_owner()
        print(f"\n\nEscalation Owners: {len(organized)}")
        print("\nTop 5 Owners by Escalation Count:")
        for owner, escalations in sorted(organized.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            print(f"  {owner}: {len(escalations)} escalations")
        
        # Generate reports
        print("\n" + "="*80)
        print("GENERATING REPORTS")
        print("="*80)
        
        csv_path = agent.generate_csv_report()
        print(f"\n✓ CSV Report: {csv_path}")
        
        output_files = agent.export_for_review()
        print(f"\n✓ Generated {len(output_files)} JSON reports")
        
        # Generate email reports
        reviewer_assignments = agent.assign_to_reviewers()
        if reviewer_assignments:
            email_gen = EmailReportGenerator()
            stats['current_fiscal_week'] = 24
            
            results = email_gen.generate_and_send_reports(
                reviewer_assignments,
                stats=stats,
                save_to_file=True,
                send_email=False
            )
            
            print(f"✓ Generated {len(results['saved_files'])} HTML email reports")
        
        print("\n" + "="*80)
        print("SUCCESS! ICM Kusto connection working")
        print("="*80)
        
    except Exception as e:
        print("\n" + "="*80)
        print("ERROR")
        print("="*80)
        print(f"\n{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
