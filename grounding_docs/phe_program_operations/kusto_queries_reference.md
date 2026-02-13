# PHE Kusto Queries Reference

**Last Updated:** February 4, 2026  
**Status:** Active  
**Owner:** PHE Operations / Data Analytics Team

---

## Executive Summary

This document contains frequently used Kusto queries for Purview Product Health & Escalation (PHE) operations. Includes queries for customer cohorts (MCS/IC), support case analytics, escalation tracking, tenant health monitoring, and product metrics.

**Purpose:** Enable orchestrator agent and sub-agents to retrieve structured data from Kusto clusters for decision-making, health monitoring, and escalation management.

---

## Query Categories

1. [Customer & Cohort Queries](#1-customer--cohort-queries)
2. [Support Case Queries](#2-support-case-queries)
3. [Escalation & ICM Queries](#3-escalation--icm-queries)
4. [Tenant Health & SHI Queries](#4-tenant-health--shi-queries)
5. [Product Metrics & Usage](#5-product-metrics--usage)
6. [Onboarding & Program Queries](#6-onboarding--program-queries)
7. [SLA & Performance Queries](#7-sla--performance-queries)

---

## 1. Customer & Cohort Queries

### 1.1 Active MCS Customers (Last 30 Days)

**Purpose:** Retrieve all Mission Critical Service (MCS) customers with active engagements.

**Query:**
```kusto
CustomerList
| where Program == "MCS" or Program == "MissionCritical"
| project CustomerName, TenantId, TPID, Program, StartDate, EndDate
| where Timestamp > ago(30d)
| order by CustomerName asc
```

**Fields:**
- `CustomerName` - Customer display name (redact in outputs)
- `TenantId` - Azure AD tenant ID (GUID)
- `TPID` - Top Parent ID (Microsoft account hierarchy)
- `Program` - MCS or MissionCritical
- `StartDate` - Program enrollment date
- `EndDate` - Program end date (null if ongoing)

**Orchestrator Usage:**
- **Program Onboarding Manager:** Track active MCS cohorts
- **Tenant Health Monitor:** Cross-reference with SHI scores
- **Contacts & Escalation Finder:** Identify customer PM assignments

**Example Output:**
```
CustomerName: [REDACTED - Customer A]
TenantId: a1b2c3d4-e5f6-7890-abcd-ef1234567890
TPID: 12345678
Program: MCS
StartDate: 2025-08-15
EndDate: null
```

---

### 1.2 Intensive Care (IC) Customers (Current)

**Purpose:** Retrieve all customers currently in Intensive Care program.

**Query:**
```kusto
CustomerList
| where Program == "IntensiveCare" or Program == "IC"
| where EndDate > now() or isempty(EndDate)
| project CustomerName, TenantId, TPID, NominationDate, ExitCriteria, CurrentSHI, AssignedPM
| order by NominationDate desc
```

**Fields:**
- `NominationDate` - Date customer entered IC
- `ExitCriteria` - Criteria for exiting IC (e.g., "SHI > 70 for 2 weeks")
- `CurrentSHI` - Latest Support Health Index score
- `AssignedPM` - PM managing IC engagement

**Orchestrator Usage:**
- **Program Onboarding Manager:** Monitor IC cohort health
- **Tenant Health Monitor:** Track exit readiness
- **Support Case Manager:** Prioritize IC customer cases

---

### 1.3 Catalyst Program Customers

**Purpose:** Retrieve customers enrolled in Catalyst proactive support program.

**Query:**
```kusto
CustomerList
| where Program == "Catalyst"
| where Timestamp > ago(90d)
| project CustomerName, TenantId, TPID, CohortName, StartDate, CatalystTier, AssignedCSAM
| order by StartDate desc
```

**Fields:**
- `CohortName` - Catalyst cohort identifier (e.g., "Catalyst Q1 2026")
- `CatalystTier` - Tier level (1, 2, or 3)
- `AssignedCSAM` - Customer Success Account Manager

**Orchestrator Usage:**
- **Program Onboarding Manager:** Track Catalyst enrollments
- **Tenant Health Monitor:** Monitor proactive engagement impact

---

### 1.4 All Active PHE Programs (Cross-Program View)

**Purpose:** Unified view of all customers across MCS, IC, and Catalyst.

**Query:**
```kusto
CustomerList
| where Program in ("MCS", "MissionCritical", "IntensiveCare", "IC", "Catalyst")
| where Timestamp > ago(30d)
| summarize Programs = make_set(Program), 
            EarliestStart = min(StartDate),
            LatestEnd = max(EndDate)
            by CustomerName, TenantId, TPID
| project CustomerName, TenantId, TPID, Programs, EarliestStart, LatestEnd
| order by CustomerName asc
```

**Use Case:** Identify customers enrolled in multiple programs (e.g., MCS + IC).

---

## 2. Support Case Queries

### 2.1 At-Risk Cases (SLA Breach Imminent)

**Purpose:** Identify cases within 4 hours of SLA breach.

**Query:**
```kusto
SupportCases
| where Status == "Active" or Status == "InProgress"
| where Product startswith "Purview" or Product contains "Compliance" or Product contains "DLP"
| extend TimeToSLABreach = SLATarget - (now() - LastUpdateTime)
| where TimeToSLABreach < 4h
| project CaseId, TenantId, CustomerName, Severity, Product, TimeToSLABreach, AssignedEngineer
| order by TimeToSLABreach asc
```

**Fields:**
- `TimeToSLABreach` - Hours remaining before SLA breach
- `AssignedEngineer` - Current case owner

**Orchestrator Usage:**
- **Support Case Manager:** Generate at-risk case alerts
- **Escalation Manager:** Flag for potential escalation

**Alert Threshold:** Cases with `TimeToSLABreach < 2h` require immediate escalation.

---

### 2.2 Aged Cases (> 14 Days Open)

**Purpose:** Identify cases open longer than 14 days.

**Query:**
```kusto
SupportCases
| where Status == "Active" or Status == "InProgress"
| where Product startswith "Purview"
| extend DaysOpen = datetime_diff('day', now(), CreatedDate)
| where DaysOpen > 14
| project CaseId, TenantId, CustomerName, Severity, Product, DaysOpen, LastUpdateTime, AssignedEngineer
| order by DaysOpen desc
```

**Use Case:** Case hygiene review, shiproom prep.

---

### 2.3 VIP Customer Cases (Open)

**Purpose:** All open cases for VIP/MCS/IC customers.

**Query:**
```kusto
let VIPTenants = CustomerList
    | where Program in ("MCS", "IntensiveCare", "Catalyst")
    | project TenantId;
SupportCases
| where Status == "Active" or Status == "InProgress"
| where Product startswith "Purview"
| join kind=inner VIPTenants on TenantId
| project CaseId, TenantId, CustomerName, Severity, Product, CreatedDate, SLAStatus, AssignedEngineer
| order by Severity asc, CreatedDate asc
```

**Use Case:** IC/MCS case risk reviews, WSR narrative.

---

### 2.4 Case Volume Trends (Weekly)

**Purpose:** Weekly case volume and severity distribution.

**Query:**
```kusto
SupportCases
| where Product startswith "Purview"
| where CreatedDate > ago(7d)
| summarize TotalCases = count(),
            CriticalCases = countif(Severity == "Critical"),
            HighCases = countif(Severity == "High"),
            MediumCases = countif(Severity == "Medium"),
            LowCases = countif(Severity == "Low")
            by bin(CreatedDate, 1d)
| order by CreatedDate desc
```

**Use Case:** WSR scorecard, trend analysis.

---

### 2.5 Transfer Cases (Inter-Team Transfers)

**Purpose:** Cases transferred to/from Purview support.

**Query:**
```kusto
SupportCases
| where Product startswith "Purview"
| where TransferCount > 0
| where Timestamp > ago(7d)
| project CaseId, TenantId, CustomerName, Severity, TransferCount, TransferReason, CurrentQueue, PreviousQueue
| order by TransferCount desc
```

**Use Case:** Transfer rate tracking, root cause analysis for shiprooms.

---

## 3. Escalation & ICM Queries

### 3.1 Active ICM Incidents (Purview)

**Purpose:** All active ICM incidents for Purview products.

**Query:**
```kusto
ICMIncidents
| where Status == "Active" or Status == "Mitigating"
| where OwningService contains "Purview" or ImpactedService contains "Purview"
| project IncidentId, TenantId, CustomerName, Severity, Title, CreatedDate, CurrentMitigationState, AssignedDRI
| order by Severity asc, CreatedDate asc
```

**Fields:**
- `IncidentId` - ICM incident ID (e.g., 728221759)
- `CurrentMitigationState` - Active, Mitigating, Monitoring
- `AssignedDRI` - Directly Responsible Individual

**Orchestrator Usage:**
- **Escalation Manager:** Track active escalations
- **Tenant Health Monitor:** Correlate with SHI scores

---

### 3.2 ICM Incidents by Customer (MCS/IC)

**Purpose:** ICM incidents impacting MCS or IC customers.

**Query:**
```kusto
let VIPTenants = CustomerList
    | where Program in ("MCS", "IntensiveCare")
    | project TenantId;
ICMIncidents
| where Status == "Active" or Status == "Mitigating"
| where OwningService contains "Purview"
| join kind=inner VIPTenants on TenantId
| project IncidentId, TenantId, CustomerName, Severity, Title, CreatedDate, CustomerProgram = "MCS/IC"
| order by Severity asc
```

**Use Case:** IC/MCS case risk reviews, executive escalations.

---

### 3.3 Recent Escalations (Last 7 Days)

**Purpose:** All escalations opened in the last week.

**Query:**
```kusto
ICMIncidents
| where OwningService contains "Purview"
| where CreatedDate > ago(7d)
| summarize TotalEscalations = count(),
            CritSit = countif(Severity == "Critical"),
            High = countif(Severity == "High")
            by bin(CreatedDate, 1d)
| order by CreatedDate desc
```

**Use Case:** WSR narrative, escalation trend analysis.

---

### 3.4 Time to Mitigation (TTM) Analysis

**Purpose:** Average time to mitigation for closed incidents.

**Query:**
```kusto
ICMIncidents
| where Status == "Resolved" or Status == "Closed"
| where OwningService contains "Purview"
| where CreatedDate > ago(30d)
| extend TTM = datetime_diff('hour', MitigatedDate, CreatedDate)
| summarize AvgTTM = avg(TTM),
            MedianTTM = percentile(TTM, 50),
            P95_TTM = percentile(TTM, 95)
            by Severity
| order by Severity asc
```

**Use Case:** Escalation quality metrics, performance benchmarking.

---

## 4. Tenant Health & SHI Queries

### 4.1 Support Health Index (SHI v2) - Current Scores

**Purpose:** Latest SHI v2 scores for all tenants.

**Query:**
```kusto
SupportHealthIndex
| where Timestamp > ago(1d)
| where ModelVersion == "v2"
| project TenantId, CustomerName, SHIScore, ProactiveScore, ReactiveScore, RiskBin, LastUpdated
| order by SHIScore asc
```

**Fields:**
- `SHIScore` - Overall SHI v2 score (0-100)
- `ProactiveScore` - Proactive component (50% weight)
- `ReactiveScore` - Reactive component (50% weight)
- `RiskBin` - High/Medium/Low risk categorization

**Orchestrator Usage:**
- **Tenant Health Monitor:** Primary health signal
- **Program Onboarding Manager:** IC nomination criteria

**Thresholds:**
- `SHIScore < 40` → Intensive Care candidate
- `SHIScore < 55` → MCS risk assessment
- `SHIScore > 70` → IC exit criteria

---

### 4.2 Tenants at Risk (SHI < 55)

**Purpose:** Identify tenants with poor support health.

**Query:**
```kusto
SupportHealthIndex
| where Timestamp > ago(1d)
| where ModelVersion == "v2"
| where SHIScore < 55
| project TenantId, CustomerName, SHIScore, RiskBin, OpenCases, ActiveICMs, DaysBelowThreshold
| order by SHIScore asc
```

**Fields:**
- `OpenCases` - Count of open support cases
- `ActiveICMs` - Count of active ICM incidents
- `DaysBelowThreshold` - Days tenant has been below SHI 55

**Use Case:** MCS risk reviews, proactive outreach.

---

### 4.3 SHI Trend (Last 30 Days)

**Purpose:** Track SHI score trend over time for a tenant.

**Query:**
```kusto
SupportHealthIndex
| where TenantId == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"  // Replace with actual tenant ID
| where Timestamp > ago(30d)
| where ModelVersion == "v2"
| project Timestamp, SHIScore, ProactiveScore, ReactiveScore
| order by Timestamp asc
```

**Use Case:** IC exit readiness, health trend visualization.

---

### 4.4 IC Exit Candidates (SHI > 70 for 14 Days)

**Purpose:** Identify IC customers ready to exit program.

**Query:**
```kusto
let ICTenants = CustomerList
    | where Program == "IntensiveCare"
    | project TenantId;
SupportHealthIndex
| where Timestamp > ago(14d)
| where ModelVersion == "v2"
| join kind=inner ICTenants on TenantId
| summarize MinSHI = min(SHIScore), AvgSHI = avg(SHIScore), DaysAbove70 = countif(SHIScore > 70) by TenantId, CustomerName
| where MinSHI > 70
| project TenantId, CustomerName, MinSHI, AvgSHI, DaysAbove70, ExitReady = "Yes"
| order by AvgSHI desc
```

**Use Case:** IC exit planning, program offboarding.

---

## 5. Product Metrics & Usage

### 5.1 Feature Adoption by Tenant

**Purpose:** Track Purview feature adoption across tenants.

**Query:**
```kusto
FeatureUsage
| where Product startswith "Purview"
| where Timestamp > ago(30d)
| summarize UniqueFeatures = dcount(FeatureName), TotalUsage = sum(UsageCount) by TenantId, CustomerName
| order by TotalUsage desc
```

**Use Case:** Feature adoption tracking, roadmap prioritization.

---

### 5.2 DLP Policy Performance

**Purpose:** Analyze DLP policy effectiveness and alerts.

**Query:**
```kusto
DLPTelemetry
| where Timestamp > ago(7d)
| summarize TotalPolicies = dcount(PolicyId),
            TotalAlerts = count(),
            BlockedActions = countif(Action == "Block"),
            AllowedOverrides = countif(Action == "AllowOverride")
            by TenantId, CustomerName
| order by TotalAlerts desc
```

**Use Case:** DLP shiproom, customer health assessment.

---

### 5.3 eDiscovery Collection Performance

**Purpose:** Monitor eDiscovery collection job performance.

**Query:**
```kusto
eDiscoveryJobs
| where JobType == "Collection"
| where Timestamp > ago(7d)
| extend DurationHours = datetime_diff('hour', EndTime, StartTime)
| summarize AvgDuration = avg(DurationHours),
            TotalJobs = count(),
            FailedJobs = countif(Status == "Failed"),
            AvgDataSizeGB = avg(DataSizeGB)
            by TenantId, CustomerName
| order by FailedJobs desc
```

**Use Case:** eDiscovery shiproom, performance troubleshooting.

---

## 6. Onboarding & Program Queries

### 6.1 MCS Onboarding Status (Current Cohort)

**Purpose:** Track onboarding progress for new MCS customers.

**Query:**
```kusto
OnboardingTasks
| where Program == "MCS"
| where CohortName == "MCS Q1 2026"  // Replace with current cohort
| summarize TotalTasks = count(),
            CompletedTasks = countif(Status == "Completed"),
            InProgressTasks = countif(Status == "InProgress"),
            NotStartedTasks = countif(Status == "NotStarted")
            by TenantId, CustomerName
| extend CompletionPercent = round((CompletedTasks * 100.0 / TotalTasks), 1)
| order by CompletionPercent asc
```

**Orchestrator Usage:**
- **Program Onboarding Manager:** Track onboarding velocity
- **Access & Role Manager:** Verify access provisioning

---

### 6.2 IC Nomination Pipeline

**Purpose:** Track customers in IC nomination pipeline.

**Query:**
```kusto
ICNominations
| where Status in ("Pending", "UnderReview", "Approved")
| project TenantId, CustomerName, NominationDate, CurrentSHI, NominationReason, Approver, Status
| order by NominationDate desc
```

**Use Case:** IC program planning, leadership updates.

---

## 7. SLA & Performance Queries

### 7.1 SLA Compliance Rate (Weekly)

**Purpose:** Calculate SLA compliance percentage by severity.

**Query:**
```kusto
SupportCases
| where Product startswith "Purview"
| where CreatedDate > ago(7d)
| where Status == "Resolved" or Status == "Closed"
| extend SLAMet = iff(TimeToEngagement <= SLATarget, 1, 0)
| summarize TotalCases = count(),
            SLAMetCases = sum(SLAMet),
            ComplianceRate = round((sum(SLAMet) * 100.0 / count()), 1)
            by Severity
| order by Severity asc
```

**Use Case:** WSR scorecard, SLA performance tracking.

---

### 7.2 Average Time to Engagement (TTE)

**Purpose:** Track average time to first engineer engagement.

**Query:**
```kusto
SupportCases
| where Product startswith "Purview"
| where CreatedDate > ago(7d)
| extend TTE = datetime_diff('hour', FirstEngagementTime, CreatedDate)
| summarize AvgTTE = avg(TTE),
            MedianTTE = percentile(TTE, 50),
            P95_TTE = percentile(TTE, 95)
            by Severity
| order by Severity asc
```

**Use Case:** Performance benchmarking, SLA optimization.

---

## Query Execution Best Practices

### Performance Optimization
1. **Use Time Filters:** Always include `Timestamp > ago(Xd)` to limit data scan
2. **Project Early:** Use `project` to reduce columns before joins/summarizations
3. **Limit Results:** Add `| take 100` for exploratory queries
4. **Avoid `*`:** Always specify columns explicitly

### Data Privacy
1. **Redact Customer Names:** Use `project-away CustomerName` when sharing results
2. **Mask Tenant IDs:** Only include TenantId when operationally necessary
3. **PII Guardrails:** Never query user-level data without explicit approval

### Query Testing
1. **Start Small:** Test with `| take 10` before running full query
2. **Verify Filters:** Confirm `where` clauses return expected scope
3. **Check Joins:** Validate join results with `| count` before proceeding

---

## Orchestrator Query Patterns

### Pattern 1: Health Check Workflow
```
1. Run: SHI Current Scores (4.1)
2. Filter: SHI < 55 (4.2)
3. Cross-reference: Active MCS Customers (1.1)
4. Output: At-risk MCS tenants with SHI scores
```

### Pattern 2: Escalation Detection
```
1. Run: At-Risk Cases (2.1)
2. Cross-reference: VIP Customer Cases (2.3)
3. Run: Active ICM Incidents (3.1)
4. Output: Cases/incidents requiring immediate escalation
```

### Pattern 3: IC Exit Readiness
```
1. Run: IC Customers (1.2)
2. Run: SHI Trend (4.3) for each IC tenant
3. Run: IC Exit Candidates (4.4)
4. Output: Tenants ready for IC exit with supporting data
```

---

## Kusto Clusters & Databases

### Production Clusters
- **DFM Cluster:** `https://cxedataplatformcluster.westus2.kusto.windows.net`
  - Database: `cxedata` (GetSCIMIncidentV2 table)
  - Refresh: Real-time

- **ICM Cluster:** `https://icm.kusto.windows.net`
  - Database: `Incidents`
  - Refresh: Real-time

- **SHI Cluster:** `https://cxe-analytics.kusto.windows.net`
  - Database: `CustomerHealth`
  - Refresh: Daily (6 AM UTC)

- **Telemetry Cluster:** `https://purview-telemetry.kusto.windows.net`
  - Database: `ProductMetrics`
  - Refresh: Hourly

### Access Requirements
- **DFM:** CSS / Support Engineer role
- **ICM:** Escalation Manager role
- **SHI:** CXE / PHE team member
- **Telemetry:** Purview Engineering or PM

---

## Related Grounding Docs

- `shi_v2_support_health_index.md` – SHI v2 scoring model details
- `dfm_sla_definitions.md` – SLA thresholds and rules
- `mcs_ic_cohort_registry.md` – Customer cohort definitions
- `operational_rhythms_governance.md` – WSR/MBR meeting cadences

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-04 | 1.0 | Initial creation with 25+ core PHE queries | PHE Operations |

---

**Last Updated:** February 4, 2026  
**Owner:** PHE Operations / Data Analytics Team  
**Status:** ✅ Active
