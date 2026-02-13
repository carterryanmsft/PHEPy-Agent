# IC/MCS Risk Dashboard for Azure Data Explorer

This folder contains everything needed to deploy an interactive, real-time risk monitoring dashboard in Azure Data Explorer for IC and MCS customer cases.

## 📁 What's Inside

```
dashboard/
├── IC_Risk_Dashboard.json          # Complete dashboard definition (import this!)
├── DEPLOYMENT_GUIDE.md             # Step-by-step setup instructions
├── QUICK_REFERENCE.md              # Cheat sheet for common tasks
├── README.md                       # This file
└── queries/                        # 14 KQL query files
    ├── dashboard_summary.kql       
    ├── dashboard_critical_count.kql
    ├── dashboard_high_count.kql
    ├── dashboard_avg_risk.kql
    ├── dashboard_avg_age.kql
    ├── dashboard_risk_distribution.kql
    ├── dashboard_age_distribution.kql
    ├── dashboard_top_customers.kql
    ├── dashboard_icm_status.kql
    ├── dashboard_risk_trend.kql
    ├── dashboard_unassigned_icms.kql
    ├── dashboard_bugs_count.kql
    ├── dashboard_critical_cases.kql
    └── dashboard_all_cases.kql
```

## ⚡ Quick Start (5 Minutes)

1. **Navigate to Azure Data Explorer Dashboards**
   ```
   https://dataexplorer.azure.com/dashboards
   ```

2. **Import Dashboard**
   - Click "+ New dashboard"
   - Click "Import" → "From file"
   - Select `IC_Risk_Dashboard.json`

3. **Update Subscription ID**
   - Find `YOUR_SUBSCRIPTION_ID` in the JSON
   - Replace with your Azure subscription GUID

4. **Save & View**
   - Click "Apply changes"
   - Dashboard loads with all 14 tiles
   - Auto-refreshes every 15 minutes

**That's it!** 🎉

## 📊 Dashboard Features

### Visual Components

- **5 KPI Cards**: Critical count, high count, avg risk, avg age, summary stats
- **4 Charts**: Risk distribution (pie), age distribution (column), top customers (bar), risk trend (line)
- **3 ICM Tiles**: Status breakdown (donut), unassigned count (card), bugs count (card)
- **2 Data Tables**: Critical cases (90+ days), all cases with risk levels

### Interactive Features

- **Time Range Filter**: Default 180 days, customizable
- **Customer Filter**: Multi-select dropdown for specific customers
- **Risk Level Filter**: Filter by Critical/High/Medium/Low
- **Click-Through**: Case IDs link directly to OneSupport
- **Auto-Refresh**: Configurable interval (5/15/30/60 minutes)
- **Export**: Excel, PDF, PNG export options

### Intelligence

- **Risk Scoring**: 7-factor algorithm (age, ownership, transfers, idle, reopens, ICM, severity)
- **Critical Threshold**: Automatic Critical flag for 90+ day cases
- **ICM Integration**: Cross-cluster queries to IcmDataWarehouse
- **Bug Tracking**: Linked bug detection and count
- **SCIM Filtering**: Excludes SCIM Escalation Management cases

## 🎯 Use Cases

### Daily Operations
- Monitor critical case count at a glance
- Identify unassigned active ICMs
- Track risk score trends
- Quick access to case details

### Weekly Reviews
- Review all critical cases table
- Analyze customer risk distribution
- Identify patterns in age distribution
- Export reports for stakeholders

### Strategic Planning
- Track risk trends over 30 days
- Compare customer risk scores
- Assess ICM status breakdown
- Monitor bug link coverage

## 🔧 Customization

### Add New Customer

Edit the `ICTenants` datatable in query files:

```kql
"New Customer", 123456, "tenant-guid-here", "cle@email", "phe@email", "IC",
```

### Adjust Risk Scoring

Modify age thresholds in query files:

```kql
| extend AgeScore = case(
    DaysOpen > 180, 56,  // ⬅️ Adjust these
    DaysOpen > 120, 49,
    DaysOpen > 90, 42,
    ...
)
```

### Change Colors

Update in dashboard JSON under `visualOptions`:

```json
"backgroundColor": "#FFC7CE",  // Red for critical
"fontColor": "#9C0006"
```

## 📖 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**: Complete setup instructions, troubleshooting, advanced config
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**: Cheat sheet for common tasks, shortcuts, formulas
- **Query Files**: Each `.kql` file has inline comments explaining logic

## 🔐 Permissions Required

**To View Dashboard:**
- Reader on `cxedataplatformcluster.westus2.kusto.windows.net`
- Reader on `icmcluster.kusto.windows.net`
- Dashboard Reader role

**To Edit Dashboard:**
- Contributor on both clusters
- Dashboard Contributor role

## 🚨 Important Notes

1. **Subscription ID**: Must be updated in JSON before import
2. **Cluster Access**: Requires permissions on both CXE and ICM clusters
3. **SCIM Filtering**: Built into queries (excludes SCIM Escalation Management)
4. **Data Freshness**: Real-time queries, no delay (aside from auto-refresh)
5. **Performance**: Queries optimized for 180-day window (adjust for faster response)

## 🆚 Dashboard vs HTML Report

| Feature | Dashboard | HTML Report |
|---------|-----------|-------------|
| **Data Freshness** | Real-time | Manual refresh |
| **Interactivity** | Full filtering | Static |
| **Accessibility** | Browser + mobile | Email attachment |
| **Updates** | Auto (15 min) | Regenerate manually |
| **Sharing** | URL with params | Send file |
| **Drill-down** | Click-through | N/A |
| **Export** | Excel/PDF/PNG | HTML only |
| **Maintenance** | Edit queries | Regenerate Python |

**Recommendation**: Use dashboard for daily monitoring, HTML for weekly email reports.

## 🐛 Troubleshooting

### "No data" in tiles
✅ Check cluster permissions  
✅ Verify time range includes data  
✅ Test query in Azure Data Explorer web UI

### "Authentication failed"
✅ Re-login to Azure Portal  
✅ Verify Azure AD group membership  
✅ Check both cluster connections

### Slow performance
✅ Reduce time range (try 30-60 days)  
✅ Enable query result caching  
✅ Apply customer filter

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for detailed troubleshooting.

## 🔄 Maintenance

### Weekly
- Review critical cases table
- Check for unassigned ICMs
- Export snapshot for records

### Monthly
- Review risk trend chart
- Update customer tenant list if needed
- Adjust risk scoring if patterns change

### As Needed
- Add new customers to queries
- Modify filters/parameters
- Update color schemes
- Create custom alerts

## 📞 Support

**Questions about:**
- Dashboard setup → See DEPLOYMENT_GUIDE.md
- Query syntax → See QUICK_REFERENCE.md
- Cluster access → Contact CXE Care team
- Risk scoring → Review HTML report generator comments

## 🚀 Next Steps

1. ✅ Import `IC_Risk_Dashboard.json`
2. ✅ Update subscription ID
3. ✅ Test all tiles load correctly
4. ✅ Share dashboard URL with team
5. ✅ Set up weekly critical case review
6. ✅ (Optional) Configure Teams notifications
7. ✅ (Optional) Create Power BI integration

## 📝 Version History

**v1.0** (February 2026)
- Initial release
- 14 tiles (cards, charts, tables)
- 4 interactive parameters
- Cross-cluster ICM integration
- Bug tracking support
- 90-day critical threshold
- SCIM filtering built-in

---

**Dashboard URL**: `https://dataexplorer.azure.com/dashboards/<id>`  
**Created**: February 10, 2026  
**Maintained by**: PHE/CLE Program Team  
**Source**: [risk_reports/dashboard/](.)
