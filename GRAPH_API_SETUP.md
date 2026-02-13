# Microsoft Graph API Email Setup

## Prerequisites

Install required packages:
```bash
pip install msal requests
```

## Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com) → Azure Active Directory → App registrations
2. Click "New registration"
3. Name: "Email Automation" (or your choice)
4. Supported account types: "Accounts in this organizational directory only"
5. Click "Register"

## Configure Permissions

### Option A: Delegated Permissions (User Context)
1. Go to "API permissions"
2. Add permission → Microsoft Graph → Delegated permissions
3. Select: `Mail.Send`, `Mail.ReadWrite`
4. Click "Add permissions"
5. **Admin consent may be required**

### Option B: Application Permissions (App-Only)
1. Go to "API permissions"
2. Add permission → Microsoft Graph → Application permissions
3. Select: `Mail.Send`
4. Click "Add permissions"
5. Click "Grant admin consent for [your organization]"

## Get Credentials

### Client ID & Tenant ID
1. Go to "Overview" page
2. Copy "Application (client) ID" → This is your `CLIENT_ID`
3. Copy "Directory (tenant) ID" → This is your `TENANT_ID`

### Client Secret (for app-only auth)
1. Go to "Certificates & secrets"
2. Click "New client secret"
3. Description: "Email automation secret"
4. Expires: Choose duration
5. Click "Add"
6. **Copy the secret value immediately** → This is your `CLIENT_SECRET`

## Configure Environment Variables

### Windows (PowerShell)
```powershell
$env:AZURE_CLIENT_ID = "your-client-id"
$env:AZURE_TENANT_ID = "your-tenant-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
```

### Permanent (System Environment Variables)
```powershell
[System.Environment]::SetEnvironmentVariable('AZURE_CLIENT_ID', 'your-client-id', 'User')
[System.Environment]::SetEnvironmentVariable('AZURE_TENANT_ID', 'your-tenant-id', 'User')
[System.Environment]::SetEnvironmentVariable('AZURE_CLIENT_SECRET', 'your-client-secret', 'User')
```

### Or Edit Script Directly
Edit `send_email_graph.py` and set:
```python
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
TENANT_ID = 'your-tenant-id'
```

## Usage

### Basic Email
```python
from send_email_graph import send_email

send_email(
    to_recipients='recipient@microsoft.com',
    subject='Test Email',
    body='<h1>Hello</h1><p>This is a test.</p>',
    body_type='HTML'
)
```

### Send Report
```python
from send_email_graph import send_html_report

send_html_report(
    to_recipients=['person1@microsoft.com', 'person2@microsoft.com'],
    subject='IC MCS Risk Report',
    html_file_path='IC_MCS_REPORT_IC.htm',
    cc_recipients='manager@microsoft.com'
)
```

### Send Risk Report (Automated)
```bash
cd risk_reports
python send_report_email.py
```

## Authentication Methods

### 1. Client Credentials Flow (App-Only)
- Requires: CLIENT_ID, CLIENT_SECRET, TENANT_ID
- Use case: Automated scripts, server-side apps
- Permissions: Application permissions

### 2. Device Code Flow (Interactive)
- Requires: CLIENT_ID, TENANT_ID
- Use case: When no client secret (more secure)
- Permissions: Delegated permissions
- User will see a code to enter in browser

## Troubleshooting

### "Insufficient privileges"
- Ensure correct permissions are added
- Grant admin consent in Azure portal
- Wait a few minutes for permissions to propagate

### "Invalid client secret"
- Generate new secret in Azure portal
- Update environment variable
- Restart terminal/script

### "AADSTS7000215: Invalid client secret"
- Client secret expired
- Create new secret in Azure portal

### "401 Unauthorized"
- Check CLIENT_ID, TENANT_ID are correct
- Verify permissions are granted
- Ensure user has mailbox (for delegated permissions)

## Security Best Practices

1. **Never commit secrets to git**
2. Use Azure Key Vault for production
3. Use Managed Identity if running in Azure
4. Rotate secrets regularly
5. Use least-privilege permissions
6. Consider certificate-based auth for production

## Example Integration with Risk Reports

Modify your report generation scripts:
```python
# At the end of generate_full_report_131.py
from send_email_graph import send_html_report

send_html_report(
    to_recipients=['team@microsoft.com'],
    subject=f'IC MCS Risk Report - {datetime.now().strftime("%Y-%m-%d")}',
    html_file_path='IC_MCS_REPORT_IC.htm'
)
```
