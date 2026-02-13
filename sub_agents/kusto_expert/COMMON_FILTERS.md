# Kusto Expert - Common Filters Library

**Purpose**: Reusable filter patterns to apply consistently across all queries

---

## 🎯 Standard Filters (Apply by Default)

### ICM Noise Filters

**Purpose**: Remove non-product ICMs (escalation tracking, auto-generated alerts)

```kusto
// Remove escalation tracking ICMs
| where Title !contains "ESCALATION OF CASE"
| where Title !contains "CSSCSI"
| where Title !contains "SCIM -"
| where OwningTeamName !contains "SCIMESCALATIONMANAGEMENT"

// Remove auto-generated system ICMs
| where Title !contains "[Auto-Generated]"
| where Title !contains "[Automated]"
| where Title !contains "[System]"
```

**Use When**: Querying ICM incidents for product issues

**Example**:
```kusto
Incidents
| where Status == "ACTIVE"
| where OwningTenantName == "Purview"
| where Title !contains "ESCALATION"  // Apply noise filter
| where Title !contains "CSSCSI"       // Apply noise filter
...
```

---

### Case State Filters

**Purpose**: Focus on active/open cases only

```kusto
// Open cases only (exclude closed/resolved)
| where ServiceRequestState != "Closed"
| where ServiceRequestState != "Resolved"

// OR use positive filter
| where ServiceRequestState in ("Open", "Pending", "Active")

// Exclude brand new cases (< 1 day old)
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen > 1
```

**Use When**: Querying support cases (GetSCIMIncidentV2)

---

### Purview Product Filters

**Purpose**: Scope queries to Purview products only

```kusto
// Comprehensive Purview filter
| where ProductName contains "Purview" 
   or ProductName contains "Compliance"
   or ProductName contains "Information Protection"
   or SAPPath contains "Purview"
   or SAPPath contains "Microsoft Purview"
   or PlanningCategory startswith "SCIM"
   or DerivedProductName contains "Purview"
```

**Use When**: Filtering cases or incidents to Purview scope

**Alternative - Strict Filter** (Purview only, no related products):
```kusto
| where ProductName has_any ("Microsoft Purview Compliance", "Microsoft Purview Information Protection", "Microsoft Purview")
```

---

### Date Range Filters

**Purpose**: Scope queries to relevant timeframes

```kusto
// Last 30 days (default)
| where CreateDate >= ago(30d)
| where CreatedTime >= ago(30d)

// Last 90 days (quarterly review)
| where CreateDate >= ago(90d)

// Last 6 months (analysis)
| where CreateDate >= ago(180d)

// Last year
| where CreateDate >= ago(365d)

// Custom date range
| where CreateDate between (datetime(2025-01-01) .. datetime(2026-01-31))
```

**Use When**: Any query with time-based data

---

### Aging Filters (At-Risk Cases)

**Purpose**: Identify aging/at-risk cases requiring attention

```kusto
// Calculate age
| extend DaysOpen = todouble(CaseAge)  // For cases
| extend DaysOpen = datetime_diff('day', now(), CreateDate)  // For ICMs

// Age categories
| extend AgeCategory = case(
    DaysOpen > 180, "Critical (>180 days)",
    DaysOpen > 120, "Very High (>120 days)",
    DaysOpen > 90, "High (>90 days)",
    DaysOpen > 60, "Medium (>60 days)",
    DaysOpen > 30, "Low (>30 days)",
    "Normal (<30 days)")

// Filter to at-risk only
| where DaysOpen > 60
```

**Use When**: Aging analysis, risk reporting

---

### Severity Filters

**Purpose**: Focus on high-priority issues

```kusto
// Cases: Severity A/B only (high priority)
| where ServiceRequestCurrentSeverity in ("A", "B")

// ICMs: Severity 2/3 only (Sev 1 excluded - outages handled separately)
| where Severity in (2, 3)
| where Severity < 4  // Below Sev 4 (lower priority)
```

**Use When**: Priority-based filtering

---

### Customer-Specific Filters

**Purpose**: Scope to specific customer tenants

```kusto
// Single customer (by TenantId - most reliable)
| where TenantId == "c990bb7a-51f4-439b-bd36-9c07fb1041c0"  // Ford

// Multiple customers (IC/MCS list)
| where TenantId in (
    "c990bb7a-51f4-439b-bd36-9c07fb1041c0",  // Ford
    "5280104a-472d-4538-9ccf-1e1d0efe8b1b",  // Amazon
    "157a26ef-912f-4244-abef-b45fc4bd77f9"   // Huntington
)

// By TopParentName (less reliable, use for display only)
| where TopParentName == "Ford"
```

**Use When**: Customer-specific queries

---

## 🔧 Deduplication Filters

### Remove Duplicate ICM Status History

**Purpose**: ICM table has multiple rows per incident (status changes)

```kusto
// Get unique incidents only
| summarize by IncidentId, Title, Severity, Status, CreateDate, OwningTeamName

// OR get latest status
| summarize arg_max(ModifiedDate, *) by IncidentId

// OR count unique incidents
| summarize UniqueICMs = dcount(IncidentId)
```

**Use When**: Counting ICMs, getting current state

---

### Remove Duplicate Cases

**Purpose**: Case table may have multiple rows (updates, transfers)

```kusto
// Get latest case state
| summarize arg_max(ModifiedDate, *) by ServiceRequestNumber

// OR deduplicate by case number
| summarize by ServiceRequestNumber, ServiceRequestState, DaysOpen
```

**Use When**: Counting cases, getting current status

---

## 📊 Performance Optimization Filters

### Reduce Result Set Size

```kusto
// Limit results (use for testing/debugging)
| take 100

// Top N results
| top 50 by DaysOpen desc

// Sample data (for large datasets)
| sample 1000
```

**Use When**: Query performance issues, testing

---

### Index-Friendly Filters (Apply First)

```kusto
// ✅ Good: Filter on indexed columns first
| where CreateDate >= ago(30d)        // Index-friendly
| where TenantId == "xxx"             // Index-friendly
| where ServiceRequestState != "Closed"

// ❌ Bad: String searches early in pipeline
| where Title contains "DLP"          // Slower, apply later
| where TopParentName == "Ford"       // Not indexed well
```

**Use When**: Large datasets, slow queries

---

## 🎯 Combined Filter Templates

### Template 1: Active Customer Purview Cases
```kusto
GetSCIMIncidentV2
| where CreateDate >= ago(90d)                    // Date filter first
| where TenantId == "{TENANT_ID}"                 // Customer filter
| where ServiceRequestState != "Closed"           // State filter
| where ProductName contains "Purview"            // Product filter
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen > 1                              // Exclude brand new
```

---

### Template 2: Active Product ICMs (No Noise)
```kusto
Incidents
| where CreateDate >= ago(90d)                    // Date filter first
| where OwningTenantName == "Purview"             // Product filter
| where Status in ("Active", "Mitigating")        // State filter
| where Title !contains "ESCALATION"              // Noise filter
| where Title !contains "CSSCSI"                  // Noise filter
| where OwningTeamName startswith "PURVIEW\\"     // Product team filter
| extend DaysOpen = datetime_diff('day', now(), CreateDate)
```

---

### Template 3: At-Risk Cases with ICMs
```kusto
GetSCIMIncidentV2
| where CreateDate >= ago(180d)
| where ServiceRequestState != "Closed"
| where ProductName contains "Purview"
| where TenantId in ({TENANT_ID_LIST})
| extend DaysOpen = todouble(CaseAge)
| where DaysOpen > 60                             // At-risk threshold
| extend HasICM = isnotempty(RelatedICM_Id)
| where HasICM                                    // With ICMs only
```

---

## 🚫 Anti-Patterns (Avoid These)

### ❌ DON'T:
```kusto
// Bad: No date filter (scans entire table)
Incidents
| where Status == "Active"
| where Title contains "DLP"

// Bad: String search before date filter
GetSCIMIncidentV2
| where TopParentName == "Ford"
| where CreateDate >= ago(30d)

// Bad: Using CustomerName (inconsistent)
Incidents
| where CustomerName contains "Ford"
```

### ✅ DO:
```kusto
// Good: Date filter first, indexed columns
Incidents
| where CreateDate >= ago(30d)
| where Status == "Active"
| where OwningTenantName == "Purview"
| where Title contains "DLP"

// Good: TenantId (indexed, reliable)
GetSCIMIncidentV2
| where CreateDate >= ago(30d)
| where TenantId == "c990bb7a-51f4-439b-bd36-9c07fb1041c0"
```

---

## 📋 Quick Reference

| Filter Type | When to Use | Example |
|-------------|-------------|---------|
| **Date Range** | Always (first filter) | `where CreateDate >= ago(30d)` |
| **ICM Noise** | ICM queries | `where Title !contains "ESCALATION"` |
| **Case State** | Case queries | `where ServiceRequestState != "Closed"` |
| **Product Scope** | Purview focus | `where ProductName contains "Purview"` |
| **Customer** | Customer-specific | `where TenantId == "{ID}"` |
| **Aging** | Risk analysis | `where DaysOpen > 60` |
| **Deduplication** | Counting | `summarize by IncidentId` |

---

**Best Practice**: Apply filters in this order for optimal performance:
1. Date range (indexed)
2. TenantId / Tenant filters (indexed)
3. State filters (indexed)
4. Product/Title text searches (non-indexed)
5. Calculated fields (DaysOpen, etc.)

---

**Last Updated**: February 4, 2026  
**Maintained By**: Jacques (Kusto Expert Sub-Agent)
