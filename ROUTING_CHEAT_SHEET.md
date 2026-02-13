# 🎯 Agent Routing Cheat Sheet (V2.0 Enhanced)

**Quick Daily Reference** | Keep This Open  
**350+ Patterns | 14 Workflows | 11 Domains**

---

## ⚡ Most Common Commands

### Reports (Type These Exactly)
```
"IC production report"
"MCS production report"  
"Friday LQE reports"
"Generate APAC LQE report"       ← NEW!
"Run EMEA regional report"       ← NEW!
"Americas LQE analysis"          ← NEW!
"All regional reports"           ← NEW!
```

### Analysis
```
"Run by design analysis"
"Generate doc gap report"
"DLP report for last 6 months"
"Analyze TSG gaps"               ← NEW!
"Team performance for my team"   ← NEW!
```

### ICM Operations
```
"Get ICM details for [ID]"
"Find similar ICMs"
"Sev2 incidents this week"       ← NEW!
"ICMs from last 7 days"          ← NEW!
"DLP team ICMs this month"       ← NEW!
```

### Kusto Queries
```
"Query Kusto for [metric]"
"Errors in last 48 hours"        ← ENHANCED!
"Tenant health check for [customer]"
"Compare tenant metrics"
```

### Work Items
```
"Create bug for [issue]"
"High priority bugs assigned to me"  ← NEW!
"Search ADO for [keyword]"
"Link bug to ICM [ID]"
"My open bugs"                   ← NEW!
```

### Combined Operations  ← NEW SECTION!
```
"Generate and email IC report"
"Refresh data then run report"
"Generate all regional and send emails"
"Create bug and link to ICM"
```

---

## 🌍 Regional Intelligence (NEW!)

```
"APAC LQE report"               → 90% confidence
"EMEA regional report"          → 80% confidence  
"Americas analysis"             → 90% confidence
"All regional LQE reports"      → 95% confidence workflow
```

---

## ⏰ Time-Based Queries (NEW!)

```
"Last 7 days"
"Last 30 days"
"This week"
"Last week"
"Today"
"Yesterday"
"Last 24 hours"
"Last 48 hours"
"This month"
"Last month"
"This quarter"
```

**Examples:**
```
"Show ICMs from last 7 days"
"Sev2 incidents this week"
"Errors in last 48 hours"
"DLP issues last month"
```

---

## 🚨 Severity & Priority (NEW!)

```
"Sev2 incidents"
"Sev3 issues"
"P0 ICMs"
"P1 escalations"
"High priority bugs"
"Critical cases"
"High severity incidents"
```

---

## 👥 Team & Personal (NEW!)

```
"My bugs"
"My cases"
"My team ICMs"
"Assigned to me"
"For DLP team"
"For MIP team"
"For Purview team"
"Team performance"
```

---

## 🔄 Workflows (Multi-Step)

```
"New P0 ICM workflow"            → 5 steps
"Weekly health review"           → 4 steps
"Customer deep dive"             → 6 steps
"Root cause analysis"            → 5 steps
"Executive briefing"             → 4 steps
"Friday operations"              → 3 steps
"Generate and email"             → 2 steps  ← NEW!
"Refresh and report"             → 3 steps  ← NEW!
"TSG gap workflow"               → 3 steps  ← NEW!
"Team performance review"        → 4 steps  ← NEW!
```

---

## 📧 Email Operations (NEW!)

```
"Send report"
"Email report"
"Send LQE email"
"Email regional reports"
"Generate and email"            ← Workflow!
```

---

## 📚 TSG Operations (NEW!)

```
"Analyze TSG gaps"
"Find missing TSGs"
"TSG coverage report"
"TSG effectiveness"
"Create TSG"
"Update TSG"
```

---

## 🔧 Data Operations

```
"Refresh ICM data"              ← NEW!
"Load from Kusto"               ← NEW!
"Save Kusto data"               ← NEW!
"Convert to CSV"                ← NEW!
"Refresh then report"           ← NEW workflow!
```

---

## 🧪 Test Your Query

```python
from agent_router import AgentRouter
router = AgentRouter()

result = router.route("your query here")
print(f"{result['routing_type']} → {result.get('agent', result.get('workflow'))}")
print(f"Confidence: {result['confidence']:.0%}")
```

---

## 📊 Confidence Guide

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100% | Direct script match | Execute immediately |
| 80-89% | High confidence routing | Proceed confidently |
| 60-79% | Medium confidence | Verify if needed |
| <60% | Ask for clarification | Too vague |

---

## 💡 Smart Combinations

```
"Generate APAC report and send email"
"Refresh IC data then run production report"
"Create bug for TSG gap and link to ICM"
"Show DLP team Sev2s from last week and email"
"Analyze customer health and generate executive brief"
```

---

## 🎯 Most Likely Next Asks

Based on your patterns:

1. `"Generate Friday LQE reports and send emails"`
2. `"APAC Sev2 ICMs from last week"`
3. `"Refresh IC data and generate report"`
4. `"Team performance for DLP team"`
5. `"Customer deep dive for [customer name]"`

---

## 🔧 Quick Customization

Edit `agent_routing_map.json`:

```json
{
  "patterns": {
    "your_domain": {
      "agent": "agent_name",
      "patterns": ["your keyword"]
    }
  }
}
```

---

## 🆘 When Stuck

```python
# Get suggestions
suggestions = router.suggest_query_improvements("vague query")
print(suggestions)
```

---

## 📞 Full Docs

- **V2.0 Enhancements:** ROUTING_V2_ENHANCEMENTS.md  ← NEW!
- **Complete Guide:** AGENT_ROUTING_GUIDE.md
- **Quick Reference:** ROUTING_QUICK_REFERENCE.md
- **Architecture:** ROUTING_ARCHITECTURE.md

---

## 📈 V2.0 Stats

- **Patterns:** 350+ (was 100)
- **Workflows:** 14 (was 6)
- **Domains:** 11 (was 9)
- **Test Success:** 25/25 (100%)
- **High Confidence:** 72%

---

**Test Script:** `python test_routing.py`  
**Status:** ✅ 30-50x faster | 350+ patterns | Deeply anticipatory  
**Version:** 2.0 Enhanced
