# 📧 Automated Email Setup Guide for Regional LQE Reports

## Quick Start (Easiest Method)

The simplest way to send emails is using **your own Microsoft credentials** with interactive authentication:

### Step 1: Test Email Sending

```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"

# Test mode - sends only to you
python send_regional_lqe_emails.py --from-email carterryan@microsoft.com --test
```

This will:
1. Open a browser for you to authenticate with your Microsoft account
2. Send test emails only to yourself
3. Verify everything works before sending to reviewers

### Step 2: Send to All Reviewers

Once tested, run without `--test`:

```powershell
python send_regional_lqe_emails.py --from-email carterryan@microsoft.com
```

This will send the three regional reports to all configured reviewers automatically.

---

## Authentication Options

### Option 1: Interactive (Recommended - Easiest)

**No setup needed!** Just run the command and authenticate when prompted.

```powershell
python send_regional_lqe_emails.py --from-email carterryan@microsoft.com
```

The system will:
- Prompt you to visit https://microsoft.com/devicelogin
- Enter a code
- Sign in with your Microsoft credentials
- Token is cached for future runs

### Option 2: Delegated Permissions (Your Identity)

If you want to avoid interactive prompts, register an Azure AD app:

1. Go to https://portal.azure.com
2. Navigate to **Azure Active Directory** → **App registrations** → **New registration**
3. Name: "PHEPy LQE Email Sender"
4. Supported account types: "Accounts in this organizational directory only"
5. Click **Register**

6. **Configure API Permissions:**
   - Click **API permissions** → **Add a permission**
   - Select **Microsoft Graph** → **Delegated permissions**
   - Add: `Mail.Send`, `Mail.ReadWrite`, `User.Read`
   - Click **Grant admin consent** (if you have permissions)

7. **Get Application Details:**
   - Copy the **Application (client) ID**
   - Copy the **Directory (tenant) ID**
   - Go to **Certificates & secrets** → **New client secret**
   - Copy the secret value (only shown once!)

8. **Set Environment Variables:**

```powershell
# Add to your PowerShell profile or run each time
$env:AZURE_CLIENT_ID = "your-app-client-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
$env:AZURE_TENANT_ID = "your-tenant-id"
```

Then run:
```powershell
python send_regional_lqe_emails.py --from-email carterryan@microsoft.com
```

### Option 3: Application Permissions (Unattended/Scheduled)

For fully automated scheduled sends (via Task Scheduler):

1. Follow steps 1-5 from Option 2
2. **Configure API Permissions:**
   - Click **API permissions** → **Add a permission**
   - Select **Microsoft Graph** → **Application permissions**
   - Add: `Mail.Send`
   - Click **Grant admin consent** (requires admin)

3. Follow steps 7-8 from Option 2

This allows the script to run without any user interaction.

---

## Weekly Schedule Setup

To automate weekly Friday sends:

### Create a PowerShell Script

Create `C:\Scripts\send_weekly_lqe.ps1`:

```powershell
# Change to script directory
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"

# Set environment variables if using Option 2 or 3
$env:AZURE_CLIENT_ID = "your-app-client-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
$env:AZURE_TENANT_ID = "your-tenant-id"

# Fetch latest data
Write-Host "Fetching LQE data..." -ForegroundColor Cyan
python fetch_real_lqe_data.py

# Get the most recent data file
$dataFile = Get-ChildItem "data\regional_lqe_14day_real_*.json" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1

if ($dataFile) {
    Write-Host "Generating reports from $($dataFile.Name)..." -ForegroundColor Cyan
    python generate_regional_lqe_reports.py $dataFile.FullName
    
    Write-Host "Sending emails..." -ForegroundColor Cyan
    python send_regional_lqe_emails.py --from-email carterryan@microsoft.com
    
    Write-Host "✓ Weekly LQE reports sent successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ No data file found" -ForegroundColor Red
}
```

### Create Windows Task Scheduler Job

1. Open **Task Scheduler**
2. **Create Task** (not Basic Task)
3. **General** tab:
   - Name: "Weekly LQE Reports"
   - Run whether user is logged on or not
   - Run with highest privileges

4. **Triggers** tab:
   - New → Weekly
   - Day: Friday
   - Time: 6:00 PM (or your preferred time)

5. **Actions** tab:
   - New → Start a program
   - Program: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "C:\Scripts\send_weekly_lqe.ps1"`

6. **Conditions** tab:
   - Uncheck "Start only if on AC power" (if laptop)

7. Click **OK** and enter your password if prompted

---

## Manual Sending (No Automation)

If you prefer to manually review before sending:

```powershell
# 1. Generate reports
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"
python fetch_real_lqe_data.py
python generate_regional_lqe_reports.py "data\regional_lqe_14day_real_TIMESTAMP.json"

# 2. Review the HTML files in browser

# 3. Copy/paste into Outlook
# - Open HTML file in browser
# - Ctrl+A, Ctrl+C
# - Paste into Outlook email body
# - Add recipients from regional_reviewers_config.json
# - Send
```

---

## Troubleshooting

### "Failed to get token"
- Ensure you're authenticated to Microsoft (try `az login` first)
- Check environment variables are set correctly
- Verify Azure AD app permissions are granted

### "403 Forbidden"
- Your app needs admin consent for the permissions
- Ask your Azure AD admin to grant consent

### "Emails not sending"
- Run with `--test` first to verify authentication
- Check the reviewer email addresses in `regional_reviewers_config.json`
- Verify the HTML files were generated in `regional_reports/`

### "No recipients configured"
- Ensure `regional_reviewers_config.json` has email addresses for each region/feature

---

## Testing Checklist

Before going to production:

- [ ] Run with `--test` flag to send only to yourself
- [ ] Verify HTML formatting looks correct in your email
- [ ] Check all three regions (Americas, EMEA, APAC) sent successfully
- [ ] Confirm clickable ICM links work in the email
- [ ] Review the recipient list is correct
- [ ] Test the weekly schedule script manually
- [ ] Document your specific setup for future reference

---

## Current Configuration

Your reviewer configuration is in:
- `sub_agents/regional_reviewers_config.json`

Current reviewers will receive emails automatically based on their region and product area assignments.

**Ready to test?** Run:
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"
python send_regional_lqe_emails.py --from-email carterryan@microsoft.com --test
```
