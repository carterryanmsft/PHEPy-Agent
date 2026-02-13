# Purview Product Expert - Content Organization Structure

**Version:** 1.0  
**Last Updated:** February 5, 2026  
**Purpose:** Define how grounding content is organized, indexed, and accessed

---

## 📁 Directory Structure

```
sub_agents/purview_product_expert/
│
├── AGENT_INSTRUCTIONS.md          # Agent behavior & responsibilities
├── CAPABILITIES.md                # What the agent can do
├── EXAMPLE_PROMPTS.md             # Sample questions & responses
├── GROUNDING_DOCS.md              # This file - content sources
├── TEST_SCENARIOS.md              # Test cases for validation
├── CONTENT_EXTRACTION_GUIDE.md    # How to extract from sources (NEW)
├── SEARCH_QUERIES.md              # Pre-defined search templates (NEW)
├── ORGANIZATION_STRUCTURE.md      # This file (NEW)
│
└── grounding_docs/                # Actual grounding content
    └── purview_product/
        │
        ├── 00_INDEX.md            # Master index (directory of all docs)
        │
        ├── core/                  # Core architecture & fundamentals
        │   ├── architecture.md
        │   ├── scale_limits.md
        │   ├── regional_availability.md
        │   └── licensing_matrix.md
        │
        ├── services/              # Per-service deep dives
        │   ├── dlp/
        │   │   ├── overview.md
        │   │   ├── policy_design.md
        │   │   ├── sensitive_info_types.md
        │   │   └── endpoint_dlp.md
        │   ├── mip/
        │   │   ├── overview.md
        │   │   ├── sensitivity_labels.md
        │   │   ├── auto_labeling.md
        │   │   └── encryption.md
        │   ├── ediscovery/
        │   │   ├── overview.md
        │   │   ├── content_search.md
        │   │   ├── legal_hold.md
        │   │   └── review_sets.md
        │   ├── dlm/
        │   │   ├── overview.md
        │   │   ├── retention_policies.md
        │   │   ├── retention_labels.md
        │   │   └── disposition.md
        │   └── audit/
        │       ├── overview.md
        │       └── audit_search.md
        │
        ├── troubleshooting/       # Diagnostic & resolution guides
        │   ├── playbooks/
        │   │   ├── dlp_not_triggering.md
        │   │   ├── labels_not_appearing.md
        │   │   ├── ediscovery_timeout.md
        │   │   ├── retention_not_applied.md
        │   │   └── performance_degradation.md
        │   ├── error_codes.md
        │   └── diagnostic_commands.md
        │
        ├── known_issues/          # Bugs & limitations
        │   ├── active_bugs.md
        │   ├── by_design.md
        │   ├── workarounds.md
        │   └── fixed_recently.md
        │
        ├── integration/           # Integration & API docs
        │   ├── office_apps.md
        │   ├── teams.md
        │   ├── sharepoint.md
        │   ├── exchange.md
        │   ├── powershell.md
        │   └── rest_api.md
        │
        ├── best_practices/        # Guidance & recommendations
        │   ├── policy_design.md
        │   ├── feature_adoption.md
        │   ├── performance_tuning.md
        │   └── migration_guides.md
        │
        └── reference/             # Quick reference materials
            ├── glossary.md
            ├── acronyms.md
            ├── links.md
            └── contacts.md        # PG squad contacts (separate from this)
```

---

## 🗂️ Master Index Structure

**File:** `grounding_docs/purview_product/00_INDEX.md`

```markdown
# Purview Product Expert - Master Index

**Last Updated:** [Auto-generated date]  
**Total Documents:** [Auto-counted]

---

## 📚 Quick Navigation

### By User Intent
- [I need to configure something](#configuration-guides)
- [Something is broken](#troubleshooting)
- [Is this a known bug?](#known-issues)
- [What are the limits?](#scale-and-limits)
- [How does it work?](#architecture)

### By Service
- [DLP (Data Loss Prevention)](#dlp-documentation)
- [MIP (Information Protection)](#mip-documentation)
- [eDiscovery](#ediscovery-documentation)
- [DLM (Lifecycle Management)](#dlm-documentation)
- [Audit](#audit-documentation)

### By Problem Type
- [Performance Issues](#performance-troubleshooting)
- [Configuration Problems](#configuration-troubleshooting)
- [Integration Issues](#integration-troubleshooting)

---

## 📖 Complete Document List

### Core Architecture & Fundamentals
1. [Purview Architecture Overview](core/architecture.md)
2. [Scale Limits & Thresholds](core/scale_limits.md)
3. [Regional Availability Matrix](core/regional_availability.md)
4. [Licensing & SKU Comparison](core/licensing_matrix.md)

### DLP Documentation
1. [DLP Overview](services/dlp/overview.md)
2. [DLP Policy Design](services/dlp/policy_design.md)
3. [Sensitive Information Types](services/dlp/sensitive_info_types.md)
4. [Endpoint DLP](services/dlp/endpoint_dlp.md)

[... continue for all services ...]

### Troubleshooting Playbooks
1. [DLP Policy Not Triggering](troubleshooting/playbooks/dlp_not_triggering.md)
2. [Labels Not Appearing](troubleshooting/playbooks/labels_not_appearing.md)
[... etc ...]

---

## 🔍 Search by Keyword

### By Symptom
- **"Not working"** → See [Troubleshooting Playbooks](#troubleshooting-playbooks)
- **"Slow" / "Performance"** → See [Performance Tuning](best_practices/performance_tuning.md)
- **"Error"** → See [Error Code Reference](troubleshooting/error_codes.md)
- **"Missing" / "Not appearing"** → See [Label Troubleshooting](troubleshooting/playbooks/labels_not_appearing.md)

### By Configuration Task
- **"Create policy"** → DLP: [Policy Design](services/dlp/policy_design.md)
- **"Enable labels"** → MIP: [Sensitivity Labels](services/mip/sensitivity_labels.md)
- **"Set up eDiscovery"** → [eDiscovery Overview](services/ediscovery/overview.md)
- **"Configure retention"** → DLM: [Retention Policies](services/dlm/retention_policies.md)

---

## 📊 Document Metadata

Each document includes:
- **Source:** IP Wiki / ADO / Microsoft Learn
- **Last Updated:** Date of last refresh
- **Confidence Level:** High / Medium / Low
- **Review Cadence:** Weekly / Monthly / Quarterly
- **Owner:** Squad responsible for content

---

## 🔄 Update Log
[Most recent updates appear at top]

| Date | Document | Change | Updated By |
|------|----------|--------|------------|
| 2026-02-05 | dlp_not_triggering.md | Added ADO #12345 workaround | PHE Ops |
| 2026-02-04 | scale_limits.md | Updated DLP policy max count | PG Docs |
```

---

## 📄 Document Template

**File:** `grounding_docs/purview_product/TEMPLATE.md`

```markdown
# [Document Title]

**Service:** DLP / MIP / eDiscovery / DLM / Audit  
**Category:** Overview / Configuration / Troubleshooting / Best Practice  
**Last Updated:** YYYY-MM-DD  
**Source:** IP Wiki / ADO / Microsoft Learn  
**Confidence Level:** 🟢 High / 🟡 Medium / 🔴 Low  
**Review Cadence:** Weekly / Monthly / Quarterly

---

## Overview
[Brief description of what this document covers]

---

## Key Concepts
[Important terms and definitions]

---

## Main Content
[The actual guidance, steps, or reference material]

---

## Common Issues
[Links to related troubleshooting playbooks]

---

## Related Documents
- [Link to related doc 1]
- [Link to related doc 2]

---

## External References
1. [Microsoft Learn - Title](URL)
2. [IP Engineering Wiki - Title](URL)
3. [ADO Work Item #ID](URL)

---

## Metadata
- **Content Owner:** [Squad name]
- **Technical Reviewer:** [PM/Engineer name]
- **Next Review Date:** YYYY-MM-DD
- **Change History:**
  - YYYY-MM-DD: [Description of change]
```

---

## 🏷️ Tagging & Classification

### Service Tags
- `#DLP` - Data Loss Prevention
- `#MIP` - Information Protection
- `#eDiscovery` - eDiscovery & Search
- `#DLM` - Data Lifecycle Management
- `#Audit` - Audit & Compliance
- `#IRM` - Insider Risk Management
- `#CommComp` - Communication Compliance

### Category Tags
- `#Architecture` - Design & components
- `#Configuration` - Setup guides
- `#Troubleshooting` - Problem resolution
- `#KnownIssue` - Bugs & limitations
- `#BestPractice` - Recommended patterns
- `#Integration` - APIs & connectors
- `#Performance` - Scale & optimization
- `#Licensing` - SKU & entitlements

### Priority Tags
- `#P0-Critical` - Blocking issues
- `#P1-High` - Major impact
- `#P2-Medium` - Standard priority
- `#P3-Low` - Minor issues

### Status Tags
- `#Active` - Current information
- `#Deprecated` - Outdated (keep for reference)
- `#Preview` - In preview/testing
- `#Draft` - Work in progress

---

## 🔗 Cross-Referencing Strategy

### Automatic Cross-References
When mentioning other services/features, auto-link to their doc:
```markdown
See also: [DLP Policy Design](services/dlp/policy_design.md)
```

### Related Issues
Link troubleshooting to known issues:
```markdown
**Known Issues:** See [ADO #12345](known_issues/active_bugs.md#12345)
```

### Prerequisite Docs
Show learning path:
```markdown
**Prerequisites:**
1. Read [Purview Architecture](core/architecture.md) first
2. Understand [Scale Limits](core/scale_limits.md)
```

---

## 📊 Content Health Metrics

### Freshness Score
- 🟢 **Fresh** (< 30 days): Content is current
- 🟡 **Stale** (30-90 days): Consider review
- 🔴 **Outdated** (> 90 days): Needs update

### Completeness Score
- ✅ **Complete** (100%): All sections filled
- 🔄 **In Progress** (50-99%): Missing sections
- ❌ **Stub** (< 50%): Placeholder only

### Usage Tracking
Track which docs are accessed most by agent queries:
```
Top 10 Most-Accessed Docs (Last 30 Days):
1. dlp_not_triggering.md - 142 queries
2. labels_not_appearing.md - 98 queries
3. scale_limits.md - 87 queries
...
```

---

## 🔄 Content Lifecycle

### 1. Content Creation
- Extract from authoritative source
- Apply template
- Add metadata & tags
- Cross-reference related docs
- Review for accuracy

### 2. Content Review
- **Weekly:** Known issues, active bugs
- **Monthly:** Feature guides, configuration
- **Quarterly:** Architecture, best practices

### 3. Content Update
- Monitor source for changes
- Flag outdated content
- Update and re-review
- Update "Last Updated" date

### 4. Content Retirement
- Mark as `#Deprecated`
- Add redirect to new content
- Keep for historical reference (6 months)
- Archive after retention period

---

## 🎯 Agent Integration

### How Agent Uses This Structure

1. **User asks question** → Identify intent (troubleshoot / configure / known issue)
2. **Search 00_INDEX.md** → Find relevant documents by tag/keyword
3. **Read relevant docs** → Extract answer
4. **Cite sources** → Provide links to grounding docs + external sources
5. **Cross-reference** → Suggest related docs for deeper learning

### Agent Query Flow
```
User: "Why is my DLP policy not triggering?"
  ↓
Agent searches: 00_INDEX.md for "#DLP #Troubleshooting #NotWorking"
  ↓
Agent finds: troubleshooting/playbooks/dlp_not_triggering.md
  ↓
Agent reads playbook, finds diagnostic steps
  ↓
Agent checks: known_issues/active_bugs.md for related bugs
  ↓
Agent responds with answer + citations + related docs
```

---

## 🚀 Quick Start: Using This Structure

### For Content Creators
1. Use `TEMPLATE.md` for new documents
2. Tag appropriately
3. Add to `00_INDEX.md`
4. Cross-reference related docs
5. Set review cadence

### For Agent Developers
1. Start queries at `00_INDEX.md`
2. Use tags for filtering
3. Follow cross-references
4. Cite sources in responses
5. Track usage metrics

### For Product Experts
1. Review content monthly
2. Update from source systems
3. Flag outdated content
4. Provide SME review
5. Maintain accuracy

---

## 📝 Content Contribution Guidelines

### Adding New Content
1. Extract from authoritative source
2. Apply template
3. Add unique filename
4. Update 00_INDEX.md
5. Submit for review

### Updating Existing Content
1. Preserve existing structure
2. Update "Last Updated" date
3. Add change note
4. Re-review for accuracy

### Removing Content
1. Mark as `#Deprecated`
2. Add redirect note
3. Schedule for archive
4. Notify stakeholders

---

## ✅ Quality Checklist

Before publishing any grounding doc:
- [ ] Template applied correctly
- [ ] Metadata complete
- [ ] Tags added
- [ ] Cross-references added
- [ ] Indexed in 00_INDEX.md
- [ ] Source cited
- [ ] Technical review done
- [ ] Markdown formatting correct
- [ ] No broken links
- [ ] Review cadence set

---

## 📞 Content Governance

**Content Owners:**
- Core Architecture: IP Engineering PG
- Service Guides: Individual squad leads
- Troubleshooting: PHE Operations + PG
- Known Issues: ADO → PHE Ops sync
- Best Practices: PG + CEM collaboration

**Review Board:**
- Monthly sync: PHE Ops + PG Docs
- Quarterly review: Squad leads + PMs
- Ad-hoc: As needed for critical updates
