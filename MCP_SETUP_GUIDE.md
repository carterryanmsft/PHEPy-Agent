# MCP Server Setup Guide for PHEPy Agent

**Model Context Protocol (MCP)** integration for Azure AI Foundry deployment

---

## 📋 Overview

Your PHEPy agent uses **6 MCP servers** to access enterprise data:

| MCP Server | Type | Purpose | Authentication |
|------------|------|---------|----------------|
| **ICM MCP** | HTTP | Incident management | API Key |
| **ADO o365exchange** | stdio | O365 work items | PAT Token |
| **ADO ASIM-Security** | stdio | Security work items | PAT Token |
| **One Agentic Platform** | HTTP | Support cases (primary) | OAuth/API Key |
| **Enterprise MCP** | stdio | Support cases (legacy) | SCIM Token |
| **Kusto MCP** | stdio | Telemetry queries | Azure AD Auth |

---

## 🔧 Current Configuration

Your [mcp.json](mcp.json) has these servers configured:

```json
{
  "servers": {
    "o365exchange-mcp-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["@azure-devops/mcp", "o365exchange"]
    },
    "ASIM-Security-mcp-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp", "ASIM-Security"]
    },
    "ICM MCP ENG": {
      "type": "http",
      "url": "https://icm-mcp-prod.azure-api.net/v1/"
    },
    "one-agentic-platform": {
      "type": "http",
      "url": "https://oap.microsoft.com/api/v1/"
    },
    "enterprise-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["@mcp-apps/enterprise-mcp-server@latest"]
    },
    "kusto-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["@mcp-apps/kusto-mcp@latest"]
    }
  }
}
```

---

## 🚀 Setup Instructions

### Prerequisites

1. **Node.js** (for stdio servers)
   ```powershell
   winget install OpenJS.NodeJS
   ```

2. **Azure CLI** (for authentication)
   ```powershell
   az login
   ```

3. **Environment variables** (see sections below)

---

## 1️⃣ ICM MCP Server (HTTP)

### Purpose
Access ICM incidents, escalations, customer impact data

### Setup

**Endpoint:** `https://icm-mcp-prod.azure-api.net/v1/`

**Authentication:** API Key via Azure API Management

**Environment Variables:**
```powershell
$env:ICM_MCP_API_KEY = "YOUR_API_KEY_HERE"
$env:ICM_API_ENDPOINT = "https://icm-mcp-prod.azure-api.net/v1/"
```

**Get API Key:**
```powershell
# Option 1: From Azure Portal
# Navigate to: Azure Portal → API Management → icm-mcp-prod → Subscriptions

# Option 2: Request from ICM team
# Email: icm-support@microsoft.com
# Subject: "MCP API Access Request for PHEPy Agent"
```

**Test Connection:**
```powershell
# Test via curl
curl -H "Ocp-Apim-Subscription-Key: YOUR_KEY" `
     "https://icm-mcp-prod.azure-api.net/v1/incidents/728221759"
```

**Available Operations:**
- Get incident by ID
- Search incidents by criteria
- Get customer impact data
- List recent escalations
- Get incident timeline

---

## 2️⃣ Azure DevOps MCP Servers (stdio)

### Purpose
Access ADO work items (bugs, features, tasks)

### Setup for o365exchange Project

**Install:**
```powershell
npm install -g @azure-devops/mcp
```

**Environment Variables:**
```powershell
$env:AZURE_DEVOPS_ORG_URL = "https://dev.azure.com/YOUR_ORG"
$env:AZURE_DEVOPS_PAT = "YOUR_PERSONAL_ACCESS_TOKEN"
$env:AZURE_DEVOPS_PROJECT = "o365exchange"
```

**Get Personal Access Token (PAT):**
1. Go to: https://dev.azure.com/YOUR_ORG/_usersSettings/tokens
2. Click **"+ New Token"**
3. Name: `PHEPy Agent MCP`
4. **Scopes:** 
   - ✅ Work Items: Read & Write
   - ✅ Code: Read
   - ✅ Build: Read
   - ✅ Release: Read
5. Click **Create**
6. **Copy the token immediately** (won't be shown again)

**Set Environment Variable:**
```powershell
# For current session
$env:AZURE_DEVOPS_PAT = "your_pat_token_here"

# Permanently (Windows)
[System.Environment]::SetEnvironmentVariable('AZURE_DEVOPS_PAT', 'your_pat_here', 'User')

# Verify
$env:AZURE_DEVOPS_PAT
```

**Test Connection:**
```powershell
# Test with npx
npx @azure-devops/mcp o365exchange --test

# Or test via az CLI
az devops project show --org https://dev.azure.com/YOUR_ORG --project o365exchange
```

**Setup for ASIM-Security Project:**

Same process, just use `ASIM-Security` as project name:
```powershell
$env:AZURE_DEVOPS_PROJECT = "ASIM-Security"
npx @azure-devops/mcp ASIM-Security --test
```

---

## 3️⃣ One Agentic Platform (OAP) - HTTP

### Purpose
Primary support case management system

### Setup

**Endpoint:** `https://oap.microsoft.com/api/v1/`

**Authentication:** OAuth 2.0 or API Key

**Environment Variables:**
```powershell
$env:OAP_API_KEY = "YOUR_OAP_API_KEY"
$env:OAP_ENDPOINT = "https://oap.microsoft.com/api/v1/"

# OR for OAuth
$env:OAP_CLIENT_ID = "YOUR_CLIENT_ID"
$env:OAP_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
$env:OAP_TENANT_ID = "YOUR_TENANT_ID"
```

**Get API Key:**
```powershell
# Request from OAP team
# Portal: https://oap.microsoft.com/admin/api-keys
# Or contact: oap-support@microsoft.com
```

**Test Connection:**
```powershell
# Test API
$headers = @{
    "Authorization" = "Bearer YOUR_API_KEY"
    "Content-Type" = "application/json"
}
Invoke-RestMethod -Uri "https://oap.microsoft.com/api/v1/health" -Headers $headers
```

---

## 4️⃣ Enterprise MCP Server (stdio) - Legacy

### Purpose
Fallback for DFM support cases with SCIM access

### Setup

**Install:**
```powershell
npm install -g @mcp-apps/enterprise-mcp-server
```

**Environment Variables:**
```powershell
$env:ENTERPRISE_SCIM_TOKEN = "YOUR_SCIM_TOKEN"
$env:ENTERPRISE_API_ENDPOINT = "https://enterprise.microsoft.com/api"
```

**Get SCIM Token:**
```powershell
# Request from Microsoft Enterprise Portal
# Navigate to: Security & Compliance → API Access → SCIM Tokens
```

**Test:**
```powershell
npx @mcp-apps/enterprise-mcp-server@latest --test
```

**Note:** This is a fallback. Prefer OAP for new implementations.

---

## 5️⃣ Kusto MCP Server (stdio)

### Purpose
Query telemetry databases for diagnostics and analytics

### Setup

**Install:**
```powershell
npm install -g @mcp-apps/kusto-mcp
```

**Environment Variables:**
```powershell
$env:KUSTO_CLUSTER_URL = "https://YOUR_CLUSTER.kusto.windows.net"
$env:KUSTO_DATABASE = "YOUR_DATABASE_NAME"
$env:KUSTO_AUTH_MODE = "AzureCLI"  # or "InteractiveBrowser" or "ManagedIdentity"
```

**Authentication Options:**

**Option 1: Azure CLI (Recommended for local development)**
```powershell
# Login first
az login

# Set auth mode
$env:KUSTO_AUTH_MODE = "AzureCLI"

# Test
npx @mcp-apps/kusto-mcp@latest --test
```

**Option 2: Service Principal (Production)**
```powershell
$env:KUSTO_AUTH_MODE = "ServicePrincipal"
$env:AZURE_CLIENT_ID = "YOUR_SP_CLIENT_ID"
$env:AZURE_CLIENT_SECRET = "YOUR_SP_SECRET"
$env:AZURE_TENANT_ID = "YOUR_TENANT_ID"
```

**Option 3: Managed Identity (Azure resources)**
```powershell
$env:KUSTO_AUTH_MODE = "ManagedIdentity"
```

**Common Kusto Clusters:**
```powershell
# Purview Production Telemetry
$env:KUSTO_CLUSTER_URL = "https://purview.kusto.windows.net"
$env:KUSTO_DATABASE = "PurviewTelemetry"

# Diagnostic Logs
$env:KUSTO_CLUSTER_URL = "https://diagnostics.kusto.windows.net"
$env:KUSTO_DATABASE = "DiagnosticLogs"
```

**Test Connection:**
```powershell
npx @mcp-apps/kusto-mcp@latest --query ".show tables" --cluster $env:KUSTO_CLUSTER_URL --database $env:KUSTO_DATABASE
```

---

## 🔐 Environment Variables Setup (Complete)

### Create a Setup Script

**File:** `setup-mcp-env.ps1`

```powershell
#!/usr/bin/env pwsh
# PHEPy MCP Environment Configuration

Write-Host "🔧 Setting up MCP environment variables..." -ForegroundColor Cyan

# ICM MCP
[System.Environment]::SetEnvironmentVariable('ICM_MCP_API_KEY', 'YOUR_KEY', 'User')
[System.Environment]::SetEnvironmentVariable('ICM_API_ENDPOINT', 'https://icm-mcp-prod.azure-api.net/v1/', 'User')

# Azure DevOps
[System.Environment]::SetEnvironmentVariable('AZURE_DEVOPS_ORG_URL', 'https://dev.azure.com/YOUR_ORG', 'User')
[System.Environment]::SetEnvironmentVariable('AZURE_DEVOPS_PAT', 'YOUR_PAT', 'User')

# OAP
[System.Environment]::SetEnvironmentVariable('OAP_API_KEY', 'YOUR_KEY', 'User')
[System.Environment]::SetEnvironmentVariable('OAP_ENDPOINT', 'https://oap.microsoft.com/api/v1/', 'User')

# Kusto
[System.Environment]::SetEnvironmentVariable('KUSTO_CLUSTER_URL', 'https://YOUR_CLUSTER.kusto.windows.net', 'User')
[System.Environment]::SetEnvironmentVariable('KUSTO_DATABASE', 'YOUR_DATABASE', 'User')
[System.Environment]::SetEnvironmentVariable('KUSTO_AUTH_MODE', 'AzureCLI', 'User')

# Enterprise MCP (optional/legacy)
[System.Environment]::SetEnvironmentVariable('ENTERPRISE_SCIM_TOKEN', 'YOUR_TOKEN', 'User')

Write-Host "✅ Environment variables set!" -ForegroundColor Green
Write-Host "⚠️  Restart your terminal for changes to take effect" -ForegroundColor Yellow
```

**Usage:**
```powershell
# Edit the script with your actual tokens
notepad setup-mcp-env.ps1

# Run it
.\setup-mcp-env.ps1

# Restart terminal
```

---

## 🧪 Testing MCP Servers

### Test All Servers

```powershell
# Test ICM
curl -H "Ocp-Apim-Subscription-Key: $env:ICM_MCP_API_KEY" `
     "$env:ICM_API_ENDPOINT/health"

# Test ADO
npx @azure-devops/mcp o365exchange --test

# Test Kusto
npx @mcp-apps/kusto-mcp@latest --test

# Test OAP
$headers = @{"Authorization" = "Bearer $env:OAP_API_KEY"}
Invoke-RestMethod -Uri "$env:OAP_ENDPOINT/health" -Headers $headers
```

### Create Test Script

**File:** `test-mcp-servers.ps1`

```powershell
#!/usr/bin/env pwsh
# Test all MCP server connections

Write-Host "`n🧪 Testing MCP Server Connections" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# 1. Test ICM
Write-Host "`n1️⃣  Testing ICM MCP..." -ForegroundColor Yellow
if ($env:ICM_MCP_API_KEY) {
    try {
        $result = curl -s -H "Ocp-Apim-Subscription-Key: $env:ICM_MCP_API_KEY" `
                       "$env:ICM_API_ENDPOINT/health"
        Write-Host "✅ ICM MCP: Connected" -ForegroundColor Green
    } catch {
        Write-Host "❌ ICM MCP: Failed - $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  ICM MCP: Key not set" -ForegroundColor Yellow
}

# 2. Test Azure DevOps
Write-Host "`n2️⃣  Testing Azure DevOps MCP..." -ForegroundColor Yellow
if ($env:AZURE_DEVOPS_PAT) {
    try {
        npx @azure-devops/mcp o365exchange --test 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ ADO MCP: Connected" -ForegroundColor Green
        } else {
            Write-Host "❌ ADO MCP: Connection failed" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ ADO MCP: Error - $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  ADO MCP: PAT not set" -ForegroundColor Yellow
}

# 3. Test Kusto
Write-Host "`n3️⃣  Testing Kusto MCP..." -ForegroundColor Yellow
if ($env:KUSTO_CLUSTER_URL) {
    try {
        npx @mcp-apps/kusto-mcp@latest --test 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Kusto MCP: Connected" -ForegroundColor Green
        } else {
            Write-Host "❌ Kusto MCP: Connection failed" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Kusto MCP: Error - $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  Kusto MCP: Cluster URL not set" -ForegroundColor Yellow
}

# 4. Test OAP
Write-Host "`n4️⃣  Testing One Agentic Platform..." -ForegroundColor Yellow
if ($env:OAP_API_KEY) {
    try {
        $headers = @{"Authorization" = "Bearer $env:OAP_API_KEY"}
        Invoke-RestMethod -Uri "$env:OAP_ENDPOINT/health" -Headers $headers | Out-Null
        Write-Host "✅ OAP: Connected" -ForegroundColor Green
    } catch {
        Write-Host "❌ OAP: Failed - $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  OAP: API key not set" -ForegroundColor Yellow
}

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "✅ MCP Server Test Complete" -ForegroundColor Green
```

---

## 🔗 Integrating MCP with Azure AI Agent

### Option 1: Function Calling (Recommended)

Configure your agent to use MCP servers as functions:

```python
# In agent configuration
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_icm",
            "description": "Query ICM for incident data",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_id": {"type": "string"},
                    "operation": {"type": "string", "enum": ["get", "search", "impact"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_ado",
            "description": "Query ADO work items",
            "parameters": {
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer"},
                    "project": {"type": "string", "enum": ["o365exchange", "ASIM-Security"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_kusto_query",
            "description": "Execute KQL query for telemetry",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "database": {"type": "string"}
                }
            }
        }
    }
]
```

### Option 2: MCP Proxy Service

Create a proxy that forwards agent requests to MCP servers:

**Architecture:**
```
Azure AI Agent → Azure Function (Proxy) → MCP Servers
```

**Benefits:**
- Centralized authentication
- Request rate limiting
- Logging and monitoring
- Error handling

---

## 📚 Quick Reference

### Environment Variable Checklist

```powershell
# Check all required variables
Write-Host "ICM_MCP_API_KEY: $($env:ICM_MCP_API_KEY -ne $null)" 
Write-Host "AZURE_DEVOPS_PAT: $($env:AZURE_DEVOPS_PAT -ne $null)"
Write-Host "KUSTO_CLUSTER_URL: $($env:KUSTO_CLUSTER_URL -ne $null)"
Write-Host "OAP_API_KEY: $($env:OAP_API_KEY -ne $null)"
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Authentication failed" | Check token expiration, regenerate if needed |
| "npx command not found" | Install Node.js: `winget install OpenJS.NodeJS` |
| "Module not found" | Run `npm install -g @package/name` |
| "Permission denied" | Check firewall, corporate proxy settings |
| "Rate limit exceeded" | Implement caching, reduce query frequency |

---

## 🎯 Next Steps

1. **Set environment variables** using `setup-mcp-env.ps1`
2. **Test connections** using `test-mcp-servers.ps1`
3. **Configure agent tools** to call MCP servers
4. **Test agent integration** with `test-agent-cli.ps1`
5. **Monitor usage** and optimize queries

---

## 📖 Additional Resources

- **MCP Specification:** https://modelcontextprotocol.io
- **Azure DevOps PAT:** https://docs.microsoft.com/azure/devops/organizations/accounts/use-personal-access-tokens
- **Kusto Query Language:** https://docs.microsoft.com/azure/data-explorer/kusto/query/
- **ICM Documentation:** Internal Microsoft ICM docs
- **OAP Portal:** https://oap.microsoft.com

---

**Need help?** Run `.\test-mcp-servers.ps1` to diagnose connection issues.
