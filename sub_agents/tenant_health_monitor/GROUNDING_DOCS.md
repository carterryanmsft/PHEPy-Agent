# Tenant Health Monitor - Grounding Documents

**Agent:** Tenant Health Monitor  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 📚 Required Grounding Documents

### 1. Customer & Tenant Registry

#### 1.1 Customer List Registry
**File:** `grounding_docs/customer_tenant_data/customer_list_registry.md`

**Required Content:**
- Customer name to TenantId mapping
- Customer tier (VIP, Enterprise, Standard)
- Revenue category
- Strategic importance flags
- Contact information (PM, Account Manager)
- Cohort assignment (MCS Alpha, IC Onboarding, etc.)

**Format:**
```markdown
| Customer Name | TenantId | Tier | Revenue Tier | Cohort | PM Owner |
|---------------|----------|------|--------------|--------|----------|
| Contoso | c990bb7a-... | VIP | Platinum | MCS Alpha | Jane Doe |
```

**Status:** ✅ Partial (CSV exists in contacts_access/IC and MCS 2.4.csv)

---

#### 1.2 Tenant Health Metrics Baseline
**File:** `grounding_docs/customer_tenant_data/tenant_health_metrics.md`

**Required Content:**
- Health score calculation formula
- Component score weights
- Baseline expectations by cohort
- Success criteria and KPIs
- Health score thresholds

**Status:** 🟡 Needs Creation

---

### 2. Cohort Definitions

#### 2.1 MCS/IC Cohort Registry
**File:** `grounding_docs/phe_program_operations/mcs_ic_cohort_registry.md`

**Required Content:**
- Cohort definitions (Alpha, Beta, Production, IC Onboarding, IC Exit)
- Tenant membership per cohort
- Cohort stage and expected timelines
- Success milestones per cohort
- Baseline health expectations

**Format:**
```markdown
## MCS Alpha Cohort

**Definition:** Early adopter pilot customers  
**Tenant Count:** 15  
**Onboarding Date:** 2025-Q4  
**Expected Duration:** 12 weeks  
**Success Criteria:**
- Health score > 80 by week 12
- All core features adopted
- Zero SLA breaches

**Tenant List:**
- Contoso (c990bb7a-51f4-439b-bd36-9c07fb1041c0)
- Fabrikam (...)
```

**Status:** 🟡 Needs Creation

---

### 3. Health Metric Definitions

#### 3.1 Adoption Metrics
**File:** `grounding_docs/customer_tenant_data/adoption_metrics.md`

**Required Content:**
- Active user definition and calculation
- Feature adoption rate formula
- Policy coverage calculation
- Label coverage methodology
- Baseline expectations

**Status:** 🟡 Needs Creation

---

#### 3.2 Support Health Metrics
**File:** `grounding_docs/customer_tenant_data/support_health_metrics.md`

**Required Content:**
- SLA definitions by priority
- SLA compliance calculation
- Case resolution time benchmarks
- Escalation rate thresholds
- Reopened case rate targets

**Status:** 🟡 Needs Creation

---

#### 3.3 Performance Metrics
**File:** `grounding_docs/customer_tenant_data/performance_metrics.md`

**Required Content:**
- Error rate thresholds
- Timeout rate acceptable ranges
- Operation latency SLAs
- Service availability targets
- Performance degradation criteria

**Status:** 🟡 Needs Creation

---

### 4. Alert & Escalation Rules

#### 4.1 Alert Definitions
**File:** `grounding_docs/customer_tenant_data/alert_rules.md`

**Required Content:**
- Critical alert conditions
- Warning alert conditions
- Info alert conditions
- Alert routing logic
- Escalation thresholds

**Format:**
```markdown
### Critical Alert: VIP Tenant at Risk

**Condition:** 
- Tenant tier = VIP
- Health score < 60 OR active P0/P1 ICM

**Routing:**
- Escalation Manager
- PHE PM
- Customer Success Manager

**SLA:** Respond within 1 hour
```

**Status:** 🟡 Needs Creation

---

#### 4.2 VIP Customer List
**File:** `grounding_docs/customer_tenant_data/vip_customer_list.md`

**Required Content:**
- List of VIP customers
- Special SLA requirements
- Escalation contacts
- Monitoring cadence
- Success criteria

**Status:** 🟡 Needs Creation

---

### 5. Kusto Query Library

#### 5.1 Standard Health Queries
**File:** `sub_agents/tenant_health_monitor/QUERY_PATTERNS.md`

**Required Content:**
- Pre-built queries for each health metric
- Query optimization notes
- Update frequencies
- Data source references

**Status:** ✅ Created (in this sub-agent folder)

---

### 6. Success Criteria & KPIs

#### 6.1 Onboarding Success Milestones
**File:** `grounding_docs/phe_program_operations/onboarding_milestones.md`

**Required Content:**
- Week-by-week onboarding milestones
- Expected health score progression
- Feature adoption timeline
- Configuration completeness checklist

**Format:**
```markdown
## MCS Onboarding Milestones

### Week 1-2: Setup
- Initial config complete
- Admin trained
- First policies deployed
- Expected Health Score: 40-50

### Week 3-4: Pilot
- Pilot group onboarded
- Labels applied to test content
- DLP policies tested
- Expected Health Score: 55-65
```

**Status:** 🟡 Needs Creation

---

### 7. Historical Benchmarks

#### 7.1 Historical Cohort Performance
**File:** `grounding_docs/customer_tenant_data/historical_benchmarks.md`

**Required Content:**
- Previous cohort health score averages
- Time to reach health score milestones
- Common challenges and resolutions
- Success patterns and best practices

**Status:** 🟡 Needs Creation

---

## 📊 Data Source Integration

### Kusto Clusters

| Cluster | Database | Tables Used | Access Required |
|---------|----------|-------------|-----------------|
| cxe-analytics.kusto.windows.net | CustomerHealth | PurviewActivityLogs, PurviewTelemetry | Reader |
| cxe-analytics.kusto.windows.net | AuditLogs | PurviewAuditLogs | Reader |
| cxe-analytics.kusto.windows.net | CustomerHealth | TenantHealthScores (if exists) | Reader |

---

### MCP Servers

| MCP Server | Purpose | Queries Used |
|------------|---------|--------------|
| **Enterprise MCP** | Support case data | GetSCIMIncidentV2 by TenantId |
| **ICM MCP** | Incident data | Get incidents by TenantId |
| **Kusto MCP** | Execute telemetry queries | All Kusto queries from QUERY_PATTERNS.md |

---

### APIs & Services

| Service | Endpoint | Data Retrieved | Auth Method |
|---------|----------|----------------|-------------|
| Purview Tenant Config | purview.microsoft.com/api | Feature enablement, policies | OAuth |
| Content Explorer | compliance.microsoft.com | Label coverage | OAuth |
| Azure Monitor | monitor.azure.com | Service availability | MSI |

---

## 🔄 Document Maintenance

### Update Frequency

| Document Type | Update Frequency | Owner |
|---------------|------------------|-------|
| Customer Registry | Weekly | PHE PM |
| Cohort Membership | Monthly | Program Manager |
| Alert Rules | Quarterly | PHE Operations |
| Success Criteria | Per-cohort | Program Manager |
| VIP List | Monthly | Customer Success |

---

### Version Control

All grounding documents should:
- Include "Last Updated" date
- Track version changes
- Document who made updates
- Include changelog at bottom

---

## 📝 Creating Missing Documents

### Priority 1: Essential for Basic Functionality

1. **tenant_health_metrics.md** - Health score formula
2. **mcs_ic_cohort_registry.md** - Cohort definitions
3. **vip_customer_list.md** - VIP monitoring
4. **alert_rules.md** - Alert conditions

### Priority 2: Enhances Accuracy

5. **adoption_metrics.md** - Metric definitions
6. **support_health_metrics.md** - SLA definitions  
7. **performance_metrics.md** - Performance thresholds
8. **onboarding_milestones.md** - Success criteria

### Priority 3: Provides Context

9. **historical_benchmarks.md** - Comparison data
10. **customer_list_registry.md** - Full customer details

---

## 🆘 Temporary Fallbacks

**Until grounding docs are created:**

1. **For health scores:** Use default formula from CAPABILITIES.md
2. **For cohorts:** Use existing CSV in contacts_access folder
3. **For VIP customers:** Flag any tenant with "VIP" or "Strategic" in name
4. **For alerts:** Use conservative thresholds (score < 60 = at risk)
5. **For baselines:** Use industry-standard adoption rates

**Important:**
- Always disclose when using defaults vs documented criteria
- Flag missing grounding docs as gaps
- Do NOT fabricate customer-specific thresholds
- Recommend creating proper grounding docs for accuracy

---

## 📚 External References

- **Microsoft Learn - Purview Analytics:** https://learn.microsoft.com/purview/analytics
- **Azure Monitor Documentation:** https://learn.microsoft.com/azure/azure-monitor
- **Customer Success Playbooks:** Internal SharePoint (link in grounding docs)

---

## 🔗 Related Agent Dependencies

### Shared Grounding Docs
- `CUSTOMER_LOOKUP_GUIDE.md` - Shared with all agents
- `IC and MCS 2.4.csv` - Shared customer registry

### Agent-Specific Cross-References
- **Support Case Manager** → Provides SLA definitions
- **Program Onboarding Manager** → Provides onboarding milestones
- **Purview Product Expert** → Provides performance baselines
