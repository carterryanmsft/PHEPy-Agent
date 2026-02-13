# MCP Setup - Quick Reference

**For PHEPy Agent deployment**

---

## 🎯 Your MCP Servers

| Server | Purpose | Config Required |
|--------|---------|-----------------|
| **ICM MCP** | Incident management | API Key |
| **ADO MCP** | Work items (bugs/features) | PAT Token |
| **Kusto MCP** | Telemetry queries | Azure Auth |
| **OAP** | Support cases (primary) | API Key |
| **Enterprise MCP** | Support cases (legacy) | SCIM Token |

---

## ⚡ Quick Setup (3 Steps)

### Step 1: Configure Environment Variables
```powershell
.\setup-mcp-env.ps1
```
This will prompt you for each server's credentials interactively.

### Step 2: Test Connections
```powershell
.\test-mcp-servers.ps1
```
Validates all configured servers are accessible.

### Step 3: Test Agent Integration
```powershell
.\test-agent-cli.ps1 -Message "What MCP servers are available?"
```

---

## 📋 Current Configuration

**File:** [mcp.json](mcp.json)

```json
{
  "servers": {
    "ICM MCP ENG": {
      "type": "http",
      "url": "https://icm-mcp-prod.azure-api.net/v1/"
    },
    "o365exchange-mcp-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["@azure-devops/mcp", "o365exchange"]
    },
    "kusto-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["@mcp-apps/kusto-mcp@latest"]
    },
    "one-agentic-platform": {
      "type": "http",
      "url": "https://oap.microsoft.com/api/v1/"
    }
  }
}
```

---

## 🔑 Required Tokens/Keys

### Where to Get Them:

**1. ICM MCP API Key**
- Portal: Azure Portal → API Management → icm-mcp-prod
- Or email: icm-support@microsoft.com

**2. Azure DevOps PAT**
- Go to: https://dev.azure.com/YOUR_ORG/_usersSettings/tokens
- Scopes needed: Work Items (Read/Write), Code (Read)

**3. Kusto Auth**
- Option A: `az login` (recommended for dev)
- Option B: Service Principal credentials

**4. OAP API Key**
- Portal: https://oap.microsoft.com/admin/api-keys
- Or email: oap-support@microsoft.com

---

## 🧪 Test Individual Servers

### Test ICM
```powershell
curl -H "Ocp-Apim-Subscription-Key: YOUR_KEY" `
     "https://icm-mcp-prod.azure-api.net/v1/health"
```

### Test ADO
```powershell
az devops project list --org https://dev.azure.com/YOUR_ORG
```

### Test Kusto
```powershell
az login  # If using AzureCLI auth mode
npx @mcp-apps/kusto-mcp@latest --test
```

### Test OAP
```powershell
$headers = @{"Authorization" = "Bearer YOUR_KEY"}
Invoke-RestMethod -Uri "https://oap.microsoft.com/api/v1/health" -Headers $headers
```

---

## 🔧 Common Commands

```powershell
# Show current configuration
.\setup-mcp-env.ps1 -ShowCurrent

# Test all servers
.\test-mcp-servers.ps1

# Configure new server
.\setup-mcp-env.ps1

# Test agent with MCP
.\test-agent-cli.ps1 -Message "Query ICM for incident 728221759"
```

---

## 🚨 Troubleshooting

### "Authentication failed"
- Check token hasn't expired
- Regenerate token and update environment variable
- Restart terminal after setting new variables

### "npx command not found"
```powershell
winget install OpenJS.NodeJS
```

### "Module not found"
```powershell
npm install -g @azure-devops/mcp
npm install -g @mcp-apps/kusto-mcp
npm install -g @mcp-apps/enterprise-mcp-server
```

### "Azure CLI not logged in"
```powershell
az login
az account show  # Verify login
```

### Check Environment Variables
```powershell
# Check if variables are set
$env:ICM_MCP_API_KEY
$env:AZURE_DEVOPS_PAT
$env:KUSTO_CLUSTER_URL
$env:OAP_API_KEY

# Or use the script
.\setup-mcp-env.ps1 -ShowCurrent
```

---

## 📖 Full Documentation

See **[MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)** for:
- Detailed setup instructions for each server
- Authentication methods and options
- Integration with Azure AI Agent
- Advanced configuration
- Security best practices

---

## 🎯 Integration with Azure AI Agent

Your agent (asst_Oybm3OHCwVHWSk3bUb9oF9le) is configured with system instructions that reference these MCP servers.

**To enable MCP function calling:**

1. The agent knows about these servers from system instructions
2. For actual data access, implement function calling:
   - Define tools in agent configuration
   - Create Azure Functions to proxy MCP calls
   - Map agent tool calls to MCP server operations

**Example test:**
```powershell
.\test-agent-cli.ps1 -Message "What data sources do you have access to?"
```

The agent will describe the MCP servers it knows about.

---

## ✅ Setup Checklist

- [ ] Node.js installed (`node --version`)
- [ ] Azure CLI installed and logged in (`az login`)
- [ ] Environment variables configured (`.\setup-mcp-env.ps1`)
- [ ] MCP servers tested (`.\test-mcp-servers.ps1`)
- [ ] Agent tested (`.\test-agent-cli.ps1`)
- [ ] Read full guide: [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)

---

**Need help?** Run `.\test-mcp-servers.ps1` to diagnose issues!
