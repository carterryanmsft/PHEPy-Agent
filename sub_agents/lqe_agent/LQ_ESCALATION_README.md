# Low Quality Escalation Insight Agent

Automated system for analyzing low quality escalations, organizing them by owner, and distributing weekly reports to reviewers for follow-up.

## Overview

The Low Quality Escalation Insight Agent identifies escalations marked as low quality, organizes them by the person who created them, assigns them to appropriate reviewers, and generates weekly email reports to facilitate quality improvement initiatives.

## Features

- **Automated Data Retrieval**: Queries Kusto database for low quality escalations from the last 30 days
- **Smart Organization**: Groups escalations by creator/owner for targeted follow-up
- **Reviewer Assignment**: Maps escalation owners to designated reviewers
- **HTML Email Reports**: Generates professional, formatted email reports
- **CSV Export**: Creates comprehensive CSV files for further analysis
- **Weekly Automation**: Designed to run automatically via scheduled tasks
- **Audit Logging**: Maintains logs of each analysis run

## Components

### 1. `low_quality_escalation_agent.py`
Main agent that handles data retrieval, processing, and organization.

**Key Functions:**
- `load_escalations()` - Queries Kusto or loads from file
- `organize_by_owner()` - Groups escalations by creator
- `assign_to_reviewers()` - Maps owners to reviewers
- `generate_summary_stats()` - Calculates metrics
- `export_for_review()` - Exports data for each reviewer
- `run_analysis()` - Orchestrates complete workflow

### 2. `lq_email_report_generator.py`
Generates formatted HTML and text email reports for reviewers.

**Key Functions:**
- `generate_html_report()` - Creates styled HTML email
- `generate_text_report()` - Creates plain text version
- `create_email_message()` - Builds MIME email message
- `send_email()` - Sends via SMTP
- `generate_and_send_reports()` - Processes all reviewers

### 3. `run_weekly_lq_analysis.py`
Automated runner for weekly execution via scheduler.

**Key Functions:**
- `run_weekly_analysis()` - Complete weekly workflow
- `test_run()` - Test mode without sending emails
- `setup_kusto_client()` - Configures Kusto connection

### 4. `lq_escalation_config.json`
Configuration file mapping escalation owners to reviewers.

## Installation

### Prerequisites

```bash
# Python 3.8+
pip install pandas
pip install azure-kusto-data azure-identity  # For Kusto connectivity
```

### Setup

1. **Clone or copy the agent files** to your `sub_agents/` directory:
   - `low_quality_escalation_agent.py`
   - `lq_email_report_generator.py`
   - `run_weekly_lq_analysis.py`
   - `lq_escalation_config.json`

2. **Configure Kusto connection** (set environment variables):
   ```bash
   set KUSTO_CLUSTER=https://icmcluster.kusto.windows.net
   set KUSTO_DATABASE=IcMDataWarehouse
   ```

3. **Update `lq_escalation_config.json`** with your reviewer mappings:
   ```json
   {
     "escalation_owners": {
       "alice@microsoft.com": "reviewer1@microsoft.com",
       "bob@microsoft.com": "reviewer1@microsoft.com",
       "charlie@microsoft.com": "reviewer2@microsoft.com"
     },
     "reviewers": [
       {
         "name": "Reviewer 1",
         "email": "reviewer1@microsoft.com",
         "team": "Support Leadership"
       }
     ],
     "email_settings": {
       "send_from": "escalation-insights@microsoft.com",
       "cc_list": []
     }
   }
   ```

## Usage

### Command Line Interface

#### Basic Usage - Test Mode (No Emails)
```bash
cd sub_agents
python run_weekly_lq_analysis.py --test
```

#### Analyze Last 7 Days
```bash
python run_weekly_lq_analysis.py --days 7
```

#### Analyze Last 30 Days and Send Emails
```bash
python run_weekly_lq_analysis.py --days 30
```

#### Generate Reports Without Sending Emails
```bash
python run_weekly_lq_analysis.py --days 7 --no-email
```

#### Use Custom Config File
```bash
python run_weekly_lq_analysis.py --config /path/to/config.json
```

#### Load from Cached Data File
```bash
python run_weekly_lq_analysis.py --from-file data/cached_escalations.json
```

### Python API

#### Basic Usage
```python
from low_quality_escalation_agent import LowQualityEscalationAgent
from lq_email_report_generator import EmailReportGenerator

# Initialize agent
agent = LowQualityEscalationAgent()

# Load escalations (last 30 days)
agent.load_escalations(days_back=30)

# Organize by owner
agent.organize_by_owner()

# Generate stats
stats = agent.generate_summary_stats()
print(f"Total low quality escalations: {stats['total_escalations']}")

# Export reports
output_files = agent.export_for_review()

# Generate CSV
csv_path = agent.generate_csv_report()
```

#### Generate and Send Email Reports
```python
from lq_email_report_generator import EmailReportGenerator

# Initialize generator
email_gen = EmailReportGenerator()

# Get reviewer assignments
reviewer_assignments = agent.assign_to_reviewers()

# Generate and send reports
results = email_gen.generate_and_send_reports(
    reviewer_assignments,
    stats=stats,
    save_to_file=True,  # Save HTML files
    send_email=True     # Send actual emails
)

print(f"Emails sent: {len(results['sent'])}")
```

## Weekly Automation

### Windows Task Scheduler

1. **Open Task Scheduler** → Create Basic Task

2. **Configure Task**:
   - Name: "Weekly LQ Escalation Analysis"
   - Trigger: Weekly, Monday, 9:00 AM
   - Action: Start a program
   
3. **Program/Script**:
   ```
   C:\Python\python.exe
   ```

4. **Arguments**:
   ```
   "C:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\run_weekly_lq_analysis.py" --days 7
   ```

5. **Start in**:
   ```
   C:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents
   ```

### Linux/Mac Cron

Add to crontab:
```bash
# Run every Monday at 9:00 AM
0 9 * * 1 cd /path/to/PHEPy/sub_agents && /usr/bin/python3 run_weekly_lq_analysis.py --days 7
```

### PowerShell Script

Create `schedule_lq_analysis.ps1`:
```powershell
cd "C:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"
python run_weekly_lq_analysis.py --days 7

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host "Analysis completed successfully"
} else {
    Write-Host "Analysis failed with exit code: $LASTEXITCODE"
    # Send alert email or log error
}
```

## Configuration

### Reviewer Mapping

The `lq_escalation_config.json` file controls how escalations are assigned:

```json
{
  "escalation_owners": {
    "creator@microsoft.com": "reviewer@microsoft.com"
  },
  "team_assignments": {
    "Team Name": "reviewer@microsoft.com"
  },
  "default_reviewer": "fallback@microsoft.com"
}
```

**Fallback Logic**:
1. Check `escalation_owners` for exact email match
2. If not found, check `team_assignments` by owning team
3. If still not found, use `default_reviewer`

### Email Settings

Configure SMTP and email preferences:

```json
{
  "email_settings": {
    "send_from": "noreply@microsoft.com",
    "cc_list": ["manager@microsoft.com"],
    "subject_template": "Weekly Low Quality Escalation Review - Week {fiscal_week}",
    "send_day": "Monday",
    "send_time": "09:00"
  }
}
```

## Output Files

### Directory Structure
```
sub_agents/
├── lq_escalation_reports/          # HTML reports
│   ├── lq_report_reviewer1_20260204_090015.html
│   └── lq_report_reviewer2_20260204_090016.html
│
├── lq_escalation_logs/              # Run logs
│   └── weekly_run_20260204_090000.json
│
└── lq_escalations_20260204_090020.csv  # CSV export
```

### Report Contents

Each HTML report includes:
- **Summary**: Total escalations, owner count, fiscal week
- **Owner Sections**: Grouped by escalation creator
- **Escalation Details**: 
  - Incident ID and IcM ID
  - Title and severity
  - Owning team
  - Quality issue and reason
  - Resolution date
- **Action Items**: Clear instructions for follow-up

### CSV Export

The CSV file contains all escalations with columns:
- IncidentId, IcMId, RoutingId
- Title, Severity
- CreatedBy, OwningTeam
- ResolveDate, FiscalWeek
- EscalationQuality, LowQualityReason
- CustomerSegment
- AssignedReviewer

## Kusto Query

The agent uses this query to identify low quality escalations:

```kql
let escalationInformation = IncidentsDedupView
| where OwningTenantName == "Purview"
| where ResolveDate > ago(30d)
| where IncidentType == "CustomerReported"
| extend FiscalWeek = 24 - toint((fw24EndDate - ResolveDate) / 7d)
| project ResolveDate, FiscalWeek, IncidentId, SourceCreatedBy, OwningTeamName, 
    Title, Severity, RoutingId, IcMId, CustomerSegment;

let qualityInformation =
IncidentCustomFieldEntriesDedupView
| where Name == "Escalation Quality"
| project IncidentId, EscalationQuality = Value;

let supportReviews = IncidentCustomFieldEntriesDedupView
| where Name == "Escalation quality standards"
| project IncidentId, QualityReviewFalsePositive = Value;

let qualityReasons = IncidentCustomFieldEntriesDedupView
| where Name == "Low Quality Reason"
| project IncidentId, LowQualityReason = Value;

escalationInformation
| join kind=inner (qualityInformation) on IncidentId
| join kind=leftouter (supportReviews) on IncidentId
| join kind=leftouter (qualityReasons) on IncidentId
| where EscalationQuality != "All Data Provided"
| where QualityReviewFalsePositive != "Yes" or isempty(QualityReviewFalsePositive)
```

**Query Logic**:
- Filters for Purview incidents resolved in last 30 days
- Excludes escalations marked "All Data Provided" (good quality)
- Excludes false positives (marked as LQ but reviewed as acceptable)
- Returns true low quality escalations needing follow-up

## Troubleshooting

### Kusto Connection Issues

**Problem**: Cannot connect to Kusto cluster

**Solutions**:
1. Verify environment variables:
   ```bash
   echo %KUSTO_CLUSTER%
   echo %KUSTO_DATABASE%
   ```

2. Check Azure authentication:
   ```bash
   az login
   az account show
   ```

3. Use cached data for testing:
   ```bash
   python run_weekly_lq_analysis.py --from-file test_data.json
   ```

### No Escalations Found

**Problem**: Analysis returns 0 escalations

**Possible Causes**:
- No low quality escalations in the time period
- Kusto query filters too restrictive
- Custom field names don't match

**Solutions**:
1. Check raw query results in Kusto Explorer
2. Adjust `days_back` parameter
3. Verify custom field names in your IcM environment

### Email Not Sending

**Problem**: Reports generate but emails don't send

**Solutions**:
1. Check SMTP configuration in code
2. Verify network connectivity
3. Test with `--no-email` flag first
4. Review saved HTML files in `lq_escalation_reports/`

### Missing Reviewer Assignments

**Problem**: Warning: "No reviewer assigned for owner: email@microsoft.com"

**Solution**: Update `lq_escalation_config.json`:
```json
{
  "escalation_owners": {
    "email@microsoft.com": "reviewer@microsoft.com"
  }
}
```

## Best Practices

1. **Weekly Cadence**: Run every Monday morning for consistent follow-up
2. **Test First**: Always run with `--test` flag before enabling emails
3. **Archive Reports**: Keep HTML reports for historical tracking
4. **Update Mappings**: Review and update reviewer assignments quarterly
5. **Monitor Logs**: Check run logs for errors and trends
6. **Validate Data**: Spot-check a few escalations in IcM before sending reports

## Customization

### Change Time Window

Edit the query in `low_quality_escalation_agent.py`:
```python
def get_detailed_escalation_query(self, days_back: int = 30):
    # Change 30 to your desired default
```

### Add Custom Fields

Modify the query to include additional fields:
```python
# In the escalationInformation section:
| project ResolveDate, FiscalWeek, IncidentId, SourceCreatedBy, 
    OwningTeamName, Title, Severity, RoutingId, IcMId, CustomerSegment,
    YourCustomField  # Add here
```

### Customize Email Template

Edit `lq_email_report_generator.py` → `generate_html_report()`:
- Change colors in the `<style>` section
- Modify HTML structure
- Add company logo or branding

### Add Slack Notifications

```python
# Add to run_weekly_lq_analysis.py
import requests

def send_slack_notification(webhook_url, results):
    message = {
        "text": f"Weekly LQ Analysis Complete: {results['escalation_count']} escalations analyzed"
    }
    requests.post(webhook_url, json=message)
```

## Support and Maintenance

### Updating Reviewer Lists

1. Edit [lq_escalation_config.json](lq_escalation_config.json)
2. Add new mappings to `escalation_owners`
3. Test with: `python run_weekly_lq_analysis.py --test`

### Monitoring Performance

Check run logs in `lq_escalation_logs/`:
```python
import json
with open('lq_escalation_logs/weekly_run_latest.json') as f:
    log = json.load(f)
    print(f"Duration: {log['end_time'] - log['start_time']}")
    print(f"Success: {log['success']}")
```

### Debugging

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Roadmap / Future Enhancements

- [ ] Teams/Slack integration for notifications
- [ ] Interactive Power BI dashboard
- [ ] Trend analysis over time
- [ ] Automated quality score calculation
- [ ] Integration with escalation training system
- [ ] AI-powered quality prediction
- [ ] Real-time alerts for severe quality issues

## Related Work Items

- Azure DevOps: [Work Item #19173](https://dev.azure.com/seccxeds/DataServices/_workitems/edit/19173)

## Contributors

- Carter Ryan (Primary Author)

## License

Internal Microsoft tool - Not for external distribution

---

**Last Updated**: February 4, 2026

For questions or support, contact the Purview Escalation Quality Team.
