# Program Onboarding Manager - Test Scenarios & Grounding Docs

**Agent:** Program Onboarding Manager  
**Version:** 1.0  
**Last Updated:** February 4, 2026

---

## 🧪 Key Test Scenarios

### Test 1: Cohort Status Query
**Prompt:** "What's the status of MCS Alpha cohort?"

**Expected:** Phase, milestone completion %, at-risk tenants, next milestones

**Success Criteria:** ✅ Retrieves from cohort registry, ✅ Provides actionable summary

---

### Test 2: Blocker Identification
**Prompt:** "Why is Contoso's onboarding delayed?"

**Expected:** Identify specific blockers, escalation recommendations, timeline impact

**Success Criteria:** ✅ Root cause analysis, ✅ Actionable next steps

---

### Test 3: Go-Live Readiness
**Prompt:** "Is Fabrikam ready to go live next week?"

**Expected:** Checklist validation, confidence score, risk assessment, recommendation

**Success Criteria:** ✅ Objective assessment, ✅ Clear go/no-go recommendation

---

## 📚 Required Grounding Documents

### 1. Cohort Registry
**File:** `grounding_docs/phe_program_operations/mcs_ic_cohort_registry.md`
- Cohort definitions, tenant membership, timelines, owners
- **Status:** 🟡 Needs Creation

### 2. Onboarding Runbook
**File:** `grounding_docs/phe_program_operations/phe_onboarding_runbook.md`
- Phase definitions, milestones, deliverables, gate criteria
- **Status:** 🟡 Needs Creation

### 3. Comms Templates
**File:** `grounding_docs/phe_program_operations/comms_templates.md`
- Kickoff, weekly update, risk alert, completion templates
- **Status:** 🟡 Needs Creation

### 4. Lifecycle Cadences
**File:** `grounding_docs/phe_program_operations/lifecycle_cadences.md`
- Meeting schedules, review cadences, reporting timelines
- **Status:** 🟡 Needs Creation

### 5. Roles & Responsibilities
**File:** `grounding_docs/phe_program_operations/roles_responsibilities_matrix.md`
- RACI matrix for onboarding activities
- **Status:** 🟡 Needs Creation

---

## 💡 Example Prompts

```
What's the status of [MCS Alpha / IC Onboarding / MCS Production] cohort?
```

```
Is [customer/tenant] on track for go-live?
```

```
What are the blockers for [cohort/customer]?
```

```
Show me onboarding progress for all active cohorts
```

```
Which tenants need attention this week?
```

```
What communication templates should I use for [situation]?
```

---

## 🔗 Related Agents

- **Tenant Health Monitor** - Tracks adoption and health metrics
- **Support Case Manager** - Monitors support load during onboarding
- **Contacts & Escalation Finder** - Program PM contacts
