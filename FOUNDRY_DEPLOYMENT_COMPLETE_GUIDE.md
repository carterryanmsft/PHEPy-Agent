# 🚀 PHEPy Deployment to Azure AI Foundry

**Target Environment:** CxESharedServicesAI-Prod
**Deployment Method:** Azure AI Foundry with MCP Server Integration

---

## 📋 Prerequisites Check

```powershell
# Verify you have access
az login
az account list --query "[].{Name:name, Id:id}" -o table

# Install AI extension
az extension add --name ml --upgrade
```

---

## 🎯 Step 1: Access Azure AI Foundry (5 min)

### Portal Access
```powershell
# Open Azure AI Studio
Start-Process "https://ai.azure.com"
```

**In the portal:**
1. Sign in with your Microsoft account
2. Look for **CxESharedServicesAI-Prod** workspace
3. If not visible:
   - Click **All resources** or **Browse**
   - Search for "CxESharedServicesAI"
   - Select the workspace

### Alternative: Find workspace via CLI
```powershell
# List all AI workspaces you have access to
az ml workspace list --query "[].{Name:name, ResourceGroup:resourceGroup, Location:location}" -o table
```

---

## 🛠️ Step 2: Create Agent Project (10 min)

### In Azure AI Foundry Portal:

1. **Navigate to your workspace:** CxESharedServicesAI-Prod

2. **Create new project:**
   - Click **+ New project** or **Create**
   - Project name: **PHEPy-Orchestrator**
   - Description: **Purview Product Health & Escalation Orchestrator Agent**
   - Click **Create**

3. **Wait for deployment** (~2-3 minutes)

---

## 🤖 Step 3: Deploy Agent with Instructions (15 min)

### Create the Agent

1. In your project, go to **Playground** or **Chat**

2. **Configure Instructions:**
   Click **System message** and paste:

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

3. **Configure Model Settings:**
   - Model: **GPT-4** or **GPT-4o** (recommended)
   - Temperature: **0.3** (more precise, less creative)
   - Max tokens: **4000**

---

## 📚 Step 4: Add Knowledge/Grounding Data (15 min)

### Upload Documentation

1. Go to **Data** → **+ Add data** or **Upload files**

2. Navigate to your PHEPy folder and upload:

```powershell
# Essential documentation files:
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\GETTING_STARTED.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\CAPABILITY_MATRIX.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\ADVANCED_CAPABILITIES.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\QUICK_REFERENCE.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\docs\QUERY_CHEAT_SHEET.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\docs\AGENT_BEST_PRACTICES.md
C:\Users\carterryan\OneDrive - Microsoft\PHEPy\tsg_system\wiki_tsg_baseline_report.md
```

3. **Create an index** for better retrieval:
   - Indexing strategy: **Keyword + Semantic**
   - Chunk size: **1024** tokens
   - Overlap: **128** tokens

### Or: Connect to Azure AI Search (Advanced)
```powershell
# Create AI Search index for your documentation
az search index create \
  --name phepy-docs \
  --service-name <your-search-service> \
  --fields name:string,content:string
```

---

## 🔌 Step 5: Configure MCP Server Connections (20 min)

### Option A: Using Azure Functions as MCP Proxy

Since MCP servers aren't natively supported yet in Foundry, we'll create HTTP wrappers:

#### Deploy MCP Proxy Function

```powershell
cd "C:\Users\carterryan\OneDrive - Microsoft\PHEPy"

# Create Azure Function wrapper
New-Item -ItemType Directory -Path "mcp-proxy" -Force
cd mcp-proxy

# Create function.json
@"
{
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get", "post"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "res"
    }
  ]
}
"@ | Set-Content function.json

# Deploy (requires func core tools)
func azure functionapp publish <your-function-app-name>
```

### Option B: Use Direct API Endpoints

Configure these as **HTTP connections** in your deployment:

1. **ICM API:**
   ```
   Base URL: https://icm-mcp-prod.azure-api.net/v1/
   Auth: Microsoft Entra ID (OAuth 2.0)
   Scope: api://icm-mcp/.default
   ```

2. **Azure DevOps API:**
   ```
   Base URL: https://dev.azure.com/microsoft/
   Auth: Personal Access Token or OAuth
   Projects: o365exchange, ASIM-Security
   ```

3. **OAP API:**
   ```
   Base URL: https://oap.microsoft.com/api/v1/
   Auth: Microsoft Entra ID
   ```

### Configure in Foundry

1. Go to **Connections** or **Data connections**
2. **+ New connection** → **REST API**
3. Configure each endpoint:
   - Name: ICM MCP Server
   - URL: https://icm-mcp-prod.azure-api.net/v1/
   - Authentication: Set up Microsoft Entra ID app registration
   - Test connection

---

## 📦 Step 6: Deploy Configuration as Code (Advanced)

### Create deployment specification

```yaml
# phepy-deployment.yaml
$schema: https://azuremlschemas.azureedge.net/latest/deployment.schema.json
name: phepy-orchestrator
description: Purview Product Health & Escalation Orchestrator
model: gpt-4o
system_message_file: ./system-instructions.txt
data_sources:
  - type: azure_search
    index_name: phepy-docs
  - type: rest_api
    name: icm-mcp
    base_url: https://icm-mcp-prod.azure-api.net/v1/
endpoints:
  - name: chat
    type: rest
    model: gpt-4o
```

### Deploy via CLI

```powershell
# Deploy the agent
az ml online-deployment create \
  --file phepy-deployment.yaml \
  --workspace-name CxESharedServicesAI-Prod \
  --resource-group <resource-group-name>
```

---

## 🧪 Step 7: Test Your Deployment (10 min)

### In the Playground

Test with these queries:

```
1. "What capabilities does PHEPy have?"
   → Should reference your uploaded documentation

2. "Explain how to troubleshoot DLP label visibility issues"
   → Should use TSG documentation

3. "What are the key products you support?"
   → Should list DLP, MIP, eDiscovery, etc.

4. "How do I query ICM for critical incidents?"
   → Should provide guidance on ICM queries

5. "Show me the structure of a Kusto query for DLP telemetry"
   → Should provide KQL query example
```

### Check Responses
- Verify accuracy against your documentation
- Check if knowledge retrieval is working (sources cited)
- Test conversation flow with follow-up questions

---

## 🚀 Step 8: Deploy to Endpoint (15 min)

### Create Managed Endpoint

1. Go to **Endpoints** → **+ Create endpoint**

2. Configure:
   - **Name:** phepy-orchestrator
   - **Authentication:** Key-based or Microsoft Entra ID
   - **Compute:** Serverless (for auto-scaling)
   - **Model**: Your configured chat model

3. **Deploy** and wait for provisioning (~5-10 minutes)

4. **Get endpoint URL:**
   ```powershell
   az ml online-endpoint show \
     --name phepy-orchestrator \
     --workspace-name CxESharedServicesAI-Prod \
     --query scoring_uri -o tsv
   ```

### Test Endpoint

```powershell
# Get the endpoint key
$key = az ml online-endpoint get-credentials `
  --name phepy-orchestrator `
  --workspace-name CxESharedServicesAI-Prod `
  --query primaryKey -o tsv

# Test with curl
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $key"
}

$body = @{
    messages = @(
        @{role = "user"; content = "What capabilities does PHEPy have?"}
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "<endpoint-url>" -Method Post -Headers $headers -Body $body
```

---

## 🔗 Step 9: Integrate with Tools (10 min)

### Teams Integration

1. Create **Teams app manifest**:

```json
{
  "version": "1.0.0",
  "manifestVersion": "1.16",
  "id": "phepy-orchestrator-bot",
  "name": {
    "short": "PHEPy",
    "full": "PHEPy Orchestrator Assistant"
  },
  "description": {
    "short": "Purview support assistant",
    "full": "AI assistant for Microsoft Purview product health and escalation management"
  },
  "bots": [{
    "botId": "<your-bot-id>",
    "scopes": ["personal", "team"],
    "commandLists": [{
      "scopes": ["personal", "team"],
      "commands": [
        {"title": "Critical Incidents", "description": "Show Sev 0/1 incidents"},
        {"title": "P0 Bugs", "description": "Show priority 0 bugs"},
        {"title": "Help", "description": "Show available commands"}
      ]
    }]
  }]
}
```

2. **Upload to Teams:**
   - Teams Admin Center → Apps → Upload custom app
   - Select manifest package
   - Approve for your organization

### VS Code Extension (Future)

Your MCP configuration in `mcp.json` can be used directly in VS Code with Copilot extensions.

---

## 📊 Step 10: Monitor & Optimize (Ongoing)

### View Analytics

```powershell
# Get deployment metrics
az ml online-deployment show \
  --name phepy-orchestrator \
  --workspace-name CxESharedServicesAI-Prod
```

### Application Insights

1. Go to **Monitoring** → **Application Insights**
2. View:
   - Request volume
   - Response latency (target: <2 seconds)
   - Token usage
   - Error rates

### Optimize Based on Usage

- **High latency?** Consider caching common queries
- **High token costs?** Reduce max_tokens or optimize system prompt
- **Low accuracy?** Add more documentation or refine instructions
- **Missing data?** Add MCP server connections or APIs

---

## 🎯 Quick Start Commands

```powershell
# Open Azure AI Studio
Start-Process "https://ai.azure.com"

# Or deploy via CLI in one command
az ml online-deployment create `
  --name phepy-orchestrator `
  --workspace-name CxESharedServicesAI-Prod `
  --model gpt-4o `
  --system-message-file system-instructions.txt
```

---

## ✅ Success Checklist

- [ ] Azure AI Foundry workspace accessed (CxESharedServicesAI-Prod)
- [ ] New project created (PHEPy-Orchestrator)
- [ ] System instructions configured
- [ ] GPT-4/GPT-4o model selected
- [ ] Documentation uploaded (7+ files)
- [ ] Knowledge index created
- [ ] MCP/API connections configured (at least 1)
- [ ] Playground tested (5+ queries)
- [ ] Endpoint deployed
- [ ] Endpoint tested via API
- [ ] Teams integration (optional)
- [ ] Monitoring dashboard configured

---

## 📞 Troubleshooting

**Can't find workspace?**
```powershell
az ml workspace list -o table
# Or check in portal: portal.azure.com → Search "CxESharedServicesAI"
```

**Authentication errors?**
```powershell
az login --tenant microsoft.onmicrosoft.com
az account set --subscription <subscription-id>
```

**Deployment fails?**
- Check quota limits in subscription
- Verify model availability in region
- Ensure proper permissions (Contributor role)

---

## 📚 Resources

- Azure AI Foundry: https://ai.azure.com
- Azure AI Documentation: https://learn.microsoft.com/azure/ai-studio/
- Your MCP config: `mcp.json`
- Your docs: `GETTING_STARTED.md`, `CAPABILITY_MATRIX.md`

---

**Estimated Time:** 90-120 minutes for full deployment
**Minimum Viable:** 30 minutes (project + instructions + docs + test)

🎉 Once deployed, you'll have an enterprise-grade AI agent accessible via API, Teams, and other integrations!
