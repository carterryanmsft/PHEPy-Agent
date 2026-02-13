# Purview Product Expert - Master Index

**Last Updated:** February 5, 2026  
**Total Documents:** 15 core documents + expanding  
**Status:** 🟢 Active - Populated from Microsoft Learn

---

## 🚀 Quick Start - Answer These Questions Fast

### "Something is broken"
→ **[Troubleshooting Section](#troubleshooting-playbooks)**  
Common issues: [DLP Not Triggering](#dlp-policy-not-triggering) | [Labels Missing](#labels-not-appearing) | [eDiscovery Timeout](#ediscovery-search-timeout)

### "How do I configure X?"
→ **[Service Guides](#service-documentation)**  
Setup: [DLP Policies](services/dlp/overview.md) | [Sensitivity Labels](services/mip/sensitivity_labels.md) | [Retention Policies](services/dlm/retention_policies.md)

### "Is this a known bug?"
→ **[Known Issues](#known-issues-registry)**  
Check: [Active Bugs](known_issues/active_bugs.md) | [By-Design Behaviors](known_issues/by_design.md)

### "What are the limits?"
→ **[Core Documentation](#core-architecture--fundamentals)**  
See: [Scale Limits & Thresholds](core/scale_limits.md)

### "Is feature X supported in cloud Y?"
→ **[Regional Availability](core/regional_availability.md)**

---

## 📚 Complete Document Library

### Core Architecture & Fundamentals

| Document | Status | Source | Last Updated |
|----------|--------|--------|--------------|
| [Purview Architecture Overview](core/architecture.md) | 🟡 Needs Population | IP Wiki | Pending |
| [Scale Limits & Thresholds](core/scale_limits.md) | 🟡 Needs Population | IP Wiki | Pending |
| [Regional Availability Matrix](core/regional_availability.md) | 🟡 Needs Population | Learn + Wiki | Pending |
| [Licensing & SKU Comparison](core/licensing_matrix.md) | 🟡 Needs Population | Microsoft Learn | Pending |

---

### Service Documentation

#### Data Loss Prevention (DLP)
| Document | Status | Source | Last Updated |
|----------|--------|--------|--------------|
| [DLP Overview](services/dlp/overview.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [DLP Policy Design](services/dlp/policy_design.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Sensitive Information Types](services/dlp/sensitive_info_types.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Endpoint DLP](services/dlp/endpoint_dlp.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |

**Key Capabilities:**
- Monitor: Exchange, SharePoint, OneDrive, Teams, Endpoints, On-prem, Fabric, M365 Copilot
- Policy Types: Templates, Custom, Simulation Mode
- Actions: Block, Warn, Alert, Quarantine
- SITs: 500+ built-in, custom regex/patterns
- Locations: Cloud apps, On-premises, Network traffic

**Common Scenarios:**
- Prevent credit card/SSN sharing
- Block uploads to unmanaged cloud apps
- Protect data in Teams chat
- Monitor endpoint file operations
- Control M365 Copilot data access

---

#### Microsoft Information Protection (MIP)
| Document | Status | Source | Last Updated |
|----------|--------|--------|--------------|
| [MIP Overview](services/mip/overview.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Sensitivity Labels](services/mip/sensitivity_labels.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Auto-Labeling](services/mip/auto_labeling.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Encryption & Rights Management](services/mip/encryption.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |

**Key Capabilities:**
- Label Scopes: Files, Emails, Meetings, Groups & Sites
- Protection: Encryption, Watermarks, Headers/Footers
- Auto-labeling: ML classifiers, SITs, keywords
- Inheritance: Email attachments, SharePoint
- Integration: Office apps, File Explorer, PowerShell

**Label Priority:**
- Highly Confidential (highest)
- Confidential
- General
- Public (lowest)

**M365 Copilot Integration:**
- Labels recognized by Copilot
- EXTRACT usage right required
- Highest priority label selected

---

#### eDiscovery
| Document | Status | Source | Last Updated |
|----------|--------|--------|--------------|
| [eDiscovery Overview](services/ediscovery/overview.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Content Search](services/ediscovery/content_search.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Legal Hold Management](services/ediscovery/legal_hold.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Review Sets & Analysis](services/ediscovery/review_sets.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |

**Three Tiers:**
1. **Content Search**: Basic search & export
2. **eDiscovery (Standard)**: Cases + legal holds
3. **eDiscovery (Premium)**: Custodians, analytics, predictive coding

**Key Capabilities:**
- Search: Exchange, SharePoint, OneDrive, Teams, Groups
- Hold: Preserve content for litigation
- Collection: Copy to review sets
- Analytics: Near-duplicates, email threading, themes
- Export: PST, native files, metadata

---

#### Data Lifecycle Management (DLM)
| Document | Status | Source | Last Updated |
|----------|--------|--------|--------------|
| [DLM Overview](services/dlm/overview.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Retention Policies](services/dlm/retention_policies.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Retention Labels](services/dlm/retention_labels.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Disposition & Records](services/dlm/disposition.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |

**Core Features:**
- Retention Policies: Org-wide, location-based
- Retention Labels: Item-level, user/auto-applied
- Adaptive Protection: Insider risk integration
- Archive Mailboxes: 100GB+ with auto-expansion
- Inactive Mailboxes: Preserve after employee departure

**Precedence Rules:**
1. Legal holds (highest)
2. Retention policies
3. Retention labels (lowest)

---

#### Audit & Compliance Logging
| Document | Status | Source | Last Updated |
|----------|--------|--------|--------------|
| [Audit Overview](services/audit/overview.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Audit Search & Investigation](services/audit/search.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Audit Log Retention](services/audit/retention.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |

**Audit Tiers:**
- **Audit (Standard)**: 180-day retention, enabled by default
- **Audit (Premium)**: 1-year retention, 10-year add-on available

**Key Events:**
- Exchange: MailItemsAccessed, Send, SendAs
- SharePoint: FileAccessed, FileModified, FileDeleted
- Teams: MessageSent, MeetingCreated, ChatCreated
- Azure AD: UserLoggedIn, ConsentToApplication

**APIs:**
- Audit Search Graph API
- Search-UnifiedAuditLog PowerShell
- Office 365 Management Activity API

---

#### Insider Risk Management
| Document | Status | Source | Last Updated |
|----------|--------|--------|--------------|
| [IRM Overview](services/irm/overview.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Policy Templates](services/irm/policy_templates.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |
| [Forensic Evidence](services/irm/forensic_evidence.md) | ✅ Populated | Microsoft Learn | 2026-02-05 |

**Policy Templates:**
- Data theft by departing users
- Data leaks (general, priority users, risky users)
- Security policy violations
- Patient data misuse (healthcare)
- Risky AI usage
- Risky browser usage

**Workflow:**
1. Policies → 2. Alerts → 3. Triage → 4. Investigate → 5. Action

**Integrations:**
- HR Connector (terminations, performance reviews)
- eDiscovery (Premium) escalation
- Communication Compliance
- DLP alerts

---

### Support Operations & Escalation Procedures

| Document | Status | Source | Last Updated |
|----------|--------|--------|--------------|
| [Escalation Workflows](operations/escalation_workflows.md) | 🟡 Needs Manual Extract | CxE SharePoint | Pending |
| [Support Procedures](operations/support_procedures.md) | 🟡 Needs Manual Extract | CxE SharePoint | Pending |
| [Customer Engagement Playbooks](operations/customer_engagement.md) | 🟡 Needs Manual Extract | CxE SharePoint | Pending |
| [PHE Operations Guide](operations/phe_operations.md) | 🟡 Needs Manual Extract | CxE SharePoint | Pending |
| [Incident Management](operations/incident_management.md) | 🟡 Needs Manual Extract | CxE SharePoint | Pending |
| [SLA & Response Times](operations/sla_guidelines.md) | 🟡 Needs Manual Extract | CxE SharePoint | Pending |

**Key Procedures:**
- Escalation by severity (Sev 0, 1, 2, 3)
- Handoff between CSS → PG
- Customer communication templates
- Ticket routing and assignment
- War room procedures

---

### Troubleshooting Playbooks

| Playbook | Severity | Service | Status |
|----------|----------|---------|--------|
| [DLP Policy Not Triggering](troubleshooting/playbooks/dlp_not_triggering.md) | 🔴 High | DLP | Template Ready |
| [Labels Not Appearing](troubleshooting/playbooks/labels_not_appearing.md) | 🔴 High | MIP | Template Ready |
| [eDiscovery Search Timeout](troubleshooting/playbooks/ediscovery_timeout.md) | 🟡 Medium | eDiscovery | Template Ready |
| [Retention Not Applied](troubleshooting/playbooks/retention_not_applied.md) | 🟡 Medium | DLM | Template Ready |
| [Policy Sync Delay](troubleshooting/playbooks/policy_sync_delay.md) | 🟡 Medium | All | Template Ready |
| [Audit Log Latency](troubleshooting/playbooks/audit_log_latency.md) | 🟢 Low | Audit | Template Ready |
| [Teams Protection Not Working](troubleshooting/playbooks/teams_protection.md) | 🔴 High | DLP/MIP | Template Ready |
| [Endpoint DLP Issues](troubleshooting/playbooks/endpoint_dlp.md) | 🔴 High | DLP | Template Ready |
| [Label Inheritance Problems](troubleshooting/playbooks/label_inheritance.md) | 🟡 Medium | MIP | Template Ready |
| [Performance Degradation](troubleshooting/playbooks/performance_degradation.md) | 🔴 High | All | Template Ready |

---

### Known Issues Registry

| Category | Document | Source | Status |
|----------|----------|--------|--------|
| Active Bugs | [Active Issues List](known_issues/active_bugs.md) | ADO | 🟡 Needs ADO Sync |
| By-Design | [Expected Behaviors](known_issues/by_design.md) | IP Wiki | 🟡 Needs Population |
| Workarounds | [Temporary Fixes](known_issues/workarounds.md) | ADO + Wiki | 🟡 Needs Population |
| Recently Fixed | [Resolved Issues](known_issues/fixed_recently.md) | ADO | 🟡 Needs ADO Sync |

**Update Frequency:** Weekly (automated from ADO)

---

## 🔍 Search by Keyword

### Symptoms
- **"Not working"** → [Troubleshooting Playbooks](#troubleshooting-playbooks)
- **"Slow" / "Performance"** → [Performance Degradation](troubleshooting/playbooks/performance_degradation.md)
- **"Error"** → [Error Code Reference](troubleshooting/error_codes.md)
- **"Missing" / "Not appearing"** → [Label Troubleshooting](troubleshooting/playbooks/labels_not_appearing.md)
- **"Timeout"** → [eDiscovery Timeout](troubleshooting/playbooks/ediscovery_timeout.md)
- **"Delay"** → [Policy Sync Delay](troubleshooting/playbooks/policy_sync_delay.md)

### Configuration Tasks
- **"Create policy"** → DLP: [Policy Design](services/dlp/policy_design.md)
- **"Enable labels"** → MIP: [Sensitivity Labels](services/mip/sensitivity_labels.md)
- **"Set up eDiscovery"** → [eDiscovery Overview](services/ediscovery/overview.md)
- **"Configure retention"** → DLM: [Retention Policies](services/dlm/retention_policies.md)
- **"Enable audit"** → Audit: [Overview](services/audit/overview.md)

### Features
- **"Encryption"** → MIP: [Encryption & RMS](services/mip/encryption.md)
- **"Watermark"** → MIP: [Content Markings](services/mip/sensitivity_labels.md)
- **"Legal hold"** → eDiscovery: [Legal Hold](services/ediscovery/legal_hold.md)
- **"Auto-label"** → MIP: [Auto-Labeling](services/mip/auto_labeling.md)
- **"Policy tip"** → DLP: [User Notifications](services/dlp/policy_design.md)

---

## 📊 Document Status Summary

### ✅ Populated (11 documents)
- All service overviews from Microsoft Learn
- DLP, MIP, eDiscovery, DLM, Audit, IRM core docs

### 🟡 Templates Ready / Needs Population (16+ documents)
- Troubleshooting playbooks (10) - Awaiting IP Wiki content
- Support operations (6) - Awaiting CxE SharePoint extraction
- Core architecture - Awaiting IP Wiki content

### 🔴 Needs Population (15+ docs)
- Known issues (ADO sync required)
- Scale limits (IP Wiki required)
- Regional availability (Learn + Wiki)

---

## 🎯 Priority Population Order

### Week 1 (High Priority)
1. ✅ **Microsoft Learn Content** - COMPLETE
2. 🟡 **Troubleshooting Playbooks** - Templated, needs IP Wiki content
3. 🔴 **Known Issues** - Needs ADO query setup
4. 🔴 **Scale Limits** - Needs IP Wiki extraction

### Week 2 (Medium Priority)
5. Core Architecture
6. Regional Availability
7. Licensing Matrix
8. Error Code Reference

### Week 3 (Lower Priority)
9. Integration guides
10. Best practices
11. Migration guides

---

## 🔗 External References

### Primary Sources
1. **Microsoft Learn**: `https://learn.microsoft.com/en-us/purview/`
2. **IP Engineering Wiki**: `https://o365exchange.visualstudio.com/IP%20Engineering/_wiki/`
3. **ASIM Compliance ADO**: `https://dev.azure.com/ASIM-Security/Compliance`
4. **CxE Security Care CEM**: `https://microsoft.sharepoint.com/teams/CxE-Security-Care-CEM/` (Auth Required)

### Quick Links
- [Purview Portal](https://purview.microsoft.com/)
- [Microsoft 365 Roadmap](https://www.microsoft.com/microsoft-365/roadmap?filters=Microsoft%20Information%20Protection)
- [Tech Community](https://techcommunity.microsoft.com/t5/security-compliance-and-identity/ct-p/MicrosoftSecurityandCompliance)

---

## 🔄 Maintenance Schedule

| Task | Frequency | Owner | Next Due |
|------|-----------|-------|----------|
| Sync Microsoft Learn | Monthly | Automated Script | 2026-03-05 |
| Update Known Issues | Weekly | ADO Sync | 2026-02-12 |
| Review Troubleshooting | Quarterly | PHE Ops | 2026-05-05 |
| Architecture Updates | Quarterly | PG Docs | 2026-05-05 |

---

## 📝 How to Use This Index

### For Purview Product Expert Agent
1. Start here for all queries
2. Use keyword search to find relevant docs
3. Follow cross-references for deeper context
4. Cite sources in responses (Microsoft Learn, IP Wiki, ADO)

### For Content Maintainers
1. Update "Last Updated" dates when refreshing content
2. Change status from 🟡 to ✅ when populating
3. Add new documents and update totals
4. Keep external links current

### For Users
1. Quick Start section → Fast answers
2. Keyword search → Find by symptom
3. Service Guides → Learn features
4. Troubleshooting → Fix problems

---

**🎉 Phase 1 Complete**: Microsoft Learn content populated  
**📅 Next Milestone**: Populate troubleshooting playbooks from IP Wiki  
**🔜 Coming Soon**: ADO known issues sync automation
