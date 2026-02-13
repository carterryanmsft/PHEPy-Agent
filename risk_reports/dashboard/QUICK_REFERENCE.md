# Azure Data Explorer Dashboard - Quick Reference

## File Structure

```
risk_reports/dashboard/
├── IC_Risk_Dashboard.json          # Main dashboard definition
├── DEPLOYMENT_GUIDE.md             # Comprehensive setup instructions
├── QUICK_REFERENCE.md              # This file
└── queries/
    ├── dashboard_summary.kql       # Total cases summary card
    ├── dashboard_critical_count.kql # Critical cases count
    ├── dashboard_high_count.kql    # High risk count
    ├── dashboard_avg_risk.kql      # Average risk score
    ├── dashboard_avg_age.kql       # Average case age
    ├── dashboard_risk_distribution.kql # Pie chart
    ├── dashboard_age_distribution.kql # Column chart
    ├── dashboard_top_customers.kql # Top 10 bar chart
    ├── dashboard_icm_status.kql    # ICM donut chart
    ├── dashboard_risk_trend.kql    # 30-day trend line
    ├── dashboard_unassigned_icms.kql # Unassigned count
    ├── dashboard_bugs_count.kql    # Bugs count
    ├── dashboard_critical_cases.kql # Critical table
    └── dashboard_all_cases.kql     # All cases table
```

## Quick Commands

### Deploy Dashboard
```powershell
# Navigate to Azure Data Explorer Dashboards
Start-Process "https://dataexplorer.azure.com/dashboards"

# Import the JSON file
# File → Import → Select IC_Risk_Dashboard.json
```

### Test Individual Query
```kql
// In Azure Data Explorer web UI:
// 1. Connect to cxedataplatformcluster.westus2.kusto.windows.net
// 2. Select cxedata database
// 3. Paste query from queries/*.kql
// 4. Replace {MinAge} with 20
// 5. Click Run
```

### Update Dashboard
```powershell
# Edit query file locally
code risk_reports/dashboard/queries/dashboard_critical_count.kql

# In dashboard:
# 1. Click tile → Edit query
# 2. Paste updated KQL
# 3. Apply → Save dashboard
```

## Dashboard Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| TimeRange | Time Range | 180 days | Data lookback window |
| CustomerFilter | Multi-Select | All | Filter by specific customers |
| MinAge | Number | 20 | Minimum case age (days) |
| RiskLevelFilter | Multi-Select | All | Filter by risk level |

## Tile Overview

### Row 1: KPI Cards (Height: 2)
| Position | Tile | Width | Color |
|----------|------|-------|-------|
| (0,0) | Summary Stats | 4 | Default |
| (4,0) | Critical Count | 2 | Red (#FFC7CE) |
| (6,0) | High Count | 2 | Yellow (#FFF2CC) |
| (8,0) | Avg Risk Score | 2 | Default |
| (10,0) | Avg Age | 2 | Default |

### Row 2: Charts (Height: 4)
| Position | Tile | Width | Type |
|----------|------|-------|------|
| (0,2) | Risk Distribution | 4 | Pie Chart |
| (4,2) | Age Distribution | 4 | Column Chart |
| (8,2) | Top Customers | 4 | Bar Chart |

### Row 3: ICM & Trends (Height: 4)
| Position | Tile | Width | Type | Source |
|----------|------|-------|------|--------|
| (0,6) | ICM Status | 3 | Donut Chart | ICM Cluster |
| (3,6) | Risk Trend | 5 | Line Chart | CXE Data |
| (8,6) | Unassigned ICMs | 2 | Card | ICM Cluster |
| (10,6) | Linked Bugs | 2 | Card | ICM Cluster |

### Row 4-5: Tables
| Position | Tile | Width | Height |
|----------|------|-------|--------|
| (0,10) | Critical Cases | 12 | 6 |
| (0,16) | All Cases | 12 | 8 |

## Risk Scoring Formula

```kql
AgeScore = case(
    DaysOpen > 180, 56,
    DaysOpen > 120, 49,
    DaysOpen > 90, 42,
    DaysOpen > 60, 35,
    DaysOpen > 30, 28,
    DaysOpen >= 20, 14,
    0)

OwnershipScore = min(OwnershipCount * 2, 20)  // Max 20
TransferScore = min(TransferCount * 3, 15)    // Max 15
IdleScore = min(DaysSinceUpdate / 7 * 3, 15)  // Max 15
ReopenScore = min(ReopenCount * 5, 10)        // Max 10
ICMScore = isnotempty(RelatedICM_Id) ? 10 : 0  // 10 or 0
SevScore = case(Severity == "A", 5, "B", 3, 0) // 0-5
CritSitBonus = IsCritSit ? 10 : 0              // 10 or 0

TotalRiskScore = Sum of above (Max: ~131)
```

## Risk Level Thresholds

```
Critical: DaysOpen > 90 (overrides score)
High:     RiskScore >= 60
Medium:   RiskScore >= 40
Low:      RiskScore < 40
```

## Common Filters

### Filter by Specific Customer
```kql
| where TopParentName == "Ford"
```

### Filter by Risk Level
```kql
| where RiskLevel in ("Critical", "High")
```

### Filter by Age Range
```kql
| where DaysOpen between (90 .. 180)
```

### Cases with Active ICMs
```kql
| where isnotempty(RelatedICM_Id)
| extend ICMList = split(RelatedICM_Id, ",")
| mv-expand ICMId = ICMList to typeof(long)
| join kind=inner (
    cluster('icmcluster').database('IcmDataWarehouse').Incidents
    | where Status == "ACTIVE"
) on $left.ICMId == $right.IncidentId
```

## Refresh Schedule

### Auto-Refresh
- Dashboard: Every 15 minutes
- Query cache: 10 minutes
- Data source: Real-time (no delay)

### Manual Refresh
- Click refresh button (top-right)
- Keyboard: Ctrl+R (Win) / Cmd+R (Mac)
- URL parameter: `&refresh=true`

## Sharing & Permissions

### Share Dashboard
```
URL: https://dataexplorer.azure.com/dashboards/<id>
Parameters: ?p-MinAge=20&p-CustomerFilter=Ford
```

### Required Permissions
- **Viewer**: Reader on both clusters + Dashboard Reader
- **Editor**: Contributor on clusters + Dashboard Contributor

### Export Options
1. **Excel**: Right-click table → Export to Excel
2. **PDF**: Dashboard menu → Export → PDF
3. **Image**: Dashboard menu → Export → PNG
4. **JSON**: Dashboard menu → Export → Dashboard JSON

## Troubleshooting

### No Data Displayed
```powershell
# Test cluster connection
Test-NetConnection cxedataplatformcluster.westus2.kusto.windows.net -Port 443

# Verify in Azure Data Explorer web UI
# Run query manually with larger time range
```

### Query Timeout
```kql
// Add to start of query
set notruncation;
set query_take_max_records = 10000;

// Or add at end
| take 1000
```

### Authentication Issues
```powershell
# Clear Kusto cache
Remove-Item $env:LOCALAPPDATA\Kusto.Explorer\* -Recurse -Force

# Re-login to Azure
az login
az account show
```

## Performance Tips

1. **Use smaller time windows**: 30-60 days for daily use
2. **Apply filters early**: Filter by customer before calculations
3. **Limit join operations**: Only join when necessary
4. **Use summarize**: Aggregate before expanding
5. **Enable caching**: Dashboard settings → Cache results

## Color Scheme

### Risk Levels
- Critical: `#FFC7CE` (background), `#9C0006` (text)
- High: `#FFF2CC` (background), `#9C6500` (text)
- Medium: `#C6EFCE` (background), `#006100` (text)
- Low: `#F0F0F0` (background), `#3F3F76` (text)

### ICM Status
- ACTIVE: `#f57c00` (orange, bold)
- MITIGATED: Default
- RESOLVED: Default (dim)
- UNASSIGNED: `#FFC7CE` (red background)

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Refresh dashboard | Ctrl+R |
| Edit query | Ctrl+E |
| Save dashboard | Ctrl+S |
| Open filter panel | Ctrl+F |
| Export to Excel | Ctrl+Shift+E |
| Full screen | F11 |
| Help | F1 |

## API Access

### Dashboard API (Future)
```powershell
# Get dashboard definition
Invoke-RestMethod -Uri "https://api.dataexplorer.azure.com/v1/dashboards/<id>" `
  -Headers @{Authorization="Bearer $token"}

# Update tile query
Invoke-RestMethod -Uri "https://api.dataexplorer.azure.com/v1/dashboards/<id>/tiles/<tile-id>" `
  -Method PUT -Body $query -Headers @{Authorization="Bearer $token"}
```

## Next Steps

1. ☐ Import dashboard JSON
2. ☐ Test all tiles
3. ☐ Share URL with team
4. ☐ Set up Teams notifications
5. ☐ Create weekly snapshot
6. ☐ Document customizations

## Support

- **Dashboard Issues**: Check DEPLOYMENT_GUIDE.md
- **Query Errors**: Test in Azure Data Explorer web UI
- **Access Problems**: Verify cluster permissions
- **Performance**: Review Performance Tips section above
