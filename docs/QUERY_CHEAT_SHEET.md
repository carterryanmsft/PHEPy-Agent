# PHEPy Query Cheat Sheet

**Purpose**: Quick reference for common queries - copy, customize, execute!

**Clusters**:
- **Cases**: `cxedataplatformcluster.westus2.kusto.windows.net/cxedata`
- **ICMs**: `icmcluster.kusto.windows.net/IcmDataWarehouse`

---

## 🚀 Quick Queries (Copy & Paste)

### 1. Customer Case Count
```kusto
// Replace: {TENANT_ID} with customer's TenantId
GetSCIMIncidentV2
| where TenantId == "{TENANT_ID}"
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| summarize TotalOpenCases = count()
```

**Example** (Ford):
```kusto
GetSCIMIncidentV2
| where TenantId == "c990bb7a-51f4-439b-bd36-9c07fb1041c0"
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| summarize TotalOpenCases = count()
```

---

### 2. Customer Case Details
```kusto
// Replace: {TENANT_ID}
GetSCIMIncidentV2
| where TenantId == "{TENANT_ID}"
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| extend DaysOpen = todouble(CaseAge)
| project 
    ServiceRequestNumber,
    ServiceRequestState,
    ServiceRequestStatus,
    ProductName,
    DaysOpen,
    ServiceRequestCurrentSeverity,
    CreatedTime,
    RelatedICM_Id
| order by DaysOpen desc
```

---

### 3. All IC/MCS Customers - Case Summary
```kusto
let ICMCSTenants = datatable(TopParentName:string, TenantId:string, PHE:string)
[
    "Ford", "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "Ron Mustard",
    "Amazon", "5280104a-472d-4538-9ccf-1e1d0efe8b1b", "Kanika Kapoor",
    "Walmart", "3cbcc3d3-094d-4006-9849-0d11d61f484d", "Tim Griffin",
    "Huntington", "157a26ef-912f-4244-abef-b45fc4bd77f9", "Hemanth Varyani"
    // Add more customers as needed
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| join kind=inner ICMCSTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| summarize 
    TotalCases = count(),
    AvgAge = avg(DaysOpen),
    OldestCase = max(DaysOpen)
    by TopParentName, PHE
| order by TotalCases desc
```

---

### 4. Active ICMs for Customer (by Case IDs)
```kusto
// Step 1: Get case ICM IDs first, then use those here
// Replace: {ICM_ID_LIST} with actual IDs like (51000000865253, 693849812)
Incidents
| where IncidentId in ({ICM_ID_LIST})
| where Status in ("Active", "Mitigating", "Assigned")
| where Title !contains "ESCALATION"
| where Title !contains "CSSCSI"
| extend DaysOpen = datetime_diff('day', now(), CreateDate)
| summarize by IncidentId, Title, Severity, Status, CreateDate, DaysOpen, OwningTeamName, SupportTicketId
| order by DaysOpen desc
```

**Example** (Ford ICMs):
```kusto
Incidents
| where IncidentId in (51000000865253, 693849812, 693543577, 693952482, 694253124)
| where Status == "ACTIVE"
| where Title !contains "ESCALATION"
| where Title !contains "CSSCSI"
| extend DaysOpen = datetime_diff('day', now(), CreateDate)
| summarize by IncidentId, Title, Severity, CreateDate, DaysOpen, OwningTeamName, SupportTicketId
| order by DaysOpen desc
```

---

### 5. At-Risk Cases (>60 Days Old)
```kusto
// Replace: {TENANT_ID}
GetSCIMIncidentV2
| where TenantId == "{TENANT_ID}"
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen > 60
| extend RiskCategory = case(
    DaysOpen > 180, "Critical (>180 days)",
    DaysOpen > 120, "Very High (>120 days)",
    DaysOpen > 90, "High (>90 days)",
    "Medium (60-90 days)")
| project 
    ServiceRequestNumber,
    DaysOpen,
    RiskCategory,
    ServiceRequestStatus,
    ProductName,
    ServiceRequestCurrentSeverity
| order by DaysOpen desc
```

---

### 6. Cases with ICM Breakdown
```kusto
// Replace: {TENANT_ID}
GetSCIMIncidentV2
| where TenantId == "{TENANT_ID}"
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| extend DaysOpen = todouble(CaseAge)
| extend HasICM = isnotempty(RelatedICM_Id)
| summarize 
    TotalCases = count(),
    CasesWithICM = countif(HasICM),
    CasesWithoutICM = countif(not(HasICM)),
    AvgDaysOpen = avg(DaysOpen),
    OldestCase = max(DaysOpen)
```

---

### 7. Top Purview Teams by ICM Count
```kusto
Incidents
| where CreateDate >= ago(90d)
| where OwningTenantName == "Purview"
| where Status in ("Active", "Mitigating")
| where Title !contains "ESCALATION"
| where Title !contains "CSSCSI"
| extend DaysOpen = datetime_diff('day', now(), CreateDate)
| summarize 
    ICMCount = dcount(IncidentId),
    AvgAge = avg(DaysOpen)
    by OwningTeamName
| order by ICMCount desc
| take 20
```

---

### 8. Cases by Product Area
```kusto
// Replace: {TENANT_ID}
GetSCIMIncidentV2
| where TenantId == "{TENANT_ID}"
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| extend DaysOpen = todouble(CaseAge)
| summarize 
    Cases = count(),
    AvgAge = avg(DaysOpen)
    by ProductName
| order by Cases desc
```

---

### 9. Weekly Case Trend
```kusto
// Replace: {TENANT_ID}
GetSCIMIncidentV2
| where TenantId == "{TENANT_ID}"
| where CreatedTime >= ago(90d)
| where ProductName contains "Purview"
| summarize Cases = count() by Week = startofweek(CreatedTime)
| order by Week asc
```

---

### 10. SLA at Risk (Status = "Waiting for product team")
```kusto
// Replace: {TENANT_ID}
GetSCIMIncidentV2
| where TenantId == "{TENANT_ID}"
| where ServiceRequestState != "Closed"
| where ServiceRequestStatus == "Waiting for product team"
| where ProductName contains "Purview"
| extend DaysOpen = todouble(CaseAge)
| project 
    ServiceRequestNumber,
    DaysOpen,
    ServiceRequestCurrentSeverity,
    ProductName,
    CreatedTime
| order by DaysOpen desc
```

---

## 🎯 Common Scenarios

### Scenario 1: "How many cases does Ford have?"

**Step 1**: Lookup TenantId
- Ford TenantId: `c990bb7a-51f4-439b-bd36-9c07fb1041c0`

**Step 2**: Run Query #1
```kusto
GetSCIMIncidentV2
| where TenantId == "c990bb7a-51f4-439b-bd36-9c07fb1041c0"
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| summarize TotalOpenCases = count()
```

---

### Scenario 2: "How many ICMs does Ford have?"

**Step 1**: Get case list with ICM IDs (Query #2)
```kusto
GetSCIMIncidentV2
| where TenantId == "c990bb7a-51f4-439b-bd36-9c07fb1041c0"
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| where isnotempty(RelatedICM_Id)
| project ServiceRequestNumber, RelatedICM_Id
```

**Step 2**: Extract ICM IDs from results (e.g., `51000000865253;693849812`)

**Step 3**: Run Query #4 with those IDs

---

### Scenario 3: "Which customers have the most cases?"

**Use Query #3** (All IC/MCS summary)

---

### Scenario 4: "What are Ford's oldest cases?"

**Use Query #2** (already sorted by DaysOpen desc)

---

## 📋 Quick Lookup: Customer TenantIds

| Customer | TenantId | Query Snippet |
|----------|----------|---------------|
| **Ford** | c990bb7a-51f4-439b-bd36-9c07fb1041c0 | `where TenantId == "c990bb7a-..."` |
| **Amazon** | 5280104a-472d-4538-9ccf-1e1d0efe8b1b | `where TenantId == "5280104a-..."` |
| **Walmart** | 3cbcc3d3-094d-4006-9849-0d11d61f484d | `where TenantId == "3cbcc3d3-..."` |
| **Huntington** | 157a26ef-912f-4244-abef-b45fc4bd77f9 | `where TenantId == "157a26ef-..."` |
| **State of WA** | 11d0e217-264e-400a-8ba0-57dcc127d72d | `where TenantId == "11d0e217-..."` |

**Full List**: See `grounding_docs/contacts_access/CUSTOMER_LOOKUP_GUIDE.md`

---

## 🔧 Filter Snippets

### Standard Filters (Apply to Most Queries):
```kusto
// Date range (last 90 days)
| where CreateDate >= ago(90d)

// Open cases only
| where ServiceRequestState != "Closed"

// Purview products
| where ProductName contains "Purview"

// Remove escalation ICMs
| where Title !contains "ESCALATION"
| where Title !contains "CSSCSI"

// Calculate days open
| extend DaysOpen = todouble(CaseAge)  // For cases
| extend DaysOpen = datetime_diff('day', now(), CreateDate)  // For ICMs
```

---

## 🚨 Troubleshooting

### Query Returns 0 Results?
1. ✅ Check TenantId is correct (no typos)
2. ✅ Check date range (may need to expand: `ago(180d)`)
3. ✅ Check product filter (try removing to see all products)
4. ✅ Verify customer actually has cases (run without filters)

### Query Too Slow?
1. ✅ Add date filter first: `where CreateDate >= ago(30d)`
2. ✅ Limit results: `| take 100`
3. ✅ Use indexed columns first (TenantId, CreateDate)

### Seeing Duplicate ICMs?
1. ✅ Use: `| summarize by IncidentId, ...`
2. ✅ Or: `| summarize UniqueICMs = dcount(IncidentId)`

---

## 📚 Related Resources

- **Query Patterns**: `sub_agents/support_case_manager/QUERY_PATTERNS.md`
- **Common Filters**: `sub_agents/kusto_expert/COMMON_FILTERS.md`
- **Customer Lookup**: `grounding_docs/contacts_access/CUSTOMER_LOOKUP_GUIDE.md`
- **Kusto Expert**: `sub_agents/kusto_expert/AGENT_INSTRUCTIONS.md`

---

**Pro Tip**: Save frequently used queries with your customer TenantIds for even faster execution!

---

**Last Updated**: February 4, 2026  
**Maintained By**: Jacques (Kusto Expert) + Support Case Manager
