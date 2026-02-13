# Purview Product Expert - Search Query Templates

**Version:** 1.0  
**Last Updated:** February 5, 2026  
**Purpose:** Pre-defined search queries for finding product documentation

---

## 🔍 Query Categories

### 1. Architecture & Design Queries

#### IP Engineering Wiki Searches
```
Source: o365exchange.visualstudio.com/IP Engineering

Query Templates:
- "DLP architecture AND service design"
- "MIP pipeline AND data flow"
- "Purview service map AND component dependencies"
- "Information Protection backend AND APIs"
- "eDiscovery architecture AND search indexing"
- "Retention service AND disposition workflow"
- "Sensitivity label propagation AND inheritance"
- "DLP policy evaluation AND enforcement"
```

---

### 2. Known Issues Queries

#### ADO Bug Searches
```
Source: dev.azure.com/ASIM-Security/Compliance

WIQL Query for Critical Bugs:
SELECT [System.Id], [System.Title], [System.State], 
       [Microsoft.VSTS.Common.Severity], [System.AreaPath]
FROM WorkItems
WHERE [System.WorkItemType] = 'Bug'
  AND [System.AreaPath] UNDER 'Compliance\Purview'
  AND [System.State] IN ('Active', 'Resolved')
  AND [Microsoft.VSTS.Common.Severity] IN (0, 1)
ORDER BY [Microsoft.VSTS.Common.Priority] ASC

WIQL Query by Feature Area:
SELECT *
FROM WorkItems
WHERE [System.WorkItemType] = 'Bug'
  AND [System.AreaPath] UNDER 'Compliance\Purview\[AREA]'
  AND [System.State] <> 'Closed'

Areas:
- Compliance\Purview\DLP
- Compliance\Purview\MIP
- Compliance\Purview\eDiscovery
- Compliance\Purview\DLM
- Compliance\Purview\Audit
```

#### Microsoft Learn Known Limitations
```
Source: learn.microsoft.com/en-us/purview/

Search Queries:
- site:learn.microsoft.com/en-us/purview "known issues"
- site:learn.microsoft.com/en-us/purview "limitations"
- site:learn.microsoft.com/en-us/purview "not supported"
- site:learn.microsoft.com/en-us/purview "troubleshoot"
```

---

### 3. Troubleshooting & Diagnostics Queries

#### IP Engineering Wiki - Troubleshooting
```
Source: o365exchange.visualstudio.com/IP Engineering

Query Templates:
- "DLP policy not working AND troubleshooting"
- "Sensitivity labels not appearing AND diagnostics"
- "eDiscovery search failing AND resolution"
- "Retention policy not applying AND fix"
- "Performance degradation AND tuning"
- "Label sync issues AND remediation"
- "Policy propagation delay AND investigation"
```

#### Common Symptom Searches
```
Symptom-based queries:
- "labels missing from Outlook"
- "DLP alert not triggering"
- "eDiscovery export timeout"
- "retention tag not applied"
- "audit log delay"
- "endpoint DLP blocked"
- "Teams message not protected"
```

---

### 4. Feature & Capability Queries

#### Microsoft Learn - Feature Documentation
```
Source: learn.microsoft.com/en-us/purview/

By Service Area:
DLP:
- "data loss prevention policy"
- "DLP sensitive information types"
- "DLP endpoint protection"
- "DLP policy tips"
- "DLP alert configuration"

MIP:
- "sensitivity labels"
- "automatic labeling"
- "label encryption"
- "label inheritance"
- "trainable classifiers"

eDiscovery:
- "content search"
- "legal hold"
- "review set"
- "custodian management"
- "advanced indexing"

DLM:
- "retention policies"
- "retention labels"
- "disposition review"
- "records management"
- "adaptive scopes"
```

---

### 5. Performance & Scale Queries

#### IP Engineering Wiki - Scale Limits
```
Source: o365exchange.visualstudio.com/IP Engineering

Query Templates:
- "DLP policy limits AND maximum"
- "label count threshold AND scale"
- "eDiscovery export limits AND size"
- "retention policy limits AND throttling"
- "performance benchmarks AND SLA"
- "scale testing results AND capacity"
- "throughput metrics AND optimization"
```

---

### 6. Integration & API Queries

#### IP Engineering Wiki - APIs
```
Source: o365exchange.visualstudio.com/IP Engineering

Query Templates:
- "Purview REST API AND endpoints"
- "PowerShell cmdlets AND automation"
- "Graph API integration AND permissions"
- "Office integration AND client support"
- "third-party connector AND SDK"
```

#### Microsoft Learn - Integration Docs
```
Source: learn.microsoft.com/en-us/purview/

- "Microsoft 365 integration"
- "Office apps protection"
- "Teams DLP"
- "SharePoint sensitivity"
- "Exchange Online DLP"
```

---

### 7. Configuration & Setup Queries

#### Step-by-Step Guides
```
Source: learn.microsoft.com/en-us/purview/

Query Templates:
- "create DLP policy"
- "configure sensitivity labels"
- "set up eDiscovery case"
- "configure retention policy"
- "enable audit logging"
- "deploy endpoint DLP"
- "publish sensitivity labels"
```

---

### 8. Licensing & SKU Queries

#### Microsoft Learn - Licensing
```
Source: learn.microsoft.com/en-us/purview/

Query Templates:
- "Purview licensing"
- "E3 vs E5 comparison"
- "compliance licensing guidance"
- "feature availability by SKU"
- "add-on licenses"
```

---

### 9. Regional & Cloud Queries

#### Availability Documentation
```
Source: learn.microsoft.com/en-us/purview/ + IP Wiki

Query Templates:
- "GCC High support"
- "DoD cloud availability"
- "national cloud features"
- "regional data residency"
- "multi-geo tenant"
- "sovereign cloud support"
```

---

### 10. Product Roadmap Queries

#### ADO Feature Tracking
```
Source: dev.azure.com/ASIM-Security/Compliance

WIQL Query for Upcoming Features:
SELECT [System.Id], [System.Title], [System.State], 
       [Microsoft.VSTS.Scheduling.TargetDate]
FROM WorkItems
WHERE [System.WorkItemType] = 'Feature'
  AND [System.AreaPath] UNDER 'Compliance\Purview'
  AND [System.State] IN ('New', 'Active', 'Committed')
ORDER BY [Microsoft.VSTS.Scheduling.TargetDate] ASC
```

---

## 🎯 Query by User Intent

### Intent: "Is this a known bug?"
**Sources to Search:**
1. ADO: `[System.WorkItemType] = 'Bug' AND [System.Title] CONTAINS '[symptom]'`
2. IP Wiki: `"known issue" AND "[service]" AND "[symptom]"`
3. Learn: `site:learn.microsoft.com/en-us/purview "known limitations" "[service]"`

---

### Intent: "How do I configure [feature]?"
**Sources to Search:**
1. Learn: `"configure" OR "create" OR "set up" AND "[feature]"`
2. IP Wiki: `"[feature] configuration" AND "step by step"`
3. ADO: Check for open bugs related to configuration

---

### Intent: "Why is [feature] not working?"
**Sources to Search:**
1. IP Wiki: `"[feature] troubleshooting" OR "[feature] not working"`
2. ADO: `[System.Title] CONTAINS '[feature]' AND [System.State] = 'Active'`
3. Learn: `"troubleshoot [feature]" OR "[feature] common issues"`

---

### Intent: "What are the limits for [feature]?"
**Sources to Search:**
1. IP Wiki: `"[feature] limits" OR "[feature] threshold" OR "[feature] maximum"`
2. Learn: `"[feature] limitations" OR "[feature] scale"`

---

### Intent: "Is [feature] supported in [cloud]?"
**Sources to Search:**
1. Learn: `"[feature]" AND "[cloud]" AND "availability"`
2. IP Wiki: `"regional availability" AND "[feature]"`

---

## 📊 Search Priority Matrix

| User Question Type | Primary Source | Secondary Source | Tertiary Source |
|-------------------|----------------|------------------|-----------------|
| Architecture | IP Wiki | Learn | ADO Specs |
| Known Bugs | ADO | IP Wiki | Learn |
| Troubleshooting | IP Wiki | Learn | ADO Workarounds |
| Configuration | Learn | IP Wiki | ADO Docs |
| Scale Limits | IP Wiki | Learn | - |
| Feature Support | Learn | IP Wiki | ADO Roadmap |
| API/Integration | IP Wiki | Learn | - |
| Licensing | Learn | - | - |

---

## 🔧 Advanced Search Operators

### ADO WIQL Operators
```sql
-- Text matching
[Field] CONTAINS 'text'
[Field] CONTAINS WORDS 'word1 word2'

-- Hierarchy
[System.AreaPath] UNDER 'Path'

-- Date ranges
[System.CreatedDate] >= @Today - 30

-- Logical operators
AND, OR, NOT

-- Collections
IN ('Value1', 'Value2')
```

### Wiki Search Syntax
```
-- Exact phrase
"exact phrase"

-- Multiple terms (OR)
term1 OR term2

-- Required term
+required

-- Excluded term
-excluded

-- Wildcard
term*
```

---

## 💡 Query Optimization Tips

1. **Start broad, then narrow** - Begin with service name, add symptoms
2. **Use official terminology** - "DLP" not "data loss", "MIP" not "labeling"
3. **Check multiple sources** - Wiki for depth, Learn for official stance, ADO for bugs
4. **Date filter** - Prioritize recent content (< 6 months)
5. **Cross-reference** - If found in one source, verify in another

---

## 📝 Query Response Template

When answering user questions using queries:

```markdown
### [User Question]

**Sources Consulted:**
- [✓] IP Engineering Wiki: [query used]
- [✓] ASIM ADO: [query used]
- [✓] Microsoft Learn: [query used]

**Findings:**
[Summarized answer with citations]

**References:**
1. [Source 1 - Title](URL)
2. [Source 2 - Title](URL)
3. [Source 3 - Title](URL)

**Confidence Level:** High / Medium / Low
**Last Verified:** [Date]
```

---

## 🚀 Quick Reference: Most Common Queries

### Top 10 Queries for Daily Use

1. **DLP Not Triggering**
   - ADO: `[System.Title] CONTAINS 'DLP' AND [System.Title] CONTAINS 'not triggering'`
   - Wiki: `"DLP policy evaluation" AND "not working"`

2. **Labels Not Appearing**
   - ADO: `[System.Title] CONTAINS 'label' AND [System.Title] CONTAINS 'missing'`
   - Wiki: `"sensitivity label propagation" AND "troubleshooting"`

3. **eDiscovery Search Timeout**
   - Wiki: `"eDiscovery performance" AND "timeout" AND "optimization"`
   - Learn: `"eDiscovery search" AND "performance"`

4. **Retention Not Applied**
   - ADO: `[System.Title] CONTAINS 'retention' AND [System.State] = 'Active'`
   - Wiki: `"retention policy precedence" AND "not applying"`

5. **Policy Sync Delay**
   - Wiki: `"policy propagation" AND "delay" AND "latency"`
   - Learn: `"policy sync" OR "policy distribution"`

6. **Endpoint DLP Issues**
   - ADO: `[System.AreaPath] UNDER 'Compliance\Purview\DLP\Endpoint'`
   - Wiki: `"endpoint DLP" AND "troubleshooting"`

7. **Teams Protection Not Working**
   - Learn: `"Teams DLP" AND "troubleshoot"`
   - Wiki: `"Teams message protection" AND "issues"`

8. **Label Inheritance Problems**
   - Wiki: `"label inheritance" AND "precedence rules"`
   - Learn: `"sensitivity label" AND "inheritance"`

9. **Audit Log Latency**
   - Wiki: `"audit pipeline" AND "latency" AND "delay"`
   - Learn: `"audit log" AND "availability"`

10. **Performance Degradation**
    - Wiki: `"performance tuning" AND "[service]"`
    - ADO: `[System.Title] CONTAINS 'performance' AND [System.Severity] <= 1`
