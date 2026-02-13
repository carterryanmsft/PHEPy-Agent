"""
Test Low Quality Escalation Agent with Sample Kusto Data

This script demonstrates the LQ Escalation agent using real sample data
from the Kusto query results.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from low_quality_escalation_agent import LowQualityEscalationAgent
from lq_email_report_generator import EmailReportGenerator

# Sample data from Kusto query (last 30 days)
SAMPLE_DATA = {
    "name": "PrimaryResult",
    "data": [
        {
            "IncidentId": 739305162,
            "IcMId": "739305162",
            "RoutingId": "icmportal://routing/1E668D6D5ADB4096BEED31BF7CC1D8AA",
            "Title": "[Issue] [CRI]: [GCCH] Deletion blocked by lingering retention policy",
            "Severity": 4,
            "CreatedBy": "v-contaylor@microsoftsupport.com",
            "OwningTeam": "PURVIEW\\DLMSharePointRetention",
            "ResolveDate": "2026-02-05T06:55:23.970Z",
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Information",
            "LowQualityReason": "Missing customer environment details",
            "QualityReviewFalsePositive": None,
            "CustomerSegment": "Enterprise",
            "IsTrueLowQuality": True
        },
        {
            "IncidentId": 739816278,
            "IcMId": "739816278",
            "RoutingId": "icmportal://routing/CB13C3CFB11F454EBA72072F1A50D4E3",
            "Title": "[Issue] Tenant-Wide Unified Policy Distribution Service Hang",
            "Severity": 3,
            "CreatedBy": "v-avinashas@microsoft.com",
            "OwningTeam": "PURVIEW\\DLMPolicyManagement",
            "ResolveDate": "2026-02-05T05:55:22.683Z",
            "FiscalWeek": 24,
            "EscalationQuality": "Insufficient Documentation",
            "LowQualityReason": "Incomplete troubleshooting steps documented",
            "QualityReviewFalsePositive": None,
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True
        },
        {
            "IncidentId": 739261768,
            "IcMId": "739261768",
            "RoutingId": "icmportal://routing/457ADBD0586645F482AF5E511081B29B",
            "Title": "[Issue] non-rcri",
            "Severity": 4,
            "CreatedBy": "olangness@microsoft.com",
            "OwningTeam": "PURVIEW\\MIPDLPEEE",
            "ResolveDate": "2026-01-26T20:20:50.560Z",
            "FiscalWeek": 23,
            "EscalationQuality": "Unclear Issue Description",
            "LowQualityReason": "Title does not describe the actual issue",
            "QualityReviewFalsePositive": None,
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True
        },
        {
            "IncidentId": 739643751,
            "IcMId": "739643751",
            "RoutingId": "icmportal://routing/1D57A6BFE3224B3AB5B0D08E74CD8C9A",
            "Title": "[Issue] Non-rCRI",
            "Severity": 4,
            "CreatedBy": "olangness@microsoft.com",
            "OwningTeam": "PURVIEW\\MIPDLPEEE",
            "ResolveDate": "2026-01-27T16:28:16.467Z",
            "FiscalWeek": 23,
            "EscalationQuality": "Unclear Issue Description",
            "LowQualityReason": "Insufficient context in escalation",
            "QualityReviewFalsePositive": None,
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True
        }
    ]
}


def save_sample_data():
    """Save sample data to a file for testing."""
    output_dir = Path(__file__).parent / 'test_data'
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'sample_lq_escalations.json'
    with open(output_file, 'w') as f:
        json.dump(SAMPLE_DATA['data'], f, indent=2)
    
    print(f"Sample data saved to: {output_file}")
    return str(output_file)


def main():
    """Test the LQ Escalation agent with sample data."""
    print("="*80)
    print("Testing Low Quality Escalation Agent with Sample Data")
    print("="*80)
    print()
    
    # Save sample data
    data_file = save_sample_data()
    
    # Initialize agent (without Kusto client)
    agent = LowQualityEscalationAgent()
    
    # Load sample data from file
    print(f"Loading sample escalations from: {data_file}")
    agent.load_escalations(from_file=data_file)
    
    # Analyze the data
    print("\n" + "="*80)
    print("DATA ANALYSIS")
    print("="*80)
    
    # Show summary statistics
    stats = agent.generate_summary_stats()
    print("\nSummary Statistics:")
    print(f"  Total Low Quality Escalations: {stats['total_escalations']}")
    print(f"  Unique Escalation Owners: {stats['unique_owners']}")
    print(f"  Teams Affected: {stats['teams_affected']}")
    
    print("\n  By Severity:")
    for severity, count in stats['by_severity'].items():
        print(f"    Sev {severity}: {count}")
    
    print("\n  By Team:")
    for team, count in stats['by_team'].items():
        print(f"    {team}: {count}")
    
    print("\n  By Quality Reason:")
    for reason, count in stats['by_quality_reason'].items():
        if reason:
            print(f"    {reason}: {count}")
    
    # Organize by owner
    print("\n" + "="*80)
    print("ESCALATIONS BY OWNER")
    print("="*80)
    
    organized = agent.organize_by_owner()
    for owner, escalations in sorted(organized.items()):
        print(f"\n{owner} ({len(escalations)} escalations):")
        for esc in escalations:
            print(f"  - IcM {esc['IcMId']}: {esc['Title'][:60]}...")
            print(f"    Reason: {esc['LowQualityReason']}")
    
    # Assign to reviewers
    print("\n" + "="*80)
    print("REVIEWER ASSIGNMENTS")
    print("="*80)
    
    reviewer_assignments = agent.assign_to_reviewers()
    
    if not reviewer_assignments:
        print("\nNo reviewer assignments configured.")
        print("Update lq_escalation_config.json to map owners to reviewers.")
    else:
        for reviewer, owners_data in reviewer_assignments.items():
            total_escs = sum(len(escs) for escs in owners_data.values())
            print(f"\n{reviewer}: {total_escs} escalations from {len(owners_data)} owners")
            for owner, escalations in owners_data.items():
                print(f"  - {owner}: {len(escalations)} escalations")
    
    # Generate test reports
    print("\n" + "="*80)
    print("GENERATING TEST REPORTS")
    print("="*80)
    
    # Generate CSV
    csv_path = agent.generate_csv_report()
    print(f"\nCSV Report: {csv_path}")
    
    # Generate JSON reports for each reviewer
    output_files = agent.export_for_review()
    print(f"\nJSON Reports generated:")
    for reviewer, filepath in output_files.items():
        print(f"  {reviewer}: {filepath}")
    
    # Generate HTML email reports
    if reviewer_assignments:
        email_gen = EmailReportGenerator()
        stats['current_fiscal_week'] = 24  # Add fiscal week to stats
        
        results = email_gen.generate_and_send_reports(
            reviewer_assignments,
            stats=stats,
            save_to_file=True,
            send_email=False  # Don't actually send emails in test
        )
        
        print(f"\nHTML Email Reports generated:")
        for filepath in results['saved_files']:
            print(f"  {filepath}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    print("\nNext Steps:")
    print("1. Update lq_escalation_config.json with actual reviewer mappings")
    print("2. Review the generated HTML reports in lq_escalation_reports/")
    print("3. Verify the CSV export looks correct")
    print("4. Configure SMTP settings for email delivery")
    print("5. Set up weekly automation with run_weekly_lq_analysis.py")
    

if __name__ == "__main__":
    main()
