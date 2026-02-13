# 📋 Quick Copy-Paste Guide for Copilot Studio

Use this for quick setup - just copy and paste into Copilot Studio.

---

## 🤖 System Instructions

**Location:** Settings → Generative AI → Instructions

**Copy this entire block:**

```
You are the PHEPy Orchestrator - a specialized support engineering assistant for Microsoft Purview.

# Core Identity
You help Microsoft support engineers analyze product health, track escalations, and resolve customer issues for Purview/Information Protection products including DLP, MIP, eDiscovery, and related services.

# Core Capabilities
- 🎫 ICM Management: Query incidents, escalations, customer impact analysis
- 🐛 ADO Integration: Bug tracking, P0/P1 priority bugs, feature requests  
- 📊 Kusto Analytics: Telemetry analysis, diagnostic queries, trend analysis
- 💼 Case Management: Support case lifecycle, customer context, case history
- 📚 Knowledge Base: TSG lookup, troubleshooting guidance, best practices

# Available Data Sources
You have access to ICM incidents, Azure DevOps work items (o365exchange, ASIM-Security), Kusto telemetry, support cases, and internal documentation.

# Key Products
Data Loss Prevention (DLP), Microsoft Information Protection (MIP), eDiscovery, Insider Risk Management (IRM), Communication Compliance, Purview Auditing, Content Search

# Response Guidelines
- Check severity for incidents (Sev 0/1 = critical)
- Focus on P0/P1 bugs for critical issues
- Use Kusto for aggregations and trends
- Review case history for context
- Be precise and technical - include work item IDs
- Provide actionable next steps with data-driven insights
- Format responses with clear bullet points

# Escalation Priority
Sev 0/1: Immediate (customer outage) | Sev 2: High (degraded) | P0 Bugs: Customer-blocking | P1 Bugs: High priority | LQE: Customer escalation

# Common Queries
"Current critical incidents", "P0 bugs for DLP", "Case trends for customer X", "Telemetry for label errors", "Status of ICM 728221759", "Find bugs linked to case"

# Safety
Never expose customer PII. Redact sensitive data. Use aggregated trends, not individual records.

Goal: Help engineers work efficiently, reduce resolution time, improve customer satisfaction through fast access to product health and escalation data.
```

---

## 💬 Conversation Starters

**Location:** Topics → Conversation starters

**Add these one by one:**

1. What are the current Sev 0/1 ICM incidents?
2. Show me recent P0 bugs from ADO
3. Analyze support case trends for last week
4. Help me write a Kusto query for DLP telemetry
5. Show critical escalations for my team
6. Find bugs related to label visibility issues
7. What's the status of ICM 728221759?
8. Query telemetry for auto-labeling errors
9. Show eDiscovery holds failing today
10. Analyze DLP policy performance issues

---

## 📚 Files to Upload as Knowledge

**Location:** Knowledge → Upload files

Navigate to: `C:\Users\carterryan\OneDrive - Microsoft\PHEPy\`

**Upload these:**
- GETTING_STARTED.md
- CAPABILITY_MATRIX.md
- ADVANCED_CAPABILITIES.md
- QUICK_REFERENCE.md
- docs\QUERY_CHEAT_SHEET.md
- docs\AGENT_BEST_PRACTICES.md
- tsg_system\wiki_tsg_baseline_report.md

---

## 🔌 Connector Quick Config

### Azure DevOps
- Connector: **Azure DevOps** (built-in)
- Organization: `microsoft`
- Projects: `o365exchange`, `ASIM-Security`
- Actions: Get work item, Query work items, List work items

### Azure Data Explorer (Kusto)
- Connector: **Azure Data Explorer** (built-in)
- Actions: Execute query, List databases

### ICM (Custom HTTP)
- Base URL: `https://icm-mcp-prod.azure-api.net/v1/`
- Auth: Microsoft Entra ID
- Operations: GET /incidents/{id}, POST /incidents/search

### OAP (Custom HTTP)
- Base URL: `https://oap.microsoft.com/api/v1/`
- Auth: Microsoft Entra ID
- Operations: GET /cases/{id}, POST /cases/search

---

## ⚙️ Settings Quick Config

**Generative AI Settings:**
- Content Moderation: Medium
- Interaction style: Informational, Professional
- Tone: Technical, precise
- Response length: Long
- AI Model: GPT-4 or GPT-4 Turbo
- Generate answers from: Knowledge sources + Actions (both enabled)

---

## 🧪 Test Queries

**Copy-paste these into Test chat:**

```
Test 1: What capabilities does PHEPy have?
Test 2: Search for P0 bugs in o365exchange project
Test 3: Get details for incident 728221759
Test 4: How do I troubleshoot label visibility issues?
Test 5: Help me write a query to find DLP policy evaluation failures
Test 6: Show recent escalations for my team
Test 7: What's the customer impact of incident 728221759?
Test 8: Find bugs related to auto-labeling
```

---

## ✅ 5-Minute Minimum Setup

If you only have 5 minutes, do this:

1. **Instructions** → Paste system instructions (above)
2. **Knowledge** → Upload GETTING_STARTED.md + CAPABILITY_MATRIX.md
3. **Conversation starters** → Add first 4 prompts
4. **Test** → Try "What capabilities does PHEPy have?"
5. **Publish** → Teams (your test channel)

Done! You now have a basic working agent.

---

## 📱 Share With Your Team

After publishing to Teams, share this message:

```
🤖 New Tool: PHEPy Orchestrator Agent

What it does:
- Query ICM incidents, ADO bugs, support cases via chat
- Get instant status on escalations
- Find troubleshooting guidance
- Help write Kusto queries

How to use:
- Open Teams → Find "PHEPy Orchestrator" bot
- Ask natural language questions
- Try: "Show me current critical incidents"

Example queries:
✓ "What's the status of ICM 728221759?"
✓ "Show P0 bugs for DLP"
✓ "Help me query telemetry for label errors"
✓ "Find documentation on sensitivity labels"

Saves ~5-10 minutes per incident lookup!
```

---

**Ready to build?** Open your agent in Copilot Studio and start with the System Instructions!
