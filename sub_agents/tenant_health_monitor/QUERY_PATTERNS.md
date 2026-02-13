# Tenant Health Monitor - Query Patterns

**Agent:** Tenant Health Monitor  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 🔍 Kusto Query Patterns

### 1. Active Users by Tenant

```kusto
// Get active users count per tenant (last 7 days)
let lookbackDays = 7;
PurviewActivityLogs
| where Timestamp >= ago(lookbackDays * 1d)
| where TenantId == "<tenant-id>"
| where ActivityType in ("LabelApplied", "DLPPolicyEvaluated", "ContentSearched")
| summarize ActiveUsers = dcount(UserId) by TenantId
| extend Timestamp = now()
```

**Usage:** Component of Adoption Score  
**Update Frequency:** Daily

---

### 2. Feature Adoption Rate

```kusto
// Calculate feature adoption percentage
let tenantId = "<tenant-id>";
// Get enabled features
let enabledFeatures = PurviewTenantConfig
| where TenantId == tenantId
| summarize EnabledCount = countif(FeatureEnabled == true);
// Get actively used features (last 30 days)
let activeFeatures = PurviewActivityLogs
| where TenantId == tenantId
| where Timestamp >= ago(30d)
| summarize by FeatureName
| count;
// Calculate adoption rate
enabledFeatures
| extend ActiveFeatures = toscalar(activeFeatures)
| extend AdoptionRate = (ActiveFeatures * 100.0) / EnabledCount
```

**Usage:** Component of Adoption Score  
**Update Frequency:** Weekly

---

### 3. Support Case Volume

```kusto
// Get open case count per tenant
GetSCIMIncidentV2
| where TenantId == "<tenant-id>"
| where Status in ("Active", "Investigation", "CustomerActionRequired")
| summarize OpenCases = count() by TenantId, Priority
| order by Priority asc
```

**Usage:** Component of Support Score  
**Update Frequency:** Real-time

---

### 4. SLA Compliance Rate

```kusto
// Calculate SLA compliance for resolved cases (last 30 days)
let tenantId = "<tenant-id>";
GetSCIMIncidentV2
| where TenantId == tenantId
| where ClosedDate >= ago(30d)
| extend SLAMet = ResolutionTime <= SLAThreshold
| summarize 
    TotalCases = count(),
    SLAMetCases = countif(SLAMet == true)
| extend SLAComplianceRate = (SLAMetCases * 100.0) / TotalCases
```

**Usage:** Component of Support Score  
**Update Frequency:** Daily

---

### 5. Error Rate

```kusto
// Calculate error rate per 1000 operations (last 24 hours)
let tenantId = "<tenant-id>";
PurviewTelemetry
| where TenantId == tenantId
| where Timestamp >= ago(1d)
| summarize 
    TotalOperations = count(),
    ErrorOperations = countif(ResultCode >= 400)
| extend ErrorRate = (ErrorOperations * 1000.0) / TotalOperations
```

**Usage:** Component of Performance Score  
**Update Frequency:** Hourly

---

### 6. Search Performance

```kusto
// Average eDiscovery search duration (last 7 days)
let tenantId = "<tenant-id>";
eDiscoveryTelemetry
| where TenantId == tenantId
| where Timestamp >= ago(7d)
| where OperationType == "ContentSearch"
| summarize 
    AvgDuration = avg(DurationMs),
    P50Duration = percentile(DurationMs, 50),
    P95Duration = percentile(DurationMs, 95)
by TenantId
```

**Usage:** Component of Performance Score  
**Update Frequency:** Hourly

---

### 7. Admin Activity

```kusto
// Count admin console activities (last 30 days)
let tenantId = "<tenant-id>";
PurviewAuditLogs
| where TenantId == tenantId
| where Timestamp >= ago(30d)
| where UserRole == "Admin"
| where ActivityType in ("PolicyCreated", "PolicyModified", "LabelCreated", "ConfigChanged")
| summarize AdminActivities = count() by TenantId
```

**Usage:** Component of Engagement Score  
**Update Frequency:** Daily

---

### 8. Health Score Trend (Historical)

```kusto
// Get weekly health scores for last 90 days
let tenantId = "<tenant-id>";
TenantHealthScores
| where TenantId == tenantId
| where Timestamp >= ago(90d)
| summarize HealthScore = avg(OverallScore) by bin(Timestamp, 7d), TenantId
| order by Timestamp asc
| extend PreviousScore = prev(HealthScore, 1)
| extend ScoreChange = HealthScore - PreviousScore
| extend TrendDirection = case(
    ScoreChange > 5, "Improving",
    ScoreChange < -5, "Declining",
    "Stable"
)
```

**Usage:** Trend analysis  
**Update Frequency:** Daily

---

### 9. Cohort Aggregate Statistics

```kusto
// Get health score distribution for cohort
let cohortTenants = dynamic(["tenant-1", "tenant-2", "tenant-3"]);
TenantHealthScores
| where Timestamp >= startofday(now())
| where TenantId in (cohortTenants)
| summarize 
    AvgScore = avg(OverallScore),
    MinScore = min(OverallScore),
    MaxScore = max(OverallScore),
    MedianScore = percentile(OverallScore, 50),
    StdDev = stdev(OverallScore),
    TenantCount = dcount(TenantId)
| extend 
    LowerOutlier = AvgScore - (2 * StdDev),
    UpperOutlier = AvgScore + (2 * StdDev)
```

**Usage:** Cohort health analysis  
**Update Frequency:** Daily

---

### 10. At-Risk Case Detection

```kusto
// Find cases with SLA breach risk (<4 hours remaining)
let threshold = 4h;
GetSCIMIncidentV2
| where Status in ("Active", "Investigation")
| where TenantId != ""
| extend TimeToSLA = SLADeadline - now()
| where TimeToSLA <= threshold
| project TenantId, CaseNumber, Title, Priority, TimeToSLA, SLADeadline
| order by TimeToSLA asc
```

**Usage:** SLA risk alerting  
**Update Frequency:** Real-time

---

## 📊 MCP Tool Usage

### Enterprise MCP (Support Cases)

```typescript
// Get case count by tenant
mcp_enterprise_get_cases({
  tenantId: "c990bb7a-51f4-439b-bd36-9c07fb1041c0",
  status: ["Active", "Investigation"],
  includeMetrics: true
})
```

**Returns:** Case count, SLA status, priority distribution

---

### Kusto MCP (Telemetry & Metrics)

```typescript
// Execute health metric query
mcp_kusto_execute_query({
  clusterUrl: "https://cxe-analytics.kusto.windows.net",
  database: "CustomerHealth",
  query: "<kusto-query-from-above>",
  maxRows: 1000
})
```

**Returns:** Query results with metrics

---

### ICM MCP (Incidents)

```typescript
// Get active incidents by tenant
mcp_icm_get_incidents({
  tenantId: "c990bb7a-51f4-439b-bd36-9c07fb1041c0",
  status: "Active",
  severity: ["Sev0", "Sev1", "Sev2"]
})
```

**Returns:** Incident count and details

---

## 🎯 Query Optimization Tips

### 1. Use Time Filters First
```kusto
// ✅ Good: Filter by time first (indexed column)
| where Timestamp >= ago(7d)
| where TenantId == "..."

// ❌ Bad: Filter by TenantId before time
| where TenantId == "..."
| where Timestamp >= ago(7d)
```

### 2. Limit Result Sets
```kusto
// Always include top N or summarize to limit results
| summarize ... by TenantId
// OR
| top 100 by Timestamp desc
```

### 3. Cache Common Queries
- Store daily/weekly aggregates in summary tables
- Use materialized views for expensive calculations
- Cache health scores in dedicated table

### 4. Parallel Execution
- For cohort analysis, query multiple tenants in parallel
- Use dynamic batching for large cohorts

---

## 🔗 Data Source Reference

| Data Source | Cluster/Endpoint | Database | Refresh Frequency |
|-------------|------------------|----------|-------------------|
| Purview Telemetry | cxe-analytics.kusto.windows.net | CustomerHealth | Real-time |
| Support Cases | Enterprise MCP | GetSCIMIncidentV2 | Real-time |
| ICM Incidents | ICM MCP | - | Real-time |
| Tenant Config | Purview APIs | - | Daily |
| Activity Logs | cxe-analytics.kusto.windows.net | AuditLogs | 1-hour delay |
| Content Explorer | Purview Portal | - | 24-48h delay |

---

## 📝 Query Library Maintenance

**Add new queries here when:**
- New metric is added to health score
- New data source becomes available
- Query optimization improves performance
- New alert condition is defined

**Update existing queries when:**
- Table schema changes
- Cluster endpoint changes
- Performance issues identified
- More accurate calculation method found
