"""
Email Report Generator for Low Quality Escalation Insights

Generates formatted HTML email reports for reviewers with their assigned
low quality escalations to review.

Author: Carter Ryan
Created: February 4, 2026
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


class EmailReportGenerator:
    """Generator for formatted email reports to reviewers."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize the email report generator.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 'lq_escalation_config.json'
        )
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def generate_html_report(self, reviewer_email: str, escalations_by_owner: Dict[str, List[Dict]],
                           stats: Dict[str, Any] = None) -> str:
        """
        Generate HTML email report for a reviewer.
        
        Args:
            reviewer_email: Reviewer's email address
            escalations_by_owner: Dictionary mapping owner to their escalations
            stats: Optional summary statistics
            
        Returns:
            HTML string for email body
        """
        total_escalations = sum(len(escs) for escs in escalations_by_owner.values())
        owner_count = len(escalations_by_owner)
        
        # Get current fiscal week
        fiscal_week = stats.get('current_fiscal_week', 'N/A') if stats else 'N/A'
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #0078d4;
            border-bottom: 3px solid #0078d4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #106ebe;
            margin-top: 30px;
            border-left: 4px solid #0078d4;
            padding-left: 10px;
        }}
        h3 {{
            color: #323130;
            margin-top: 20px;
        }}
        .summary {{
            background-color: #f3f2f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .summary-stat {{
            display: inline-block;
            margin-right: 30px;
            font-size: 16px;
        }}
        .summary-stat strong {{
            color: #0078d4;
            font-size: 24px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background-color: white;
        }}
        th {{
            background-color: #0078d4;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e1dfdd;
        }}
        tr:hover {{
            background-color: #f3f2f1;
        }}
        .owner-section {{
            margin-bottom: 40px;
            border: 1px solid #e1dfdd;
            border-radius: 5px;
            padding: 20px;
            background-color: #fafafa;
        }}
        .owner-header {{
            background-color: #e1dfdd;
            padding: 10px 15px;
            margin: -20px -20px 20px -20px;
            border-radius: 5px 5px 0 0;
        }}
        .severity-high {{
            color: #a80000;
            font-weight: bold;
        }}
        .severity-medium {{
            color: #f7630c;
            font-weight: bold;
        }}
        .severity-low {{
            color: #107c10;
        }}
        .incident-link {{
            color: #0078d4;
            text-decoration: none;
        }}
        .incident-link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e1dfdd;
            font-size: 12px;
            color: #605e5c;
        }}
        .action-required {{
            background-color: #fff4ce;
            border-left: 4px solid #f7630c;
            padding: 15px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Weekly Low Quality Escalation Review</h1>
        
        <div class="summary">
            <div class="summary-stat">
                <strong>{total_escalations}</strong><br>
                Total Escalations to Review
            </div>
            <div class="summary-stat">
                <strong>{owner_count}</strong><br>
                Escalation Owners
            </div>
            <div class="summary-stat">
                <strong>Week {fiscal_week}</strong><br>
                Fiscal Week
            </div>
        </div>
        
        <div class="action-required">
            <strong>⚠️ Action Required:</strong> Please review the low quality escalations below 
            and follow up with the respective escalation owners to improve future escalation quality.
        </div>
"""
        
        # Generate sections for each owner
        for owner, escalations in sorted(escalations_by_owner.items()):
            html += self._generate_owner_section(owner, escalations)
        
        # Footer
        html += f"""
        <div class="footer">
            <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Reviewer:</strong> {reviewer_email}</p>
            <p>This is an automated report from the Low Quality Escalation Insight Agent.</p>
            <p>For questions or issues, please contact the Escalation Quality Team.</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_owner_section(self, owner: str, escalations: List[Dict]) -> str:
        """Generate HTML section for one owner's escalations."""
        escalation_count = len(escalations)
        
        html = f"""
        <div class="owner-section">
            <div class="owner-header">
                <h2 style="margin: 0;">👤 {owner}</h2>
                <p style="margin: 5px 0 0 0; font-size: 14px;">
                    {escalation_count} escalation{'s' if escalation_count != 1 else ''} to review
                </p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Incident ID</th>
                        <th>Title</th>
                        <th>Severity</th>
                        <th>Team</th>
                        <th>Quality Issue</th>
                        <th>Low Quality Reason</th>
                        <th>Resolved Date</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Add each escalation
        for esc in sorted(escalations, key=lambda x: x.get('ResolveDate', ''), reverse=True):
            incident_id = esc.get('IncidentId', 'N/A')
            icm_id = esc.get('IcMId', '')
            routing_id = esc.get('RoutingId', '')
            title = esc.get('Title', 'No title')
            severity = esc.get('Severity', 'N/A')
            team = esc.get('OwningTeam', 'N/A')
            quality = esc.get('EscalationQuality', 'N/A')
            reason = esc.get('LowQualityReason', 'Not specified')
            resolve_date = esc.get('ResolveDate', 'N/A')
            
            # Format severity with color
            severity_class = ''
            if 'Sev' in str(severity):
                if '0' in str(severity) or '1' in str(severity):
                    severity_class = 'severity-high'
                elif '2' in str(severity):
                    severity_class = 'severity-medium'
                else:
                    severity_class = 'severity-low'
            
            # Create incident link
            incident_link = f"IcM {icm_id}" if icm_id else incident_id
            
            # Format resolve date
            if resolve_date and resolve_date != 'N/A':
                try:
                    if 'T' in resolve_date:
                        dt = datetime.fromisoformat(resolve_date.replace('Z', '+00:00'))
                        resolve_date = dt.strftime('%Y-%m-%d')
                except:
                    pass
            
            html += f"""
                    <tr>
                        <td><span class="incident-link">{incident_link}</span></td>
                        <td>{title[:80]}{'...' if len(title) > 80 else ''}</td>
                        <td class="{severity_class}">{severity}</td>
                        <td>{team}</td>
                        <td>{quality}</td>
                        <td>{reason}</td>
                        <td>{resolve_date}</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
"""
        return html
    
    def generate_text_report(self, reviewer_email: str, escalations_by_owner: Dict[str, List[Dict]],
                           stats: Dict[str, Any] = None) -> str:
        """
        Generate plain text email report for a reviewer.
        
        Args:
            reviewer_email: Reviewer's email address
            escalations_by_owner: Dictionary mapping owner to their escalations
            stats: Optional summary statistics
            
        Returns:
            Plain text string for email body
        """
        total_escalations = sum(len(escs) for escs in escalations_by_owner.values())
        owner_count = len(escalations_by_owner)
        fiscal_week = stats.get('current_fiscal_week', 'N/A') if stats else 'N/A'
        
        text = f"""
{'='*80}
Weekly Low Quality Escalation Review
{'='*80}

SUMMARY
-------
Total Escalations to Review: {total_escalations}
Escalation Owners: {owner_count}
Fiscal Week: {fiscal_week}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Reviewer: {reviewer_email}

ACTION REQUIRED: Please review the low quality escalations below and follow up
with the respective escalation owners to improve future escalation quality.

"""
        
        for owner, escalations in sorted(escalations_by_owner.items()):
            text += f"\n{'='*80}\n"
            text += f"OWNER: {owner}\n"
            text += f"Escalations to Review: {len(escalations)}\n"
            text += f"{'='*80}\n\n"
            
            for i, esc in enumerate(sorted(escalations, key=lambda x: x.get('ResolveDate', ''), reverse=True), 1):
                text += f"{i}. Incident: {esc.get('IcMId', esc.get('IncidentId', 'N/A'))}\n"
                text += f"   Title: {esc.get('Title', 'No title')}\n"
                text += f"   Severity: {esc.get('Severity', 'N/A')}\n"
                text += f"   Team: {esc.get('OwningTeam', 'N/A')}\n"
                text += f"   Quality Issue: {esc.get('EscalationQuality', 'N/A')}\n"
                text += f"   Reason: {esc.get('LowQualityReason', 'Not specified')}\n"
                text += f"   Resolved: {esc.get('ResolveDate', 'N/A')}\n"
                text += f"\n"
        
        text += f"\n{'='*80}\n"
        text += "This is an automated report from the Low Quality Escalation Insight Agent.\n"
        text += "For questions or issues, please contact the Escalation Quality Team.\n"
        text += f"{'='*80}\n"
        
        return text
    
    def create_email_message(self, to_email: str, subject: str, html_body: str, 
                           text_body: str = None, cc_list: List[str] = None) -> MIMEMultipart:
        """
        Create MIME email message with HTML and optional plain text.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML email body
            text_body: Optional plain text body
            cc_list: Optional list of CC recipients
            
        Returns:
            MIMEMultipart email message
        """
        email_settings = self.config.get('email_settings', {})
        from_email = email_settings.get('send_from', 'noreply@microsoft.com')
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        if cc_list:
            msg['Cc'] = ', '.join(cc_list)
        
        # Attach plain text version if provided
        if text_body:
            msg.attach(MIMEText(text_body, 'plain'))
        
        # Attach HTML version
        msg.attach(MIMEText(html_body, 'html'))
        
        return msg
    
    def send_email(self, msg: MIMEMultipart, smtp_server: str = None, 
                   smtp_port: int = 587, use_tls: bool = True) -> bool:
        """
        Send email message via SMTP.
        
        Args:
            msg: MIME email message
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            use_tls: Whether to use TLS
            
        Returns:
            True if sent successfully, False otherwise
        """
        # Note: This is a template - actual SMTP settings should be configured
        # for your environment. May need authentication, etc.
        
        try:
            if smtp_server is None:
                # Default to local SMTP relay
                smtp_server = 'localhost'
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if use_tls:
                    server.starttls()
                
                # If authentication is required:
                # server.login(username, password)
                
                server.send_message(msg)
            
            print(f"Email sent successfully to {msg['To']}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def save_report_to_file(self, reviewer_email: str, html_content: str, 
                          output_dir: str = None) -> str:
        """
        Save HTML report to file for testing or archiving.
        
        Args:
            reviewer_email: Reviewer's email
            html_content: HTML report content
            output_dir: Output directory
            
        Returns:
            Path to saved file
        """
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'lq_escalation_reports')
        
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        reviewer_name = reviewer_email.split('@')[0].replace('.', '_')
        filename = f"lq_report_{reviewer_name}_{timestamp}.html"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Report saved to: {filepath}")
        return filepath
    
    def generate_and_send_reports(self, reviewer_assignments: Dict[str, Dict[str, List[Dict]]],
                                stats: Dict[str, Any] = None, 
                                save_to_file: bool = True,
                                send_email: bool = False) -> Dict[str, Any]:
        """
        Generate and optionally send email reports to all reviewers.
        
        Args:
            reviewer_assignments: Dictionary mapping reviewer to their assignments
            stats: Summary statistics
            save_to_file: Whether to save reports to files
            send_email: Whether to send actual emails (requires SMTP setup)
            
        Returns:
            Dictionary with results
        """
        results = {
            'generated': [],
            'sent': [],
            'failed': [],
            'saved_files': []
        }
        
        email_settings = self.config.get('email_settings', {})
        subject_template = email_settings.get('subject_template', 
                                             'Weekly Low Quality Escalation Review - Week {fiscal_week}')
        fiscal_week = stats.get('current_fiscal_week', 'N/A') if stats else 'N/A'
        subject = subject_template.format(fiscal_week=fiscal_week)
        
        for reviewer_email, escalations_by_owner in reviewer_assignments.items():
            if not escalations_by_owner:
                print(f"No escalations for {reviewer_email}, skipping...")
                continue
            
            try:
                # Generate HTML report
                html_body = self.generate_html_report(reviewer_email, escalations_by_owner, stats)
                text_body = self.generate_text_report(reviewer_email, escalations_by_owner, stats)
                
                results['generated'].append(reviewer_email)
                
                # Save to file if requested
                if save_to_file:
                    filepath = self.save_report_to_file(reviewer_email, html_body)
                    results['saved_files'].append(filepath)
                
                # Send email if requested
                if send_email:
                    cc_list = email_settings.get('cc_list', [])
                    msg = self.create_email_message(reviewer_email, subject, html_body, text_body, cc_list)
                    
                    if self.send_email(msg):
                        results['sent'].append(reviewer_email)
                    else:
                        results['failed'].append(reviewer_email)
                        
            except Exception as e:
                print(f"Error processing report for {reviewer_email}: {e}")
                results['failed'].append(reviewer_email)
        
        return results


def main():
    """Test the email report generator."""
    # Sample data for testing
    sample_escalations = {
        "reviewer1@microsoft.com": {
            "owner1@microsoft.com": [
                {
                    "IncidentId": "INC123456",
                    "IcMId": "123456",
                    "RoutingId": "ROUTE123",
                    "Title": "Customer unable to access Purview catalog",
                    "Severity": "Sev2",
                    "OwningTeam": "Purview Data Catalog",
                    "ResolveDate": "2026-02-01T10:30:00Z",
                    "FiscalWeek": 24,
                    "EscalationQuality": "Missing Information",
                    "LowQualityReason": "Missing customer environment details",
                    "CustomerSegment": "Enterprise"
                }
            ]
        }
    }
    
    stats = {
        "current_fiscal_week": 24,
        "total_escalations": 1
    }
    
    # Generate report
    generator = EmailReportGenerator()
    results = generator.generate_and_send_reports(
        sample_escalations,
        stats=stats,
        save_to_file=True,
        send_email=False  # Set to True when SMTP is configured
    )
    
    print("\nReport Generation Results:")
    print(f"  Generated: {len(results['generated'])}")
    print(f"  Saved Files: {len(results['saved_files'])}")
    print(f"  Sent: {len(results['sent'])}")
    print(f"  Failed: {len(results['failed'])}")


if __name__ == "__main__":
    main()
