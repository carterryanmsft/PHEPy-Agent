# Kusto Schema Analysis - ICM Database
## Analysis Date: February 5, 2026

### Database: IcMDataWarehouse
### Cluster: https://icmcluster.kusto.windows.net

---

## Key Tables

### 1. IncidentsDedupView (100 columns)
Main incident tracking table with core metadata

**Key Fields for LQE Reporting:**

| Field | Type | Purpose | Population |
|-------|------|---------|------------|
| `IncidentId` | Int64 | Primary key | 100% |
| `Title` | String | Incident title | 100% |
| `Severity` | Int32 | 1-4, 25 for Premier | 100% |
| `SourceCreatedBy` | String | SE who created | 100% |
| `OwningTeamName` | String | Engineering team | 100% |
| `ResolveDate` | DateTime | When closed | 100% |
| `SupportTicketId` | String | CSS case number | ~90% |
| `CustomerName` | String | Customer name | Varies (often redacted) |
| `SourceOrigin` | String | "Other" or "Customer" | 100% (not useful) |
| `RaisingDatacenter` | String | Always "PHX" for Purview | 100% (not useful) |

### 2. IncidentCustomFieldEntriesDedupView
Custom field key-value pairs attached to incidents

**Purview LQE Custom Fields (52 incidents analyzed):**

| Field Name | Population | Values/Notes |
|------------|------------|--------------|
| `Escalation Quality` | 52 (100%) | TSG Not Followed (17), Missing Information (14), Incomplete SE Investigation (11), Missing Logs (6), etc. |
| `Escalation Type` | 51 (98%) | Issue, RFC, DCR |
| `Customer Tenant ID` | 51 (98%) | GUID format |
| `Company Domain Name` | 51 (98%) | Customer company name |
| `Link to TSG` | 51 (98%) | Azure DevOps wiki links |
| `Case Severity on Opening` | 51 (98%) | A, B, C severity |
| `TSG Effectiveness` | 51 (98%) | 0-5 rating |
| `DFM Case Number` | 51 (98%) | CSS case reference |
| `Prevention Type` | 38 (73%) | Prevention categories |
| `OCE TSG` | 37 (71%) | OCE TSG information |
| `Issue Classification` | 18 (35%) | Issue categories |
| `Feature Area` | 0 (0%) | **NOT POPULATED** - explains "Unknown" product areas |
| `Region` | 0 (0%) | **NOT POPULATED** - explains "Unknown" regions |

---

## Region Detection Strategy

### ❌ Fields That Don't Work:
- `SourceOrigin` - only contains "Other" or "Customer"
- `Region` custom field - empty for all Purview incidents
- `RaisingDatacenter` - all show "PHX" (Phoenix)
- `OccurringDatacenter` - empty

### ✅ Fields That Can Help:

#### 1. SourceCreatedBy Patterns (Partial Coverage)

**APAC Indicators (6/52 = 12%):**
- `wcl_hcm_*` → Vietnam (Ho Chi Minh) - 4 cases
- `cvg_pun_*` → India (Pune) - 1 case  
- `inf_hyd_*` → India (Hyderabad) - 1 case

**Unknown Region (46/52 = 88%):**
- `v-*` prefix → Vendor SE (31 cases) - various locations
- FTE names (14 cases) - various locations
- Email addresses (1 case)

**Distribution:**
```
Vendor SEs:     31 cases (60%)
FTE SEs:        14 cases (27%)
Vietnam APAC:    4 cases (8%)
India APAC:      2 cases (4%)
Email-based:     1 case (2%)
```

#### 2. DFM Case Number Pod Codes

Format: `YYMMDD-PPPP-NNNNN` where PPPP = Pod/Routing Code

**Pod Code Distribution (24 cases with valid numbers):**
- `0030` - 9 cases (38%)
- `0040` - 7 cases (29%)
- `0010` - 4 cases (17%)
- `0020` - 1 case (4%)
- `1420` - 1 case (4%)
- `0060` - 1 case (4%)
- `0050` - 1 case (4%)

*Note: Pod codes may map to regions but mapping not available in ICM*

---

## Product Area Mapping

### ❌ Feature Area Custom Field
- **NOT POPULATED** for any Purview LQE incidents
- Explains why all show "Unknown" in current query

### ✅ Use OwningTeamName (100% Coverage)

**Team-to-Product Mapping:**

#### DLM (Data Lifecycle Management) - 22 cases (42%)
- `PURVIEW\DLMIngestion` - 10 cases (archive, PST import)
- `PURVIEW\DLMExchangeRetentionandJournaling` - 6 cases (retention, holds)
- `PURVIEW\DLMPolicyManagement` - 3 cases (policy distribution)
- `PURVIEW\DLMAppRetention` - 1 case (Teams retention)
- `PURVIEW\DLMSharePointRetention` - 1 case (SharePoint retention)
- `PURVIEW\DLMRM` - 1 case (records management)

#### MIP/DLP (Information Protection) - 17 cases (33%)
- `PURVIEW\DLPEndpoint` - 5 cases (endpoint DLP)
- `PURVIEW\ExactDataMatch(EDM)` - 3 cases (EDM classifiers)
- `PURVIEW\DLPAlerts` - 2 cases (DLP alerts)
- `PURVIEW\DLP(Generic)` - 2 cases (general DLP)
- `PURVIEW\DLPCopilot` - 2 cases (Copilot DLP)
- `PURVIEW\MIPDLPEEE` - 1 case (EEE)
- `PURVIEW\SensitivityLabels` - 1 case (labels)
- `PURVIEW\DLPExchangePolicyTips` - 1 case (policy tips)

#### eDiscovery - 6 cases (12%)
- `PURVIEW\eDiscovery` - 6 cases (search, export, review sets)

#### Other - 7 cases (13%)
- `PURVIEW\Audit` - 2 cases (audit logs)
- `PURVIEW\InformationBarriers` - 1 case (IB)
- `PURVIEW\RBAC` - 1 case (adaptive scopes)
- `PURVIEW\ServerSideAutoLabeling` - 1 case (auto-labeling)
- `PURVIEW\TrainableClassifiers` - 1 case (classifiers)
- `PURVIEW\PRIVA` - 1 case (PRIVA)

---

## Additional Useful Fields

### Customer Information
- `SupportTicketId` - Original CSS case number (~90% populated)
- `DFM Case Number` - DFM system reference (98% populated)
- `Customer Tenant ID` - Customer tenant GUID (98% populated)
- `Company Domain Name` - Customer company (98% populated, may be redacted)

### Quality Metadata
- `Link to TSG` - Azure DevOps TSG wiki link (98% populated)
- `TSG Effectiveness` - Rating 0-5 (98% populated)
- `Case Severity on Opening` - A/B/C severity (98% populated)
- `Prevention Type` - Prevention categories (73% populated)
- `Issue Classification` - Issue categories (35% populated)

### Escalation Type
- `Escalation Type` custom field:
  - Issue - Standard technical issue
  - RFC - Request for Change  
  - DCR - Design Change Request

---

## Recommendations for Updated Query

### 1. Product Area Mapping ✅
Replace current `FeatureArea` custom field logic with `OwningTeamName` mapping:

```kql
| extend ProductArea = case(
    OwningTeamName contains "DLM", "DLM",
    OwningTeamName contains "DLP" or OwningTeamName contains "MIP" 
        or OwningTeamName contains "EDM" or OwningTeamName contains "Sensitivity", "MIP/DLP",
    OwningTeamName contains "eDiscovery", "eDiscovery",
    OwningTeamName contains "Audit", "Audit",
    OwningTeamName contains "PRIVA", "PRIVA",
    "Other"
)
```

### 2. Region Detection (Partial) ⚠️
Add pattern-based region detection for APAC:

```kql
| extend CreatorRegion = case(
    SourceCreatedBy contains "wcl_hcm", "APAC-Vietnam",
    SourceCreatedBy contains "cvg_pun", "APAC-India",
    SourceCreatedBy contains "inf_hyd", "APAC-India",
    "Unknown"
)
```

**Note:** 88% will show "Unknown" - this is acceptable since region data not available in ICM

### 3. Additional Fields to Include
```kql
| project 
    IcMId = IncidentId,
    IncidentId,
    Title,
    Severity,
    CreatedBy = SourceCreatedBy,
    CreatorRegion,
    ProductArea,
    OwningTeam = OwningTeamName,
    ResolveDate,
    EscalationQuality,
    SupportTicketId,           // ADD
    CustomerName,              // ADD
    EscalationType = "",       // From custom fields
    TsgLink = "",              // From custom fields
    TsgEffectiveness = ""      // From custom fields
```

### 4. Join Custom Fields
To get escalation type and TSG info:

```kql
let escalationType = IncidentCustomFieldEntriesDedupView
| where Name == "Escalation Type"
| project IncidentId, EscalationType = Value;

let tsgLink = IncidentCustomFieldEntriesDedupView
| where Name == "Link to TSG"
| project IncidentId, TsgLink = Value;

// Join in main query
| join kind=leftouter (escalationType) on IncidentId
| join kind=leftouter (tsgLink) on IncidentId
```

---

## Quality Issue Breakdown (Last 7 Days)

**Total:** 52 Low Quality Escalations

### By Quality Issue Type:
1. **TSG Not Followed** - 17 cases (33%)
2. **Missing Information** - 14 cases (27%)
3. **Incomplete SE Investigation** - 11 cases (21%)
4. **Missing Logs** - 6 cases (12%)
5. **Other** - 4 cases (8%)

### By Product Area:
1. **DLM** - 22 cases (42%)
2. **MIP/DLP** - 17 cases (33%)
3. **eDiscovery** - 6 cases (12%)
4. **Other** - 7 cases (13%)

### By SE Type:
1. **Vendor SE (v-)** - 31 cases (60%)
2. **FTE SE** - 14 cases (27%)
3. **APAC CSS** - 6 cases (12%)
   - Vietnam: 4
   - India: 2
4. **Email-based** - 1 case (2%)

---

## Schema Export

### IncidentsDedupView - All 100 Columns:
```
ChildCount, CommitDate, CommsMgrEngagementAdditionalDetails, CommsMgrEngagementMode,
CommunicationsManagerContactId, Component, CorrelationId, CreateDate, CustomerName,
ExecutiveIncidentManagerContactId, ExternalLinksCount, HitCount, HowFixed,
ImpactStartDate, ImpactedScenarios, IncidentId, IncidentManagerContactId,
IncidentSubType, IncidentType, IsCustomerImpacting, IsCustomerSupportEngagement,
IsNoise, IsOutage, IsPurged, IsRestricted, IsSecurityRisk, KBArticleId, Keywords,
LastCorrelationDate, Lens_BatchId, Lens_IngestionTime, Lens_Originator,
Lens_OriginatorData, Lens_SessionId, MitigateDate, MitigatedBy, Mitigation,
ModifiedDate, MonitorId, OccurringDatacenter, OccurringDeviceGroup, OccurringDeviceName,
OccurringEnvironment, OccurringServiceInstanceId, OriginatingTenantId,
OriginatingTenantName, OriginatingTenantPublicId, OutageDeclaredDate, OutageImpactLevel,
OwningContactAlias, OwningContactId, OwningTeamId, OwningTeamName, OwningTenantId,
OwningTenantName, OwningTenantPublicId, PIRLinkDate, PIRReportId, ParentIncidentId,
PublicPirId, RaisingDatacenter, RaisingDeviceGroup, RaisingDeviceName, RaisingEnvironment,
RaisingServiceInstanceId, RelatedLinksCount, ReproSteps, ResolveDate, ResolvedBy,
ResponsibleTeamId, ResponsibleTeamName, ResponsibleTenantId, ResponsibleTenantName,
ResponsibleTenantPublicId, Revision, RootCauseId, RootCauseLinkDate, RoutingId,
Severity, SiloId, SourceCreateDate, SourceCreatedBy, SourceId, SourceIncidentId,
SourceModifiedDate, SourceName, SourceOrigin, SourceType, Status, SubscriptionId,
Summary, SupportTicketId, Tags, Title, TsgId, TsgOutput
```

---

## Next Steps

1. ✅ Update [lqequery.kql](lqequery.kql) with OwningTeamName product mapping
2. ✅ Add SourceCreatedBy region pattern detection (accept 88% Unknown)
3. ✅ Include SupportTicketId and CustomerName in output
4. ⏳ Optionally join escalation type and TSG link custom fields
5. ⏳ Test updated query and regenerate report with improved data
