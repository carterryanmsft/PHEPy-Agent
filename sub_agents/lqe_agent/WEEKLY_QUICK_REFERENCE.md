# Weekly LQE Reports - Quick Reference Card

## 🚀 One-Line Execution

```powershell
.\Run-WeeklyLQEReports.ps1
```

---

## 📅 When to Run
- **Recommended:** Every Friday afternoon or Monday morning
- **Frequency:** Weekly
- **Data Range:** Last 7 days

---

## 📊 Output

### Reports Per Region
- **Americas** (US, Canada, LATAM)
- **EMEA** (Europe, Middle East, Africa)  
- **APAC** (Asia-Pacific + Unknown)

### File Formats
- ✅ **HTML** - Email-ready report with formatting
- ✅ **JSON** - Structured data for automation
- ✅ **CSV** - Excel export for analysis

---

## 🎯 What's Included

**Escalations that are:**
- ✅ Closed in last 7 days
- ✅ Low quality (NOT "All Data Provided")
- ✅ Unassigned (no reviewer)
- ✅ Not false positive
- ✅ Purview products only

---

## 📂 Report Location

```
sub_agents/lqe_agent/reports/regional_reports/
├── americas_lqe_report_TIMESTAMP.htm
├── emea_lqe_report_TIMESTAMP.htm
└── apac_lqe_report_TIMESTAMP.htm
```

---

## ⚙️ Command Options

### Basic
```powershell
# Fresh data (default)
.\Run-WeeklyLQEReports.ps1

# Use existing data (faster)
.\Run-WeeklyLQEReports.ps1 -SkipDataFetch

# Specific data file
.\Run-WeeklyLQEReports.ps1 -DataFile "data\regional_lqe_14day_real_20260213.json"
```

### Email Distribution
```powershell
# Send reports via email
.\Run-WeeklyLQEReports.ps1 -SendEmail -FromEmail "your.email@microsoft.com"

# Test mode (no emails sent)
.\Run-WeeklyLQEReports.ps1 -SendEmail -FromEmail "your.email@microsoft.com" -TestMode
```

---

## 🧪 Test Mode

```powershell
# Generate test data (no Kusto required)
python generate_test_weekly_data.py

# Run with test data
.\Run-WeeklyLQEReports.ps1 -DataFile "data\regional_lqe_test_TIMESTAMP.json"
```

---

## 🔧 Prerequisites

- ✅ Python 3.8+
- ✅ Azure authentication (`az login`)
- ✅ Kusto access (icmcluster)
- ✅ Packages: `pip install pandas azure-kusto-data azure-identity`

---

## 📈 Success Indicators

```
✓ Data fetched: 25-50 escalations typical
✓ 3 regional reports generated
✓ HTML files < 2 minutes old
✓ No Python errors
```

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Azure not authenticated | Run: `az login` |
| No data returned | Check Kusto permissions |
| 0 escalations for region | Normal for slow weeks |
| HTML not generated | Check Python packages installed |

---

## 📚 Documentation

- **[Full Guide](WEEKLY_LQE_QUICK_START.md)** - Complete instructions
- **[Main README](README.md)** - System overview
- **[Friday Workflow](FRIDAY_QUICK_START.md)** - Friday-specific process

---

## 🔄 Automation Setup

```powershell
# Windows Task Scheduler - Every Friday 4pm
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File 'C:\...\Run-WeeklyLQEReports.ps1'"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At 4PM
Register-ScheduledTask -TaskName "Weekly LQE Reports" -Action $action -Trigger $trigger
```

---

## 📊 Typical Output

```
WEEKLY REGIONAL LQE REPORT - EXECUTION SUMMARY
================================================

📅 Generated: 2026-02-13 14:30:00
📊 Data Source: regional_lqe_14day_real_20260213_143000.json

📁 Reports Generated:
   ✓ Americas    → americas_lqe_report_20260213_143015.htm
   ✓ EMEA        → emea_lqe_report_20260213_143015.htm
   ✓ APAC        → apac_lqe_report_20260213_143015.htm
```

---

## ✅ Quick Checklist

- [ ] Python 3.8+ installed
- [ ] Azure authenticated (`az login`)
- [ ] Navigate to lqe_agent folder
- [ ] Run: `.\Run-WeeklyLQEReports.ps1`
- [ ] Verify 3 HTML files created
- [ ] Review reports for accuracy
- [ ] Distribute to stakeholders

---

**Questions?** See [WEEKLY_LQE_QUICK_START.md](WEEKLY_LQE_QUICK_START.md)
