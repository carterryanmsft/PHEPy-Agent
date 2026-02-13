# Risk Reports Folder Structure

This folder contains all risk assessment and reporting resources for IC/MCS customer support cases.

## Quick Start: Automated JSON Workflow (✨ NEW - No Manual Export Required!)

The report generator now accepts **JSON input directly from Kusto MCP tools**:

```powershell
# Run Python generator with JSON input (auto-detected):
python ic_mcs_risk_report_generator.py production_cases.json IC_MCS_Production_Report.htm icm.csv
```

**Benefits:**
- ✅ No manual CSV export from Azure Data Explorer
- ✅ Works with Kusto MCP JSON output (up to 500 rows)
- ✅ Current query returns 131 cases (well under limit)
- ✅ Same features as CSV: ICM owner, ACTIVE highlighting, formatting

**Input Format Auto-Detection:**
- `.json` → Reads JSON, extracts `data` array
- `.csv` → Reads CSV (legacy method)

Both formats produce identical HTML reports!

---

## Folder Organization

### `/queries`
Kusto (KQL) queries for risk scoring and case analysis:
- `ic_mcs_risk_report.kql` - Main risk scoring query with 7-factor CRI methodology

### `/templates`
HTML and report templates:
- `Risk Report Template.htm` - HTML template for risk report formatting

### `/documentation`
Risk scoring methodology and reference materials:
- `ICM_CRI_Risk_Score_Reference.md` - ICM CRI Risk Score methodology documentation

### `/` (root)
Generated reports and utilities:
- `ic_mcs_risk_report_generator.py` - Python script to generate HTML reports from Kusto results
- `CaseRiskReport - 2026-02-03.csv` - Sample risk report data

## Complete Workflow (With ICM Owner Data)

### 1. Run Support Case Query (Required)
**Cluster**: cxedataplatformcluster.westus2.kusto.windows.net/cxedata  
**File**: `queries/ic_mcs_risk_report.kql`  
**Export to**: `cases.csv`

### 2. Run ICM Query (Optional - for ICM owner names)
**Cluster**: icmcluster.kusto.windows.net/icmdatawarehouse  
**File**: `queries/icm_incidents_query.kql`  
**Export to**: `icm.csv`  
**Note**: This pulls OwningContactAlias (ICM owner) for each incident

### 3. Generate HTML Report
```powershell
# Without ICM owner data:
python ic_mcs_risk_report_generator.py cases.csv report.htm

# With ICM owner data (RECOMMENDED):
python ic_mcs_risk_report_generator.py cases.csv icm.csv report.htm
```

### 4. View Report
```powershell
Invoke-Item report.htm
```

**Important**: The report will show "N/A" for ICM Owner if you don't provide the `icm.csv` file

## Risk Scoring Model

Based on ICM CRI Risk Score methodology (7 factors):
- Age/Status (0-40 pts)
- Ownership Changes (0-20 pts)
- Transfer Count (0-15 pts)
- Idle Period (0-15 pts)
- Reactivation/Reopen (0-10 pts)
- ICM Escalation (0-10 pts)
- Severity + Crit Sit (0-15 pts)

**Risk Levels:**
- **Critical**: 80-100 points
- **High**: 60-79 points
- **Medium**: 40-59 points
- **Low**: 0-39 points

## Usage

```powershell
# 1. Run Kusto query and export to CSV
# 2. Generate HTML report
python ic_mcs_risk_report_generator.py query_results.csv output_report.htm
```

## Owner
- **Agent**: Jacques (Kusto Expert)
- **Team**: PHE Operations
- **Last Updated**: February 4, 2026

---

# IC/MCS Risk Report System - Complete Guide

## System Overview
Automated end-to-end risk reporting for IC/MCS Purview Compliance cases with 7-factor scoring, HTML generation, and ICM integration.

## Complete Workflow

### 1. Run Support Case Query (Required)
**Location:** Kusto Web Explorer → cxedataplatformcluster.westus2.kusto.windows.net/cxedata
**File:** queries/ic_mcs_risk_report.kql
**Export to:** cases.csv

### 2. Run ICM Query (Optional - for ICM owner data)
**Location:** Kusto Web Explorer → icmcluster.kusto.windows.net/icmdatawarehouse
**File:** queries/icm_incidents_query.kql  
**Export to:** icm.csv

### 3. Generate HTML Report
```powershell
# Without ICM data:
python ic_mcs_risk_report_generator.py cases.csv report.htm

# With ICM data:
python ic_mcs_risk_report_generator.py cases.csv icm.csv report.htm
```

### 4. View Report
```powershell
Invoke-Item report.htm
```

## Risk Scoring Formula (0-100 points)

| Factor | Max Points | Description |
|--------|------------|-------------|
| Age/Status | 40 | >180d=40, >120d=35, >90d=30, >60d=25, >30d=20 |
| Ownership Changes | 20 | >20=20, >10=15, >5=10, >2=5 |
| Transfers | 15 | >20=15, >10=12, >5=8, >2=4 |
| Idle Period | 15 | >30d=15, >21d=12, >14d=8, >7d=4 |
| Reopens | 10 | >=3=10, 2=7, 1=5 |
| ICM Present | 10 | Yes=10, No=0 |
| Severity/CritSit | 15 | CritSit+10, Sev1/A/Crit=5, Sev2/B/High=3 |

**Risk Levels:** Critical (80-100) | High (60-79) | Medium (40-59) | Low (0-39)

## Report Features
✅ Executive summary with risk level statistics
✅ Customer-organized view (highest risk first)
✅ Clickable case IDs → ServiceDesk
✅ Clickable ICM IDs → ICM Portal v5
✅ Case owner and manager information
✅ Color-coded risk levels
✅ PHE/CLE assignments

## IC/MCS Customers (23)
**MCS (8):** ADNOC, Amazon, Barclays, EY, Morgan Stanley, NHS, Palantir, Walmart
**IC (15):** AGL, Autodesk, BHP, Ford, Huntington, MUFJ, NAB, Nestle, Novartis, Sainsbury's, Santander, State of WA, Vodafone, WSP, Zurich

## Test Results (Latest Run)
- ✅ Query executed successfully
- ✅ Report generated: 4 cases, 3 customers
- ✅ Risk distribution: Medium (4), Low (0)
- ✅ Top risk: Barclays Bank (58 points)
- ✅ All links functional (Case IDs, ICM IDs)

## Maintenance
**Update customers:** Edit ICMCSTenants datatable in ic_mcs_risk_report.kql
**Adjust scoring:** Modify RiskScore calculation in query
**Customize HTML:** Edit CSS in ic_mcs_risk_report_generator.py

**Author:** Jacques (Kusto Expert) | **Date:** February 4, 2026
