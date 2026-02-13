# Purview Product Expert - Capabilities Matrix

**Agent:** Purview Product Expert  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 🎯 Core Capabilities

### 1. Product Knowledge & Architecture

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Service Architecture** | Explain Purview component relationships, data flows, dependencies | Grounding docs, Wiki | ✅ Ready |
| **Feature Inventory** | List available features by service (MIP, DLP, eDiscovery, etc.) | Grounding docs | ✅ Ready |
| **Regional Availability** | Identify feature availability by region/cloud (Commercial, Gov, National) | Grounding docs | ✅ Ready |
| **Licensing & SKUs** | Explain E5, E3, A5, compliance SKU coverage | Grounding docs | ✅ Ready |
| **Scale Limits** | Document performance thresholds, tenant limits, throttling | Grounding docs | ✅ Ready |

### 2. Troubleshooting & Root Cause Analysis

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Configuration Validation** | Diagnose policy, rule, label configuration issues | Grounding docs, DFM | ✅ Ready |
| **Performance Analysis** | Identify bottlenecks, timeouts, scaling issues | Kusto, Grounding docs | ✅ Ready |
| **Known Issue Matching** | Map symptoms to known bugs/limitations | Grounding docs, ADO | ✅ Ready |
| **Error Code Lookup** | Translate error codes to user-friendly explanations | Grounding docs | ✅ Ready |
| **Root Cause Classification** | Determine if issue is config, bug, or by-design | Multi-source | ✅ Ready |

### 3. Guidance & Best Practices

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Feature Adoption** | Recommend rollout strategy for new features | Grounding docs | ✅ Ready |
| **Policy Design** | Guide optimal DLP/retention/sensitivity policies | Grounding docs | ✅ Ready |
| **Migration Planning** | Legacy → modern Purview migration guidance | Grounding docs | ✅ Ready |
| **Performance Tuning** | Optimize for scale, latency, resource usage | Grounding docs, Kusto | ✅ Ready |
| **Security Hardening** | Secure configuration recommendations | Grounding docs | ✅ Ready |

### 4. Issue Pattern Detection

| Capability | Description | Data Sources | Status |
|------------|-------------|--------------|--------|
| **Cross-Case Analysis** | Identify multiple cases with same root cause | DFM, Kusto | ✅ Ready |
| **Regression Detection** | Flag recently introduced issues after deployments | Kusto, ICM | ✅ Ready |
| **Systemic Issue Alerts** | Detect widespread impact across tenants | Kusto, DFM | ✅ Ready |
| **Rollback Candidates** | Recommend service rollback based on issue patterns | Multi-source | ✅ Ready |

---

## 📚 Service-Specific Expertise

### Microsoft Information Protection (MIP)

**Deep Knowledge Areas:**
- Sensitivity labels (manual, auto, default)
- Label inheritance and priority
- Office integration (Word, Excel, Outlook, Teams)
- Encryption and RMS integration
- Custom permissions and co-authoring
- Label migration from AIP to unified

**Common Issues:**
- Label not appearing in Office apps
- Auto-labeling not triggering
- Encrypted files not opening
- Label conflicts and inheritance issues
- Performance with large label sets

**Grounding Docs:**
- `grounding_docs/purview_product/mip_dip_guide.md`
- `grounding_docs/purview_product/mip_known_issues.md`
- `grounding_docs/purview_product/mip_performance_tuning.md`

---

### Data Loss Prevention (DLP)

**Deep Knowledge Areas:**
- Policy creation and scoping (Exchange, SharePoint, Teams, Endpoints)
- Sensitive info types (SIT) and custom patterns
- DLP alerts and incident management
- False positive reduction strategies
- Endpoint DLP deployment and management
- Cross-workload DLP coverage

**Common Issues:**
- False positives with custom SITs
- Policy not applying to expected users/locations
- Alert fatigue and tuning
- Endpoint DLP client issues
- Policy precedence and conflicts

**Grounding Docs:**
- `grounding_docs/purview_product/dlp_policies_guide.md`
- `grounding_docs/purview_product/dlp_known_issues.md`
- `grounding_docs/purview_product/dlp_sit_library.md`

---

### eDiscovery

**Deep Knowledge Areas:**
- Case creation and management
- Legal hold application and removal
- Content search and collection
- Review set creation and exports
- Advanced eDiscovery with AI
- Compliance boundaries
- Search performance at scale

**Common Issues:**
- Search timeouts with large mailboxes
- Hold not applying correctly
- Export failures
- Search query syntax errors
- Performance degradation > 10M items

**Grounding Docs:**
- `grounding_docs/purview_product/ediscovery_guide.md`
- `grounding_docs/purview_product/ediscovery_known_issues.md`
- `grounding_docs/purview_product/ediscovery_performance.md`

---

### Information Rights Management (IRM)

**Deep Knowledge Areas:**
- RMS service activation
- Template creation and management
- Rights policy enforcement
- Office integration for protection
- External user access (B2B)
- Decrypt and view protected content

**Common Issues:**
- License activation failures
- Cannot open protected documents
- Permission inheritance problems
- External sharing not working
- RMS service connectivity issues

**Grounding Docs:**
- `grounding_docs/purview_product/irm_guide.md`
- `grounding_docs/purview_product/irm_known_issues.md`

---

### Data Lifecycle Management (DLM)

**Deep Knowledge Areas:**
- Retention policies and labels
- Retention precedence rules
- Disposition review workflows
- Records management
- Compliance boundaries
- Multi-stage retention
- Preservation vs. deletion

**Common Issues:**
- Policy not applying as expected
- Disposition review not triggering
- Conflict between retention and holds
- Unexpected content deletion
- Performance with large policy sets

**Grounding Docs:**
- `grounding_docs/purview_product/dlm_retention_guide.md`
- `grounding_docs/purview_product/dlm_known_issues.md`

---

### Insider Risk Management

**Deep Knowledge Areas:**
- Policy templates and indicators
- User risk scoring
- Alert triage and investigation
- Integration with HR systems
- Privacy and compliance considerations
- Machine learning signal tuning

**Common Issues:**
- Too many false positive alerts
- Indicators not triggering
- User not in scope
- Integration with UEBA
- Privacy controls not enforced

**Grounding Docs:**
- `grounding_docs/purview_product/insider_risk_guide.md`
- `grounding_docs/purview_product/insider_risk_tuning.md`

---

### Communication Compliance

**Deep Knowledge Areas:**
- Policy creation for Teams/Email monitoring
- Offensive language detection
- Reviewer workflows
- Escalation and remediation
- Integration with HR and legal

**Common Issues:**
- High false positive rates
- Policy not capturing expected content
- Reviewer access issues
- Performance with large message volumes

**Grounding Docs:**
- `grounding_docs/purview_product/communication_compliance_guide.md`

---

### Content Explorer & Activity Explorer

**Deep Knowledge Areas:**
- Label usage analytics
- DLP incident tracking
- User activity monitoring
- Reporting and dashboards

**Common Issues:**
- Data latency (24-48 hour delay)
- Missing activity logs
- Permission issues for viewers

**Grounding Docs:**
- `grounding_docs/purview_product/content_activity_explorer_guide.md`

---

## 🔍 Diagnostic Workflows

### Workflow 1: Feature Not Working as Expected

```
1. Gather context:
   - Tenant ID, feature name, expected behavior, actual behavior
   - When did it start? Recent changes?
   - Scope: all users or specific subset?

2. Check grounding docs:
   - Is feature GA or preview?
   - Regional/cloud restrictions?
   - Known limitations?

3. Validate configuration:
   - Policy/label/rule settings
   - Scope and targeting
   - Precedence/conflicts

4. Check known issues:
   - Search grounding docs for matching symptoms
   - Cross-reference ADO bugs
   - Check if workaround exists

5. Recommend next steps:
   - If known: cite ADO #, workaround, ETA
   - If config: provide correction steps
   - If unknown: escalate to PG with diagnostic data
```

### Workflow 2: Performance Degradation

```
1. Quantify impact:
   - Baseline vs current performance
   - Affected operations (search, label, export, etc.)
   - Scope: single tenant or widespread?

2. Check scale limits:
   - Item count, user count, policy count
   - Compare against documented thresholds
   - Identify if limit exceeded

3. Review recent changes:
   - New policies or labels added?
   - Recent service deployment?
   - Tenant configuration changes?

4. Query telemetry:
   - Use Kusto to get performance metrics
   - Compare current vs historical trends
   - Identify bottleneck operations

5. Recommend optimization:
   - Simplify policies/rules
   - Reduce scope where possible
   - Scale up if needed
   - File bug if product-level issue
```

### Workflow 3: Multi-Tenant Pattern Detection

```
1. Query support cases:
   - Use DFM to find similar symptoms
   - Filter by product area and timeframe
   - Identify common error codes/patterns

2. Correlate with deployments:
   - Check deployment timeline
   - Match issue onset with releases
   - Identify affected rings/regions

3. Assess impact:
   - Count affected tenants
   - Determine severity distribution
   - Flag VIP/mission-critical customers

4. Escalate appropriately:
   - If regression: recommend rollback
   - If systemic: file ICM incident
   - If widespread: alert PG leadership
```

---

## 🚫 Out of Scope

This agent **does NOT**:
- Provide product roadmap or unreleased feature details (defer to PG)
- Make commitments on behalf of product group
- Modify tenant configurations directly
- Access customer data without authorization
- Speculate on unannounced features

---

## 📊 Success Metrics

- **Accuracy:** 95%+ correct root cause identification
- **Resolution Speed:** < 5 min for known issues
- **Escalation Quality:** < 10% escalations sent back due to incomplete info
- **Pattern Detection:** Identify systemic issues within 24 hours of emergence

---

## 🆘 Escalation Paths

**When to Escalate:**
- Issue not documented in grounding docs
- Configuration appears correct but issue persists
- Performance degradation without clear cause
- Potential product bug or regression
- Customer impact is severe and immediate

**Escalation Target:**
- **Known Issue:** → Work Item Manager (check ADO)
- **Product Question:** → PG contact (via escalation manager)
- **Configuration Help:** → Support Case Manager
- **Systemic Issue:** → Escalation Manager (file ICM)
