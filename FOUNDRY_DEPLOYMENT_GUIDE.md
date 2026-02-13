# PHEPy Agent - Foundry Deployment Guide
## CxESharedServicesAI-Prod Environment

**Deployment Date**: February 11, 2026  
**Target Environment**: CxESharedServicesAI-Prod  
**Agent Name**: PHEPy Orchestrator (Purview Health & Escalation Agent)  
**Status**: Ready for Deployment

---

## 🎯 Pre-Deployment Checklist

### ✅ Workspace Preparation (COMPLETED)
- [x] Root directory cleaned (16 files)
- [x] 54 scripts archived
- [x] Documentation organized
- [x] All 8 sub-agents with AGENT_INSTRUCTIONS.md
- [x] mcp.json configured (6 MCP servers)
- [x] .gitignore protecting sensitive data
- [x] OAP integration documented

### 🔐 Security Review (REQUIRED BEFORE UPLOAD)
- [ ] No PII in any markdown files
- [ ] No customer names in code examples
- [ ] No tenant IDs in documentation
- [ ] No credentials or API keys
- [ ] No email addresses (except generic examples)
- [ ] Review: data/, output/, archive/ excluded via .gitignore

### 📦 Files to Include in Deployment
```
✅ Include:
- Root config files (mcp.json, requirements.txt, .gitignore, README.md, etc.)
- agent_memory/ (complete system)
- sub_agents/ (all 8 agents)
- docs/ (organized documentation)
- grounding_docs/ (domain knowledge)
- purview_analysis/ (queries & templates only)
- tsg_system/ (complete system)
- risk_reports/templates/ (templates only)
- risk_reports/scripts/ (core scripts only)

❌ Exclude:
- archive/ (old scripts)
- data/ (customer data - gitignored)
- output/ (generated reports - gitignored)
- .venv/ (virtual environment)
- __pycache__/ (Python cache)
- *.csv, *.json files (data - gitignored)
- agent_memory/memory.db (user-specific)
```

---

## 🚀 Deployment Steps

### Step 1: Access Azure AI Foundry Portal
```bash
# Navigate to Azure AI Foundry
https://ai.azure.com

# Or use Azure Portal
https://portal.azure.com
-> Search "Azure AI Foundry"
```

**Login**: Use your @microsoft.com credentials

---

### Step 2: Navigate to CxESharedServicesAI-Prod

1. **Select Workspace**
   - Look for "CxESharedServicesAI-Prod" in workspace list
   - If not visible, use subscription filter:
     - Subscription: `CxE Shared Services`
     - Resource Group: `CxESharedServicesAI-Prod-RG` (or similar)

2. **Verify Access**
   - You need "Contributor" or "AI Developer" role
   - Contact admin if access denied: cxe-ai-admins@microsoft.com

---

### Step 3: Create New Agent Project

#### Option A: Via Azure AI Foundry Portal (Recommended)

1. **Navigate to Agents**
   - Left menu → "Agents" or "Projects"
   - Click "New Agent" or "Create Project"

2. **Agent Configuration**
   ```yaml
   Basic Info:
     Name: PHEPy-Orchestrator
     Display Name: Purview Health & Escalation Agent
     Description: Multi-agent orchestration system for Purview support operations with ICM/ADO/Kusto integration
     Version: 1.0.0
     
   Environment:
     Workspace: CxESharedServicesAI-Prod
     Runtime: Python 3.11
     Region: [Same as workspace - likely West US 2 or East US 2]
   ```

3. **Upload Project Files**
   - Method 1: Drag & drop entire PHEPy folder (excludes .gitignore files)
   - Method 2: Git repository integration (if you have Git repo)
   - Method 3: Azure CLI upload (see Option B below)

#### Option B: Via Azure CLI (Alternative)

```bash
# Install Azure AI CLI extension
az extension add --name ml

# Login
az login

# Set subscription
az account set --subscription "CxE Shared Services"

# Create AI project
az ml project create \
  --name "PHEPy-Orchestrator" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --workspace-name "CxESharedServicesAI-Prod"

# Upload project files (from PHEPy root directory)
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy"

az ml project upload \
  --name "PHEPy-Orchestrator" \
  --path . \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --workspace-name "CxESharedServicesAI-Prod"
```

---

### Step 4: Configure MCP Servers in Foundry

The 6 MCP servers from your mcp.json need to be configured in Foundry:

#### MCP Server Configuration

1. **Navigate to**: Agent Settings → Connections → MCP Servers

2. **Add Each Server**:

**Server 1: ICM MCP ENG** (HTTP)
```json
{
  "name": "ICM MCP ENG",
  "type": "http",
  "url": "https://icm-mcp-prod.azure-api.net/v1/",
  "description": "ICM incidents and escalations"
}
```

**Server 2: o365exchange-mcp-server** (stdio)
```json
{
  "name": "o365exchange-mcp-server",
  "type": "stdio", 
  "command": "npx",
  "args": ["@azure-devops/mcp", "o365exchange"],
  "description": "ADO work items (O365Exchange project)"
}
```

**Server 3: ASIM-Security-mcp-server** (stdio)
```json
{
  "name": "ASIM-Security-mcp-server",
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@azure-devops/mcp", "ASIM-Security"],
  "description": "ASIM Security work items"
}
```

**Server 4: One Agentic Platform** (HTTP)
```json
{
  "name": "one-agentic-platform",
  "type": "http",
  "url": "https://oap.microsoft.com/api/v1/",
  "auth": {
    "type": "oauth2",
    "tenant_id": "${OAP_TENANT_ID}",
    "client_id": "${OAP_CLIENT_ID}",
    "scope": "https://oap.microsoft.com/.default"
  },
  "description": "OAP - Primary for support cases"
}
```

**Server 5: enterprise-mcp** (stdio - fallback)
```json
{
  "name": "enterprise-mcp",
  "type": "stdio",
  "command": "npx",
  "args": ["@mcp-apps/enterprise-mcp-server@latest"],
  "description": "DFM support cases (fallback for OAP)"
}
```

**Server 6: kusto-mcp** (stdio)
```json
{
  "name": "kusto-mcp",
  "type": "stdio",
  "command": "npx",
  "args": ["@mcp-apps/kusto-mcp@latest"],
  "description": "Kusto query engine"
}
```

3. **Set Environment Variables** (for authenticated servers)
   - Navigate to: Agent Settings → Environment Variables
   - Add:
     - `OAP_TENANT_ID` = (from OAP team)
     - `OAP_CLIENT_ID` = (from OAP team)
     - `OAP_CLIENT_SECRET` = (from OAP team) [if using service principal]

---

### Step 5: Configure Grounding Documents

1. **Navigate to**: Agent Settings → Knowledge → Grounding Documents

2. **Upload grounding_docs/ folder**
   - Foundry will index these for RAG (Retrieval Augmented Generation)
   - Creates vector embeddings automatically

3. **Verify Indexing**
   - Check that all .md files are indexed
   - Test semantic search: "What are SLA definitions?"

---

### Step 6: Configure Sub-Agents

Foundry needs to understand your 8 sub-agents:

1. **Navigate to**: Agent Settings → Sub-Agents or Tools

2. **Register Each Sub-Agent**:
   - ICM Agent
   - Kusto Expert
   - Support Case Manager
   - Work Item Manager
   - Tenant Health Monitor
   - Purview Product Expert
   - Program Onboarding Manager
   - Escalation Manager

3. **For Each Sub-Agent**:
   - Point to `sub_agents/{name}/AGENT_INSTRUCTIONS.md`
   - Set role description
   - Configure when to invoke

**Example Configuration (Support Case Manager)**:
```yaml
Sub-Agent: support_case_manager
Instructions File: sub_agents/support_case_manager/AGENT_INSTRUCTIONS.md
Trigger Keywords: 
  - "support case"
  - "customer case"
  - "DFM"
  - "SCIM"
  - "at-risk cases"
MCP Servers: 
  - one-agentic-platform
  - kusto-mcp
  - enterprise-mcp
```

---

### Step 7: Configure Agent Memory (Optional but Recommended)

1. **Navigate to**: Agent Settings → Memory → State Management

2. **Configure Persistent Storage**:
   ```yaml
   Memory Type: Custom (SQLite)
   Storage Location: Azure Blob Storage (for persistence)
   Database: agent_memory/memory.db (will be user-specific)
   ```

3. **Enable Session Management**:
   - Conversations
   - Preferences
   - Insights
   - Search index

---

### Step 8: Set Agent Behavior & Guardrails

1. **Navigate to**: Agent Settings → Behavior

2. **Configure**:
   ```yaml
   System Prompt: (from docs/project/AGENT_INSTRUCTIONS.md)
   
   Temperature: 0.7 (balanced)
   Max Tokens: 4000
   
   Guardrails:
     - PII Redaction: Enabled
     - Customer Data Protection: Enabled
     - Code Execution: Enabled (for Python scripts)
     - External API Calls: Enabled (for MCP servers)
   
   Safety:
     - Content Filter: Standard
     - Jailbreak Detection: Enabled
     - Prompt Injection Protection: Enabled
   ```

---

### Step 9: Test Deployment

1. **Open Foundry Playground**
   - Navigate to: Agent → Test Playground

2. **Run Test Queries**:

**Test 1: Basic Orchestration**
```
"List all available agents and their capabilities"
Expected: Should list 8 sub-agents
```

**Test 2: MCP Connection**
```
"How many ICMs does the Purview team have?"
Expected: Should use ICM MCP to query
```

**Test 3: Sub-Agent Invocation**
```
"Show me at-risk support cases for this week"
Expected: Should invoke support_case_manager with OAP
```

**Test 4: Grounding Docs**
```
"What is the SLA for P0 cases?"
Expected: Should retrieve from grounding docs
```

**Test 5: Multi-Agent Workflow**
```
"Analyze ICM 693849812 and check if there are related support cases"
Expected: Should invoke icm_agent + support_case_manager
```

---

### Step 10: Configure Access & Permissions

1. **Navigate to**: Agent Settings → Access Control

2. **Add Users/Groups**:
   ```yaml
   User Groups:
     - Purview-PHE-Team (full access)
     - Purview-PMs (read access)
     - Purview-Escalation-Owners (full access)
     - CxE-Leadership (read access)
   ```

3. **Set Permissions**:
   - **Full Access**: Can query agent, view results, modify settings
   - **Read Access**: Can query agent, view results only
   - **Admin**: Can modify agent configuration

---

### Step 11: Publish Agent

1. **Validate Deployment**
   - Review all test results
   - Check all MCP servers connected
   - Verify grounding docs indexed
   - Confirm sub-agents registered

2. **Publish**
   - Navigate to: Agent → Publish
   - Version: 1.0.0
   - Release Notes: "Initial PHEPy Orchestrator deployment"
   - Click "Publish to Environment"

3. **Get Agent Endpoint**
   - Copy agent URL (e.g., `https://ai.azure.com/agents/phepy-orchestrator`)
   - Share with team

---

## 📊 Post-Deployment Tasks

### Immediate (Day 1)
- [ ] Share agent URL with PHE team
- [ ] Send getting started email with example queries
- [ ] Monitor usage in first 24 hours
- [ ] Check for errors in Application Insights

### Week 1
- [ ] Collect user feedback
- [ ] Identify most common queries
- [ ] Optimize slow queries
- [ ] Add more examples to documentation

### Month 1
- [ ] Usage metrics review
- [ ] Add new capabilities based on feedback
- [ ] Update grounding docs with learnings
- [ ] Publish v1.1 with improvements

---

## 🔍 Monitoring & Troubleshooting

### Application Insights
```bash
# Navigate to Azure Portal
Resource: CxESharedServicesAI-Prod
-> Monitoring -> Application Insights

# Key Metrics to Watch:
- Agent invocations per day
- Average response time
- Error rate
- MCP server connection failures
- Sub-agent invocation distribution
```

### Common Issues & Solutions

**Issue 1: MCP Server Connection Failed**
- Check: Network connectivity
- Check: Authentication credentials
- Solution: Test MCP server independently

**Issue 2: Grounding Docs Not Found**
- Check: Files uploaded correctly
- Check: Indexing completed
- Solution: Re-upload and re-index

**Issue 3: Sub-Agent Not Invoked**
- Check: Trigger keywords configured
- Check: AGENT_INSTRUCTIONS.md accessible
- Solution: Update routing logic

**Issue 4: Slow Response Times**
- Check: Which MCP server is slow
- Check: Kusto query complexity
- Solution: Add caching, optimize queries

---

## 📞 Support Contacts

### Azure AI Foundry Support
- **Email**: azureai-support@microsoft.com
- **Teams**: [Azure AI Foundry Support](https://teams.microsoft.com/l/channel/...)
- **Docs**: https://aka.ms/azureai-docs

### CxE Environment Access
- **Email**: cxe-ai-admins@microsoft.com
- **DL**: CxESharedServicesAI-Admins@microsoft.com

### OAP Support (for OAP integration)
- **Email**: oap-support@microsoft.com
- **Teams**: [OAP Support](https://teams.microsoft.com/l/channel/...)

---

## 📚 Additional Resources

### Foundry Documentation
- **Agent Development**: https://aka.ms/foundry-agents
- **MCP Integration**: https://aka.ms/foundry-mcp
- **Deployment Guide**: https://aka.ms/foundry-deploy

### PHEPy Documentation
- **[README.md](../README.md)** - Project overview
- **[GETTING_STARTED.md](../GETTING_STARTED.md)** - Quick start
- **[CAPABILITY_MATRIX.md](../CAPABILITY_MATRIX.md)** - Feature reference
- **[FOUNDRY_READINESS_REPORT.md](../FOUNDRY_READINESS_REPORT.md)** - Deployment analysis

---

## ✅ Deployment Checklist Summary

### Before Deployment
- [x] Workspace cleaned and organized
- [ ] Security review completed (no PII)
- [ ] Test all MCP servers locally
- [ ] OAP credentials obtained

### During Deployment
- [ ] Agent project created in Foundry
- [ ] All files uploaded
- [ ] 6 MCP servers configured
- [ ] Grounding docs uploaded & indexed
- [ ] 8 sub-agents registered
- [ ] Agent memory configured
- [ ] Guardrails set

### Testing
- [ ] Basic orchestration test
- [ ] MCP connection test
- [ ] Sub-agent invocation test
- [ ] Grounding docs test
- [ ] Multi-agent workflow test

### Go-Live
- [ ] Access permissions set
- [ ] Agent published
- [ ] Team notified
- [ ] Monitoring configured
- [ ] Feedback channel established

---

## 🎯 Success Criteria

**Agent is successfully deployed when:**
- ✅ All 6 MCP servers connect successfully
- ✅ All 8 sub-agents accessible
- ✅ Grounding docs searchable
- ✅ Test queries return correct results
- ✅ Response time < 5 seconds for simple queries
- ✅ Team can access and use agent

---

**Deployment Owner**: Ryan Carter (carterryan@microsoft.com)  
**Deployment Date**: TBD  
**Environment**: CxESharedServicesAI-Prod  
**Status**: Ready for Deployment ✅

---

*Good luck with your deployment! 🚀*
