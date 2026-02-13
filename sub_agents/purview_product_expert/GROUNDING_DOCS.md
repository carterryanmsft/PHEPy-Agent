# Purview Product Expert - Grounding Documents

**Agent:** Purview Product Expert  
**Version:** 1.1  
**Last Updated:** February 5, 2026

---

## 🔗 Primary Authoritative Sources

The Purview Product Expert is grounded in authoritative Microsoft internal documentation:

### Internal Engineering Wikis & Repositories
1. **IP Engineering Core Wiki**  
   📍 `https://o365exchange.visualstudio.com/IP%20Engineering/_wiki/wikis/IP%20Engineering.wiki/15457/IP-Engineering-Core`  
   **Content:** Engineering architecture, design specs, feature implementation details, troubleshooting playbooks
   
2. **ASIM Security/Compliance Azure DevOps**  
   📍 `https://dev.azure.com/ASIM-Security/Compliance`  
   **Content:** Compliance engineering docs, security architecture, product roadmaps, known issues

3. **CxE Security Care CEM SharePoint**  
   📍 `https://microsoft.sharepoint.com/teams/CxE-Security-Care-CEM/`  
   **Content:** Support procedures, escalation workflows, customer engagement playbooks, PHE operations guides  
   **Access:** Requires Microsoft AAD authentication (manual extraction needed)

4. **Microsoft Learn (Public Documentation)**  
   📍 `https://learn.microsoft.com/en-us/purview/`  
   **Content:** Customer-facing product documentation, configuration guides, best practices

### Grounding Strategy
- **Internal wikis** → Engineering truth, architecture, root cause analysis
- **Azure DevOps** → Bugs, known issues, workarounds, fix timelines
- **CxE SharePoint** → Support procedures, escalation workflows, operational playbooks
- **Microsoft Learn** → Customer-facing capabilities, supported scenarios, licensing

---

## 📚 Curated Grounding Documents

This agent requires comprehensive product documentation to function effectively. Below is the complete list of grounding documents needed.

---

## 1. Core Product Architecture

### 1.1 Purview Service Overview
**File:** `grounding_docs/purview_product/purview_product_architecture.md`

**Required Content:**
- Complete service map (MIP, DLP, eDiscovery, IRM, DLM, Insider Risk, etc.)
- Component dependencies and data flows
- Integration points with Office, Azure AD, Exchange, SharePoint, Teams
- Deployment architecture (cloud vs on-prem, hybrid)

**Status:** 🟡 Needs Creation

---

### 1.2 Regional Availability Matrix
**File:** `grounding_docs/purview_product/regional_availability.md`

**Required Content:**
- Feature availability by region
- Commercial, GCC, GCC High, DoD, National Cloud support
- Feature parity gaps between clouds
- Roadmap for feature expansion (if available)

**Status:** 🟡 Needs Creation

---

### 1.3 Licensing & SKUs
**File:** `grounding_docs/purview_product/licensing_sku_matrix.md`

**Required Content:**
- E3 vs E5 vs A5 vs G5 feature comparison
- Compliance add-on SKUs
- Per-user vs tenant-level licensing
- Upgrade paths and migration considerations

**Status:** 🟡 Needs Creation

---

### 1.4 Scale Limits & Performance Thresholds
**File:** `grounding_docs/purview_product/scale_limits.md`

**Required Content:**
- Maximum items per search, export, hold
- Label, policy, rule count limits
- Tenant-level constraints
- Throttling thresholds
- Recommended sizing guidelines

**Status:** 🟡 Needs Creation

---

## 2. Service-Specific Guides

### 2.1 Microsoft Information Protection (MIP)
**File:** `grounding_docs/purview_product/mip_dip_guide.md`

**Required Content:**
- Label creation, configuration, scoping
- Auto-labeling rules and ML classifiers
- Office integration (Word, Excel, PowerPoint, Outlook, Teams)
- File Explorer and right-click integration
- Inheritance and precedence rules
- Encryption and RMS integration
- Custom permissions and co-authoring
- Migration from AIP to unified labeling

**Status:** 🟡 Needs Creation

---

### 2.2 Data Loss Prevention (DLP)
**File:** `grounding_docs/purview_product/dlp_policies_guide.md`

**Required Content:**
- Policy creation wizard walkthrough
- Location scoping (Exchange, SharePoint, Teams, Endpoint, On-prem)
- Sensitive info types (SIT) library and custom patterns
- Alert configuration and incident management
- User notifications and policy tips
- Policy precedence and conflict resolution
- Endpoint DLP deployment and management

**Status:** 🟡 Needs Creation

---

### 2.3 eDiscovery
**File:** `grounding_docs/purview_product/ediscovery_guide.md`

**Required Content:**
- Case creation and permissions
- Content search syntax and operators
- Legal hold application and removal
- Collection and review set workflows
- Export formats and options
- Advanced eDiscovery with AI/ML
- Compliance boundaries
- Search performance optimization

**Status:** 🟡 Needs Creation

---

### 2.4 Information Rights Management (IRM)
**File:** `grounding_docs/purview_product/irm_guide.md`

**Required Content:**
- RMS service activation
- Template creation and management
- Rights policy enforcement
- Office document protection
- External user access (B2B scenarios)
- Key management and escrow
- Decryption workflows

**Status:** 🟡 Needs Creation

---

### 2.5 Data Lifecycle Management (DLM)
**File:** `grounding_docs/purview_product/dlm_retention_guide.md`

**Required Content:**
- Retention policy vs retention label
- Multi-stage retention workflows
- Disposition review process
- Records management
- Preservation locks
- Retention precedence rules (holds > policies > labels)
- Event-based retention

**Status:** 🟡 Needs Creation

---

### 2.6 Insider Risk Management
**File:** `grounding_docs/purview_product/insider_risk_guide.md`

**Required Content:**
- Policy templates and indicators
- User risk scoring model
- Alert triage workflows
- Integration with HR connectors
- Privacy controls and data minimization
- Investigator roles and permissions
- Machine learning signal tuning

**Status:** 🟡 Needs Creation

---

### 2.7 Communication Compliance
**File:** `grounding_docs/purview_product/communication_compliance_guide.md`

**Required Content:**
- Policy creation for Teams/Email monitoring
- Offensive language and threat detection
- Custom keyword and regex patterns
- Reviewer workflows and escalation
- Integration with legal/HR
- Privacy and ethical considerations

**Status:** 🟡 Needs Creation

---

### 2.8 Content Explorer & Activity Explorer
**File:** `grounding_docs/purview_product/content_activity_explorer_guide.md`

**Required Content:**
- Label usage analytics
- DLP incident tracking
- User activity monitoring
- Dashboard and reporting features
- Data latency expectations (24-48 hours)
- Permission requirements for viewers

**Status:** 🟡 Needs Creation

---

## 3. Troubleshooting Resources

### 3.1 Known Issues Registry
**File:** `grounding_docs/purview_product/purview_known_issues.md`

**Required Content:**
- Categorized by service (MIP, DLP, eDiscovery, etc.)
- Issue description, symptoms, affected versions
- ADO bug number and status (Active, Fixed, By-Design)
- Workarounds and mitigation steps
- Fix ETA (if available)
- Last updated date

**Format Example:**
```markdown
## MIP Known Issues

### Issue: Labels not appearing in Outlook Mac (Build 16.55)
- **ADO #:** 12345678
- **Status:** Fixed in Build 16.56
- **Symptoms:** Sensitivity ribbon missing in Outlook
- **Workaround:** Manually update to 16.56 or use Outlook Web
- **ETA:** Available in Current Channel
- **Last Updated:** 2026-02-01
```

**Status:** 🟡 Needs Creation

---

### 3.2 Troubleshooting Playbooks
**File:** `grounding_docs/purview_product/purview_troubleshooting_playbooks.md`

**Required Content:**
- Step-by-step diagnostic workflows
- Common symptoms → root cause mapping
- Diagnostic commands and tools
- Log collection procedures
- Escalation criteria

**Status:** 🟡 Needs Creation

---

### 3.3 Error Code Reference
**File:** `grounding_docs/purview_product/error_codes.md`

**Required Content:**
- Complete error code catalog
- User-friendly explanations
- Common causes and remediation steps
- When to escalate vs self-resolve

**Status:** 🟡 Needs Creation

---

### 3.4 Performance Tuning Guide
**File:** `grounding_docs/purview_product/performance_tuning.md`

**Required Content:**
- Query optimization techniques
- Policy and rule simplification strategies
- Scale-out recommendations
- Throttling avoidance best practices
- Monitoring and alerting setup

**Status:** 🟡 Needs Creation

---

## 4. Best Practices & Guidance

### 4.1 Feature Adoption Strategy
**File:** `grounding_docs/purview_product/feature_adoption_guide.md`

**Required Content:**
- Phased rollout recommendations
- Pilot group sizing and selection
- Success metrics and KPIs
- Change management considerations
- Training and communication templates

**Status:** 🟡 Needs Creation

---

### 4.2 Policy Design Best Practices
**File:** `grounding_docs/purview_product/policy_design_best_practices.md`

**Required Content:**
- DLP policy design patterns
- Retention policy strategies
- Label taxonomy design
- Avoiding false positives
- Balancing security and usability

**Status:** 🟡 Needs Creation

---

### 4.3 Migration Guides
**File:** `grounding_docs/purview_product/migration_guides.md`

**Required Content:**
- AIP → Unified Labeling migration
- Legacy DLP → Modern DLP
- On-prem → Cloud migration
- Cross-tenant migration considerations

**Status:** 🟡 Needs Creation

---

## 5. Integration References

### 5.1 Office Integration
**File:** `grounding_docs/purview_product/office_integration.md`

**Required Content:**
- Word, Excel, PowerPoint integration
- Outlook desktop and web
- Teams protection
- OneDrive and SharePoint
- Mobile app support

**Status:** 🟡 Needs Creation

---

### 5.2 Third-Party Integrations
**File:** `grounding_docs/purview_product/third_party_integrations.md`

**Required Content:**
- API references
- SDK documentation
- Partner connectors
- Custom connector development

**Status:** 🟡 Needs Creation

---

## 📊 Grounding Doc Priority

### High Priority (Required for Basic Functionality)
1. ✅ `purview_product_architecture.md` - Service overview
2. ✅ `purview_known_issues.md` - Known issues registry
3. ✅ `mip_dip_guide.md` - MIP/labeling guide
4. ✅ `dlp_policies_guide.md` - DLP guide
5. ✅ `scale_limits.md` - Performance limits

### Medium Priority (Enhances Capabilities)
6. ✅ `ediscovery_guide.md` - eDiscovery guide
7. ✅ `dlm_retention_guide.md` - Retention guide
8. ✅ `regional_availability.md` - Cloud/region support
9. ✅ `troubleshooting_playbooks.md` - Diagnostic workflows
10. ✅ `error_codes.md` - Error reference

### Lower Priority (Nice to Have)
11. ⚪ `insider_risk_guide.md` - Insider Risk
12. ⚪ `communication_compliance_guide.md` - Comm Compliance
13. ⚪ `migration_guides.md` - Migration docs
14. ⚪ `feature_adoption_guide.md` - Adoption strategy

---

## 🔄 Document Maintenance

### Update Frequency
- **Known Issues:** Weekly (or as bugs are filed/resolved)
- **Feature Guides:** Monthly (or with major releases)
- **Architecture Docs:** Quarterly
- **Best Practices:** Quarterly

### Ownership
- **Content Owner:** Purview PG Documentation Team
- **Agent Maintainer:** PHE Operations
- **Review Cadence:** Monthly sync between teams

---

## 📝 Creating Missing Documents

### Template for New Grounding Docs

```markdown
# [Service/Feature Name] Guide

**Last Updated:** [Date]
**Owner:** [Team Name]
**Review Cadence:** [Frequency]

---

## Overview
[Brief description of service/feature]

## Key Capabilities
[Bullet list of what it does]

## Configuration
[Step-by-step setup instructions]

## Common Scenarios
[Use cases and examples]

## Troubleshooting
[Common issues and solutions]

## Known Limitations
[Documented constraints]

## References
[Links to official docs, ADO, etc.]
```

---

## 🆘 Temporary Fallbacks

**Until grounding docs are created:**
1. Use Microsoft Learn official documentation: https://learn.microsoft.com/purview
2. Search ADO for known bugs directly
3. Escalate to PG for undocumented scenarios
4. Clearly state "Not documented in grounding docs" when info is missing

**Never:**
- Fabricate information
- Speculate on features/timelines
- Provide outdated information without disclaimers
