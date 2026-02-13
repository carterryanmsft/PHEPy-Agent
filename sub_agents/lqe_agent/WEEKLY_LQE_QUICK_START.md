# Weekly Regional LQE Reports - Quick Start Guide

## 📅 Purpose
Generate **weekly regional LQE reports** for Americas, EMEA, and APAC regions with fresh data from Kusto.

---

## 🚀 Quick Run (One Command)

### PowerShell (Recommended)
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent"
.\Run-WeeklyLQEReports.ps1
```

### Python
```bash
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent"
python run_weekly_regional_reports.py
```

---

## 📊 What You Get

### Reports Generated (Per Region)
1. **HTML Report** (`americas_lqe_report_TIMESTAMP.htm`)
   - Professional formatted report with color coding
   - Organized by feature area (MIP/DLP, DLM, eDiscovery)
   - Clickable ICM links
   - Ready for email distribution

2. **JSON Report** (`americas_lqe_report_TIMESTAMP.json`)
   - Structured data for programmatic access
   - Region metadata
   - Escalation details by feature area

3. **CSV Export** (`americas_lqe_report_TIMESTAMP.csv`)
   - Flat file for Excel analysis
   - All escalations with full details

### Regions Covered
- ✅ **Americas** (US, Canada, LATAM)
- ✅ **EMEA** (Europe, Middle East, Africa)
- ✅ **APAC** (Asia-Pacific + Unknown regions)

---

## ⚙️ Command Options

### Basic Options

```powershell
# Fresh data fetch (default)
.\Run-WeeklyLQEReports.ps1

# Use existing data (faster, no Kusto query)
.\Run-WeeklyLQEReports.ps1 -SkipDataFetch

# Use specific data file
.\Run-WeeklyLQEReports.ps1 -DataFile "data\regional_lqe_14day_real_20260213.json"
```

### Email Distribution

```powershell
# Generate reports and send via email
.\Run-WeeklyLQEReports.ps1 -SendEmail -FromEmail "your.email@microsoft.com"

# Test mode (generates reports but doesn't send)
.\Run-WeeklyLQEReports.ps1 -SendEmail -FromEmail "your.email@microsoft.com" -TestMode
```

---

## 📅 Recommended Schedule

### Weekly Cadence
- **Best Time**: Friday afternoon or Monday morning
- **Frequency**: Once per week
- **Data Range**: Last 7 days of unassigned LQEs

### Automation Setup

#### Windows Task Scheduler
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File 'C:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent\Run-WeeklyLQEReports.ps1'"

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At 4PM

Register-ScheduledTask -TaskName "Weekly LQE Reports" `
    -Action $action `
    -Trigger $trigger `
    -Description "Generate weekly regional LQE reports"
```

#### Manual Run
Just double-click `Run-WeeklyLQEReports.ps1` in Windows Explorer

---

## 🔍 What Data is Included

### Escalation Criteria
- ✅ Last 7 days (configurable)
- ✅ Low quality classification (NOT "All Data Provided")
- ✅ Unassigned (no reviewer name)
- ✅ Not marked as false positive
- ✅ Purview product only
- ✅ Customer-reported incidents

### Data Fields
- Incident ID and ICM link
- Title and severity
- Created by (support engineer)
- Owning team
- Resolve date
- Escalation quality reason
- Origin region
- Feature area
- Customer segment

---

## 📂 File Structure

```
lqe_agent/
├── Run-WeeklyLQEReports.ps1           # ⭐ PowerShell automation
├── run_weekly_regional_reports.py     # ⭐ Python automation
├── fetch_real_lqe_data.py             # Kusto data fetcher
├── generate_regional_lqe_reports.py   # Report generator
├── send_regional_lqe_emails.py        # Email sender
├── WEEKLY_LQE_QUICK_START.md          # This file
├── config/
│   └── regional_reviewers_config.json # Region/reviewer mappings
├── data/
│   └── regional_lqe_*.json            # Fetched data
└── reports/
    └── regional_reports/              # ⭐ Generated reports
        ├── americas_lqe_report_*.htm
        ├── emea_lqe_report_*.htm
        └── apac_lqe_report_*.htm
```

---

## 🔧 Prerequisites

### Required
- ✅ Python 3.8+
- ✅ Azure authentication (`az login`)
- ✅ Kusto access to `icmcluster.kusto.windows.net`
- ✅ Python packages:
  ```bash
  pip install pandas azure-kusto-data azure-identity
  ```

### Optional (for email)
- Microsoft Graph API credentials
- Email configuration in `config/email_config.json`

---

## 🐛 Troubleshooting

### "Azure not authenticated"
```powershell
az login
```

### "No data fetched from Kusto"
- Check your Kusto access permissions
- Verify you can access: `https://icmcluster.kusto.windows.net`
- Try using `--skip-fetch` with existing data file

### "No reports generated"
- Check if data file has escalations for each region
- Some regions may have 0 escalations in slow weeks

### Data looks stale
- Always run without `--skip-fetch` for fresh data
- Check the timestamp in data filename: `regional_lqe_14day_real_TIMESTAMP.json`

---

## 📊 Example Output

```
================================================================================
WEEKLY REGIONAL LQE REPORT - EXECUTION SUMMARY
================================================================================

📅 Generated: 2026-02-13 14:30:00
📊 Data Source: data/regional_lqe_14day_real_20260213_143000.json

📁 Reports Generated:
   ✓ Americas    → americas_lqe_report_20260213_143015.htm
   ✓ EMEA        → emea_lqe_report_20260213_143015.htm
   ✓ APAC        → apac_lqe_report_20260213_143015.htm

📂 Report Location:
   c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent\reports\regional_reports

================================================================================
```

---

## 📧 Distribution

### Email Recipients
Configure in `config/regional_reviewers_config.json`:
```json
{
  "regions": {
    "Americas": {
      "reviewers": ["reviewer1@microsoft.com"],
      "MIP/DLP": ["dlp.lead@microsoft.com"],
      "DLM": ["dlm.lead@microsoft.com"]
    }
  }
}
```

### Manual Distribution
1. Open generated HTML reports
2. Send via Outlook to regional stakeholders
3. Attach CSV for detailed analysis

---

## 🎯 Key Metrics Tracked

### Per Region
- Total unassigned LQEs
- Breakdown by feature area
- Breakdown by quality issue type
- Support engineer patterns

### Quality Issues
- "Incomplete or Limited Information"
- "Duplicate"
- "Not a Valid Escalation"
- "Other"

---

## 💡 Tips

1. **Run on Friday**: Analyze the full week before weekend
2. **Check all 3 regions**: Some weeks may be unbalanced
3. **Monitor trends**: Compare week-over-week totals
4. **Share quickly**: Reviewers need time to follow up
5. **Archive reports**: Keep historical record for analysis

---

## 📚 Related Documentation

- **[Full LQE System](README.md)** - Complete documentation
- **[Friday Workflow](FRIDAY_QUICK_START.md)** - Friday-specific workflow
- **[Email Setup](EMAIL_AUTOMATION_SETUP.md)** - Configure email distribution
- **[Configuration](config/README.md)** - Reviewer and region setup

---

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Azure authenticated (`az login`)
- [ ] Kusto access verified
- [ ] Run script: `.\Run-WeeklyLQEReports.ps1`
- [ ] Verify 3 HTML reports generated
- [ ] Review reports for accuracy
- [ ] Distribute to stakeholders
- [ ] Schedule for next week

---

**Questions?** Contact: Carter Ryan (carterryan@microsoft.com)
