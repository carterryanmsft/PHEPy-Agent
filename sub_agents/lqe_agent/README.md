# Low Quality Escalation (LQE) Agent

## Overview

The LQE Agent is a comprehensive system for monitoring, analyzing, and reporting on Low Quality Escalations (LQEs) across Purview products. It provides automated weekly reporting, Friday night analysis, and regional distribution capabilities.

## Purpose

- **Monitor** unassigned and low-quality escalations across DLM, MIP/DLP, and eDiscovery
- **Analyze** escalation patterns by region, product area, and support engineer
- **Report** actionable insights to regional reviewers and stakeholders
- **Automate** weekly and Friday night reporting workflows

## Key Capabilities

### 1. Weekly Regional LQE Reports
- 14-day rolling analysis of unassigned LQEs
- Region-based categorization (Americas, EMEA, APAC)
- Product area breakdown (DLM, MIP/DLP, eDiscovery)
- HTML, JSON, and CSV output formats
- Automated email distribution

### 2. Friday Night LQE Analysis
- Dedicated Friday analysis workflow
- Enhanced region and feature detection
- Sample data testing capabilities
- Production-ready HTML reports

### 3. Data Collection & Integration
- Real-time ICM query execution
- Support engineer region mapping
- Customer impact assessment
- Historical trend tracking

## Quick Start

### ⚡ Automated Weekly Reports (Recommended)
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent"

# One-command automation - fetches fresh data and generates all regional reports
.\Run-WeeklyLQEReports.ps1
```

**What you get:**
- ✅ Fresh data from Kusto (last 7 days)
- ✅ 3 regional reports (Americas, EMEA, APAC)
- ✅ HTML, JSON, and CSV formats

**See:** [WEEKLY_LQE_QUICK_START.md](WEEKLY_LQE_QUICK_START.md) for detailed instructions

---

### 📊 Manual Workflow

#### 1. Fetch Latest Data
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\lqe_agent"
python fetch_real_lqe_data.py
```

#### 2. Generate Reports
```powershell
# Weekly regional reports
python generate_regional_lqe_reports.py "data\regional_lqe_14day_real_TIMESTAMP.json"

# Friday analysis
python run_friday_lq_analysis.py
```

### 3. Send Reports (Optional)
```powershell
# Test mode
python send_regional_lqe_emails.py --from-email your.email@microsoft.com --test

# Production
python send_regional_lqe_emails.py --from-email your.email@microsoft.com
```

## Directory Structure

```
lqe_agent/
├── config/                          # Configuration files
│   ├── lq_escalation_config.json    # Reviewer mappings
│   ├── regional_reviewers_config.json
│   └── support_engineer_regions.json
├── data/                            # Data storage
├── queries/                         # Kusto/KQL queries
├── reports/                         # Generated reports
│   ├── friday_reports/
│   ├── lq_escalation_reports/
│   └── regional_reports/
├── test_data/                       # Test datasets
├── lqe_agent.py                     # Main agent class
├── collect_lq_data.py               # Data collection
├── fetch_real_lqe_data.py           # ICM data fetcher
├── generate_regional_lqe_reports.py # Regional report generator
├── generate_weekly_lqe_report.py    # Weekly report generator
├── friday_lq_html_generator.py      # Friday HTML generator
├── run_friday_lq_analysis.py        # Friday workflow runner
├── run_lqe_report.py                # General report runner
├── send_regional_lqe_emails.py      # Email automation
└── README.md                        # This file
```

## Configuration Files

### `config/lq_escalation_config.json`
Maps reviewer emails for each region and product area
```json
{
  "reviewers": {
    "americas": ["reviewer1@microsoft.com"],
    "emea": ["reviewer2@microsoft.com"],
    "apac": ["reviewer3@microsoft.com"]
  }
}
```

### `config/support_engineer_regions.json`
Maps support engineer aliases to home regions (78+ engineers)

### `config/regional_reviewers_config.json`
Regional distribution lists for automated emails

## Main Scripts

| Script | Purpose |
|--------|---------|
| `lqe_agent.py` | Core agent with analysis logic |
| `fetch_real_lqe_data.py` | Query ICM for latest LQE data |
| `generate_regional_lqe_reports.py` | Create regional reports (HTML/CSV/JSON) |
| `generate_weekly_lqe_report.py` | Weekly report generation |
| `run_friday_lq_analysis.py` | Friday night workflow |
| `send_regional_lqe_emails.py` | Automated email distribution |
| `execute_weekly_report.py` | Orchestrated weekly execution |

## Documentation

- **[AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md)** - Detailed usage instructions
- **[LQE_SYSTEM_QUICK_REFERENCE.md](LQE_SYSTEM_QUICK_REFERENCE.md)** - Quick command reference
- **[FRIDAY_INDEX.md](FRIDAY_INDEX.md)** - Friday workflow documentation index
- **[FRIDAY_QUICK_START.md](FRIDAY_QUICK_START.md)** - Friday workflow quick start
- **[MULTI_REPORT_GUIDE.md](MULTI_REPORT_GUIDE.md)** - Multi-region reporting guide
- **[EMAIL_AUTOMATION_SETUP.md](EMAIL_AUTOMATION_SETUP.md)** - Email setup guide

## Testing

```powershell
# Test with sample data
python test_lq_with_sample_data.py

# Test Friday analysis
python test_friday_analysis.py
```

## Dependencies

- Python 3.8+
- Required packages (see root requirements.txt):
  - azure-identity
  - azure-kusto-data
  - requests
  - pandas (for CSV exports)

## Output Formats

### HTML Reports
- Email-optimized with inline CSS
- Tables with hover effects and sorting
- Direct paste into Outlook

### CSV Reports
- Excel-ready format
- All escalation details included
- Region and product categorization

### JSON Reports
- Complete structured data
- API integration ready
- Historical tracking enabled

## Integration Points

- **ICM**: Primary data source for escalations
- **Kusto**: Query backend for data retrieval
- **Microsoft Graph**: Email sending (if using Graph API)
- **Outlook**: Manual email distribution

## Maintenance

### Weekly Tasks
1. Fetch latest data (Fridays)
2. Generate reports
3. Review and send to stakeholders

### Monthly Tasks
1. Update `support_engineer_regions.json` with new engineers
2. Review reviewer distribution lists
3. Archive old reports (optional)

### As Needed
1. Update query parameters in scripts
2. Adjust region/product categorization logic
3. Modify HTML templates for branding

## Support

For questions or issues:
1. Check documentation in this directory
2. Review test scripts for examples
3. Examine sample data in `test_data/`

## Version History

- **v2.0** (Feb 2026): Organized into agent structure
- **v1.5** (Feb 2026): Friday workflow added
- **v1.0** (Jan 2026): Initial regional reporting system
