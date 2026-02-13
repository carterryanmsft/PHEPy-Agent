# 🎯 Azure AI Foundry - Copy/Paste Reference

Keep this open while setting up in portal: https://ai.azure.com

---

## 📝 SYSTEM INSTRUCTIONS (Copy entire block)

**Where:** Playground → System message

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

# Available MCP Servers
You have access to:
- ICM MCP Server: https://icm-mcp-prod.azure-api.net/v1/ (incidents, escalations)
- Azure DevOps MCP: o365exchange, ASIM-Security projects (bugs, work items)
- Kusto MCP: Telemetry and diagnostic queries
- OAP MCP: https://oap.microsoft.com/api/v1/ (support cases, customer context)

# Key Products
Data Loss Prevention (DLP), Microsoft Information Protection (MIP), eDiscovery, Insider Risk Management (IRM), Communication Compliance, Purview Auditing, Content Search

# Response Guidelines
- Check severity for incidents (Sev 0/1 = critical, customer down)
- Focus on P0/P1 bugs for critical issues
- Use Kusto for aggregations and trends
- Review case history for context
- Be precise and technical - always include work item IDs (ICM, ADO, Cases)
- Provide actionable next steps with data-driven insights
- Format responses clearly with bullet points

# Escalation Priority
- Sev 0/1: Immediate attention (customer outage)
- Sev 2: High priority (degraded service)
- P0 Bugs: Customer-blocking, needs immediate fix
- P1 Bugs: High priority feature/fix
- LQE: Live Quality Escalation (customer unhappy, needs PM attention)

# Common Queries
"Current critical incidents", "P0 bugs for DLP", "Case trends for customer X", "Telemetry for label errors", "Status of ICM 728221759", "Find bugs linked to case"

# Safety & Privacy
Never expose customer PII. Redact confidential information. Use aggregated data for trends, not individual records. Follow Microsoft data handling policies.

Goal: Help engineers work efficiently, reduce mean-time-to-resolution, improve customer satisfaction through fast access to product health and escalation data.
```

---

## ⚙️ MODEL SETTINGS

**Where:** Playground → Configuration → Parameters

```
Model: GPT-4 or GPT-4o
Temperature: 0.3
Max response: 4000 tokens
Top P: 0.95
Frequency penalty: 0
Presence penalty: 0
Stop sequences: (none)
```

---

## 📚 FILES TO UPLOAD

**Where:** Data → Add data → Upload files

Navigate to: `C:\Users\carterryan\OneDrive - Microsoft\PHEPy\`

**Essential files (upload these first):**
```
✓ GETTING_STARTED.md
✓ CAPABILITY_MATRIX.md
✓ ADVANCED_CAPABILITIES.md
✓ QUICK_REFERENCE.md
```

**Additional docs (upload if time permits):**
```
✓ docs\QUERY_CHEAT_SHEET.md
✓ docs\AGENT_BEST_PRACTICES.md
✓ docs\MCP_SERVER_BEST_PRACTICES.md
✓ tsg_system\wiki_tsg_baseline_report.md
```

**Indexing settings:**
```
Indexing strategy: Keyword + Semantic
Chunk size: 1024 tokens
Chunk overlap: 128 tokens
```

---

## 🧪 TEST QUERIES (Copy one at a time)

**Where:** Playground → Chat

```
Test 1: What capabilities does PHEPy have?

Test 2: Explain how to troubleshoot DLP label visibility issues

Test 3: What products and services do you support?

Test 4: How do I query ICM for critical incidents?

Test 5: Show me an example Kusto query for DLP policy evaluation failures

Test 6: What's the difference between a Sev 1 incident and a P0 bug?

Test 7: How do I find bugs related to auto-labeling issues?

Test 8: Explain the PHEPy sub-agent architecture

Test 9: What MCP servers are available and what do they provide?

Test 10: How can I track escalations for a specific customer?
```

**Expected behaviors:**
- Should cite sources from your uploaded docs
- Should understand technical product terminology
- Should provide structured, actionable responses
- Should maintain context across follow-up questions

---

## 🚀 DEPLOYMENT CONFIG

**Where:** Endpoints → Create endpoint

```
Endpoint name: phepy-orchestrator
Authentication: Key-based
Compute: Serverless (recommended for auto-scale)
Instance type: Standard_DS3_v2 (or similar)
Instance count: Auto-scale (min: 1, max: 10)
Traffic allocation: 100% to this deployment
```

---

## 📋 PROJECT METADATA

**Use these when creating your project:**

```
Project name: PHEPy-Orchestrator
Display name: PHEPy Orchestrator
Description: Purview Product Health & Escalation Orchestrator Agent with ICM, ADO, Kusto, and case management capabilities
Tags:
  - Environment: Production
  - Team: CxE Support Engineering
  - Purpose: AI Assistant
  - Product: Purview
```

---

## 🔗 API CONNECTION CONFIGS

**If adding REST API connections:**

### ICM MCP
```
Name: ICM MCP Server
Base URL: https://icm-mcp-prod.azure-api.net/v1/
Authentication: Microsoft Entra ID (OAuth 2.0)
Resource/Scope: api://icm-mcp/.default
```

### OAP
```
Name: Support Case Management (OAP)
Base URL: https://oap.microsoft.com/api/v1/
Authentication: Microsoft Entra ID (OAuth 2.0)
```

### Azure DevOps
```
Name: Azure DevOps API
Base URL: https://dev.azure.com/microsoft/
Authentication: Personal Access Token or OAuth
Projects: o365exchange, ASIM-Security
```

---

## 💬 SAMPLE CONVERSATION FOR TESTING

Copy this entire conversation to test multi-turn capability:

```
User: What capabilities does PHEPy have?

[Wait for response]

User: Tell me more about the ICM management capabilities

[Wait for response]

User: How would I find all Sev 1 incidents from yesterday?

[Wait for response]

User: What if I wanted to also see related bugs?

[Wait for response]

User: Great! Can you show me how to query telemetry for those incidents?
```

This tests:
- Knowledge retrieval
- Context retention
- Multi-step reasoning
- Integration understanding

---

## ✅ 10-MINUTE QUICK START

**Absolute minimum to get working:**

1. **Create Project** (2 min)
   - Name: PHEPy-Orchestrator
   - Click Create

2. **Add Instructions** (3 min)
   - Playground → System message
   - Paste system instructions (above)

3. **Upload 1 Doc** (2 min)
   - Data → Upload → CAPABILITY_MATRIX.md

4. **Test** (3 min)
   - Try: "What capabilities does PHEPy have?"
   - Verify it cites your document

Done! You now have a working agent.

---

## 🎯 Full paths for copy-paste

```powershell
# Documentation files
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\GETTING_STARTED.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\CAPABILITY_MATRIX.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\ADVANCED_CAPABILITIES.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\QUICK_REFERENCE.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\docs\QUERY_CHEAT_SHEET.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\docs\AGENT_BEST_PRACTICES.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\tsg_system\wiki_tsg_baseline_report.md

# MCP Configuration
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\mcp.json
```

---

**Portal URL:** https://ai.azure.com

**Workspace:** CxESharedServicesAI-Prod

**Ready? Let's build!** 🚀
