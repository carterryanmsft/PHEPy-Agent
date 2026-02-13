# IC/MCS Risk Reports - Complete Guide

## 🎯 Overview
Automated end-to-end risk report generation for IC/MCS customers with Purview Compliance cases. Generates HTML reports with 7-factor risk scoring, ICM status tracking, and executive dashboards.

---

## 🚀 Quick Start

### ⚡ Automated Workflow (Recommended)
```powershell
# Run the automation script:
.\Run-ProductionReport.ps1

# Or with Python:
python generate_production_report.py
```

### 📊 Manual Workflow
```powershell
# 1. Execute Kusto query and save JSON output
# 2. Generate report:
python ic_mcs_risk_report_generator.py production_cases.json IC_MCS_Production_Report.htm icm.csv
```

**✨ JSON Support:** The report generator now accepts JSON input directly from Kusto MCP tools - no manual CSV export required!

---

## 📁 Folder Organization

### Core Files
- **ic_mcs_risk_report_generator.py** (353 lines) - Main report generator
- **Run-ProductionReport.ps1** - One-command automation
- **generate_production_report.py** - Python automation orchestrator
- **icm.csv** - ICM owner lookup data (17 records)

### `/queries` - Kusto (KQL) Queries
- **ic_mcs_risk_report.kql** (172 lines) - Main risk scoring query with 7-factor CRI methodology
- **icm_incidents_query.kql** - ICM owner lookup query

### `/templates` - HTML Templates
- **Risk Report Template.htm** - HTML template for report formatting

### `/documentation` - Reference Materials
- **ICM_CRI_Risk_Score_Reference.md** - ICM CRI Risk Score methodology documentation

### `/data` - Input Data Files
- Query results (JSON/CSV)
- ICM owner lookups
- Customer tenant mappings

### `/output` - Generated Reports
- Production HTML reports
- Archive of historical reports

### `/archive` - Historical Data
- **deprecated_scripts/** - Old/duplicate scripts (22 files archived)
- Old test reports and samples

### `/scripts` - Active Utilities
- **convert_kusto_to_csv.py** - JSON to CSV converter (if needed)
- **generate_full_report.ps1** - Alternative automation

---

## 🔧 Complete Workflow

### Step 1: Run Support Case Query (Required)
**Cluster:** cxedataplatformcluster.westus2.kusto.windows.net/cxedata  
**Database:** cxedata  
**File:** `queries/ic_mcs_risk_report.kql`  
**Export to:** `production_cases.json` or `cases.csv`  

**Query Details:**
- **Table:** GetSCIMIncidentV2
- **Customers:** 23 IC/MCS tenants (33 tenant IDs)
- **Filters:** Open cases, 20+ days old, Purview Compliance products
- **Output:** ~131 cases (well under 500-row limit)

### Step 2: Run ICM Query (Optional - for ICM owner data)
**Cluster:** icmcluster.kusto.windows.net/icmdatawarehouse  
**Database:** IcmDataWarehouse  
**File:** `queries/icm_incidents_query.kql`  
**Export to:** `icm.csv`  

**Purpose:** Enriches reports with OwningContactAlias (ICM owner names)

### Step 3: Generate HTML Report
```powershell
# With ICM owner data (RECOMMENDED):
python ic_mcs_risk_report_generator.py cases.json IC_MCS_Production_Report.htm icm.csv

# Without ICM data (shows "N/A" for owners):
python ic_mcs_risk_report_generator.py cases.json IC_MCS_Production_Report.htm
```

**Input Format Auto-Detection:**
- `.json` → Reads JSON, extracts `data` array
- `.csv` → Reads CSV (legacy method)

Both formats produce identical HTML reports!

### Step 4: View Report
```powershell
Invoke-Item IC_MCS_Production_Report.htm
```

---

## 📈 Risk Scoring Methodology

Based on ICM CRI (Customer Risk Index) - 7-factor scoring model:

| Factor | Max Points | Calculation |
|--------|------------|-------------|
| **Age/Status** | 40 | >180d=40, >120d=35, >90d=30, >60d=25, >30d=20 |
| **Ownership Changes** | 20 | >20=20, >10=15, >5=10, >2=5 |
| **Transfer Count** | 15 | >20=15, >10=12, >5=8, >2=4 |
| **Idle Period** | 15 | >30d=15, >21d=12, >14d=8, >7d=4 |
| **Reopen Count** | 10 | >=3=10, 2=7, 1=5 |
| **ICM Escalation** | 10 | Has ICM=10, No ICM=0 |
| **Severity/CritSit** | 15 | CritSit+10, Sev1/A/Crit=5, Sev2/B/High=3 |

**Total Score:** 0-100 points

**Risk Levels:**
- 🔴 **Critical** (80-100): Immediate attention required
- 🟠 **High** (60-79): High priority monitoring
- 🟡 **Medium** (40-59): Monitor closely
- 🟢 **Low** (0-39): Routine tracking

---

## 🎨 Report Features

### Executive Summary
- Total customers and cases
- Risk level distribution (Critical/High/Medium/Low)
- Top 5 highest-risk customers
- ICM escalation statistics

### Customer Grouping
- Cases organized by customer (highest risk first)
- Customer-level risk summary
- ICM count per customer

### ICM Integration
- **ACTIVE ICMs:** 🟠 Orange highlight, sorted first
- **RESOLVED ICMs:** 🔵 Blue background
- **Owner Display:** Shows active ICM owner when available
- **Clickable Links:** Direct navigation to ICM Portal v5

### Case Details (31 fields)
- **Metadata:** ServiceRequestNumber, Status, State, Dates
- **Customer Info:** TopParentName, TPID, TenantId, PHE, CLE
- **Ownership:** Agent, Manager, Queue, Transfer/Ownership counts
- **Risk Metrics:** Score, Level, Age, Days Open
- **ICM Data:** RelatedICM_Id, Status, Owner
- **Summary:** Risk factor breakdown and recommendations

### Interactive Elements
- ✅ Clickable Case IDs → ServiceDesk (onesupport.crm.dynamics.com)
- ✅ Clickable ICM IDs → ICM Portal v5
- ✅ Color-coded risk levels
- ✅ Sortable by customer/risk level
- ✅ Responsive HTML design

---

## 👥 IC/MCS Customers (23 Total)

### MCS Customers (8)
ADNOC, Amazon, Barclays, EY, Morgan Stanley, NHS, Palantir, Walmart

### IC Customers (15)
AGL, Autodesk, BHP, Ford, Huntington, MUFJ, NAB, Nestle, Novartis, Sainsbury's, Santander, State of WA, Vodafone, WSP, Zurich

**Note:** Some customers have multiple tenant IDs (e.g., Walmart: 8 tenants)

---

## 🔄 Update Frequency

**Recommended Schedule:**
- **Weekly:** Full production reports for all customers
- **Daily:** For cases with Critical risk level
- **Ad-hoc:** When new ICMs escalate or critical incidents occur

**Data Freshness:**
- **Query results:** Real-time from Kusto
- **ICM status:** Updated via separate ICM query
- **Report generation:** Instantaneous (<2 seconds)

---

## ✅ Usage Examples

### Example 1: Full Production Report (131 cases)
```powershell
# Execute Kusto query → save to production_cases_131.json
python ic_mcs_risk_report_generator.py production_cases_131.json IC_MCS_Production_Report.htm icm.csv
Invoke-Item IC_MCS_Production_Report.htm
```

**Output:**
```
Report generated: IC_MCS_Production_Report.htm
Total customers: 8
Total cases: 131

Top 5 Highest Risk Customers:
1. Huntington: Risk 81 (7 ICMs, 1 case)
2. State of WA: Risk 81 (3 ICMs, 1 case)
3. Ford: Risk 77 (1 ICM, 4 cases)
4. BHP: Risk 71 (2 ICMs, 1 case)
5. Vodafone: Risk 71 (3 ICMs, 2 cases)
```

### Example 2: Test Data Run (9 cases)
```powershell
.\Run-ProductionReport.ps1  # Uses test_output_cases.csv
```

### Example 3: JSON Input from Kusto MCP
```powershell
# Kusto MCP returns JSON directly - no CSV export needed!
python ic_mcs_risk_report_generator.py kusto_result.json report.htm icm.csv
```

---

## 🐛 Troubleshooting

### Issue: "No saved query results found"
**Solution:**
- Execute the Kusto query first
- Save results to JSON or CSV file
- Or use test data: `test_output_cases.csv`

### Issue: "KeyError: 'TopParentName'"
**Solution:**
- CSV schema mismatch - re-export with all 31 fields
- **Better:** Use JSON format for guaranteed schema compatibility

### Issue: "ICM owners showing N/A"
**Solution:**
- Update `icm.csv` with latest ICM owner data
- Run `queries/icm_incidents_query.kql` separately
- Ensure ICM IDs match format in RelatedICM_Id column

### Issue: "ModuleNotFoundError: pandas"
**Solution:**
```powershell
pip install -r requirements.txt
# Or directly:
pip install pandas>=2.0.0
```

---

## 🛠️ Customization

### Add New Customers
Edit the `ICMCSTenants` datatable in `queries/ic_mcs_risk_report.kql`

### Adjust Risk Scoring
Modify the `RiskScore` calculation in the Kusto query

### Customize HTML Styling
Edit the CSS section in `ic_mcs_risk_report_generator.py` (lines 50-150)

### Change Report Layout
Modify HTML template in `templates/Risk Report Template.htm`

---

## 📊 Performance Metrics

**Full Production Run (131 cases):**
- ✅ Kusto query execution: ~3-5 seconds
- ✅ Report generation: ~1-2 seconds  
- ✅ Total end-to-end time: <10 seconds
- ✅ Memory usage: Minimal (~50MB for pandas)

**Validated Features:**
- ✅ Risk scoring (7-factor methodology)
- ✅ Customer grouping (23 customers)
- ✅ ICM owner lookup (17 ICMs mapped)
- ✅ ACTIVE ICM highlighting (orange, sorted first)
- ✅ Clickable links (Case URLs, ICM dashboard)
- ✅ JSON/CSV input (auto-detection)
- ✅ Executive summary dashboard
- ✅ Responsive HTML design

---

## 📧 Maintenance & Support

**System Owner:** Ryan Carter (PHE Team)  
**Agent:** Jacques (Kusto Expert)  
**System:** IC/MCS Risk Assessment Automation  
**Last Updated:** February 4, 2026

**Key Files to Maintain:**
- `icm.csv` - Update monthly with new ICM escalations
- `queries/ic_mcs_risk_report.kql` - Update customer list as needed
- `ic_mcs_risk_report_generator.py` - Core report logic

**Archived Files:**
- `archive/deprecated_scripts/` - 22 old scripts (Feb 2026 cleanup)
- `archive/README_original.md` - Original workflow guide
- `archive/README_AUTOMATION_original.md` - Original automation guide
- No longer maintained - kept for reference only

---

## 🔗 Related Documentation

- [Query Patterns Guide](../docs/QUERY_CHEAT_SHEET.md)
- [Customer Lookup Guide](../grounding_docs/contacts_access/CUSTOMER_LOOKUP_GUIDE.md)
- [ICM CRI Risk Score Reference](documentation/ICM_CRI_Risk_Score_Reference.md)
- [PHEPy Project Structure](../FOLDER_STRUCTURE.md)

---

**Benefits of This System:**
- ✅ **Automated:** One-command execution, no manual exports needed
- ✅ **Accurate:** Real-time data from Kusto clusters
- ✅ **Actionable:** Risk scores guide prioritization
- ✅ **Comprehensive:** 31 data fields per case
- ✅ **Integrated:** ICM status and owner tracking
- ✅ **Efficient:** <10 second report generation
- ✅ **Maintainable:** Clear documentation, standardized scripts
