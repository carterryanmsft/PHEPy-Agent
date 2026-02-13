"""
Weekly Low Quality Escalation Analysis Runner

Automated script to run weekly low quality escalation analysis and distribute
email reports to reviewers. Can be scheduled via Windows Task Scheduler or cron.

Author: Carter Ryan
Created: February 4, 2026
"""

import os
import sys
import json
from datetime import datetime, timedelta
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from low_quality_escalation_agent import LowQualityEscalationAgent
from lq_email_report_generator import EmailReportGenerator


class WeeklyRunner:
    """Runner for weekly low quality escalation analysis."""
    
    def __init__(self, config_path: str = None, kusto_client=None):
        """
        Initialize the weekly runner.
        
        Args:
            config_path: Path to configuration file
            kusto_client: Kusto client for running queries
        """
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 'lq_escalation_config.json'
        )
        self.kusto_client = kusto_client
        self.agent = LowQualityEscalationAgent(kusto_client=kusto_client, config_path=self.config_path)
        self.email_generator = EmailReportGenerator(config_path=self.config_path)
        
    def run_weekly_analysis(self, days_back: int = 7, send_emails: bool = True,
                          save_reports: bool = True) -> Dict:
        """
        Run the complete weekly analysis and distribution workflow.
        
        Args:
            days_back: Number of days to analyze (default 7 for weekly)
            send_emails: Whether to send emails to reviewers
            save_reports: Whether to save reports to files
            
        Returns:
            Dictionary with run results
        """
        print(f"\n{'='*80}")
        print(f"Weekly Low Quality Escalation Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        run_results = {
            'start_time': datetime.now().isoformat(),
            'days_analyzed': days_back,
            'success': False,
            'error': None
        }
        
        try:
            # Step 1: Load escalation data
            print(f"Step 1: Loading escalation data for last {days_back} days...")
            self.agent.load_escalations(days_back=days_back)
            
            if self.agent.escalations_data is None or len(self.agent.escalations_data) == 0:
                print("No low quality escalations found for the period.")
                run_results['escalation_count'] = 0
                run_results['success'] = True
                return run_results
            
            # Step 2: Organize by owner
            print("\nStep 2: Organizing escalations by owner...")
            self.agent.organize_by_owner()
            
            # Step 3: Generate summary statistics
            print("\nStep 3: Generating summary statistics...")
            stats = self.agent.generate_summary_stats()
            stats['current_fiscal_week'] = self._get_current_fiscal_week()
            
            print(f"\n  Total Escalations: {stats['total_escalations']}")
            print(f"  Unique Owners: {stats['unique_owners']}")
            print(f"  Teams Affected: {stats['teams_affected']}")
            
            # Step 4: Assign to reviewers
            print("\nStep 4: Assigning escalations to reviewers...")
            reviewer_assignments = self.agent.assign_to_reviewers()
            
            print(f"  Reviewers with assignments: {len(reviewer_assignments)}")
            for reviewer, owners_data in reviewer_assignments.items():
                escalation_count = sum(len(escs) for escs in owners_data.values())
                print(f"    {reviewer}: {escalation_count} escalations from {len(owners_data)} owners")
            
            # Step 5: Generate and distribute reports
            print("\nStep 5: Generating and distributing reports...")
            email_results = self.email_generator.generate_and_send_reports(
                reviewer_assignments,
                stats=stats,
                save_to_file=save_reports,
                send_email=send_emails
            )
            
            # Step 6: Export data files
            print("\nStep 6: Exporting data files...")
            output_files = self.agent.export_for_review()
            csv_path = self.agent.generate_csv_report()
            
            # Compile results
            run_results.update({
                'success': True,
                'escalation_count': stats['total_escalations'],
                'unique_owners': stats['unique_owners'],
                'teams_affected': stats['teams_affected'],
                'reviewers_notified': len(reviewer_assignments),
                'reports_generated': len(email_results['generated']),
                'reports_saved': len(email_results['saved_files']),
                'emails_sent': len(email_results['sent']),
                'emails_failed': len(email_results['failed']),
                'output_files': output_files,
                'csv_report': csv_path,
                'saved_report_files': email_results['saved_files']
            })
            
            print(f"\n{'='*80}")
            print("Weekly Analysis Complete")
            print(f"{'='*80}")
            print(f"  Escalations Analyzed: {run_results['escalation_count']}")
            print(f"  Reports Generated: {run_results['reports_generated']}")
            print(f"  Emails Sent: {run_results['emails_sent']}")
            print(f"  Reports Saved: {run_results['reports_saved']}")
            print(f"{'='*80}\n")
            
        except Exception as e:
            print(f"\nERROR: Analysis failed - {e}")
            import traceback
            traceback.print_exc()
            run_results['success'] = False
            run_results['error'] = str(e)
        
        finally:
            run_results['end_time'] = datetime.now().isoformat()
            self._save_run_log(run_results)
        
        return run_results
    
    def _get_current_fiscal_week(self) -> int:
        """Calculate current fiscal week (Microsoft FY)."""
        # Microsoft fiscal year starts July 1
        # This is a simplified calculation - adjust based on your fiscal calendar
        today = datetime.now()
        
        # Determine fiscal year start
        if today.month >= 7:
            fy_start = datetime(today.year, 7, 1)
        else:
            fy_start = datetime(today.year - 1, 7, 1)
        
        # Calculate weeks since FY start
        days_diff = (today - fy_start).days
        fiscal_week = (days_diff // 7) + 1
        
        return fiscal_week
    
    def _save_run_log(self, run_results: Dict):
        """Save run log to file for auditing and debugging."""
        log_dir = os.path.join(os.path.dirname(__file__), 'lq_escalation_logs')
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'weekly_run_{timestamp}.json')
        
        try:
            with open(log_file, 'w') as f:
                json.dump(run_results, f, indent=2)
            print(f"Run log saved to: {log_file}")
        except Exception as e:
            print(f"Warning: Could not save run log - {e}")
    
    def test_run(self, days_back: int = 7):
        """
        Run in test mode - generates reports but doesn't send emails.
        
        Args:
            days_back: Number of days to analyze
        """
        print("\n*** RUNNING IN TEST MODE - NO EMAILS WILL BE SENT ***\n")
        return self.run_weekly_analysis(
            days_back=days_back,
            send_emails=False,
            save_reports=True
        )


def setup_kusto_client():
    """
    Setup Kusto client for connecting to ICM database.
    
    Returns:
        Kusto client instance or None
    """
    try:
        from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
        from azure.identity import DefaultAzureCredential
        
        # ICM Cluster configuration
        cluster = 'https://icmcluster.kusto.windows.net'
        database = 'IcMDataWarehouse'
        
        print(f"Connecting to ICM Kusto cluster: {cluster}")
        print(f"Database: {database}")
        
        # Use AAD authentication
        kcsb = KustoConnectionStringBuilder.with_azure_token_credential(cluster, DefaultAzureCredential())
        client = KustoClient(kcsb)
        
        # Store database for reference
        client.database = database
        
        print(f"✓ Successfully connected to ICM Kusto")
        return client
        
    except ImportError:
        print("\n✗ ERROR: Azure Kusto SDK not installed")
        print("Install with: pip install azure-kusto-data azure-identity")
        return None
    except Exception as e:
        print(f"\n✗ ERROR: Could not connect to Kusto - {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure you're logged in: az login")
        print("  2. Verify cluster access permissions")
        print("  3. Check network connectivity")
        return None


def main():
    """Main entry point for the weekly runner."""
    parser = argparse.ArgumentParser(
        description='Run weekly low quality escalation analysis and reporting'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to analyze (default: 7)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run in test mode (no emails sent)'
    )
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip sending emails'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    parser.add_argument(
        '--from-file',
        type=str,
        help='Load data from JSON file instead of querying Kusto'
    )
    
    args = parser.parse_args()
    
    # Setup Kusto client
    kusto_client = None
    if not args.from_file:
        kusto_client = setup_kusto_client()
        if kusto_client is None:
            print("\nError: Could not connect to Kusto and no data file provided.")
            print("Either fix Kusto connection or provide --from-file argument.")
            sys.exit(1)
    
    # Initialize runner
    runner = WeeklyRunner(config_path=args.config, kusto_client=kusto_client)
    
    # If loading from file, override the agent's load method
    if args.from_file:
        print(f"Loading data from file: {args.from_file}")
        runner.agent.load_escalations(from_file=args.from_file)
    
    # Run analysis
    try:
        if args.test:
            results = runner.test_run(days_back=args.days)
        else:
            send_emails = not args.no_email
            results = runner.run_weekly_analysis(
                days_back=args.days,
                send_emails=send_emails,
                save_reports=True
            )
        
        # Exit with appropriate code
        sys.exit(0 if results['success'] else 1)
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
