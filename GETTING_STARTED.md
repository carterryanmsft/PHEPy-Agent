# 🚀 PHEPy Quick Start Guide

**Welcome!** This workspace helps you manage Purview customer health, escalations, and product operations.

---

## � **NEW: Agent Memory System** (Recommended First Step)

Transform GitHub Copilot CLI into a **persistent AI assistant** that remembers you across sessions!

### ⚡ Quick Setup (5 minutes)
```bash
cd agent_memory
python bootstrap.py
```

**What it does**:
- ✅ Stores your preferences (work style, communication, report formats)
- ✅ Remembers goals, decisions, and context
- ✅ Auto-reconnects at the start of each Copilot CLI session
- ✅ Gets smarter over time through conversation logging

**Full guide**: [agent_memory/QUICK_SETUP.md](agent_memory/QUICK_SETUP.md)  
**Best practices**: [docs/AGENT_BEST_PRACTICES.md](docs/AGENT_BEST_PRACTICES.md)

---

## �🤖 Available MCP Agents

Your workspace has **4 active MCP servers** configured:

### 1. 📋 **Azure DevOps (O365 Exchange)**
   - **Purpose:** Manage work items, pull requests, wikis, test plans
   - **Try these prompts:**
     - "Show me open work items assigned to me"
     - "Create a bug for Purview data classification issue"
     - "List recent pull requests in ASIM-Security repo"
     - "Search ADO for sensitivity label bugs"

### 2. 🔒 **Azure DevOps (ASIM Security)**
   - **Purpose:** Security repository management, branch operations, work item linking
   - **Try these prompts:**
     - "Create a new branch for security fix"
     - "Link work item #12345 to current pull request"
     - "Add artifact link to this commit"
     - "Reply to code review comment in PR #456"

### 3. 🚨 **ICM (Incident Management)**
   - **Purpose:** Query and manage customer incidents/escalations
   - **Try these prompts:**
     - "Get details for ICM 21000000887894"
     - "Show me on-call schedule for Purview team"
     - "Find ICMs affecting customer tenant abc123"
     - "What's the customer impact for incident 693849812?"

### 4. 📊 **Kusto Query Engine**
   - **Purpose:** Execute KQL queries against Azure data sources
   - **Try these prompts:**
     - "Execute query from purview_analysis/queries/sensitivity_labels.kql"
     - "List all tables in PurviewTelemetry database"
     - "Get schema for ICMIncidents table"
     - "Query last 24 hours of Purview errors"

---

## 🎯 Common Workflows - Try These!

### Customer Health Monitoring
```
"Run the tenant health check for customer XYZ"
"Analyze Purview sensitivity label usage trends"
"Generate risk report for IC/MCS customers"
```

### Escalation Management
```
"Find all P0/P1 incidents for Purview in the last week"
"What ICMs are linked to support case 51000000865253?"
"Create escalation summary for ICM 693849812"
```

### Product Analysis
```
"Analyze Purview DCR patterns from last 30 days"
"Compare sensitivity label adoption across tenants"
"Generate TSG gap analysis report"
```

### Development & Tracking
```
"Show me open bugs in the ServerSideAutoLabeling area"
"Create work item for new TSG: Label Removal Issues"
"Link these ICMs to the sensitivity labels feature branch"
```

---

## 📁 Key Workspace Areas

| Folder | Purpose | When to Use |
|--------|---------|-------------|
| **purview_analysis/** | Data analysis, queries, reports | Investigating product issues or trends |
| **risk_reports/** | Customer risk reporting | Generating IC/MCS production reports |
| **tsg_system/** | Troubleshooting guide management | Creating or updating TSGs |
| **sub_agents/** | Specialized agent instructions | Building custom agent workflows |
| **grounding_docs/** | Reference materials | Understanding processes, contacts, operations |

---

## 🏃 Quick Actions

### First Time Setup
1. ✅ **Check MCP Connection:** "List available Kusto databases"
2. ✅ **Test ICM Access:** "Get my on-call schedule"
3. ✅ **Verify ADO:** "Show ADO projects I have access to"

### Daily Operations
- **Morning Standup:** "What ICMs came in overnight for Purview?"
- **Health Check:** "Run purview analysis health dashboard"
- **Risk Review:** "Generate production report for IC/MCS customers"

### Investigation Mode
- **Deep Dive:** "Analyze all ICMs related to sensitivity label deletion"
- **Root Cause:** "Query Kusto for errors matching incident 21000000887894"
- **Cross-Reference:** "Find support cases linked to these work items: [list]"

---

## 🎓 Learning Resources

### New to PHE Program?
1. Read: [grounding_docs/phe_program_operations/FY26 PHEP Core Priorities.txt](grounding_docs/phe_program_operations/FY26%20PHEP%20Core%20Priorities.txt)
2. Understand: [grounding_docs/phe_program_operations/operational_rhythms_governance.md](grounding_docs/phe_program_operations/operational_rhythms_governance.md)
3. Reference: [grounding_docs/phe_program_operations/Customer Reliability Engineering Groudning.txt](grounding_docs/phe_program_operations/Customer%20Reliability%20Engineering%20Groudning.txt)

### Need Customer Contact Info?
- See: [grounding_docs/contacts_access/CUSTOMER_LOOKUP_GUIDE.md](grounding_docs/contacts_access/CUSTOMER_LOOKUP_GUIDE.md)

### Working with Kusto?
- Cheat Sheet: [docs/QUERY_CHEAT_SHEET.md](docs/QUERY_CHEAT_SHEET.md)
- Best Practices: [docs/QUERY_EFFICIENCY_IMPROVEMENTS.md](docs/QUERY_EFFICIENCY_IMPROVEMENTS.md)

---

## 💡 Pro Tips

1. **Be Specific:** Include ICM IDs, work item numbers, or tenant IDs for best results
2. **Use Context:** Mention which system (ICM, ADO, Kusto) if you have a preference
3. **Ask for Explanations:** "Explain this query" or "What does this data mean?"
4. **Save Your Work:** Ask to "Save this analysis to reports/" for future reference
5. **Chain Operations:** "Query ICMs for sensitivity labels, then create a summary report"

---

## 🆘 Need Help?

- **"What can you help me with?"** - Get capability overview
- **"Explain my MCP setup"** - Understand configured agents
- **"Show example queries for [topic]"** - Get query templates
- **"List all TSGs related to [issue]"** - Find troubleshooting guides

---

## 🔄 Recently Used Queries

Based on your terminal history, you've been working on:
- ICM analysis for specific incident IDs
- Purview sensitivity label investigations
- Risk report generation for IC/MCS customers

**Continue where you left off:**
```
"Analyze the ICMs we just extracted from Kusto"
"Generate detailed report for these ICM IDs: 21000000887894, 21000000887192, 21000000887231"
"Create risk assessment for customer tenant based on recent ICM patterns"
```

---

## 🚀 Want More Power?

You've only scratched the surface! Check out **[ADVANCED_CAPABILITIES.md](ADVANCED_CAPABILITIES.md)** for:

- 🔄 **Multi-agent orchestration** - Chain ICM + ADO + Kusto in complex workflows
- 🎯 **22 pre-built KQL queries** - Ready-to-execute product analysis
- 🧠 **9 specialized sub-agents** - Expert systems for every scenario
- 🔬 **Predictive analytics** - ML-powered incident prevention
- 📊 **Advanced patterns** - Chain-of-thought, conditional logic, automated RCA
- 🎭 **Challenge prompts** - Push your MCP environment to the limits
- 💡 **Hidden features** - SharePoint integration, parallel queries, caching

**From basic queries to autonomous AI operations - it's all here!**

---

**Ready to start? Try one of the prompts above! 🎉**
