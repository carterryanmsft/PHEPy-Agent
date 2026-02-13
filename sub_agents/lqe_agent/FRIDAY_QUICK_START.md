# Friday Night LQ Escalation Workflow - Quick Start Guide

## 📅 When to Run
**Every Friday night** to analyze the past 7 days of unassigned low quality escalations

## 🎯 What This Does
Finds escalations that:
- ✅ Closed in last 7 days
- ✅ Marked as low quality (NOT "All Data Provided")
- ✅ Have **blank/no reviewer assigned**
- ✅ Not marked as false positive
- 📊 Organized by **Region** (Americas, EMEA, APAC, LATAM) and **Feature Area** (MIP/DLP, DLM, eDiscovery)

## 🚀 Quick Run (3 Steps)

### Step 1: Execute Kusto Query
```powershell
# Option A: Use the saved KQL file
# Open: sub_agents/queries/friday_lq_unassigned.kql
# Run in Kusto Explorer or via GitHub Copilot MCP

# Option B: Run the script to see the query
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"
python run_friday_lq_analysis.py
```

**Kusto Connection:**
- Cluster: `https://icmcluster.kusto.windows.net`
- Database: `IcMDataWarehouse`

### Step 2: Save Results
Save the Kusto query results as JSON:
```
sub_agents/data/friday_lq_20260205.json
```

### Step 3: Generate Report
```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"
python run_friday_lq_analysis.py --data-file data/friday_lq_20260205.json
```

## 📊 Output Files

Located in `sub_agents/friday_reports/`:

1. **JSON Report** - `friday_lq_report_YYYYMMDD_HHMMSS.json`
   - Executive summary with counts
   - Escalations organized by region → feature area
   - Reviewer instructions

2. **CSV Export** - `friday_lq_report_YYYYMMDD_HHMMSS.csv`
   - Flat file for Excel
   - All escalations with full details

3. **HTML Report** - `friday_lq_report_YYYYMMDD_HHMMSS.htm` ⭐ NEW!
   - Professional formatted report matching risk report style
   - Color-coded severity levels
   - Clickable ICM links
   - Emoji icons for regions and features
   - Ready for email distribution

## 📧 Distribution

Send reports to reviewers listed in:
`sub_agents/lq_escalation_config.json`

Current reviewers:
- Brian Roam
- Olivia Costisanu
- Chris Pollitt
- Daniel Estrada Vaglio
- And team...

## 🔍 What Gets Filtered

```kql
WHERE:
  EscalationQuality != "All Data Provided"      // Is low quality
  AND (ReviewerName is empty OR "" )             // No reviewer assigned
  AND QualityReviewFalsePositive != "Yes"       // Not a false positive
  AND ResolveDate > ago(7d)                      // Last 7 days
```

## 📂 File Structure

```
sub_agents/
├── run_friday_lq_analysis.py          # Main runner script
├── low_quality_escalation_agent.py    # Core logic
├── lq_escalation_config.json          # Reviewer config
├── FRIDAY_LQ_README.md                # Full documentation
├── queries/
│   └── friday_lq_unassigned.kql       # Kusto query
├── data/
│   └── friday_lq_*.json               # Cached query results
└── friday_reports/
    ├── friday_lq_report_*.json        # Generated reports
    └── friday_lq_report_*.csv         # CSV exports
```

## 🤖 Automate with Task Scheduler

Create a scheduled task for automatic Friday runs:

```
Trigger: Weekly, every Friday at 8:00 PM
Action:
  Program: python.exe
  Arguments: run_friday_lq_analysis.py
  Start in: C:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents
```

## 🔧 Troubleshooting

**No results?**
- Check if "All Data Provided" is the exact text in ICM
- Verify "Escalation Reviewer" field name
- Confirm date range has closed cases

**Wrong region classification?**
- Check SourceOrigin field values
- Update region mapping in query if needed

**Feature area showing Unknown?**
- Check "Feature Area" custom field in ICM
- Update feature mapping logic

## 📚 Related Files

- [FRIDAY_LQ_README.md](FRIDAY_LQ_README.md) - Full documentation
- [LQ_ESCALATION_README.md](LQ_ESCALATION_README.md) - General LQE agent docs
- [queries/friday_lq_unassigned.kql](queries/friday_lq_unassigned.kql) - The query

---
**Created**: February 5, 2026  
**Author**: Carter Ryan  
**Purpose**: Weekly unassigned low quality escalation review
