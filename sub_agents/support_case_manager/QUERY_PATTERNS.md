# Support Case Manager - Query Patterns

**Purpose**: Standardized query patterns for efficient case retrieval and analysis  
**Updated**: February 11, 2026 - Added OAP integration patterns

---

## 🎯 Tool Selection Rules (Updated for OAP)

### When User Asks About Cases:
- **⭐ PRIMARY: Use OAP** (One Agentic Platform)
  - Natural language queries: "Show me P0 cases for Contoso"
  - Auto-enriched with customer context, sentiment, KB articles
  - Built-in PII controls & RBAC
  - Full lifecycle operations (create, update, close)
  - Multi-system aggregation (DFM + SCIM + ServiceNow)
  
- **📊 SECONDARY: Use Kusto MCP** (for analytics & trends)
  - When you need: aggregations, trends, historical analysis
  - `GetSCIMIncidentV2` via Kusto MCP (live data)
  - **Cluster**: `cxedataplatformcluster.westus2.kusto.windows.net`
  - **Database**: `cxedata`
  - **Default scope**: Last 30 days, open cases only
  
- **❌ NEVER use**: Static CSV/JSON files (outdated)
- **⚠️ FALLBACK: enterprise-mcp** (legacy SCIM-only access)

### When User Asks About ICMs:
- **✅ ALWAYS use**: ICM Kusto cluster (`icmcluster.kusto.windows.net`)
- **✅ ALWAYS filter out**:
  - Title contains "ESCALATION OF CASE"
  - Title contains "CSSCSI"
  - OwningTeamName contains "SCIMESCALATIONMANAGEMENT"
- **✅ Focus on**: Product teams (`PURVIEW\\*`, `EOP\\*`, `M365D\\*`)

### Decision Matrix: OAP vs Kusto

| User Need | Primary Tool | Why? |
|-----------|-------------|------|
| "Show cases for Customer X" | **OAP** | Enriched with customer context |
| "Get case #123 details" | **OAP** | Full interaction history + sentiment |
| "Case count by product area" | **Kusto** | Better for aggregations |
| "At-risk cases this week" | **OAP** | ML-based risk scoring |
| "Create new case" | **OAP** | Only tool that can write |
| "Historical trend (6 months)" | **Kusto** | Better for time-series analytics |
| "Link case to ICM" | **OAP** | Case lifecycle management |

---

## 🌟 OAP Query Patterns (Primary Method)

### OAP Pattern 1: Natural Language Case Retrieval
```python
# Natural language query to OAP
oap.query("Show me all P0 cases for Contoso in the last 30 days")

# Returns enriched response with:
# - Case details (number, status, SLA)
# - Customer context (tenant health, contract tier)
# - Sentiment analysis on interactions
# - Linked ICMs/bugs
# - Recommended KB articles
```

**Use When**: User asks in plain language about cases  
**Advantages**: Auto-enriched, contextual, PII-safe

---

### OAP Pattern 2: Structured Case Query
```python
# Structured query for programmatic access
oap.cases.search({
    "customer_tenant_id": "{TENANT_ID}",
    "product_area": "Purview",
    "status": ["Open", "InProgress"],
    "priority": ["P0", "P1"],
    "created_after": "2026-01-01",
    "include_context": True,
    "include_sentiment": True,
    "include_recommendations": True
})

# Response includes:
{
    "total_cases": 5,
    "cases": [
        {
            "case_id": "51000000877262",
            "status": "Open",
            "priority": "P0",
            "days_open": 3,
            "sla_breach_in_hours": 2.5,
            "customer_context": {
                "tenant_health": "Yellow",
                "contract_tier": "Premier",
                "previous_cases_count": 12,
                "avg_resolution_days": 5.2
            },
            "sentiment": {
                "current": "Frustrated",
                "trend": "Escalating"
            },
            "linked_items": {
                "icms": ["693849812"],
                "ado_bugs": ["3563451"]
            },
            "recommended_kb_articles": [
                "KB12345: Classification label not appearing",
                "KB67890: Auto-labeling troubleshooting"
            ]
        }
    ],
    "insights": "Pattern detected: 3 cases about classification labels in last week"
}
```

**Use When**: Need programmatic access or specific field filtering  
**Advantages**: Structured data, easy to parse, consistent format

---

### OAP Pattern 3: Customer Profile with Case Summary
```python
# Get comprehensive customer view
oap.customers.get_profile("{TENANT_ID}", include_cases=True)

# Returns:
{
    "tenant_id": "c990bb7a-51f4-439b-bd36-9c07fb1041c0",
    "customer_name": "Ford",
    "status": "Active",
    "contract": {
        "tier": "Enterprise",
        "products": ["Purview", "Defender", "Sentinel"],
        "expiration": "2027-06-30"
    },
    "health_score": 75,  // 0-100
    "support_metrics": {
        "total_cases_lifetime": 156,
        "open_cases": 5,
        "at_risk_cases": 1,
        "avg_resolution_days": 4.8,
        "customer_satisfaction": 4.2  // out of 5
    },
    "active_cases": [ /* case details */ ],
    "case_trends": {
        "this_month": 5,
        "last_month": 3,
        "trend": "Increasing"
    }
}
```

**Use When**: User asks "Tell me about Customer X" or needs holistic view  
**Advantages**: Contextual, shows patterns, proactive insights

---

### OAP Pattern 4: At-Risk Case Detection (ML-Powered)
```python
# OAP's ML models predict SLA breach risk
oap.cases.get_at_risk({
    "product_area": "Purview",
    "prediction_window_hours": 48,
    "min_risk_score": 70,  // 0-100
    "include_recommendations": True
})

# Returns cases with risk scoring:
{
    "at_risk_cases": [
        {
            "case_id": "51000000877262",
            "current_sla_hours_remaining": 6.5,
            "risk_score": 92,  // 0-100, higher = more risk
            "risk_factors": [
                "Case complexity high (7 escalations)",
                "Customer sentiment declining",
                "Similar case avg resolution: 8 days",
                "No engineer assignment after 2 days"
            ],
            "recommended_actions": [
                "Escalate to senior engineer immediately",
                "Apply KB12345 workaround",
                "Proactive customer communication"
            ],
            "predicted_breach_time": "2026-02-12T02:30:00Z"
        }
    ]
}
```

**Use When**: "Show me at-risk cases" or proactive monitoring  
**Advantages**: Predictive not reactive, actionable recommendations

---

### OAP Pattern 5: Create Case with Auto-Suggestions
```python
# Create new case with AI assistance
oap.cases.create({
    "customer_tenant_id": "{TENANT_ID}",
    "product": "Purview",
    "title": "Auto-classification not working",
    "description": "Customer reports auto-labeling stopped applying sensitivity labels",
    "priority": "P1",
    "reporter_email": "user@contoso.com",
    "auto_enrich": True  // OAP will add suggestions
})

# OAP auto-adds:
{
    "case_id": "NEW-51000000999999",
    "status": "Created",
    "auto_enrichments": {
        "similar_cases": ["510000008772", "510000008654"],
        "likely_issues": [
            "Exchange Online label sync delay",
            "Policy propagation timing"
        ],
        "suggested_kb_articles": ["KB12345", "KB67890"],
        "recommended_assignment": {
            "team": "Purview\\SensitivityLabels",
            "engineer": "John Smith (expert in auto-labeling)"
        },
        "estimated_resolution_days": 3.2
    },
    "linked_automatically": {
        "related_icms": ["693849812"],
        "related_bugs": ["3563451"]
    }
}
```

**Use When**: Creating new cases, need intelligent routing  
**Advantages**: Auto-linking, smart assignment, faster resolution

---

### OAP Pattern 6: Link Case to ICM/Bug
```python
# Bidirectional linking
oap.cases.link({
    "case_id": "51000000877262",
    "link_type": "related_to",
    "target_type": "icm",
    "target_id": "693849812",
    "relationship": "Case waiting on ICM resolution",
    "auto_sync_status": True  // Sync ICM status to case
})

# Also works for ADO bugs
oap.cases.link({
    "case_id": "51000000877262",
    "link_type": "blocked_by",
    "target_type": "ado_bug",
    "target_id": "3563451",
    "auto_update_case": True  // Update case when bug is fixed
})
```

**Use When**: Coordinating case with engineering work  
**Advantages**: Auto-sync, bidirectional, unified tracking

---

## 🔍 Standard Kusto Query Patterns (Secondary - Analytics)

> **Note**: Use Kusto for aggregations and historical trends. Use OAP for individual case operations.

---

## 📋 Customer Lookup Priority

### Order of Operations:
1. **TenantId** (most reliable) - Use for all queries
2. **TopParentName** (exact match) - Use for display/reporting
3. **CustomerName** (avoid) - Inconsistent, multiple variations

### Lookup Process:
```
User asks about "Ford"
↓
1. Read: grounding_docs/contacts_access/IC and MCS 2.4.csv
2. Find: TopParentName == "Ford"
3. Extract: TenantId = "c990bb7a-51f4-439b-bd36-9c07fb1041c0"
4. Query with: | where TenantId == "c990bb7a-51f4-439b-bd36-9c07fb1041c0"
```

---

## 🔍 Standard Query Patterns

### Pattern 1: Customer Active Cases (Simple Count)
```kusto
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview" or SAPPath contains "Purview"
| where TenantId == "{TENANT_ID}"
| summarize TotalOpenCases = count()
```

**Use When**: User asks "How many cases does [Customer] have?"

---

### Pattern 2: Customer Cases with Details
```kusto
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview" or SAPPath contains "Purview"
| where TenantId == "{TENANT_ID}"
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

**Use When**: User wants case details, status, or aging information

---

### Pattern 3: Cases with ICM Information
```kusto
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| where TenantId == "{TENANT_ID}"
| extend DaysOpen = todouble(CaseAge)
| extend HasICM = isnotempty(RelatedICM_Id)
| summarize 
    TotalCases = count(),
    CasesWithICM = countif(HasICM),
    AvgDaysOpen = avg(DaysOpen),
    OldestCase = max(DaysOpen),
    ICMList = make_set_if(RelatedICM_Id, HasICM)
| extend ICMCount = array_length(ICMList)
```

**Use When**: User asks about ICMs related to cases

---

### Pattern 4: At-Risk Cases (Aging Analysis)
```kusto
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| where TenantId == "{TENANT_ID}"
| extend DaysOpen = todouble(CaseAge)
| extend RiskCategory = case(
    DaysOpen > 180, "Critical (>180 days)",
    DaysOpen > 120, "Very High (>120 days)",
    DaysOpen > 90, "High (>90 days)",
    DaysOpen > 60, "Medium (>60 days)",
    "Normal (<60 days)")
| where DaysOpen > 60  // Focus on at-risk only
| project 
    ServiceRequestNumber,
    DaysOpen,
    RiskCategory,
    ServiceRequestStatus,
    ProductName,
    RelatedICM_Id
| order by DaysOpen desc
```

**Use When**: User asks about "aging cases", "at-risk cases", or "old cases"

---

### Pattern 5: Multi-Tenant Query (All IC/MCS Customers)
```kusto
let ICMCSTenants = datatable(TopParentName:string, TenantId:string, PHE:string, Program:string)
[
    "Ford", "c990bb7a-51f4-439b-bd36-9c07fb1041c0", "Ron Mustard", "IC",
    "Amazon", "5280104a-472d-4538-9ccf-1e1d0efe8b1b", "Kanika Kapoor", "MCS",
    // ... (include all from IC and MCS 2.4.csv)
];
GetSCIMIncidentV2
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| join kind=inner ICMCSTenants on TenantId
| extend DaysOpen = todouble(CaseAge)
| summarize CaseCount = count() by TopParentName, PHE, Program
| order by CaseCount desc
```

**Use When**: User asks for "all IC/MCS cases" or comparative analysis

---

## 🎯 ICM Query Patterns

### Pattern 6: Get ICMs for Specific Cases
```kusto
// Step 1: Extract ICM IDs from cases (semicolon-separated)
// Step 2: Query ICM cluster with those IDs

Incidents
| where IncidentId in ({ICM_ID_LIST})  // e.g., (51000000865253, 693849812)
| where Status in ("Active", "Mitigating", "Assigned")
| where Title !contains "ESCALATION OF CASE"  // Filter noise
| where Title !contains "CSSCSI"
| where OwningTeamName !contains "SCIMESCALATIONMANAGEMENT"
| extend DaysOpen = datetime_diff('day', now(), CreateDate)
| summarize by IncidentId, Title, Severity, Status, CreateDate, DaysOpen, OwningTeamName, SupportTicketId
| order by DaysOpen desc
```

**Use When**: User asks "How many ICMs does [Customer] have?"

---

### Pattern 7: ICM Count Summary
```kusto
Incidents
| where IncidentId in ({ICM_ID_LIST})
| where Status == "ACTIVE"
| where Title !contains "ESCALATION"
| where Title !contains "CSSCSI"
| summarize 
    UniqueICMs = dcount(IncidentId),
    TotalRecords = count(),
    Statuses = make_set(Status)
```

**Use When**: Quick count needed without details

---

## 🚫 Common Mistakes to Avoid

### ❌ DON'T:
1. Search by `CustomerName` (inconsistent: "Ford", "FORD MOTOR COMPANY", "Azureford")
2. Use static CSV files for live case counts
3. Include escalation tracking ICMs in product issue counts
4. Query without date filters (performance issues)
5. Use `TopParentName` in Kusto joins (use `TenantId`)

### ✅ DO:
1. Always use `TenantId` for queries
2. Filter out escalation tracking ICMs
3. Include `DaysOpen` calculation for aging analysis
4. Use `summarize by` to deduplicate ICM status history
5. Check `RelatedICM_Id` field for ICM associations

---

## 📊 Response Templates

### Template 1: Case Count Response
```
[Customer] has [X] open Purview cases

📊 Summary:
- Total Cases: [X]
- Average Age: [X] days
- Oldest Case: [X] days (Case #[ID])
- Cases with ICMs: [X]

[Customer] Contact:
- CLE: [Name]
- PHE: [Name]
- TPID: [ID]
```

### Template 2: ICM Count Response
```
[Customer] has [X] active ICMs

📊 Active ICM Summary:
1. ICM [ID] - [Title] | [X] days | Sev [X]
2. ICM [ID] - [Title] | [X] days | Sev [X]

(Excludes escalation tracking ICMs)
```

---

## 🔄 Workflow Summary

```
User Query → Identify Customer → Lookup TenantId → Select Pattern → Execute Query → Format Response
     ↓              ↓                 ↓                  ↓              ↓              ↓
"Ford cases"   Read CSV      Extract ID       Pattern 2      Kusto MCP      Template 1
```

---

## 🔄 OAP + Kusto Workflow (Best Practice)

```
User Request: "Show me cases for Contoso"
     ↓
Step 1: Get Customer Context (OAP)
     ↓ oap.customers.get_profile()
Customer Profile + Active Cases
     ↓
Step 2: Enrich with Historical Trends (Kusto)
     ↓ Kusto: GetSCIMIncidentV2 | summarize by month
6-month case volume trend
     ↓
Step 3: Combine & Present
     ↓
"Contoso has 5 open cases (up from avg 3/month).
 2 are at SLA risk. Customer sentiment: Frustrated.
 Recommend: Proactive engagement."
```

### Hybrid Query Example
```python
# Step 1: Get current state from OAP (fast, enriched)
current_cases = oap.cases.search({
    "customer_tenant_id": tenant_id,
    "status": ["Open", "InProgress"]
})

# Step 2: Get historical trends from Kusto (analytics)
historical_trend = kusto.query("""
    GetSCIMIncidentV2
    | where TenantId == '{tenant_id}'
    | where ProductName contains 'Purview'
    | summarize Cases = count() by bin(CreatedTime, 30d)
    | order by CreatedTime desc
""")

# Step 3: Combine for comprehensive view
response = {
    "current_state": current_cases,
    "historical_trend": historical_trend,
    "insights": oap.analyze_trend(current_cases, historical_trend)
}
```

---

## 🚦 Quick Decision Tree

```
User asks about cases?
├─ Need to CREATE/UPDATE/CLOSE case?
│  └─ Use OAP ✅ (only tool that can write)
│
├─ Need INDIVIDUAL case details?
│  └─ Use OAP ✅ (enriched with context + sentiment)
│
├─ Need AGGREGATION or TREND?
│  └─ Use Kusto 📊 (better for analytics)
│
├─ Need CUSTOMER CONTEXT?
│  └─ Use OAP ✅ (profile, health, contracts)
│
├─ Need ML PREDICTIONS (at-risk)?
│  └─ Use OAP ✅ (ML-powered risk scoring)
│
└─ Need CROSS-SYSTEM data (DFM+SCIM+ServiceNow)?
   └─ Use OAP ✅ (multi-system aggregation)
```

---

## 📊 Response Templates (Updated for OAP)

### Template 1: Case Count Response (OAP-Enhanced)
```
[Customer] has [X] open Purview cases

📊 Current Status (via OAP):
- Total Open: [X]
- At SLA Risk: [X] (OAP ML risk score > 70)
- Average Age: [X] days
- Oldest Case: [X] days (Case #[ID])
- Cases with ICMs: [X]
- Customer Sentiment: [Positive/Neutral/Frustrated]

📈 Trend (via Kusto):
- This month: [X] cases
- Last month: [Y] cases
- Trend: [Increasing/Stable/Decreasing]

🎯 OAP Recommendations:
- [Recommendation 1]
- [Recommendation 2]

[Customer] Contact:
- CLE: [Name]
- PHE: [Name]
- TPID: [ID]
```

---

## 🔄 Workflow Summary (Updated)

```
User Query → Customer Lookup → Choose Tool → Execute → Enrich → Format Response
     ↓            ↓                ↓            ↓         ↓           ↓
"Ford cases"  TenantId      OAP (primary)  Get cases  + Context  Template 1
                           + Kusto (trend)  + Trends   + Sentiment
```

---

## 🆕 OAP Migration Notes

### What Changed:
- **Was**: enterprise-mcp only (limited SCIM access)
- **Now**: OAP primary + Kusto analytics + enterprise-mcp fallback
- **Why**: OAP provides customer context, ML predictions, full lifecycle, multi-system

### Backward Compatibility:
- Keep enterprise-mcp in mcp.json as fallback
- Existing Kusto queries still work (use for analytics)
- Migration is additive (not breaking)

### Performance:
- **OAP**: ~500ms for enriched case query
- **Kusto**: ~2-5s for aggregations
- **enterprise-mcp**: ~1-2s for basic case retrieval

---

**Last Updated**: February 11, 2026  
**Version**: 2.0 (OAP Integration)  
**Maintained By**: Support Case Manager Sub-Agent
