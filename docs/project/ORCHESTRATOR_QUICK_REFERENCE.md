# Orchestrator Optimization Quick Reference

**Version:** 2.0 | **Date:** February 4, 2026

---

## ⚡ 5-Second Rule
**Before any query:** Can I answer this from cache or previous context?

---

## 🎯 Request Classification

| Type | Time Goal | Strategy | Example |
|------|-----------|----------|---------|
| **SIMPLE** | < 5s | Direct route, single agent | "Ford case count" |
| **MEDIUM** | < 15s | Sequential with context sharing | "Cases + ICMs for Ford" |
| **COMPLEX** | < 30s | Parallel execution + synthesis | "Full health report" |

---

## 🚀 Quick Wins

### 1. Customer Lookup (Use Cache!)
```
✅ FAST: Check session cache → TenantId instant
❌ SLOW: Read CSV every time → 5+ seconds
```

### 2. Query Patterns (Use Templates!)
```
✅ FAST: Copy from QUERY_CHEAT_SHEET.md
❌ SLOW: Construct query from scratch
```

### 3. Filters (Pre-built!)
```
✅ FAST: Apply COMMON_FILTERS.md patterns
❌ SLOW: Figure out filters each time
```

### 4. Parallel Queries (When Independent!)
```
✅ FAST: Launch all 3 queries at once → Wait 6s
❌ SLOW: Execute serially → Wait 18s
```

---

## 📋 Pre-Query Checklist

```
[ ] Complexity classified?
[ ] TenantId in cache or need lookup?
[ ] Pre-built query pattern available?
[ ] Standard filters ready?
[ ] Parallel execution possible?
[ ] Fallback strategy defined?
```

---

## 🔄 Execution Patterns

### Simple Query Flow
```
Request → Cache lookup → Pre-built query → Execute → Response
Estimated: 2-5 seconds
```

### Medium Query Flow
```
Request → Agent 1 → Cache results → Agent 2 (reuse) → Synthesis
Estimated: 8-15 seconds
```

### Complex Query Flow
```
Request → [Agent A | Agent B | Agent C] (parallel) → Synthesis
Estimated: 12-30 seconds
```

---

## 🛡️ Error Handling Cascade

```
Primary: Live Query
   ↓ Failed?
Level 2: Cache (< 1 hour old)
   ↓ Failed?
Level 3: Static CSV
   ↓ Failed?
Level 4: Partial Results
   ↓ Nothing?
Level 5: Actionable Guidance
```

**Never return empty error! Always provide value.**

---

## 📊 Session Cache Contents

| Item | Source | Lifetime | Purpose |
|------|--------|----------|---------|
| Customer Registry | CSV | Session | TenantId lookups |
| Common Filters | .md | Session | Query optimization |
| Query Patterns | .md | Session | Template access |
| Recent Queries | Results | 5-15 min | Avoid re-querying |

---

## ⚡ Performance Shortcuts

### For Case Counts (Most Common!)
1. Check cache: `tenant_id:Ford` → Got TenantId? ✅
2. Use Query #1 from cheat sheet
3. Execute → Done in 2-3 seconds

### For Multi-Customer Queries
1. Batch TenantIds: `IN (X, Y, Z)`
2. Single query instead of N queries
3. 10x faster than sequential

### For Health Reports
1. Identify independent sources (Cases, ICMs, ADO)
2. Launch all parallel
3. Wait for slowest (not sum of all)
4. 3x faster than sequential

---

## 🎯 Agent Selection Speed Guide

| Request Contains | Route To | Time |
|------------------|----------|------|
| "cases" only | Support Case Manager | Direct |
| "icm" / "incident" | Escalation Manager | Direct |
| "ado" / "bug" | Work Item Manager | Direct |
| "cases + icm" | Sequential (2 agents) | Medium |
| "full health" | Parallel (all agents) | Complex |

---

## 📈 Success Metrics

**Are you hitting these targets?**
- Simple queries: < 5 seconds ✅
- Cache hit rate: > 60% ✅
- Token usage: < 15K/request ✅
- Error rate: < 5% ✅
- User satisfaction: High ✅

---

## 🚨 Common Mistakes

### ❌ DON'T:
1. Read CSV multiple times in same session
2. Execute queries sequentially when parallel possible
3. Load full agent instructions for simple queries
4. Return errors without fallback attempts
5. Search by CustomerName (unreliable)

### ✅ DO:
1. Cache customer registry in session
2. Parallelize independent operations
3. Use query patterns for simple requests
4. Always try fallback strategies
5. Search by TenantId (reliable)

---

## 📚 Essential Resources

**Load once per session:**
- [CUSTOMER_LOOKUP_GUIDE.md](../grounding_docs/contacts_access/CUSTOMER_LOOKUP_GUIDE.md)
- [QUERY_CHEAT_SHEET.md](../QUERY_CHEAT_SHEET.md)
- [COMMON_FILTERS.md](../sub_agents/kusto_expert/COMMON_FILTERS.md)

**Reference as needed:**
- [ORCHESTRATOR_PERFORMANCE_GUIDE.md](ORCHESTRATOR_PERFORMANCE_GUIDE.md) - Full details
- [ORCHESTRATOR_OPTIMIZATION_PLAN.md](ORCHESTRATOR_OPTIMIZATION_PLAN.md) - Strategy

---

## 💡 Pro Tips

1. **Pre-load session cache** at start of conversation
2. **Reuse TenantIds** from previous queries in conversation
3. **Batch customer queries** when possible (single query with IN)
4. **Time-box slow queries** (60s timeout)
5. **Deliver partial results** rather than waiting for everything

---

## 🔍 Debugging Slow Performance

**If query taking > 30 seconds:**

1. **Check:** Are you querying sequentially? → Parallelize
2. **Check:** Loading unnecessary context? → Prune
3. **Check:** Re-reading customer CSV? → Use cache
4. **Check:** Missing standard filters? → Add noise reduction
5. **Check:** Timeout too generous? → Reduce to 60s

---

## ✅ Quick Validation

**Before responding to user:**
- [ ] Response time within target for complexity?
- [ ] Used cached data when appropriate?
- [ ] Applied standard filters?
- [ ] Executed parallel when possible?
- [ ] Included performance metadata in response?

---

**Remember:** Every second counts! User expects fast, accurate responses.

**Target:** 70% of queries under 5 seconds ⚡
