# PHEPy Sub-Agent System

**Version:** 1.0  
**Last Updated:** February 4, 2026  
**Status:** Development → Production Ready

---

## Overview

This directory contains **9 specialized sub-agents** that form the PHEPy orchestrator system. Each agent has a specific domain of expertise and uses designated MCP servers and grounding documents to deliver precise, actionable intelligence.

---

## 🤖 Sub-Agent Roster

| Agent | Role | Primary Tools | Status |
|-------|------|---------------|--------|
| **Jacques** (Kusto Expert) | KQL query construction & execution | Kusto MCP | ✅ Active |
| Support Case Manager | DFM case tracking & SLA monitoring | Enterprise MCP, Kusto | ✅ Active |
| Escalation Manager | ICM incident tracking & routing | ICM MCP, Kusto | ✅ Active |
| Work Item Manager | ADO bug/DCR tracking | ADO MCP (o365exchange, ASIM) | ✅ Active |
| Purview Product Expert | Product knowledge & known issues | Grounding docs, Wiki | ✅ Complete |
| Tenant Health Monitor | Customer health metrics | Kusto, SHI cluster | ✅ Complete |
| Contacts & Escalation Finder | Contact lookup & routing | CSV data, grounding docs | ✅ Complete |
| Program Onboarding Manager | MCS/IC onboarding workflows | Grounding docs, templates | ✅ Complete |
| **CI/Gemba Walker** | Process improvement & waste elimination | Kusto, DIVE, VSM | ✅ New |
| **LQE Agent** | Low Quality Escalation monitoring & reporting | ICM MCP, Kusto, Email | ✅ Production (Organized) |
| **ICM Agent** | By-design analysis & documentation gap detection | ICM MCP, Kusto | ✅ Production |

---

## 📁 Standard Agent Structure

Each sub-agent folder should contain:

```
sub_agents/<agent_name>/
├── AGENT_INSTRUCTIONS.md       # Core role, responsibilities, guardrails
├── CAPABILITIES.md              # Full capability matrix
├── QUERY_PATTERNS.md           # Standard queries & examples (if applicable)
├── TEST_SCENARIOS.md           # Test cases & expected outputs
├── GROUNDING_DOCS.md           # Required grounding doc references
├── EXAMPLE_PROMPTS.md          # User-facing example queries
└── <schema_files>.csv/kql      # Reference schemas & queries
```

---

## 🔧 Building Out Sub-Agents

### Phase 1: Core Documentation (All Agents)
- [ ] AGENT_INSTRUCTIONS.md - Role, responsibilities, boundaries
- [ ] CAPABILITIES.md - What the agent can/cannot do
- [ ] TEST_SCENARIOS.md - 5-10 test cases

### Phase 2: Tool Integration
- [ ] QUERY_PATTERNS.md - MCP tool usage patterns
- [ ] GROUNDING_DOCS.md - Document dependencies
- [ ] Schema references (if Kusto/database work)

### Phase 3: User Experience
- [ ] EXAMPLE_PROMPTS.md - Copy-paste ready prompts
- [ ] Validation tests with real data
- [ ] Integration with orchestrator

---

## 🎯 Agent Interaction Patterns

### Orchestrator → Sub-Agent
The orchestrator delegates tasks to sub-agents based on:
- **Intent detection** (keywords, domain)
- **Tool availability** (which MCP servers are connected)
- **Data source** (Kusto, ADO, ICM, DFM)

### Sub-Agent → Sub-Agent
Agents can invoke each other:
- **Support Case Manager** → **Escalation Manager** (if case needs escalation)
- **Kusto Expert** → **Any Agent** (data retrieval)
- **Purview Product Expert** → **Work Item Manager** (link bug to known issue)

### Example Flow
```
User: "What high-priority cases are at risk this week for Ford?"

Orchestrator:
  ↓
Contacts Finder (lookup Ford TenantId)
  ↓
Support Case Manager (query DFM cases)
  ↓
Jacques (Kusto query execution)
  ↓
Escalation Manager (check related ICMs)
  ↓
Return: Summary report with case #s, ICM #s, SLA deadlines
```

---

## 📊 Grounding Document Strategy

### Shared Resources (All Agents)
- `grounding_docs/contacts_access/CUSTOMER_LOOKUP_GUIDE.md`
- `grounding_docs/contacts_access/IC and MCS 2.4.csv`
- `docs/QUERY_CHEAT_SHEET.md`

### Domain-Specific
Each agent folder references specific grounding docs:
- **Purview Product Expert** → `grounding_docs/purview_product/`
- **Program Onboarding** → `grounding_docs/phe_program_operations/`
- **Access Role Manager** → `grounding_docs/contacts_access/`

---

## 🚀 Deployment to Azure AI Foundry

When packaging for Foundry:
1. **Each sub-agent becomes a Foundry Agent** with:
   - Agent instructions (system prompt)
   - Tool definitions (MCP connections)
   - Knowledge index (grounding docs)

2. **Orchestrator** becomes the **primary agent** that routes to sub-agents

3. **Shared knowledge base** uploaded to Azure AI Search

See: `../DEPLOYMENT_GUIDE.md` (created during packaging)

---

## 📝 Next Steps

1. ✅ Audit current agent state
2. 🔄 Build out missing documentation files
3. 🔄 Create test scenarios for each agent
4. 🔄 Validate with real queries
5. 🔄 Package for Foundry deployment

---

## 🆘 Getting Help

- **Agent Structure Questions:** See template in this README
- **MCP Tool Questions:** See `../mcp.json` for available servers
- **Query Patterns:** See individual agent QUERY_PATTERNS.md files
- **Deployment:** See `../DEPLOYMENT_GUIDE.md`
