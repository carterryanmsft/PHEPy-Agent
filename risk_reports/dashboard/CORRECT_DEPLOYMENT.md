# Azure Data Explorer Dashboard - CORRECT Deployment Method

## ⚠️ Important: JSON Import Doesn't Work

Azure Data Explorer dashboards **cannot be imported from JSON**. You must build them in the UI.

## ✅ Correct Method: Build in UI

### Step 1: Create Dashboard

1. Go to https://dataexplorer.azure.com
2. Click "Dashboards" in left menu
3. Click "+ New dashboard"
4. Name: **IC/MCS Case Risk Dashboard**

### Step 2: Connect Data Source

1. Click "Data sources" → "+ Add"
2. **Primary Source:**
   - Cluster: `https://cxedataplatformcluster.westus2.kusto.windows.net`
   - Database: `cxedata`
   - Name: `CXE Support Data`
3. Click "+ Add" again for second source
4. **ICM Source:**
   - Cluster: `https://icmcluster.kusto.windows.net`  
   - Database: `IcmDataWarehouse`
   - Name: `ICM Data`

### Step 3: Add Critical Count Tile (Easiest Start)

1. Click "+ Add tile"
2. **Tile settings:**
   - Name: `Critical Cases`
   - Data source: `CXE Support Data`
3. **Paste this query:**

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    "Ford", 639534, "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "", "Ron Mustard", "IC",
    "Sainsbury's", 7056084, "e11fd634-26b5-47f4-8b8c-908e466e9bdf", "", "Sonal Sagar", "IC",
    "Autodesk", 625338, "67bff79e-7f91-4433-a8e5-c9252d2ddc1d", "", "Tim Griffin", "IC",
    "Vodafone", 520413, "68283f3b-8487-4c86-adb3-a5228f18b893", "", "Josef Ibarra", "IC",
    "State of WA", 641135, "11d0e217-264e-400a-8ba0-57dcc127d72d", "", "Kanika Kapoor", "IC",
    "State of WA", 641135, "9ef85bca-98dd-4e6e-b55c-f296e678e989", "", "Kanika Kapoor", "IC",
    "BHP", 523272, "4f6e1565-c2c7-43cb-8a4c-0981d022ce20", "", "Manaswi Upadhyaya K", "IC",
    "AGL Energy", 1170498, "123913b9-915d-4d67-aaf9-ce327e8fc59f", "", "Maathangi Kannan Vaidehi", "IC",
    "WSP", 2831650, "3d234255-e20f-4205-88a5-9658a402999b", "", "Amulya Eedara", "IC",
    "Huntington", 645695, "157a26ef-912f-4244-abef-b45fc4bd77f9", "", "Hemanth Varyani", "IC",
    "Nestle", 604010, "12a3af23-a769-4654-847f-958f3d479f4a", "", "Josef Ibarra", "IC",
    "Santander", 1278397, "35595a02-4d6d-44ac-99e1-f9ab4cd872db", "", "Pavel Garmashov", "IC",
    "Zurich", 2656229, "95d1d810-50cf-4169-8565-6bfba279a0cd", "", "Pavel Garmashov", "IC",
    "Novartis", 1528952, "f35a6974-607f-47d4-82d7-ff31d7dc53a5", "", "Ramana Krishnamoorthy", "IC",
    "NAB", 1104955, "48d6943f-580e-40b1-a0e1-c07fa3707873", "", "KAPIL Chopra", "IC",
    "MUFJ", 5025483, "3a498a73-f68c-4993-9940-40f5dc4b029b", "", "Salonie Vyas", "IC",
    "MUFJ", 5025483, "952d7d55-02c8-4421-ae6d-aa79da2f5152", "", "Salonie Vyas", "IC"
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName == "Microsoft Purview Compliance"
| join kind=inner ICTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen > 90
| summarize CriticalCount = count()
| project CriticalCount
```

4. Click "Run" to test
5. **Visual settings:**
   - Type: **Stat** (or Big number)
   - Title: `Critical Cases`
   - Subtitle: `90+ days old`
6. Click "Apply changes"
7. **Resize tile**: Width 2, Height 2
8. **Style**: Background color `#FFC7CE` (red)

### Step 4: Add Critical Cases Table

1. Click "+ Add tile"
2. **Paste query** from `queries/dashboard_critical_cases.kql`
3. **Visual settings:**
   - Type: **Table**
   - Title: `🚨 Critical Cases`
4. **Table columns** - Enable these:
   - ServiceRequestNumber (link to OneSupport)
   - TopParentName
   - DaysOpen
   - RiskScore
   - AgentAlias
   - ServiceRequestStatus
5. **Apply changes**
6. Resize: Full width (12), Height 6

### Step 5: Continue Adding Tiles

Repeat for each query file in `queries/` folder:
- Copy query from `.kql` file
- Create new tile
- Paste query
- Select appropriate visual type:
  - **Cards/Stats**: `_count.kql`, `_avg.kql` queries
  - **Pie Chart**: `risk_distribution.kql`
  - **Column Chart**: `age_distribution.kql`
  - **Bar Chart**: `top_customers.kql`
  - **Line Chart**: `risk_trend.kql`
  - **Tables**: `critical_cases.kql`, `all_cases.kql`

---

## 🎯 Tile-by-Tile Guide

### Tile 1: Summary Stats (Card)
**Query**: `dashboard_summary.kql`  
**Visual**: Stat  
**Size**: 4×2  
**Position**: Top-left

### Tile 2: Critical Count (Card - Red)
**Query**: `dashboard_critical_count.kql`  
**Visual**: Stat  
**Size**: 2×2  
**Color**: #FFC7CE background

### Tile 3: High Count (Card - Yellow)
**Query**: `dashboard_high_count.kql`  
**Visual**: Stat  
**Size**: 2×2  
**Color**: #FFF2CC background

### Tile 4: Avg Risk Score (Card)
**Query**: `dashboard_avg_risk.kql`  
**Visual**: Stat  
**Size**: 2×2

### Tile 5: Avg Age (Card)
**Query**: `dashboard_avg_age.kql`  
**Visual**: Stat  
**Size**: 2×2

### Tile 6: Risk Distribution (Pie Chart)
**Query**: `dashboard_risk_distribution.kql`  
**Visual**: Pie chart  
**Size**: 4×4

### Tile 7: Age Distribution (Column Chart)
**Query**: `dashboard_age_distribution.kql`  
**Visual**: Column chart  
**Size**: 4×4

### Tile 8: Top Customers (Bar Chart)
**Query**: `dashboard_top_customers.kql`  
**Visual**: Bar chart  
**Size**: 4×4

### Tile 9: ICM Status (Donut Chart)
**Query**: `dashboard_icm_status.kql`  
**Visual**: Donut chart  
**Size**: 3×4  
**Data Source**: ICM Data (change in tile settings)

### Tile 10: Risk Trend (Line Chart)
**Query**: `dashboard_risk_trend.kql`  
**Visual**: Line chart  
**Size**: 5×4

### Tile 11: Unassigned ICMs (Card - Red)
**Query**: `dashboard_unassigned_icms.kql`  
**Visual**: Stat  
**Size**: 2×2  
**Color**: #FFC7CE background  
**Data Source**: ICM Data

### Tile 12: Linked Bugs (Card)
**Query**: `dashboard_bugs_count.kql`  
**Visual**: Stat  
**Size**: 2×2  
**Data Source**: ICM Data

### Tile 13: Critical Cases Table
**Query**: `dashboard_critical_cases.kql`  
**Visual**: Table  
**Size**: 12×6

### Tile 14: All Cases Table
**Query**: `dashboard_all_cases.kql`  
**Visual**: Table  
**Size**: 12×8

---

## 🔧 After Creating All Tiles

### Add Parameters

1. Click "Parameters" button
2. **Add Time Range:**
   - Name: `TimeRange`
   - Type: Time range
   - Default: Last 180 days
3. **Add Customer Filter:**
   - Name: `CustomerFilter`
   - Type: Multiple selection
   - Query:
   ```kql
   GetSCIMIncidentV2
   | where ServiceRequestState != "Closed"
   | where ProductName == "Microsoft Purview Compliance"
   | distinct TopParentName
   | order by TopParentName asc
   ```
   - Data source: CXE Support Data
4. **Add Min Age:**
   - Name: `MinAge`
   - Type: Free text
   - Default value: `20`

### Enable Auto-Refresh

1. Click dashboard settings (gear icon)
2. Enable "Auto-refresh"
3. Set interval: 15 minutes
4. Click "Save"

### Arrange Tiles

1. Click "Edit" mode
2. Drag tiles to arrange:
   ```
   Row 1: [Summary 4×2] [Critical 2×2] [High 2×2] [AvgRisk 2×2] [AvgAge 2×2]
   Row 2: [RiskPie 4×4] [AgeChart 4×4] [TopCust 4×4]
   Row 3: [ICMStatus 3×4] [RiskTrend 5×4] [Unassigned 2×2] [Bugs 2×2]
   Row 4: [CriticalTable 12×6]
   Row 5: [AllCasesTable 12×8]
   ```
3. Click "Save dashboard"

---

## ⚡ Quick Build Method

### Option A: Pin from Query Results

This is actually the **fastest method**:

1. Go to https://dataexplorer.azure.com
2. Connect to `cxedataplatformcluster.westus2.kusto.windows.net/cxedata`
3. Run any query from `queries/` folder
4. Click **"Pin to dashboard"** button
5. Create new dashboard or select existing
6. Configure visual type
7. Repeat for all 14 queries

### Option B: Use Existing HTML Report Data

Since you already have the Python-generated HTML reports working:

1. Keep using HTML for weekly email distribution
2. Create a simplified dashboard with just:
   - Critical count card
   - Critical cases table
   - Top customers chart
3. This takes ~10 minutes vs full dashboard

---

## 💡 Recommendations

### For Your Use Case

**Best Approach**: Hybrid solution
1. **Keep Python/HTML reports** for:
   - Weekly email distribution
   - Historical snapshots
   - Offline viewing
   - Detailed formatting

2. **Create simplified dashboard** with just:
   - Critical cases count card
   - Critical cases table (90+ days)
   - Top 10 customers chart
   - Single "All Cases" table

This gives you:
- ✅ Real-time monitoring (dashboard)
- ✅ Detailed reports (HTML)
- ✅ Minimal maintenance (fewer tiles)
- ✅ Quick setup (~15 minutes)

### Minimum Viable Dashboard (5 Tiles)

If you want to start small:

1. **Critical Count** (Card) - Red alert
2. **All Cases Table** (Table) - Sortable/filterable
3. **Top Customers** (Bar) - Quick risk view
4. **ICM Status** (Donut) - ICM health check
5. **Add others later** as needed

---

## 🐛 Why JSON Import Doesn't Work

Azure Data Explorer dashboards:
- ❌ Cannot import JSON with embedded queries
- ❌ No API for bulk tile creation
- ❌ No "dashboard as code" feature
- ✅ Must be built in UI
- ✅ Can share via URL after creation
- ✅ Can export/import simple structure (but loses queries)

The JSON file I created documents the structure but isn't importable. Use it as a reference for tile arrangement and query content.

---

## 📝 What to Do Now

**Choose your path:**

**Path A - Full Dashboard** (1-2 hours):
1. Follow Step 1-5 above
2. Add all 14 tiles
3. Configure parameters
4. Enable auto-refresh

**Path B - Quick Start** (15 minutes):
1. Create dashboard
2. Add 5 core tiles (critical count, critical table, top customers, ICM status, all cases)
3. Add others over time

**Path C - Keep It Simple** (current method):
1. Keep using Python HTML reports
2. No dashboard needed
3. Reports work great via email

**My Recommendation**: Path B or C. The HTML reports you have are excellent and work perfectly for weekly distribution. A dashboard adds real-time monitoring but isn't essential unless you need live updates.

---

## ✅ Next Steps

1. Decide: Full dashboard, minimal dashboard, or stick with HTML?
2. If dashboard: Start with "Pin from Query" method (fastest)
3. Use queries from `dashboard/queries/` folder
4. Build incrementally - add tiles as needed

Let me know which path you prefer and I can provide more specific guidance!
