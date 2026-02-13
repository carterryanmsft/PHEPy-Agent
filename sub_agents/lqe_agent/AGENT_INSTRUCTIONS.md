# LQE Agent - Usage Instructions

## Table of Contents
1. [Agent Overview](#agent-overview)
2. [Prerequisites](#prerequisites)
3. [Weekly Workflow](#weekly-workflow)
4. [Friday Workflow](#friday-workflow)
5. [Configuration Management](#configuration-management)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## Agent Overview

The LQE Agent monitors and reports on Low Quality Escalations (LQEs) - incidents that are unassigned, improperly routed, or lacking sufficient information. The agent provides:

- **Automated data collection** from ICM
- **Regional categorization** (Americas, EMEA, APAC)
- **Product-specific analysis** (DLM, MIP/DLP, eDiscovery)
- **Multi-format reporting** (HTML, CSV, JSON)
- **Email automation** for stakeholder distribution

---

## Prerequisites

### 1. Authentication
Ensure you have valid Azure credentials:
```powershell
# Test authentication
az login
az account show
```

### 2. Python Environment
```powershell
# Verify Python installation
python --version  # Should be 3.8+

# Install dependencies (from workspace root)
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy"
pip install -r requirements.txt
```

### 3. Configuration Files
Verify these exist in `config/`:
- `lq_escalation_config.json` - Main reviewer configuration
- `regional_reviewers_config.json` - Email distribution lists
- `support_engineer_regions.json` - Engineer region mappings

---

## Weekly Workflow

### Standard Weekly Report Process

#### Step 1: Fetch Latest Data (Every Friday)
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent"
python fetch_real_lqe_data.py
```

**What it does:**
- Queries ICM for the last 14 days of LQEs
- Filters for unassigned escalations
- Maps support engineers to regions
- Categorizes by product area
- Saves to: `data/regional_lqe_14day_real_YYYYMMDD_HHMMSS.json`

**Expected output:**
```
Fetching LQE data from ICM...
✓ Retrieved 47 escalations
✓ Mapped 42 to regions (5 unknown)
✓ Categorized by product areas
✓ Saved to: data/regional_lqe_14day_real_20260211_153042.json
```

#### Step 2: Generate Regional Reports
```powershell
# Use the timestamp from Step 1
python generate_regional_lqe_reports.py "data\regional_lqe_14day_real_20260211_153042.json"
```

**What it does:**
- Creates three regional reports (Americas, EMEA, APAC)
- Generates HTML (email-ready), CSV (Excel), JSON (data) formats
- Saves to: `reports/regional_reports/`

**Expected output:**
```
Generating regional reports...

Americas Report:
  - 18 escalations found
  - Saved: reports/regional_reports/americas_lqe_20260211.html
  - Saved: reports/regional_reports/americas_lqe_20260211.csv
  - Saved: reports/regional_reports/americas_lqe_20260211.json

EMEA Report:
  - 15 escalations found
  - Similar files created

APAC Report:
  - 14 escalations found
  - Similar files created
```

#### Step 3A: Automated Email Distribution
```powershell
# TEST MODE FIRST (sends only to you)
python send_regional_lqe_emails.py --from-email your.alias@microsoft.com --test

# After verification, send to all reviewers
python send_regional_lqe_emails.py --from-email your.alias@microsoft.com
```

**Test mode:**
- Sends all reports to your email only
- Review formatting and content
- Verify links and attachments

**Production mode:**
- Reads recipients from `config/regional_reviewers_config.json`
- Sends region-specific reports to each distribution list
- Includes HTML body + CSV attachment

#### Step 3B: Manual Email Distribution (Alternative)
If you prefer manual sending:

1. Open the HTML file in your browser:
   ```powershell
   start reports/regional_reports/americas_lqe_20260211.html
   ```

2. Select all content (Ctrl+A)

3. Copy (Ctrl+C)

4. Open Outlook, create new email

5. Paste into email body (Ctrl+V)

6. Add recipients from report header

7. Attach CSV file if needed

8. Send!

---

## Friday Workflow

The Friday workflow is optimized for end-of-week analysis with enhanced features.

### Friday Analysis Process

#### Step 1: Run Friday Analysis
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent"
python run_friday_lq_analysis.py
```

This single command:
1. Fetches latest ICM data
2. Applies Friday-specific filters
3. Enhances with region/feature detection
4. Generates comprehensive HTML report
5. Saves to: `reports/friday_reports/friday_lq_report_TIMESTAMP.html`

**Expected output:**
```
🗓️ Friday LQE Analysis Starting...

[1/4] Fetching data from ICM...
      ✓ Retrieved 52 escalations

[2/4] Applying Friday filters...
      ✓ Filtered to 47 relevant cases

[3/4] Analyzing patterns...
      ✓ Region detection: 44 mapped
      ✓ Feature categorization: 40 categorized

[4/4] Generating report...
      ✓ HTML report: reports/friday_reports/friday_lq_report_20260211_170000.html

✅ Friday analysis complete!
```

#### Step 2: Review Report
```powershell
# Open in browser
start reports/friday_reports/friday_lq_report_20260211_170000.html
```

Review for:
- Unusual patterns or spikes
- Specific product areas needing attention
- Engineers with multiple assignments
- Critical customers affected

#### Step 3: Distribute
Use manual or automated email method from weekly workflow.

---

## Configuration Management

### Adding New Support Engineers

Edit `config/support_engineer_regions.json`:
```json
{
  "engineer_alias": "Americas",
  "new_engineer": "EMEA"
}
```

Regions: `"Americas"`, `"EMEA"`, `"APAC"`, or `"Unknown"`

### Updating Reviewer Distribution Lists

Edit `config/regional_reviewers_config.json`:
```json
{
  "americas": {
    "reviewers": [
      "reviewer1@microsoft.com",
      "reviewer2@microsoft.com"
    ],
    "cc": ["manager@microsoft.com"]
  },
  "emea": {
    "reviewers": ["reviewer3@microsoft.com"]
  },
  "apac": {
    "reviewers": ["reviewer4@microsoft.com"]
  }
}
```

### Modifying Report Criteria

To change the LQE detection criteria, edit `lqe_agent.py`:

```python
def is_low_quality(self, escalation):
    """
    Customize criteria here:
    - Unassigned for > N hours
    - Missing required fields
    - Incorrect routing
    - etc.
    """
    # Add your logic
```

---

## Troubleshooting

### Issue: "No data retrieved from ICM"

**Possible causes:**
1. Authentication expired
2. Network connectivity
3. ICM API changes

**Solutions:**
```powershell
# Re-authenticate
az login

# Test connectivity
python test_kusto_connection.py

# Check credentials
az account show
```

### Issue: "Unknown region for engineer X"

**Solution:**
Add the engineer to `config/support_engineer_regions.json`

### Issue: "Email sending failed"

**Possible causes:**
1. Invalid email addresses
2. Missing Graph API permissions
3. Network issues

**Solutions:**
```powershell
# Verify email configuration
python -c "import json; print(json.load(open('config/regional_reviewers_config.json')))"

# Use manual distribution as fallback
start reports/regional_reports/americas_lqe_TIMESTAMP.html
```

### Issue: "Report generation failed"

**Solutions:**
```powershell
# Test with sample data first
python test_lq_with_sample_data.py

# Check data file integrity
python -c "import json; json.load(open('data/YOUR_FILE.json'))"

# Run with verbose output
python generate_regional_lqe_reports.py "data/YOUR_FILE.json" --verbose
```

---

## Advanced Usage

### Custom Date Ranges

Modify `fetch_real_lqe_data.py` to change the query window:
```python
# Change from 14 days to 30 days
days_back = 30
```

### Filtering Specific Products

To generate reports for only one product area:
```python
python generate_regional_lqe_reports.py "data/file.json" --product "MIP/DLP"
```

### Batch Processing

Process multiple data files:
```powershell
Get-ChildItem data/*.json | ForEach-Object {
    python generate_regional_lqe_reports.py $_.FullName
}
```

### Exporting for External Tools

All reports include JSON format for integration:
```python
import json

# Load report data
with open('reports/regional_reports/americas_lqe_TIMESTAMP.json') as f:
    data = json.load(f)

# Process in your tool
for escalation in data['escalations']:
    # Your logic here
    pass
```

### Scheduled Automation

Set up Windows Task Scheduler:
```powershell
# Create scheduled task (run every Friday at 5 PM)
$action = New-ScheduledTaskAction -Execute 'python' -Argument 'run_friday_lq_analysis.py' -WorkingDirectory 'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent'
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At 5pm
Register-ScheduledTask -TaskName "Friday LQE Report" -Action $action -Trigger $trigger
```

---

## Best Practices

1. **Always test in test mode** before production email sends
2. **Archive old reports** monthly to keep directory clean
3. **Update engineer mappings** as team changes occur
4. **Review sample output** before distributing to stakeholders
5. **Maintain backup** of configuration files
6. **Document custom modifications** in code comments

---

## Quick Command Reference

```powershell
# Navigate to agent
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent"

# Weekly workflow (3 commands)
python fetch_real_lqe_data.py
python generate_regional_lqe_reports.py "data\regional_lqe_14day_real_TIMESTAMP.json"
python send_regional_lqe_emails.py --from-email YOUR_EMAIL --test

# Friday workflow (1 command)
python run_friday_lq_analysis.py

# Testing
python test_lq_with_sample_data.py
python test_friday_analysis.py

# Utilities
python test_kusto_connection.py
```

---

## Additional Resources

- **[FRIDAY_INDEX.md](FRIDAY_INDEX.md)** - Complete Friday documentation index
- **[LQE_SYSTEM_QUICK_REFERENCE.md](LQE_SYSTEM_QUICK_REFERENCE.md)** - Command cheat sheet
- **[MULTI_REPORT_GUIDE.md](MULTI_REPORT_GUIDE.md)** - Advanced multi-region reporting
- **[EMAIL_AUTOMATION_SETUP.md](EMAIL_AUTOMATION_SETUP.md)** - Email configuration details
