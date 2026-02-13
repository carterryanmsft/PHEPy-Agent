"""
Send Regional LQE Reports via Email using Microsoft Graph API

This module sends the regional LQE HTML reports to designated reviewers
via Microsoft Graph API.

Author: Carter Ryan
Created: February 11, 2026
"""

import os
import sys
import json
from pathlib import Path
from msal import ConfidentialClientApplication
import requests

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from send_email_graph import send_email
except ImportError:
    print("⚠ Error: send_email_graph.py not found")
    print("Make sure send_email_graph.py is in the parent directory")
    sys.exit(1)


def load_regional_config():
    """Load regional reviewer configuration."""
    config_path = Path(__file__).parent / 'regional_reviewers_config.json'
    with open(config_path, 'r') as f:
        return json.load(f)


def get_reviewer_emails_for_region(region: str, feature_area: str, config: dict) -> list:
    """Get list of reviewer emails for a specific region and feature area."""
    region_config = config.get('regions', {}).get(region, {})
    reviewers = region_config.get(feature_area, [])
    return [r['email'] for r in reviewers]


def send_regional_lqe_report(region: str, html_content: str, report_summary: dict, 
                              from_email: str = None, test_mode: bool = False):
    """
    Send a regional LQE report via email.
    
    Args:
        region: Region name (Americas, EMEA, APAC)
        html_content: HTML content of the report
        report_summary: Summary dict with total counts and feature breakdowns
        from_email: Sender email address (default: current user)
        test_mode: If True, only send to sender for testing
    """
    config = load_regional_config()
    
    # Build subject
    total = report_summary.get('total_count', 0)
    subject = f"{region} Region - Low Quality Escalation Review ({total} cases) - Last 7 Days"
    
    # Get all unique reviewers for this region
    all_reviewers = set()
    for feature_area in report_summary.get('by_feature_area', {}).keys():
        emails = get_reviewer_emails_for_region(region, feature_area, config)
        all_reviewers.update(emails)
    
    if not all_reviewers:
        print(f"⚠ No reviewers configured for {region} region")
        return False
    
    recipients = list(all_reviewers)
    
    # Test mode - only send to sender
    if test_mode:
        if from_email:
            recipients = [from_email]
            subject = f"[TEST] {subject}"
        else:
            print("⚠ Test mode requires from_email to be specified")
            return False
    
    print(f"Sending {region} report to: {', '.join(recipients)}")
    
    # Send email
    try:
        result = send_email(
            to_recipients=recipients,
            subject=subject,
            body=html_content,
            body_type='HTML',
            from_user=from_email
        )
        
        if result:
            print(f"✓ {region} report sent successfully")
            return True
        else:
            print(f"✗ Failed to send {region} report")
            return False
            
    except Exception as e:
        print(f"✗ Error sending {region} report: {e}")
        return False


def send_all_regional_reports(reports_dir: str = None, from_email: str = None, 
                               test_mode: bool = False):
    """
    Send all generated regional reports.
    
    Args:
        reports_dir: Directory containing the reports (default: regional_reports)
        from_email: Sender email address
        test_mode: If True, only send to sender for testing
    """
    if reports_dir is None:
        reports_dir = Path(__file__).parent / 'regional_reports'
    else:
        reports_dir = Path(reports_dir)
    
    # Find the most recent reports
    regions = ['americas', 'emea', 'apac']
    results = {}
    
    for region in regions:
        # Find most recent HTML file for this region
        html_files = sorted(reports_dir.glob(f'{region}_lqe_report_*.htm'))
        if not html_files:
            print(f"⚠ No report found for {region}")
            continue
        
        latest_html = html_files[-1]
        json_file = latest_html.with_suffix('.json')
        
        if not json_file.exists():
            print(f"⚠ JSON file not found for {region}: {json_file}")
            continue
        
        # Load HTML content
        with open(latest_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Load summary from JSON
        with open(json_file, 'r') as f:
            report_data = json.load(f)
            summary = report_data.get('summary', {})
        
        # Send email
        success = send_regional_lqe_report(
            region=region.upper(),
            html_content=html_content,
            report_summary=summary,
            from_email=from_email,
            test_mode=test_mode
        )
        
        results[region] = success
    
    # Print summary
    print("\n" + "=" * 80)
    print("EMAIL SENDING SUMMARY")
    print("=" * 80)
    for region, success in results.items():
        status = "✓ Sent" if success else "✗ Failed"
        print(f"{region.upper()}: {status}")
    
    return results


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Send regional LQE reports via email')
    parser.add_argument('--reports-dir', help='Directory containing reports')
    parser.add_argument('--from-email', help='Sender email address')
    parser.add_argument('--test', action='store_true', 
                       help='Test mode - only send to sender')
    
    args = parser.parse_args()
    
    if args.test and not args.from_email:
        print("Error: --from-email required when using --test mode")
        return 1
    
    send_all_regional_reports(
        reports_dir=args.reports_dir,
        from_email=args.from_email,
        test_mode=args.test
    )


if __name__ == '__main__':
    main()
