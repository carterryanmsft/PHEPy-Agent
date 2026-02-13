"""
Send IC MCS Risk Report via email using Microsoft Graph API
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from send_email_graph import send_email, send_html_report

# Email Configuration
TO_RECIPIENTS = [
    'your.email@microsoft.com',
    # Add more recipients
]

CC_RECIPIENTS = [
    # Add CC recipients if needed
]

SUBJECT = 'IC MCS Automated Risk Report'

# Report file to send
REPORT_FILE = 'IC_MCS_REPORT_IC.htm'


def send_latest_report():
    """Send the latest IC MCS report"""
    
    report_path = Path(__file__).parent / REPORT_FILE
    
    if not report_path.exists():
        print(f"✗ Report file not found: {report_path}")
        return False
    
    # Send the report
    success = send_html_report(
        to_recipients=TO_RECIPIENTS,
        subject=SUBJECT,
        html_file_path=str(report_path),
        cc_recipients=CC_RECIPIENTS if CC_RECIPIENTS else None
    )
    
    return success


def send_report_with_summary(summary_text=''):
    """Send report with a summary message"""
    
    report_path = Path(__file__).parent / REPORT_FILE
    
    if not report_path.exists():
        print(f"✗ Report file not found: {report_path}")
        return False
    
    # Read the HTML report
    with open(report_path, 'r', encoding='utf-8') as f:
        report_html = f.read()
    
    # Create email body with summary
    email_body = f"""
    <div style="font-family: Arial, sans-serif;">
        <h2>IC MCS Automated Risk Report</h2>
        <p><strong>Generated:</strong> {Path(report_path).stat().st_mtime}</p>
        {f'<p>{summary_text}</p>' if summary_text else ''}
        <hr>
        {report_html}
    </div>
    """
    
    success = send_email(
        to_recipients=TO_RECIPIENTS,
        subject=SUBJECT,
        body=email_body,
        body_type='HTML',
        cc_recipients=CC_RECIPIENTS if CC_RECIPIENTS else None
    )
    
    return success


if __name__ == '__main__':
    # Update TO_RECIPIENTS before running
    if 'your.email@microsoft.com' in TO_RECIPIENTS:
        print("⚠ Please update TO_RECIPIENTS in the script with actual email addresses")
        exit(1)
    
    # Send the report
    print("Sending IC MCS Risk Report...")
    success = send_latest_report()
    
    if success:
        print("✓ Report sent successfully!")
    else:
        print("✗ Failed to send report")
