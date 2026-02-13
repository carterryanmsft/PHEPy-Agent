# Content Extraction Guide for Purview Product Expert

**Version:** 1.0  
**Last Updated:** February 5, 2026  
**Purpose:** Guide for extracting and organizing content from authoritative sources

---

## 🔗 Source Access

### 1. IP Engineering Core Wiki
**URL:** `https://o365exchange.visualstudio.com/IP%20Engineering/_wiki/wikis/IP%20Engineering.wiki/15457/IP-Engineering-Core`  
**Authentication:** Microsoft AAD (use browser with corp credentials)  
**Access Required:** O365 Engineering org access

### 2. ASIM Security/Compliance ADO
**URL:** `https://dev.azure.com/ASIM-Security/Compliance`  
**Authentication:** Microsoft AAD  
**Access Required:** ASIM project permissions

### 3. CxE Security Care CEM SharePoint
**URL:** `https://microsoft.sharepoint.com/teams/CxE-Security-Care-CEM/`  
**Authentication:** Microsoft AAD (use browser with corp credentials)  
**Access Required:** CxE team membership or read permissions

### 4. Microsoft Learn
**URL:** `https://learn.microsoft.com/en-us/purview/`  
**Authentication:** None (public)  
**Access Required:** Public internet

---

## 📋 Extraction Workflows

### Workflow 1: Product Architecture Documentation

**Source:** IP Engineering Wiki → Architecture Section

**Search Queries:**
```
Site: o365exchange.visualstudio.com
Topics:
- "DLP Architecture"
- "MIP Service Design"
- "Information Protection Pipeline"
- "eDiscovery Architecture"
- "Data Lifecycle Management"
- "Purview Service Map"
- "Component Dependencies"
```

**Extract To:** `grounding_docs/purview_product/purview_product_architecture.md`

**Key Sections to Capture:**
- Service component diagram
- Data flow diagrams
- Integration points (Exchange, SharePoint, Teams, Azure AD)
- Backend services and APIs
- Scale architecture
- Multi-cloud deployment models

---

### Workflow 2: Known Issues & Bugs

**Source:** ASIM Compliance ADO → Work Items → Bugs

**ADO Query:**
```kusto
[System.WorkItemType] = 'Bug'
AND [System.AreaPath] UNDER 'Compliance\Purview'
AND [System.State] IN ('Active', 'Resolved', 'Closed')
AND [Microsoft.VSTS.Common.Severity] IN (0, 1, 2)
ORDER BY [Microsoft.VSTS.Common.Priority] ASC
```

**Extract To:** `grounding_docs/purview_product/purview_known_issues.md`

**Fields to Capture:**
- ADO ID
- Title
- Description
- Severity (0=Critical, 1=High, 2=Medium, 3=Low)
- State (Active/Resolved/By-Design)
- Repro Steps
- Workaround
- Fix Version/ETA
- Affected Components (MIP/DLP/eDiscovery)

**Categorization:**
- MIP (Sensitivity Labels)
- DLP (Data Loss Prevention)
- eDiscovery (Search & Hold)
- DLM (Retention & Disposal)
- Audit (Logging & Reporting)
- Insider Risk
- Communication Compliance

---

### Workflow 3: Troubleshooting Playbooks

**Source:** IP Engineering Wiki → Troubleshooting Section

**Search Queries:**
```
Topics:
- "DLP Troubleshooting"
- "MIP Diagnostics"
- "Label Not Appearing"
- "Policy Not Syncing"
- "eDiscovery Export Failed"
- "Retention Policy Issues"
- "Performance Degradation"
```

**Extract To:** `grounding_docs/purview_product/purview_troubleshooting_playbooks.md`

**Playbook Template:**
```markdown
## Issue: [Symptom Description]

**Affected Services:** MIP / DLP / eDiscovery  
**Severity:** Critical / High / Medium / Low  
**Frequency:** Common / Occasional / Rare

### Symptoms
- User-reported behavior
- Observable indicators
- Error messages

### Root Causes
1. Configuration error (XX%)
2. Service issue (XX%)
3. Client-side problem (XX%)

### Diagnostic Steps
1. Check [X] in portal
2. Run [diagnostic command]
3. Review [logs/telemetry]
4. Validate [configuration]

### Resolution
- **If root cause = [A]:** Do [steps]
- **If root cause = [B]:** Do [steps]

### Escalation Criteria
- Escalate to PG if: [conditions]
- DRI: [Squad/PM name]
```

---

### Workflow 4: Feature Guides from Microsoft Learn

**Source:** Microsoft Learn Public Docs

**Target Pages:**
- `https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp`
- `https://learn.microsoft.com/en-us/purview/information-protection`
- `https://learn.microsoft.com/en-us/purview/ediscovery`
- `https://learn.microsoft.com/en-us/purview/data-lifecycle-management`
- `https://learn.microsoft.com/en-us/purview/insider-risk-management`
- `https://learn.microsoft.com/en-us/purview/sensitivity-labels`
- `https://learn.microsoft.com/en-us/purview/retention`

**Extract To:** `grounding_docs/purview_product/[service]_guide.md`

**Content Structure:**
```markdown
# [Service] Complete Guide

## Overview
[Service description from Learn]

## Capabilities
[Feature list with links]

## Configuration
[Step-by-step from Learn with screenshots removed]

## Supported Scenarios
[Use cases and examples]

## Limitations
[Known limitations from Learn]

## Licensing
[SKU requirements]

## Integration Points
[Office, SharePoint, Teams, etc.]

## Common Issues
[Link to troubleshooting playbooks]
```

---

### Workflow 5: Scale Limits & Performance

**Source:** IP Engineering Wiki → Performance & Scale Section

**Search Queries:**
```
Topics:
- "DLP Policy Limits"
- "Label Count Limits"
- "eDiscovery Export Limits"
- "Retention Policy Limits"
- "Throttling Thresholds"
- "Performance Benchmarks"
- "Scale Testing Results"
```

**Extract To:** `grounding_docs/purview_product/scale_limits.md`

**Content Template:**
```markdown
# Purview Scale Limits & Performance

## DLP Service Limits
- Max policies per tenant: [number]
- Max rules per policy: [number]
- Max SITs per rule: [number]
- Max locations per policy: [number]
- Policy sync time: [duration]

## MIP/Sensitivity Labels
- Max labels per tenant: [number]
- Max sublabels: [number]
- Label sync latency: [duration]
- File size limits: [size]

## eDiscovery
- Max holds per case: [number]
- Max export size: [size]
- Max items per search: [number]
- Search timeout: [duration]

## Retention/DLM
- Max retention policies: [number]
- Max locations per policy: [number]
- Disposition processing time: [duration]
```

---

### Workflow 6: Support & Escalation Procedures

**Source:** CxE Security Care CEM SharePoint

**Manual Access Steps:**
1. Navigate to `https://microsoft.sharepoint.com/teams/CxE-Security-Care-CEM/SitePages/`
2. Sign in with Microsoft AAD credentials
3. Browse to relevant sections:
   - Support Procedures
   - Escalation Workflows
   - Customer Engagement Playbooks
   - PHE Operations Guides
   - Troubleshooting Runbooks

**Extract To:** `grounding_docs/purview_product/operations/`

**Key Sections to Capture:**
- Escalation procedures by severity
- Customer engagement best practices
- PHE (Premier Handling Engineer) workflows
- Support ticket management
- SLA and response time guidelines
- Handoff procedures between teams
- Incident management workflows
- Communication templates

**Manual Extraction Process:**
1. Open SharePoint page in browser
2. Copy content section by section
3. Convert to Markdown format
4. Apply document template
5. Save with appropriate filename
6. Add to master index

**Categorization:**
- Escalation Procedures
- Support Operations
- Customer Communication
- Team Collaboration
- Incident Management

---

## 🔍 Automated Extraction Scripts

### Script 1: Fetch Microsoft Learn Content

```python
# fetch_learn_content.py
import requests
from bs4 import BeautifulSoup
import json

LEARN_URLS = {
    'dlp': 'https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp',
    'mip': 'https://learn.microsoft.com/en-us/purview/information-protection',
    'ediscovery': 'https://learn.microsoft.com/en-us/purview/ediscovery',
    'dlm': 'https://learn.microsoft.com/en-us/purview/data-lifecycle-management'
}

def fetch_and_parse(service_name, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract main content
    content = soup.find('main')
    
    # Save to markdown
    output_path = f'grounding_docs/purview_product/{service_name}_guide.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {service_name.upper()} Guide\n\n")
        f.write(f"**Source:** {url}\n")
        f.write(f"**Last Fetched:** {datetime.now()}\n\n")
        f.write(content.get_text())
    
    print(f"✓ Extracted {service_name} to {output_path}")

for service, url in LEARN_URLS.items():
    fetch_and_parse(service, url)
```

### Script 2: Query ADO for Known Issues

```python
# fetch_ado_bugs.py
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import json

# Setup
personal_access_token = '[YOUR_PAT]'
organization_url = 'https://dev.azure.com/ASIM-Security'
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get work item tracking client
wit_client = connection.clients.get_work_item_tracking_client()

# Query for Purview bugs
wiql = """
    SELECT [System.Id], [System.Title], [System.State], 
           [Microsoft.VSTS.Common.Severity], [System.Description]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Bug'
      AND [System.AreaPath] UNDER 'Compliance\\Purview'
      AND [System.State] IN ('Active', 'Resolved')
      AND [Microsoft.VSTS.Common.Severity] <= 2
    ORDER BY [Microsoft.VSTS.Common.Priority] ASC
"""

# Execute query
query_result = wit_client.query_by_wiql(wiql)

# Fetch bug details
bugs = []
for item in query_result.work_items:
    bug = wit_client.get_work_item(item.id, expand='All')
    bugs.append({
        'id': bug.id,
        'title': bug.fields['System.Title'],
        'severity': bug.fields.get('Microsoft.VSTS.Common.Severity'),
        'state': bug.fields['System.State'],
        'description': bug.fields.get('System.Description', ''),
        'workaround': bug.fields.get('Microsoft.VSTS.TCM.ReproSteps', '')
    })

# Save to grounding doc
output_path = 'grounding_docs/purview_product/purview_known_issues.md'
with open(output_path, 'w') as f:
    f.write("# Purview Known Issues Registry\n\n")
    f.write(f"**Last Updated:** {datetime.now()}\n")
    f.write(f"**Total Issues:** {len(bugs)}\n\n")
    
    for bug in bugs:
        f.write(f"## ADO #{bug['id']}: {bug['title']}\n")
        f.write(f"**Severity:** {bug['severity']}\n")
        f.write(f"**State:** {bug['state']}\n")
        f.write(f"**Description:** {bug['description'][:500]}...\n\n")

print(f"✓ Extracted {len(bugs)} bugs to {output_path}")
```

---

## 📁 Grounding Document Structure

```
grounding_docs/
└── purview_product/
    ├── 00_INDEX.md                           # Master index with links
    ├── purview_product_architecture.md       # From IP Wiki
    ├── purview_known_issues.md               # From ADO
    ├── purview_troubleshooting_playbooks.md  # From IP Wiki
    ├── scale_limits.md                       # From IP Wiki
    ├── regional_availability.md              # From Learn + Wiki
    ├── licensing_sku_matrix.md               # From Learn
    │
    ├── services/
    │   ├── mip_dlp_guide.md                 # MIP/DLP from Learn
    │   ├── dlp_policies_guide.md            # DLP deep dive
    │   ├── ediscovery_guide.md              # eDiscovery from Learn
    │   ├── dlm_retention_guide.md           # DLM from Learn
    │   ├── insider_risk_guide.md            # IRM from Learn
    │   └── communication_compliance_guide.md
    │
    ├── troubleshooting/
    │   ├── dlp_troubleshooting.md
    │   ├── mip_troubleshooting.md
    │   ├── ediscovery_troubleshooting.md
    │   └── error_codes.md
    │
    └── integration/
        ├── office_integration.md
        ├── teams_integration.md
        └── third_party_integration.md
```

---

## 🔄 Update Cadence

### Weekly
- **Known Issues** from ADO (automated script)
- **Bug fixes** and workarounds
- **Hot fixes** and patches

### Monthly
- **Feature guides** from Learn
- **Troubleshooting playbooks** updates
- **Architecture docs** (if changes)

### Quarterly
- **Scale limits** review
- **Regional availability** updates
- **Best practices** refinement

---

## ✅ Content Quality Checklist

Before adding to grounding docs:
- [ ] Content is from authoritative source (Wiki/ADO/Learn)
- [ ] Last updated date is current (< 90 days)
- [ ] Links to source material included
- [ ] Technical accuracy verified by SME
- [ ] Markdown formatting correct
- [ ] Cross-references added where relevant
- [ ] Indexed in 00_INDEX.md

---

## 🚀 Quick Start: Populate Essential Docs

### Priority 1 (Do First)
1. Run `fetch_learn_content.py` to get DLP, MIP, eDiscovery, DLM guides
2. Run `fetch_ado_bugs.py` to get known issues
3. Manually extract architecture doc from IP Wiki (requires login)

### Priority 2 (Week 1)
4. Extract troubleshooting playbooks from IP Wiki
5. Extract scale limits from IP Wiki
6. Compile error codes reference

### Priority 3 (Week 2)
7. Create regional availability matrix
8. Compile licensing SKU comparison
9. Document integration points

---

## 📞 Contacts for Content Questions

- **IP Engineering Wiki Access:** DL: ipecore@microsoft.com
- **ADO Access Issues:** DL: asim-compliance@microsoft.com  
- **Content SMEs:** See `dscgp_squad_map.md` for squad contacts
- **Documentation Feedback:** PHE Operations team
