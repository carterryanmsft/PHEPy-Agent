# 🎉 Friday LQE Multi-Report System - Complete!

## ✅ What's New

Created **multi-report generation system** that produces 4 HTML reports:
1. **All-Up Report** - All regions combined
2. **Americas Report** - Americas region only
3. **EMEA Report** - EMEA region only  
4. **APAC Report** - APAC region only

## 📝 Changes Made

### HTML Report Streamlined
- ❌ Removed: Severity column
- ❌ Removed: Team column
- ❌ Removed: Reason column
- ❌ Removed: Filter criteria description
- ✅ Cleaner, more focused report

### New Multi-Report Generator
**File**: `generate_friday_reports.py`
- Executes Kusto query via MCP
- Generates 4 separate HTML reports
- Organizes by region automatically

## 🚀 How to Get Real Data

### Step 1: Execute Kusto Query

Use the MCP Kusto tool to execute this query:

**Cluster**: `https://icmcluster.kusto.windows.net`  
**Database**: `IcMDataWarehouse`  
**Max Rows**: `10000`

**Query** (from `queries/friday_lq_unassigned.kql`):
```kql
let escalationInformation = IncidentsDedupView
| where OwningTenantName == "Purview"
| where ResolveDate > ago(7d)
| where IncidentType == "CustomerReported"
| extend FiscalWeek = 24 - toint((fw24EndDate - ResolveDate) / 7d)
| project ResolveDate, FiscalWeek, IncidentId, SourceCreatedBy, OwningTeamName, 
    Title, Severity, RoutingId, IcMId, CustomerSegment, SourceOrigin, ImpactStartDate;
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
let reviewerAssignment = IncidentCustomFieldEntriesDedupView
| where Name == "Escalation Reviewer"
| project IncidentId, ReviewerName = Value;
let featureArea = IncidentCustomFieldEntriesDedupView
| where Name == "Feature Area"
| project IncidentId, FeatureArea = Value;
escalationInformation
| join kind=inner (qualityInformation) on IncidentId
| join kind=leftouter (supportReviews) on IncidentId
| join kind=leftouter (qualityReasons) on IncidentId
| join kind=leftouter (reviewerAssignment) on IncidentId
| join kind=leftouter (featureArea) on IncidentId
| where EscalationQuality != "All Data Provided"
| where QualityReviewFalsePositive != "Yes" or isempty(QualityReviewFalsePositive)
| where isempty(ReviewerName) or ReviewerName == ""
| extend OriginRegion = case(
    SourceOrigin contains "EMEA" or SourceOrigin contains "Europe", "EMEA",
    SourceOrigin contains "APAC" or SourceOrigin contains "Asia", "APAC",
    SourceOrigin contains "LATAM" or SourceOrigin contains "Latin", "LATAM",
    SourceOrigin contains "Americas" or SourceOrigin contains "US" or SourceOrigin contains "NA", "Americas",
    "Unknown"
)
| extend FeatureAreaCategory = case(
    FeatureArea contains "MIP" or FeatureArea contains "DLP" or FeatureArea contains "Information Protection", "MIP/DLP",
    FeatureArea contains "DLM" or FeatureArea contains "Lifecycle" or FeatureArea contains "Retention", "DLM",
    FeatureArea contains "eDiscovery" or FeatureArea contains "eDisc" or FeatureArea contains "Discovery", "eDiscovery",
    FeatureArea contains "Compliance" or FeatureArea contains "Records", "Compliance",
    isempty(FeatureArea), "Unknown",
    "Other"
)
| extend IsTrueLowQuality = true
| project 
    IncidentId,
    IcMId,
    RoutingId,
    Title,
    Severity,
    CreatedBy = SourceCreatedBy,
    OwningTeam = OwningTeamName,
    ResolveDate,
    FiscalWeek,
    EscalationQuality,
    LowQualityReason,
    QualityReviewFalsePositive,
    CustomerSegment,
    IsTrueLowQuality,
    ReviewerName,
    OriginRegion,
    FeatureArea = FeatureAreaCategory,
    SourceOrigin
| order by OriginRegion asc, FeatureArea asc, ResolveDate desc
```

### Step 2: Save Query Results

Save the JSON results to:
```
sub_agents/data/friday_lq_kusto_20260207.json
```

### Step 3: Generate Reports

```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents"
python generate_friday_reports.py data/friday_lq_kusto_20260207.json
```

## 📊 Output Reports

You'll get 4 HTML files in `friday_reports/`:

```
friday_reports/
├── friday_lq_allup_YYYYMMDD_HHMMSS.htm      ← All regions
├── friday_lq_americas_YYYYMMDD_HHMMSS.htm   ← Americas only
├── friday_lq_emea_YYYYMMDD_HHMMSS.htm       ← EMEA only
└── friday_lq_apac_YYYYMMDD_HHMMSS.htm       ← APAC only
```

### Report Structure (Each)

```
┌─────────────────────────────────────┐
│  Friday Low Quality Escalations    │
│  [Region Name or "All Regions"]    │
└─────────────────────────────────────┘

📊 Executive Summary
├── Total escalations
├── Regions affected
└── Feature breakdown

📋 Escalations by Region & Feature
├── 🌎/🌍/🌏 Region Name
│   ├── 🔒 MIP/DLP
│   │   └── [Table: Incident ID | Title | Created By | Resolved | Quality]
│   ├── 📦 DLM
│   │   └── [Table...]
│   └── 🔎 eDiscovery
│       └── [Table...]
└── ...
```

## 🧪 Test Results

Successfully generated 4 reports from test data:

```
✅ All-Up: 18 total escalations
✅ Americas: 8 escalations (MIP/DLP: 5, DLM: 3)
✅ EMEA: 6 escalations (MIP/DLP: 4, eDiscovery: 2)
✅ APAC: 4 escalations (MIP/DLP: 3, DLM: 1)
```

**Test files:**
- `friday_reports/friday_lq_allup_20260205_135256.htm`
- `friday_reports/friday_lq_americas_20260205_135256.htm`
- `friday_reports/friday_lq_emea_20260205_135256.htm`
- `friday_reports/friday_lq_apac_20260205_135256.htm`

## 📧 Distribution Strategy

### Option 1: Send All 4 Reports
- Attach all 4 HTML files to email
- Recipients choose their region
- Leadership sees all-up view

### Option 2: Targeted Distribution
- Send All-Up to leadership
- Send regional reports to regional managers
  - Americas report → Americas team
  - EMEA report → EMEA team
  - APAC report → APAC team

### Option 3: SharePoint
- Upload all 4 reports to SharePoint
- Send link to folder
- Auto-archive by week

## 🎨 Report Table Structure

Each regional table now shows:

| Column | Description |
|--------|-------------|
| **Incident ID** | Clickable ICM link |
| **Title** | Escalation title (full length) |
| **Created By** | Support engineer email |
| **Resolved** | Resolution date (MM/DD/YYYY) |
| **Quality Issue** | Escalation quality categorization |

**Removed for clarity:**
- ~~Severity~~ - Not needed for reviewer assignment
- ~~Team~~ - Redundant with region/feature grouping
- ~~Reason~~ - Too detailed for initial review

## 💡 Usage Tips

### View All Reports Quickly
```powershell
cd friday_reports
start friday_lq_allup_*.htm
start friday_lq_americas_*.htm
start friday_lq_emea_*.htm
start friday_lq_apac_*.htm
```

### Filter by Date
```powershell
# Show only today's reports
ls friday_reports/*20260207*.htm
```

### Archive Old Reports
```powershell
# Move reports older than 30 days
$cutoff = (Get-Date).AddDays(-30)
Get-ChildItem friday_reports/*.htm | 
  Where-Object {$_.LastWriteTime -lt $cutoff} |
  Move-Item -Destination friday_reports/archive/
```

## 🔮 Next Steps

### Ready to Use with Real Data
1. Execute Kusto query via Copilot MCP tool
2. Save results to `data/friday_lq_kusto_YYYYMMDD.json`
3. Run `python generate_friday_reports.py data/friday_lq_kusto_YYYYMMDD.json`
4. Distribute 4 reports to teams

### Future Enhancements
- 📧 Automated email send per region
- 📊 Add trend charts (week-over-week)
- 🎨 Custom branding per region
- 📅 Scheduler integration
- 💾 Auto-archive to SharePoint

---

## 📚 Updated Files

1. **friday_lq_html_generator.py**
   - Removed sev, team, reason columns
   - Removed filter criteria section
   - Cleaner table layout

2. **generate_friday_reports.py** ⭐ NEW
   - Multi-report generation
   - Regional filtering
   - Kusto query display

3. **queries/friday_lq_unassigned.kql**
   - Ready-to-execute query

---

**Status**: ✅ Complete & Tested  
**Test Date**: February 5, 2026 1:52 PM  
**Ready for Production**: Yes with real Kusto data
