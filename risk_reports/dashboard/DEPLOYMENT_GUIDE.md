# Azure Data Explorer Dashboard - IC/MCS Risk Report

## Deployment Guide

### Prerequisites

1. **Azure Subscription** with access to:
   - Azure Data Explorer (Kusto) clusters
   - Dashboard service permissions

2. **Cluster Access:**
   - `cxedataplatformcluster.westus2.kusto.windows.net` (cxedata database)
   - `icmcluster.kusto.windows.net` (IcmDataWarehouse database)

3. **Permissions Required:**
   - Viewer/Reader on both Kusto clusters
   - Dashboard Editor role for creating/editing dashboards

---

## Quick Start

### Option 1: Import Dashboard JSON (Recommended)

1. **Navigate to Azure Data Explorer Dashboards**
   ```
   https://dataexplorer.azure.com/dashboards
   ```

2. **Create New Dashboard**
   - Click "New dashboard"
   - Click "Import" → "From file"
   - Select `IC_Risk_Dashboard.json`

3. **Update Configuration**
   - Replace `YOUR_SUBSCRIPTION_ID` in data sources section
   - Verify cluster URLs match your environment
   - Click "Save"

4. **Test Dashboard**
   - All tiles should auto-load
   - Use filters to refine data
   - Set auto-refresh interval (default: 15 minutes)

---

### Option 2: Manual Dashboard Creation

If you prefer to build step-by-step:

#### Step 1: Create Dashboard

1. Go to https://dataexplorer.azure.com/dashboards
2. Click "+ New dashboard"
3. Name: "IC/MCS Case Risk Dashboard"
4. Description: "Real-time risk monitoring for IC and MCS customer cases"

#### Step 2: Add Data Sources

**Primary Data Source (CXE Data):**
- Cluster URI: `https://cxedataplatformcluster.westus2.kusto.windows.net`
- Database: `cxedata`
- Display Name: `CXE Support Data`

**Secondary Data Source (ICM Data):**
- Cluster URI: `https://icmcluster.kusto.windows.net`
- Database: `IcmDataWarehouse`
- Display Name: `ICM Incidents`

#### Step 3: Add Parameters

1. **TimeRange** (Time Range Picker)
   - Default: 180 days
   - Allow custom range

2. **CustomerFilter** (Multi-Select)
   - Query: `GetSCIMIncidentV2 | where ServiceRequestState != 'Closed' | distinct TopParentName`
   - Default: "All"

3. **MinAge** (Number Input)
   - Default: 20
   - Description: "Minimum case age in days"

4. **RiskLevelFilter** (Multi-Select)
   - Options: Critical, High, Medium, Low, All
   - Default: "All"

#### Step 4: Add Tiles

**Row 1: KPI Cards (0-12 width)**

1. **Summary Stats Card** (0,0 - width 4, height 2)
   - Query: `queries/dashboard_summary.kql`
   - Visual: Card

2. **Critical Count Card** (4,0 - width 2, height 2)
   - Query: `queries/dashboard_critical_count.kql`
   - Visual: Card
   - Background: #FFC7CE

3. **High Risk Card** (6,0 - width 2, height 2)
   - Query: `queries/dashboard_high_count.kql`
   - Visual: Card
   - Background: #FFF2CC

4. **Avg Risk Score Card** (8,0 - width 2, height 2)
   - Query: `queries/dashboard_avg_risk.kql`
   - Visual: Card

5. **Avg Age Card** (10,0 - width 2, height 2)
   - Query: `queries/dashboard_avg_age.kql`
   - Visual: Card

**Row 2: Charts (0-12 width)**

6. **Risk Distribution** (0,2 - width 4, height 4)
   - Query: `queries/dashboard_risk_distribution.kql`
   - Visual: Pie Chart

7. **Age Distribution** (4,2 - width 4, height 4)
   - Query: `queries/dashboard_age_distribution.kql`
   - Visual: Column Chart

8. **Top Customers** (8,2 - width 4, height 4)
   - Query: `queries/dashboard_top_customers.kql`
   - Visual: Bar Chart

**Row 3: ICM & Trends (0-12 width)**

9. **ICM Status** (0,6 - width 3, height 4)
   - Query: `queries/dashboard_icm_status.kql`
   - Visual: Donut Chart
   - Data Source: ICM Incidents

10. **Risk Trend** (3,6 - width 5, height 4)
    - Query: `queries/dashboard_risk_trend.kql`
    - Visual: Line Chart

11. **Unassigned ICMs** (8,6 - width 2, height 2)
    - Query: `queries/dashboard_unassigned_icms.kql`
    - Visual: Card
    - Data Source: ICM Incidents

12. **Linked Bugs** (10,6 - width 2, height 2)
    - Query: `queries/dashboard_bugs_count.kql`
    - Visual: Card
    - Data Source: ICM Incidents

**Row 4: Critical Cases Table** (0,10 - width 12, height 6)

13. **Critical Cases Table**
    - Query: `queries/dashboard_critical_cases.kql`
    - Visual: Table
    - Enable: Click-through to OneSupport
    - Color: Risk score column by value

**Row 5: All Cases Table** (0,16 - width 12, height 8)

14. **All Cases Table**
    - Query: `queries/dashboard_all_cases.kql`
    - Visual: Table
    - Enable: Click-through to OneSupport
    - Color: Risk Level by category

#### Step 5: Configure Auto-Refresh

1. Click "Dashboard settings" (gear icon)
2. Enable "Auto-refresh"
3. Set interval: 15 minutes
4. Timezone: Pacific Standard Time
5. Save settings

---

## Dashboard Features

### Interactive Capabilities

1. **Filters**
   - Time range selector (default: 180 days)
   - Customer multi-select dropdown
   - Minimum age threshold
   - Risk level filter

2. **Click-Through Actions**
   - Case ID links → OneSupport case page
   - ICM ID links → ICM portal (if configured)
   - Customer names → Filter to specific customer

3. **Auto-Refresh**
   - Configurable interval (5, 15, 30, 60 minutes)
   - Manual refresh button
   - Last updated timestamp

4. **Export Options**
   - Export to Excel (any table tile)
   - Download as PDF (full dashboard)
   - Share via URL (with or without parameters)

### Color Coding

- **Critical**: Red background (#FFC7CE), dark red text (#9C0006)
- **High**: Yellow background (#FFF2CC), dark yellow text (#9C6500)
- **Medium**: Green background (#C6EFCE), dark green text (#006100)
- **Low**: Gray background (#F0F0F0), dark gray text (#3F3F76)

---

## Maintenance & Updates

### Updating Queries

1. Edit query files in `dashboard/queries/` folder
2. In Azure Data Explorer dashboard:
   - Click tile → "Edit query"
   - Paste updated KQL
   - Click "Apply"

### Adding New Customers

Update the `ICTenants` datatable in all query files:

```kql
let ICTenants = datatable(TopParentName:string, TPID:int, TenantId:string, CLE:string, PHE:string, Program:string)
[
    // Add new line here:
    "New Customer", 123456, "tenant-guid", "cle-email", "phe-email", "IC",
    // ... existing customers
];
```

### Modifying Risk Scoring

To adjust risk calculation, update these sections in relevant queries:

```kql
| extend AgeScore = case(
    DaysOpen > 180, 56,  // Adjust these values
    DaysOpen > 120, 49,
    DaysOpen > 90, 42,
    // ...
)
```

---

## Troubleshooting

### Common Issues

**1. "No data" in tiles**
- Verify cluster access permissions
- Check query syntax in Azure Data Explorer web UI
- Confirm data exists for selected time range

**2. "Authentication failed"**
- Re-authenticate to both clusters
- Verify Azure AD group memberships
- Check firewall/network restrictions

**3. "Query timeout"**
- Reduce time range in filter
- Add `| take 1000` limit to queries during testing
- Check cluster health/performance

**4. "Cross-cluster query failed"**
- Verify ICM cluster access
- Check cluster follower relationships
- Use `cluster().database()` syntax correctly

### Performance Optimization Tips

1. **Narrow Time Windows**
   - Default 180 days is comprehensive but slower
   - Use 30-90 days for daily monitoring
   - Archive older data queries separately

2. **Indexed Filters**
   - Filter on indexed columns first (TenantId, ServiceRequestState)
   - Apply custom filters last

3. **Summarize Early**
   - Use `summarize` before joins when possible
   - Reduce result set size before mv-expand

4. **Cache Results**
   - Enable result caching in dashboard settings
   - Set appropriate cache TTL (15-30 minutes)

---

## Advanced Configuration

### Custom Alerts

Create alerts based on dashboard queries:

1. **Unassigned Active ICMs Alert**
   ```kql
   // Use dashboard_unassigned_icms.kql
   // Trigger if count > 0
   ```

2. **Critical Cases Threshold Alert**
   ```kql
   // Use dashboard_critical_count.kql
   // Trigger if count > 30
   ```

3. **Average Risk Score Alert**
   ```kql
   // Use dashboard_avg_risk.kql
   // Trigger if score > 50
   ```

### Integration with Teams

1. Install "Azure Data Explorer" Teams app
2. Share dashboard URL in Teams channel
3. Configure automatic snapshots (daily/weekly)
4. Enable notifications for threshold breaches

### Power BI Integration

Export dashboard data to Power BI:

1. Copy KQL queries from dashboard
2. In Power BI Desktop:
   - Get Data → Azure Data Explorer (Kusto)
   - Paste query
   - Configure refresh schedule

---

## Security & Permissions

### Required Permissions

**View Dashboard:**
- Reader/Viewer on both Kusto clusters
- Dashboard Reader role

**Edit Dashboard:**
- Contributor on Kusto clusters
- Dashboard Contributor role

**Create Alerts:**
- Monitoring Contributor
- Action Group permissions

### Data Access Controls

Dashboard respects cluster-level permissions:
- Users see only data they have access to
- Customer filtering applies row-level security
- ICM data requires separate authentication

---

## Support & Resources

### Documentation Links

- [Azure Data Explorer Dashboards Overview](https://learn.microsoft.com/azure/data-explorer/azure-data-explorer-dashboards)
- [Kusto Query Language Reference](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
- [Dashboard JSON Schema](https://dataexplorer.azure.com/static/d/schema/dashboard.json)

### Contact

- PHE/CLE Team: See customer mappings in IC Tenants list
- Kusto Support: Open ticket in ICM under CXE Care team
- Dashboard Issues: Contact Copilot workspace maintainer

---

## Version History

- **v1.0** (February 2026): Initial dashboard creation
  - 14 tiles (5 cards, 4 charts, 2 tables)
  - 4 parameters (time, customer, age, risk level)
  - Auto-refresh every 15 minutes
  - Risk scoring with 90-day critical threshold
  - cross-cluster ICM and bug integration

---

## Next Steps

1. ✅ Import dashboard JSON
2. ✅ Verify data sources
3. ✅ Test all tiles load correctly
4. ✅ Share dashboard URL with stakeholders
5. ✅ Schedule weekly review of Critical Cases
6. ✅ Set up Teams notifications (optional)
7. ✅ Configure Power BI refresh (optional)

**Dashboard URL Format:**
```
https://dataexplorer.azure.com/dashboards/<dashboard-id>?p-TimeRange=180d&p-MinAge=20
```

Save this URL for easy access and sharing!
