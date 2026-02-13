"""
Send emails using Microsoft Graph API
Requires: pip install msal requests
"""

import msal
import requests
import json
import os
from pathlib import Path

# Azure AD App Configuration
CLIENT_ID = os.environ.get('AZURE_CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET', '')
TENANT_ID = os.environ.get('AZURE_TENANT_ID', '')

# Alternative: Use device code flow if no client secret
USE_DEVICE_CODE = not CLIENT_SECRET

AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPES = ['https://graph.microsoft.com/.default']


def get_access_token():
    """Get access token using client credentials or device code flow"""
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    ) if CLIENT_SECRET else msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY
    )
    
    if USE_DEVICE_CODE:
        # Interactive device code flow
        flow = app.initiate_device_flow(scopes=['Mail.Send', 'Mail.ReadWrite'])
        print(flow['message'])
        result = app.acquire_token_by_device_flow(flow)
    else:
        # Client credentials flow (app-only)
        result = app.acquire_token_for_client(scopes=SCOPES)
    
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception(f"Failed to get token: {result.get('error_description')}")


def send_email(
    to_recipients,
    subject,
    body,
    body_type='HTML',
    cc_recipients=None,
    attachments=None,
    from_user=None
):
    """
    Send email via Microsoft Graph API
    
    Args:
        to_recipients: List of email addresses or single email string
        subject: Email subject
        body: Email body content
        body_type: 'HTML' or 'Text'
        cc_recipients: Optional list of CC recipients
        attachments: Optional list of file paths to attach
        from_user: User email (required for app-only auth)
    """
    
    token = get_access_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Format recipients
    if isinstance(to_recipients, str):
        to_recipients = [to_recipients]
    
    to_list = [{'emailAddress': {'address': email}} for email in to_recipients]
    
    cc_list = []
    if cc_recipients:
        if isinstance(cc_recipients, str):
            cc_recipients = [cc_recipients]
        cc_list = [{'emailAddress': {'address': email}} for email in cc_recipients]
    
    # Build message
    message = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': body_type,
                'content': body
            },
            'toRecipients': to_list
        }
    }
    
    if cc_list:
        message['message']['ccRecipients'] = cc_list
    
    # Add attachments if provided
    if attachments:
        attachment_list = []
        for file_path in attachments:
            path = Path(file_path)
            if path.exists():
                with open(path, 'rb') as f:
                    content = f.read()
                    import base64
                    encoded = base64.b64encode(content).decode('utf-8')
                    
                    attachment_list.append({
                        '@odata.type': '#microsoft.graph.fileAttachment',
                        'name': path.name,
                        'contentBytes': encoded
                    })
        
        if attachment_list:
            message['message']['attachments'] = attachment_list
    
    # Determine endpoint
    if from_user:
        # Send as specific user (requires app permissions)
        endpoint = f'https://graph.microsoft.com/v1.0/users/{from_user}/sendMail'
    else:
        # Send as authenticated user
        endpoint = 'https://graph.microsoft.com/v1.0/me/sendMail'
    
    # Send email
    response = requests.post(endpoint, headers=headers, json=message)
    
    if response.status_code == 202:
        print(f"✓ Email sent successfully to {', '.join(to_recipients)}")
        return True
    else:
        print(f"✗ Failed to send email: {response.status_code}")
        print(response.text)
        return False


def send_html_report(to_recipients, subject, html_file_path, cc_recipients=None):
    """
    Send an HTML file as email body
    
    Args:
        to_recipients: List of email addresses
        subject: Email subject
        html_file_path: Path to HTML file
        cc_recipients: Optional CC recipients
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return send_email(
        to_recipients=to_recipients,
        subject=subject,
        body=html_content,
        body_type='HTML',
        cc_recipients=cc_recipients
    )


if __name__ == '__main__':
    # Example usage
    
    # Configuration check
    if not CLIENT_ID or not TENANT_ID:
        print("⚠ Please set environment variables:")
        print("  AZURE_CLIENT_ID")
        print("  AZURE_TENANT_ID")
        print("  AZURE_CLIENT_SECRET (optional - will use device code flow if not set)")
        print("\nOr edit the script to set these values directly.")
        exit(1)
    
    # Example: Send simple email
    # send_email(
    #     to_recipients='recipient@example.com',
    #     subject='Test Email from Graph API',
    #     body='<h1>Hello!</h1><p>This is a test email sent via Microsoft Graph API.</p>',
    #     body_type='HTML'
    # )
    
    # Example: Send report with attachment
    # send_email(
    #     to_recipients=['recipient1@example.com', 'recipient2@example.com'],
    #     subject='IC MCS Risk Report',
    #     body='<h2>Automated Risk Report</h2><p>Please see attached report.</p>',
    #     attachments=['IC_MCS_REPORT_IC.htm'],
    #     cc_recipients='manager@example.com'
    # )
    
    print("Email sender configured. Import and use send_email() function.")
