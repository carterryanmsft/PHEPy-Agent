# 🤖 Copilot Studio Deployment Guide for PHEPy

This guide walks through deploying the PHEPy Orchestrator Agent to Microsoft Copilot Studio.

## 📋 Prerequisites

Install these tools before starting:

1. **Power Platform CLI**
   ```powershell
   winget install Microsoft.PowerPlatformCLI
   ```
   Or download from: https://aka.ms/PowerPlatformCLI

2. **Azure CLI** (already installed)
   ```powershell
   winget install Microsoft.AzureCLI
   ```

3. **Node.js** (for MCP servers)
   ```powershell
   winget install OpenJS.NodeJS
   ```

## 🚀 Quick Deployment

### Step 1: Generate Manifest and Actions

```powershell
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy"
.\deploy-to-copilot-studio.ps1
```

This creates:
- `copilot-studio-manifest.json` - Main agent configuration
- `actions/` folder - Action definitions for each MCP server

### Step 2: Login to Power Platform

```powershell
# Find your environment URL from https://admin.powerplatform.microsoft.com
pac auth create --environment https://your-env.crm.dynamics.com
```

### Step 3: Open Copilot Studio

```powershell
.\deploy-to-copilot-studio.ps1 -OpenPortal
```

Or visit directly: https://copilotstudio.microsoft.com

## 🔧 Manual Configuration in Copilot Studio

### Create Declarative Agent

1. **In Copilot Studio Portal:**
   - Click **"Create"** → **"New Copilot"**
   - Select **"Declarative Agent"** or **"Agent with Copilot Studio"**
   - Choose **"Upload manifest"**

2. **Upload Manifest:**
   - Select `copilot-studio-manifest.json`
   - Review name and description
   - Click **"Create"**

### Configure Actions (MCP Server Connectors)

For each action, you'll need to create a Custom Connector:

#### 1. ICM MCP Server

**Settings:**
- Name: `ICM Incident Management`
- Base URL: `https://icm-mcp-prod.azure-api.net/v1/`
- Authentication: Microsoft Entra ID
- Resource: `api://icm-mcp`

**Operations to Add:**
```
GET /incidents/{incidentId} - Get incident details
POST /incidents/search - Search incidents by criteria
GET /incidents/{incidentId}/impact - Get customer impact data
```

#### 2. Azure DevOps MCP

**Settings:**
- Name: `Azure DevOps Work Items`
- Base URL: Handled by NPX package
- Authentication: OAuth 2.0 with Azure DevOps
- Scopes: `vso.work` `vso.code` `vso.build`

**Note:** ADO MCP runs via stdio (npx command), so you'll need to:
- Either: Create Azure DevOps connector in Power Platform
- Or: Wrap with an HTTP proxy endpoint

**Operations:**
```
GET /_apis/wit/workitems/{id} - Get work item
POST /_apis/wit/wiql - Query work items
GET /_apis/build/builds - Get builds
```

#### 3. Kusto MCP Server

**Settings:**
- Name: `Kusto Query Engine`
- Base URL: Handled by NPX package
- Authentication: Azure AD with Kusto scope

**Operations:**
```
POST /query - Execute KQL query
GET /tables - List available tables
GET /schema/{table} - Get table schema
```

#### 4. OAP (One Agentic Platform)

**Settings:**
- Name: `Support Case Management`
- Base URL: `https://oap.microsoft.com/api/v1/`
- Authentication: Microsoft Entra ID

**Operations:**
```
GET /cases/{caseId} - Get case details
POST /cases/search - Search cases
GET /cases/{caseId}/history - Get case history
```

## 🔐 Authentication Setup

### For HTTP MCP Servers (ICM, OAP)

1. Register app in Azure AD if needed
2. Add API permissions
3. Configure in Copilot Studio:
   - Authentication Type: OAuth 2.0
   - Identity Provider: Microsoft Entra ID
   - Client ID: (from app registration)
   - Client Secret: (from app registration)

### For Stdio MCP Servers (ADO, Kusto)

**Option A: Use Existing Power Platform Connectors**
- Azure DevOps connector (certified)
- Azure Data Explorer connector (for Kusto)

**Option B: Create Proxy Service**
Create an Azure Function that:
1. Receives HTTP requests
2. Calls stdio MCP via npx
3. Returns results as HTTP response

Example wrapper structure:
```javascript
// function.js
const { spawn } = require('child_process');

module.exports = async function (context, req) {
    const mcp = spawn('npx', ['@azure-devops/mcp', 'o365exchange']);
    // ... handle stdio communication ...
    context.res = { body: result };
};
```

## 📝 Conversation Starters

The manifest includes these conversation starters:

1. **"Show critical incidents"** → Queries current Sev 0/1 ICMs
2. **"Recent P0 bugs"** → Lists high-priority ADO bugs
3. **"Customer case trends"** → Analyzes support patterns
4. **"Query telemetry"** → Helps build Kusto queries

You can customize these in the manifest before upload.

## 🧪 Testing Your Agent

### In Copilot Studio Test Pane

1. Click **"Test"** in upper right
2. Try conversation starters:
   ```
   Show me critical incidents
   ```
3. Validate each MCP connection:
   ```
   Get details for ICM incident 728221759
   Show ADO bug 3563451
   Query Kusto for DLP events today
   Find support case 118 details
   ```

### Check Action Execution

In the test pane, expand action traces to see:
- ✅ Which action was called
- ✅ Request/response payloads
- ✅ Authentication status
- ❌ Any errors or failures

## 🚢 Publishing

### 1. Publish to Teams

- In Copilot Studio: **Publish** → **Microsoft Teams**
- Select channels: `General`, `PHE Team`, etc.
- Set permissions (who can use the agent)

### 2. Publish to Web

- **Publish** → **Demo website** or **Custom website**
- Get embed code
- Add to internal portal or SharePoint

### 3. Publish to Other Channels

- Power Apps
- Power Automate
- Dynamics 365
- Custom channel via Direct Line API

## 📊 Monitoring & Analytics

### View Usage Analytics

- **Analytics tab** in Copilot Studio
- Metrics: Sessions, Messages, CSAT, Escalation rate
- Topic performance
- Action success rates

### Setup Alerts

- Configure App Insights integration
- Set thresholds for:
  - Action failure rate > 5%
  - Response time > 3 seconds
  - User satisfaction < 80%

## 🔄 Advanced: MCP Server Proxy (For Stdio MCPs)

If you need to expose stdio MCP servers as HTTP:

### Create Azure Function Proxy

1. **Create Function App:**
   ```powershell
   az functionapp create `
     --name phepy-mcp-proxy `
     --resource-group PHEPy-RG `
     --consumption-plan-location eastus `
     --runtime node `
     --runtime-version 18 `
     --functions-version 4
   ```

2. **Deploy MCP Proxy Code:**
   ```javascript
   // ado-proxy/index.js
   const { exec } = require('child_process');
   
   module.exports = async function (context, req) {
       const command = `npx -y @azure-devops/mcp o365exchange`;
       const result = await executeCommand(command, req.body);
       context.res = { body: result };
   };
   ```

3. **Update Copilot Studio Action:**
   - Base URL: `https://phepy-mcp-proxy.azurewebsites.net/api/ado`
   - Authentication: Function key or Azure AD

## 🛠️ Troubleshooting

### Agent Not Responding

- Check action connectivity in "Actions" tab
- Verify authentication tokens are valid
- Review error logs in "Analytics" → "Errors"

### Authentication Failures

- Ensure app registration has correct API permissions
- Check client secret hasn't expired
- Verify resource/scope URLs are correct

### Slow Response Times

- Check MCP server latency
- Consider caching frequently accessed data
- Use conversation context to pre-fetch likely queries

## 📚 Additional Resources

- [Copilot Studio Documentation](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copilot-studio-agent)
- [Power Platform Connectors](https://learn.microsoft.com/connectors/)
- [Azure DevOps REST API](https://learn.microsoft.com/rest/api/azure/devops/)
- [ICM API Documentation](https://icmdocs.azurewebsites.net/)

## 🎯 Next Steps

1. ✅ Run deployment script
2. ✅ Upload manifest to Copilot Studio
3. ✅ Configure actions/connectors
4. ✅ Test with conversation starters
5. ✅ Publish to Teams
6. ✅ Train team on usage
7. ✅ Monitor analytics and iterate

---

**Need Help?**
- Check [GETTING_STARTED.md](GETTING_STARTED.md) for PHEPy basics
- Review [CAPABILITY_MATRIX.md](CAPABILITY_MATRIX.md) for full feature list
- See [mcp.json](mcp.json) for current MCP configuration
