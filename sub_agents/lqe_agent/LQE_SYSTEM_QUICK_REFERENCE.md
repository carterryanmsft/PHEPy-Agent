# Regional LQE Report System - Quick Reference

## 🚀 Quick Start

### 1. Fetch Latest Data (Every Week)
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"
python fetch_real_lqe_data.py
```
This will:
- Query ICM for last 14 days of unassigned LQEs
- Apply support engineer region mapping
- Categorize by product area (DLM, MIP/DLP, eDiscovery)
- Save data to `data/regional_lqe_14day_real_TIMESTAMP.json`

### 2. Generate Reports
```powershell
python generate_regional_lqe_reports.py "data\regional_lqe_14day_real_TIMESTAMP.json"
```
This creates three regional reports (Americas, EMEA, APAC) in `regional_reports/`:
- HTML files (email-optimized with inline CSS)
- JSON files (structured data)
- CSV files (Excel-ready)

### 3. Send Email Reports (Optional)
```powershell
# Test mode - sends only to you
python send_regional_lqe_emails.py --from-email your.email@microsoft.com --test

# Production - sends to all reviewers
python send_regional_lqe_emails.py --from-email your.email@microsoft.com
```

## 📧 Manual Email Distribution

If you prefer to send manually:
1. Open the HTML file in browser
2. Copy the entire page (Ctrl+A, Ctrl+C)
3. Paste into Outlook email body (Ctrl+V)
4. Add recipients from the reviewer list in the report
5. Send!

## 🔧 Configuration Files

### `support_engineer_regions.json`
Maps support engineer aliases to regions (Americas, EMEA, APAC)
- Update as you identify engineer home regions
- Currently has 78 engineers mapped

### `regional_reviewers_config.json`
Defines reviewers for each region and product area
- Update when reviewer assignments change
- Used for both report generation and email distribution

## 🎯 Product Area Categorization

Automatically categorizes escalations by owning team:

**MIP/DLP**: Teams containing DLP, MIP, SensitivityLabels, Classification, EDM, ServerSideAutoLabeling, InformationBarriers, TrainableClassifiers

**DLM**: Teams containing DLM, Lifecycle, Retention, Records

**eDiscovery**: Teams containing eDiscovery, eDisc, Discovery, Compliance

## 📊 Report Contents

Each regional report includes:
- ✅ Total unassigned LQE count
- ✅ Breakdown by product area
- ✅ Quality issues summary (most common problems)
- ✅ Detailed escalation tables with:
  - Clickable ICM links
  - Titles
  - Quality issues
  - Resolution dates
  - Owning teams
- ✅ Assigned reviewers for each product area

## 🔄 Weekly Workflow

**Every Friday:**
1. Run `fetch_real_lqe_data.py` to get latest data
2. Run `generate_regional_lqe_reports.py` with the new data file
3. Either:
   - Send emails automatically with `send_regional_lqe_emails.py`
   - Or manually distribute HTML reports

## 🛠️ Troubleshooting

### "No escalations found"
- Check the date range in the query (currently 14 days)
- Verify ICM connection and authentication

### "Engineer not mapped to region"
- Add their alias to `support_engineer_regions.json`
- Re-run `fetch_real_lqe_data.py`

### "Email sending fails"
- Ensure Microsoft Graph API credentials are configured
- Check `send_email_graph.py` for authentication setup
- Use `--test` mode to test with just your email first

## 📁 File Locations

```
sub_agents/
├── fetch_real_lqe_data.py              # Data fetching
├── generate_regional_lqe_reports.py     # Report generation
├── send_regional_lqe_emails.py          # Email distribution
├── support_engineer_regions.json        # Engineer → Region mapping
├── regional_reviewers_config.json       # Reviewer assignments
├── data/
│   └── regional_lqe_14day_real_*.json  # Cached data
└── regional_reports/
    ├── americas_lqe_report_*.htm       # Email-ready HTML
    ├── emea_lqe_report_*.htm
    ├── apac_lqe_report_*.htm
    ├── *.json                          # Structured data
    └── *.csv                           # Excel exports
```

## 💡 Tips

- **HTML is email-optimized** with inline CSS for maximum compatibility
- **Links are clickable** - recipients can click ICM IDs to go directly to incidents
- **Quality summary** helps identify common patterns to address with teams
- **Update mappings** regularly as engineers join/move teams
