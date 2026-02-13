# Available Fields Comparison - LQE Query

## Current Query Output (10 fields)

| Field Name | Source | Status | Notes |
|------------|--------|--------|-------|
| `IcMId` | IncidentId | ✅ Working | Incident ID |
| `IncidentId` | IncidentId | ✅ Working | Incident ID |
| `Title` | Title | ✅ Working | Incident title |
| `Severity` | Severity | ✅ Working | 1-4, 25 for Premier |
| `CreatedBy` | SourceCreatedBy | ✅ Working | SE who created |
| `CreatorRegion` | Calculated | ❌ **NOT WORKING** | Always "Unknown" - bad logic |
| `ProductArea` | Calculated | ❌ **NOT WORKING** | Always "Unknown" - Feature Area empty |
| `OwningTeam` | OwningTeamName | ✅ Working | Engineering team |
| `ResolveDate` | ResolveDate | ✅ Working | When closed |
| `EscalationQuality` | Custom field | ✅ Working | Quality issue type |

**Problems:**
- ❌ `CreatorRegion`: Using `SourceOrigin` which only contains "Other"/"Customer"
- ❌ `ProductArea`: Using `Feature Area` custom field which is **empty** for all Purview

---

## Available Fields - Main Table (IncidentsDedupView)

### Customer/Case Information
| Field | Type | Population | Use Case |
|-------|------|------------|----------|
| `SupportTicketId` | String | ~90% | ⭐ **CSS case number** - e.g., "2510170030001042" |
| `CustomerName` | String | Varies | Customer company name (often redacted) |
| `SubscriptionId` | String | ? | Azure subscription ID |

### Incident Metadata  
| Field | Type | Population | Use Case |
|-------|------|------------|----------|
| `CreateDate` | DateTime | 100% | When escalation created |
| `ModifiedDate` | DateTime | 100% | Last modified time |
| `Status` | String | 100% | Current status (Active/Resolved/etc) |
| `IncidentType` | String | 100% | Already filtering: "CustomerReported" |
| `IncidentSubType` | String | ? | Subtype classification |

### Ownership/Assignment
| Field | Type | Population | Use Case |
|-------|------|------------|----------|
| `OwningContactAlias` | String | ? | Owner's alias |
| `OwningContactId` | String | ? | Owner's ID |
| `ResolvedBy` | String | ? | Who resolved the incident |
| `ResponsibleTeamName` | String | ? | Responsible team |

### Content/Description
| Field | Type | Population | Use Case |
|-------|------|------------|----------|
| `Summary` | String | ? | Incident summary/description |
| `HowFixed` | String | ? | Resolution description |
| `Mitigation` | String | ? | Mitigation steps |
| `ReproSteps` | String | ? | Reproduction steps |
| `Keywords` | String | ? | Keywords/tags |
| `Tags` | String | ? | Tags |

### Relationships
| Field | Type | Population | Use Case |
|-------|------|------------|----------|
| `ParentIncidentId` | Int64 | ? | Parent incident for duplicates |
| `ChildCount` | Int64 | ? | Number of child incidents |
| `RootCauseId` | Int64 | ? | Root cause incident link |

---

## Available Custom Fields (98% populated for LQE)

### Highly Populated (>95%)
| Field Name | Values/Format | Use Case |
|------------|---------------|----------|
| `Escalation Quality` | TSG Not Followed, Missing Info, etc. | ⭐ **Already using** |
| `Escalation Type` | Issue, RFC, DCR | ⭐ **Recommended add** - categorize escalations |
| `Customer Tenant ID` | GUID | Unique customer identifier |
| `Company Domain Name` | Text | Customer company name |
| `Link to TSG` | URL | ⭐ **Recommended add** - TSG documentation link |
| `TSG Effectiveness` | 0-5 | TSG quality rating |
| `DFM Case Number` | Case number | DFM system reference |
| `Case Severity on Opening` | A, B, C | Original severity |

### Moderately Populated (>70%)
| Field Name | Values/Format | Use Case |
|------------|---------------|----------|
| `Prevention Type` | Various | Prevention categories |
| `OCE TSG` | Text | OCE TSG information |

### Sparsely Populated (<40%)
| Field Name | Values/Format | Notes |
|------------|---------------|-------|
| `Issue Classification` | Various | Only 35% populated |
| `Reviewer Name` | Name | Only 31% populated |
| `Review Details` | Text | Only 25% populated |

### Not Populated
| Field Name | Status |
|------------|--------|
| `Feature Area` | ❌ **0% populated** - causing ProductArea failure |
| `Region` | ❌ **0% populated** - causing CreatorRegion failure |

---

## Recommended Enhanced Query Output (15 fields)

### Keep Current (8 fields)
✅ `IcMId`  
✅ `IncidentId`  
✅ `Title`  
✅ `Severity`  
✅ `CreatedBy`  
✅ `OwningTeam`  
✅ `ResolveDate`  
✅ `EscalationQuality`

### Fix Broken (2 fields)
🔧 `CreatorRegion` - Use `SourceCreatedBy` patterns instead of `SourceOrigin`  
🔧 `ProductArea` - Use `OwningTeamName` instead of `Feature Area` custom field

### Add New (5 fields)
➕ `SupportTicketId` - CSS case number for tracking  
➕ `CustomerName` - Customer identification  
➕ `EscalationType` - Issue/RFC/DCR classification  
➕ `TsgLink` - TSG documentation URL  
➕ `CreateDate` - When escalation was created

---

## Updated Field Mapping Logic

### ProductArea (FIX)
```kql
// CURRENT (NOT WORKING - Feature Area is empty)
| extend ProductArea = iff(FeatureArea contains "MIP"...)

// FIXED (Use OwningTeamName)
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

**Coverage:**
- DLM: 22 cases (42%)
- MIP/DLP: 17 cases (33%)
- eDiscovery: 6 cases (12%)
- Other: 7 cases (13%)

### CreatorRegion (FIX)
```kql
// CURRENT (NOT WORKING - SourceOrigin is "Other"/"Customer")
| extend CreatorRegion = iff(SourceOrigin contains "EMEA"...)

// FIXED (Use SourceCreatedBy patterns)
| extend CreatorRegion = case(
    SourceCreatedBy contains "wcl_hcm", "APAC-Vietnam",
    SourceCreatedBy contains "cvg_pun", "APAC-India",
    SourceCreatedBy contains "inf_hyd", "APAC-India",
    "Unknown"
)
```

**Coverage:**
- Unknown: 46 cases (88%) - vendor SEs and FTEs
- APAC-Vietnam: 4 cases (8%)
- APAC-India: 2 cases (4%)

**Note:** 88% "Unknown" is acceptable - region data not available in ICM

---

## Sample Query with All Recommended Fields

```kql
// Weekly Low Quality Escalations Export - Enhanced
// Purpose: Export low quality escalations with full metadata
// Last Updated: February 5, 2026

let qualityData = IncidentCustomFieldEntriesDedupView
| where Name == "Escalation Quality"
| where isnotempty(Value) and Value != "All Data Provided"
| project IncidentId, EscalationQuality = Value;

let escalationType = IncidentCustomFieldEntriesDedupView
| where Name == "Escalation Type"
| project IncidentId, EscalationType = Value;

let tsgLink = IncidentCustomFieldEntriesDedupView
| where Name == "Link to TSG"
| project IncidentId, TsgLink = Value;

IncidentsDedupView
| where OwningTenantName == "Purview"
| where ResolveDate > ago(7d)
| where IncidentType == "CustomerReported"
| where IncidentId in ((qualityData | project IncidentId))
| join kind=inner (qualityData) on IncidentId
| join kind=leftouter (escalationType) on IncidentId
| join kind=leftouter (tsgLink) on IncidentId
| extend CreatorRegion = case(
    SourceCreatedBy contains "wcl_hcm", "APAC-Vietnam",
    SourceCreatedBy contains "cvg_pun", "APAC-India",
    SourceCreatedBy contains "inf_hyd", "APAC-India",
    "Unknown"
)
| extend ProductArea = case(
    OwningTeamName contains "DLM", "DLM",
    OwningTeamName contains "DLP" or OwningTeamName contains "MIP" 
        or OwningTeamName contains "EDM" or OwningTeamName contains "Sensitivity", "MIP/DLP",
    OwningTeamName contains "eDiscovery", "eDiscovery",
    OwningTeamName contains "Audit", "Audit",
    OwningTeamName contains "PRIVA", "PRIVA",
    "Other"
)
| project 
    IcMId = IncidentId,
    IncidentId,
    Title,
    Severity,
    CreatedBy = SourceCreatedBy,
    CreatorRegion,
    ProductArea,
    OwningTeam = OwningTeamName,
    CreateDate,
    ResolveDate,
    EscalationQuality,
    EscalationType,
    SupportTicketId,
    CustomerName,
    TsgLink
| order by ProductArea asc, ResolveDate desc
```

**Output: 15 fields instead of 10, with working ProductArea and CreatorRegion**
