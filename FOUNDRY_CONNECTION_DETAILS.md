# 🔗 PHEPy Foundry Connection Details

**Last Updated:** February 13, 2026  
**Status:** ✅ Connected

---

## 📍 Project Information

### Azure AI Foundry Project
- **Project Name:** `phepy`
- **Resource Name:** `phepy-resource`
- **Resource Group:** `rg-PHEPy`
- **Subscription:** Visual Studio Enterprise
- **Subscription ID:** `82b24542-e1a0-441c-845a-f5677d342450`

### Endpoints
- **Project API:** `https://phepy-resource.services.ai.azure.com/api/projects/phepy`
- **Base Endpoint:** `https://phepy-resource.services.ai.azure.com`

### Resource ID
```
/subscriptions/82b24542-e1a0-441c-845a-f5677d342450/resourceGroups/rg-PHEPy/providers/Microsoft.CognitiveServices/accounts/phepy-resource/projects/phepy
```

---

## 🔑 Quick Access

### Portal Links
- **Azure AI Foundry:** https://ai.azure.com
- **Direct Project Link:** https://ai.azure.com/projects/phepy
- **Azure Portal:** https://portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/82b24542-e1a0-441c-845a-f5677d342450/resourceGroups/rg-PHEPy/providers/Microsoft.CognitiveServices/accounts/phepy-resource/overview

### GitHub Repository
- **Repo:** https://github.com/carterryanmsft/PHEPy-Agent
- **Branch:** master
- **Last Sync:** February 13, 2026

---

## 🧪 Test Connection

### Azure CLI Commands
```powershell
# Set subscription
az account set --subscription "82b24542-e1a0-441c-845a-f5677d342450"

# Get project details
az cognitiveservices account show `
    --name phepy-resource `
    --resource-group rg-PHEPy `
    --output json

# List deployments
az cognitiveservices account deployment list `
    --name phepy-resource `
    --resource-group rg-PHEPy `
    --output table
```

### Test API Access (if API key configured)
```powershell
# Get API key
$apiKey = az cognitiveservices account keys list `
    --name phepy-resource `
    --resource-group rg-PHEPy `
    --query "key1" -o tsv

# Test endpoint
$headers = @{
    "api-key" = $apiKey
    "Content-Type" = "application/json"
}

Invoke-RestMethod -Uri "https://phepy-resource.services.ai.azure.com/api/projects/phepy" -Headers $headers
```

---

## 📊 Deployed Resources

### Model Deployments
- **Deployment Name:** phepy-chat *(if deployed)*
- **Model:** gpt-4o (2024-08-06)
- **Scale Type:** Standard
- **Tokens per Minute:** 10K

### Connected Services
- ✅ **GitHub Integration:** carterryanmsft/PHEPy-Agent
- ⏳ **MCP Servers:** To configure
  - ICM MCP ENG (HTTP)
  - One Agentic Platform (HTTP)
  - ADO o365exchange (stdio - local only)
  - Kusto MCP (stdio - local only)

---

## 📁 Synced Content

### From GitHub (86 files)
- ✅ Agent configurations (11 sub-agents)
- ✅ Grounding documentation (62 files)
- ✅ MCP server configs (mcp.json)
- ✅ Routing logic (agent_routing_map.json)
- ✅ System prompt (foundry_system_prompt.txt)

### Knowledge Base
- CAPABILITY_MATRIX.md
- ADVANCED_CAPABILITIES.md
- All sub_agents/*/AGENT_INSTRUCTIONS.md
- TSG system documentation
- Troubleshooting articles

---

## 🔧 Configuration Files

### Local Files
```
✅ foundry_agent_config.json       - Agent definitions
✅ foundry_system_prompt.txt       - System instructions
✅ foundry-deployment-config.json  - Model config
✅ mcp.json                        - MCP server definitions
✅ agent_routing_map.json          - Routing logic
✅ configure-foundry-agents.py     - Setup script
✅ sync-to-foundry.ps1            - Git sync automation
```

### In Foundry Project
```
✅ System Message - Copy from foundry_system_prompt.txt
✅ Data/Files - Synced from GitHub
✅ Model Deployment - phepy-chat (gpt-4o)
⏳ Git Connection - Connect to GitHub repo
⏳ MCP Integrations - Configure HTTP endpoints
```

---

## 🎯 Next Steps

### 1. Complete Git Integration
```
1. Open: https://ai.azure.com/projects/phepy
2. Go to: Settings → Git integration
3. Connect: carterryanmsft/PHEPy-Agent (master branch)
4. Wait 2-3 minutes for sync
```

### 2. Configure System Prompt
```
1. Go to: Playground
2. Copy content from: foundry_system_prompt.txt
3. Paste into: System message box
4. Click: Apply changes
```

### 3. Set Up MCP Integrations
```
1. Go to: Settings → Connections
2. Add HTTP MCPs:
   - ICM MCP: https://icm-mcp-prod.azure-api.net/v1/
   - OAP: https://oap.microsoft.com/api/v1/
```

### 4. Test Agent Routing
```
Test queries in Playground:
✅ "Show me all Sev2 ICMs from last week"
✅ "List P0 bugs for DLP"
✅ "What support cases are at risk?"
✅ "List all available sub-agents"
```

---

## 💡 Usage Examples

### Access Project Programmatically
```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient

credential = DefaultAzureCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id="82b24542-e1a0-441c-845a-f5677d342450",
    resource_group_name="rg-PHEPy",
    workspace_name="phepy-resource"
)

# List deployments
deployments = ml_client.online_deployments.list()
for deployment in deployments:
    print(f"Deployment: {deployment.name}")
```

### Update from Git
```powershell
# Make changes locally
notepad sub_agents/icm_agent/AGENT_INSTRUCTIONS.md

# Sync to GitHub (auto-syncs to Foundry)
.\sync-to-foundry.ps1 -Message "Update ICM agent instructions"
```

---

## 📞 Support

### Troubleshooting
- **Connection issues:** Check subscription permissions (Contributor role)
- **Git sync not working:** Verify repository permissions
- **API access errors:** Regenerate keys in Azure Portal
- **MCP servers not responding:** Check endpoint URLs and authentication

### Documentation
- ✅ [FOUNDRY_GIT_INTEGRATION.md](FOUNDRY_GIT_INTEGRATION.md) - Git setup guide
- ✅ [FOUNDRY_TROUBLESHOOTING.md](FOUNDRY_TROUBLESHOOTING.md) - Common issues
- ✅ [FOUNDRY_QUICK_REFERENCE.md](FOUNDRY_QUICK_REFERENCE.md) - Quick commands

---

**Status:** ✅ Project Connected | ⏳ Git Integration Pending | ⏳ MCP Configuration Pending
