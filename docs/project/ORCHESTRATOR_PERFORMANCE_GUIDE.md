# Enhanced Orchestrator Instructions - Performance Optimizations

**Version:** 2.0  
**Date:** February 4, 2026  
**Focus:** Speed, Efficiency, Smart Delegation

---

## 🚀 Core Performance Principles

### 1. Think Before You Query
**Before executing any query:**
1. Check if data is already in context (previous query result)
2. Determine request complexity (simple/medium/complex)
3. Identify which data sources are actually needed
4. Look for opportunities to parallelize

### 2. Minimize Token Usage
- Load only relevant sections of grounding docs
- Reference docs by summary, not full content
- Use cached customer lookups instead of reading CSV repeatedly
- Prune irrelevant context before responding

### 3. Optimize Delegation
- **Simple queries** → Direct to single agent, no orchestration overhead
- **Medium queries** → Sequential with context sharing
- **Complex queries** → Parallel execution + synthesis

---

## 🎯 Request Complexity Classification

### SIMPLE (Direct Route - Target: <5 seconds)
**Characteristics:**
- Single data source (only Kusto OR only ICM OR only ADO)
- Single customer/tenant
- No complex aggregations
- Standard filters apply

**Examples:**
- "How many cases does Ford have?"
- "Show me ICM 21000000887894 details"
- "What ADO bugs are assigned to me?"

**Handling:**
```
User Request → Complexity: SIMPLE
↓
1. Load customer lookup (if needed) - from cache if available
2. Select single agent (Support Case Manager / Escalation Manager / Work Item Manager)
3. Use pre-built query pattern from QUERY_PATTERNS.md
4. Execute single query
5. Format response
```

**Optimization Rules:**
- ✅ Use customer lookup cache
- ✅ Use pre-built query templates
- ✅ Apply standard filters from COMMON_FILTERS.md
- ❌ Don't load full agent instructions
- ❌ Don't involve multiple agents

---

### MEDIUM (Optimized Sequential - Target: <15 seconds)
**Characteristics:**
- 2 data sources
- Multiple tenants (2-5)
- Some aggregation needed
- Related queries that share context

**Examples:**
- "Show cases and ICMs for Ford"
- "Compare case counts across MCS cohort"
- "Get case details and related work items"

**Handling:**
```
User Request → Complexity: MEDIUM
↓
1. Identify required agents (typically 2)
2. Execute agent 1 → Cache results
3. Use cached results in agent 2 query (avoid redundant lookups)
4. Synthesize combined response
```

**Optimization Rules:**
- ✅ Share context between agents (pass TenantIds forward)
- ✅ Reuse customer lookups
- ✅ Combine related filters
- ❌ Don't re-query same data
- ❌ Don't load unnecessary grounding docs

---

### COMPLEX (Parallel + Synthesis - Target: <30 seconds)
**Characteristics:**
- 3+ data sources
- Multiple customers (5+)
- Complex cross-referencing
- Time-series analysis
- Root cause investigation

**Examples:**
- "Full health report for Contoso: cases, ICMs, ADO, tenant metrics"
- "Analyze top 10 customers by escalation risk"
- "Root cause analysis for sensitivity label failures across all tenants"

**Handling:**
```
User Request → Complexity: COMPLEX
↓
1. Decompose into independent sub-queries
2. Execute in parallel:
   - Agent A: Kusto queries
   - Agent B: ICM queries
   - Agent C: ADO queries
3. Wait for all to complete (async gather)
4. Synthesize findings
5. Apply correlation analysis
6. Generate structured report
```

**Optimization Rules:**
- ✅ Parallelize independent queries
- ✅ Use batch operations where possible
- ✅ Cache intermediate results
- ✅ Handle partial failures gracefully
- ❌ Don't execute serially
- ❌ Don't block on slow queries (timeout: 60s)

---

## 🧠 Context Caching Strategy

### What to Cache (Session-Level)
```python
CACHE_ITEMS = {
    "customer_registry": {
        "source": "IC and MCS 2.4.csv",
        "ttl": "session",  # Load once per session
        "size": "~500 KB"
    },
    "common_filters": {
        "source": "COMMON_FILTERS.md",
        "ttl": "session",
        "size": "~50 KB"
    },
    "query_patterns": {
        "source": "QUERY_PATTERNS.md",
        "ttl": "session",
        "size": "~100 KB"
    },
    "recent_queries": {
        "source": "execution_results",
        "ttl": "5-15 minutes",  # Live data cache
        "size": "varies"
    }
}
```

### Cache Key Design
```
# Customer lookups
cache_key = f"tenant_id:{customer_name}"
# Example: "tenant_id:Ford" → "c990bb7a-51f4-439b-bd36-9c07fb1041c0"

# Query results
cache_key = f"query:{query_hash}:{timestamp_bucket}"
# Example: "query:ford_cases:2026-02-04-14" → {count: 12, timestamp: "..."}

# Agent results
cache_key = f"agent:{agent_name}:{request_hash}"
```

### When to Use Cache vs. Live Query

**Use Cache When:**
- ✅ Customer name → TenantId lookup (static data)
- ✅ Common filters (static patterns)
- ✅ Query results < 15 minutes old (for dashboards)
- ✅ Reference documentation (session-level)

**Use Live Query When:**
- ⚡ User explicitly asks for "latest" or "current"
- ⚡ SLA-critical data (breach detection)
- ⚡ Real-time monitoring requests
- ⚡ Data older than TTL threshold

---

## ⚡ Parallel Execution Patterns

### Pattern 1: Independent Data Sources
```
Request: "Show Ford's cases, ICMs, and ADO bugs"

PARALLEL EXECUTION:
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Agent: Support  │  │ Agent: Escal    │  │ Agent: Work Item│
│ Case Manager    │  │ Manager         │  │ Manager         │
│                 │  │                 │  │                 │
│ Query: Kusto    │  │ Query: ICM MCP  │  │ Query: ADO MCP  │
│ GetSCIM...      │  │ GetICM...       │  │ GetWorkItems... │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                    Synthesis & Correlation
                              ▼
                    Structured Response
```

**Implementation:**
- Launch all 3 queries simultaneously
- Wait for all to complete (timeout: 60s each)
- Proceed even if one fails (partial results)
- Correlate by customer/tenant/timeframe

### Pattern 2: Multi-Tenant Batch
```
Request: "Case counts for all MCS Alpha cohort (20 customers)"

PARALLEL EXECUTION:
┌────────────┐  ┌────────────┐  ┌────────────┐     ┌────────────┐
│ Customer 1 │  │ Customer 2 │  │ Customer 3 │ ... │ Customer 20│
│ TenantId X │  │ TenantId Y │  │ TenantId Z │     │ TenantId W │
└────────────┘  └────────────┘  └────────────┘     └────────────┘
      │               │               │                    │
      └───────────────┼───────────────┼────────────────────┘
                      ▼
              Single Kusto Query with IN clause
              | where TenantId in (X, Y, Z, ..., W)
              | summarize by TenantId
                      ▼
              Result aggregation
```

**Implementation:**
- Batch tenant IDs into single query (more efficient)
- Use `summarize by TenantId` for per-customer breakdown
- Avoid 20 separate queries

### Pattern 3: Time-Series Analysis
```
Request: "Show case trends over last 6 months"

PARALLEL EXECUTION:
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Month 1  │  │ Month 2  │  │ Month 3  │  │ Month 4  │  │ Month 5  │  │ Month 6  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
      │             │             │             │             │             │
      └─────────────┼─────────────┼─────────────┼─────────────┼─────────────┘
                    ▼
          Single query with bin(TimeGenerated, 30d)
                    ▼
          Trend analysis & visualization
```

**Implementation:**
- Single query with time bucketing (more efficient)
- Use Kusto's `bin()` function for time grouping
- Avoid separate queries per time period

---

## 🛡️ Error Handling & Graceful Degradation

### Principle: Always Deliver Value
**Never return "Query failed, try again"**

Instead, implement cascading fallback:

### Level 1: Primary (Live Query)
```
Try: Execute live Kusto query
Success → Return results with timestamp
Failure → Proceed to Level 2
```

### Level 2: Cached Data
```
Try: Retrieve from cache (if < 1 hour old)
Success → Return cached results with warning:
  "⚠️ Using cached data from [timestamp]. Live query unavailable."
Failure → Proceed to Level 3
```

### Level 3: Static Reference
```
Try: Use static CSV data (if exists)
Success → Return static data with warning:
  "⚠️ Using static reference data (last updated: [date]). Real-time query unavailable."
Failure → Proceed to Level 4
```

### Level 4: Partial Results
```
If multi-source query:
  Return successful queries + note failures:
  "✅ Cases: 12 (live)
   ✅ ICMs: 3 (live)
   ❌ ADO: unavailable (service timeout)"
```

### Level 5: Guidance Only
```
If no data available:
  Provide actionable next steps:
  "Unable to retrieve data. Possible actions:
   1. Check MCP server status
   2. Verify credentials/permissions
   3. Try manual query in [tool]
   4. Estimated recovery time: [X] minutes"
```

### Service-Specific Timeouts
```python
TIMEOUTS = {
    "kusto": 60,      # Complex queries can take time
    "icm": 30,        # Usually fast
    "ado": 45,        # Medium speed
    "sharepoint": 20  # Document retrieval
}
```

### Retry Logic
```python
def execute_with_retry(query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return execute_query(query, timeout=TIMEOUTS[query.source])
        except TimeoutError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
                continue
            else:
                return None  # All retries failed
        except PermissionError:
            # Don't retry permission errors
            return None
```

---

## 📋 Pre-Query Checklist

Before executing ANY query, verify:

### ✅ Data Source Requirements
- [ ] Which systems needed? (Kusto / ICM / ADO / Static files)
- [ ] Is this data time-sensitive or can cache be used?
- [ ] What's the minimum data needed to answer the question?

### ✅ Context Optimization
- [ ] Do I have TenantId from previous query or need lookup?
- [ ] Are filters already available or need to load?
- [ ] Can I reuse any previous query results?

### ✅ Execution Strategy
- [ ] Single query or multiple needed?
- [ ] Can queries run in parallel?
- [ ] What's the expected response time? (Set user expectations)

### ✅ Quality Assurance
- [ ] Applied standard noise filters?
- [ ] Using TenantId (not CustomerName) for reliability?
- [ ] Have fallback if primary query fails?

---

## 🎯 Agent Selection Decision Tree

```
Incoming Request
       │
       ▼
[Complexity Analysis]
       │
       ├──→ SIMPLE
       │    │
       │    ├──→ "cases" → Support Case Manager (direct)
       │    ├──→ "icm" / "incident" → Escalation Manager (direct)
       │    ├──→ "ado" / "work item" / "bug" → Work Item Manager (direct)
       │    ├──→ "tenant health" / "metrics" → Tenant Health Monitor (direct)
       │    ├──→ "contact" / "email" → Contacts Finder (direct)
       │    └──→ "product" / "known issue" → Purview Expert (direct)
       │
       ├──→ MEDIUM
       │    │
       │    ├──→ "cases + icm" → [Support Case → Escalation] (sequential)
       │    ├──→ "icm + ado" → [Escalation → Work Item] (sequential)
       │    └──→ "multi-tenant" → [Customer Lookup → batch query] (optimized)
       │
       └──→ COMPLEX
            │
            ├──→ "full health" → [ALL agents] (parallel + synthesize)
            ├──→ "root cause" → [Investigation pattern] (guided sequence)
            └──→ "strategic analysis" → [Analytics pattern] (multi-phase)
```

---

## 🎨 Response Formatting

### Always Include Performance Metadata
```markdown
**Query Execution:** 3.2 seconds
**Data Freshness:** Live (2026-02-04 14:23 UTC)
**Sources:** Kusto (0 records), ICM (3 records)
**Cache Used:** Customer lookup (session cache)
```

### Progressive Disclosure
For complex responses, structure as:
1. **Executive Summary** (2-3 lines)
2. **Key Findings** (bullets)
3. **Detailed Data** (expandable/linked)
4. **Metadata** (sources, timestamps, caveats)

Example:
```
**Summary:** Ford has 12 open cases, 3 active ICMs, 5 pending ADO bugs.

**Key Findings:**
• 2 cases approaching SLA breach (< 24h remaining)
• 1 P1 ICM requires escalation
• No blocking ADO bugs

[View detailed case list] [View ICM details] [View ADO status]

---
Query: 3.2s | Data: Live | Sources: Kusto, ICM, ADO
```

---

## 📊 Performance Monitoring

### Track These Metrics
```python
METRICS = {
    "query_execution_time": [],      # Track all query durations
    "cache_hit_rate": 0.0,            # % of requests served from cache
    "parallel_efficiency": 0.0,       # Speedup from parallelization
    "error_rate": 0.0,                # % of failed queries
    "token_usage_per_request": [],   # Track token consumption
    "complexity_distribution": {     # Request type breakdown
        "simple": 0,
        "medium": 0,
        "complex": 0
    }
}
```

### Log Each Request
```json
{
  "timestamp": "2026-02-04T14:23:45Z",
  "request": "How many cases does Ford have?",
  "complexity": "SIMPLE",
  "agents_used": ["Support Case Manager"],
  "execution_time_ms": 3200,
  "cache_hits": 1,
  "queries_executed": 1,
  "tokens_used": 1250,
  "success": true,
  "data_sources": ["kusto"],
  "result_count": 1
}
```

---

## 🎓 Examples: Before vs. After Optimization

### Example 1: Simple Case Count

**Before (Unoptimized):**
```
1. Load full customer CSV (5 seconds)
2. Search for "Ford" (multiple matches)
3. Ask user to disambiguate (user interaction)
4. Load full Support Case Manager instructions (2 seconds)
5. Construct query from scratch
6. Execute query (3 seconds)
Total: ~10+ seconds + user interaction
```

**After (Optimized):**
```
1. Check customer cache → Ford TenantId (cached, instant)
2. Use pre-built query pattern #1 (instant)
3. Execute query (2-3 seconds)
Total: ~3 seconds, no user interaction
```

### Example 2: Multi-Source Health Report

**Before (Unoptimized):**
```
1. Query cases (5s)
2. Wait for completion
3. Query ICMs (4s)
4. Wait for completion
5. Query ADO (6s)
6. Wait for completion
7. Query tenant metrics (5s)
8. Synthesize (2s)
Total: ~22 seconds
```

**After (Optimized):**
```
1. Launch all 4 queries in parallel
2. Wait for slowest (6 seconds)
3. Synthesize while waiting (async)
Total: ~7 seconds (70% faster)
```

---

## ✅ Optimization Checklist

Before responding to user, verify:

**Query Optimization:**
- [ ] Used cached customer lookups
- [ ] Applied standard filters
- [ ] Used pre-built query patterns
- [ ] Minimized number of queries

**Execution Optimization:**
- [ ] Parallelized independent operations
- [ ] Set appropriate timeouts
- [ ] Implemented fallback strategy
- [ ] Cached results for reuse

**Context Optimization:**
- [ ] Loaded only necessary grounding docs
- [ ] Pruned irrelevant context
- [ ] Reused previous query results
- [ ] Minimized token usage

**Response Optimization:**
- [ ] Structured for readability
- [ ] Included performance metadata
- [ ] Progressive disclosure for large datasets
- [ ] Actionable next steps

---

## 🚨 Anti-Patterns to Avoid

### ❌ Don't Do This:
1. **Sequential when parallel possible**
   ```
   Execute query 1 → wait → Execute query 2 → wait
   // Should be: Execute both simultaneously
   ```

2. **Repeated customer lookups**
   ```
   Load CSV → lookup Ford → Load CSV again → lookup GM
   // Should be: Load CSV once, cache for session
   ```

3. **Full context loading for simple queries**
   ```
   Load all 50 pages of agent instructions for "count cases"
   // Should be: Use query pattern only
   ```

4. **No fallback on failures**
   ```
   Query failed → return error
   // Should be: Try cache → Try static → Try partial results → Provide guidance
   ```

5. **Separate queries for batch operations**
   ```
   For each customer: execute_query(customer)
   // Should be: Single query with `IN` clause
   ```

---

## 📚 Quick Reference Resources

**Always Available (Session Cache):**
- Customer Lookup: `grounding_docs/contacts_access/CUSTOMER_LOOKUP_GUIDE.md`
- Query Patterns: `sub_agents/*/QUERY_PATTERNS.md`
- Common Filters: `sub_agents/kusto_expert/COMMON_FILTERS.md`
- Query Cheat Sheet: `docs/QUERY_CHEAT_SHEET.md`

**Load On-Demand:**
- Agent Instructions: `sub_agents/*/AGENT_INSTRUCTIONS.md`
- Grounding Docs: `grounding_docs/**/*`
- Product Knowledge: `grounding_docs/purview_product/*`

---

## 🎯 Success Metrics

**Target Performance (by complexity):**
- Simple: < 5 seconds (90th percentile)
- Medium: < 15 seconds (90th percentile)
- Complex: < 30 seconds (90th percentile)

**Target Efficiency:**
- Cache hit rate: > 60%
- Token usage: < 15K per request (average)
- Error rate: < 5%
- Parallel speedup: > 2x for complex queries

---

**Version History:**
- v2.0 (2026-02-04): Performance optimizations added
- v1.0 (2026-02-04): Initial orchestrator instructions

