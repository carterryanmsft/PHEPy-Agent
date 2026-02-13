# PHEPy Foundry Deployment - CLI Guide

**Environment**: CxESharedServicesAI-Prod  
**Date**: February 11, 2026  
**Method**: Azure CLI (Command Line)

---

## 🎯 Prerequisites

### 1. Install Azure CLI
```powershell
# Check if installed
az --version

# If not installed:
winget install Microsoft.AzureCLI

# Or download from:
# https://aka.ms/installazurecliwindows
```

### 2. Install Azure AI Extension
```powershell
# Install the AI/ML extension
az extension add --name ml

# Update to latest version
az extension update --name ml

# Verify installation
az extension list --output table | Select-String "ml"
```

---

## 🚀 Step-by-Step CLI Deployment

### Step 1: Login and Set Subscription
```powershell
# Login to Azure
az login

# List subscriptions
az account list --output table

# Set to CxE Shared Services subscription
az account set --subscription "CxE Shared Services"

# Verify
az account show --query "{Name:name, SubscriptionId:id}" --output table
```

### Step 2: Find the Foundry Workspace
```powershell
# List all AI workspaces
az ml workspace list --output table

# Search for CxESharedServicesAI-Prod
az ml workspace list --query "[?contains(name, 'CxESharedServicesAI')]" --output table

# Get workspace details
az ml workspace show \
  --name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --output json
```

### Step 3: Navigate to Project Directory
```powershell
# Go to PHEPy root
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy"

# Verify you're in the right place
Get-Location
Get-ChildItem -Name | Select-Object -First 10
```

### Step 4: Create Foundry Environment
```powershell
# Create environment for the agent
az ml environment create \
  --name "phepy-orchestrator-env" \
  --version "1.0" \
  --file - <<EOF
$schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
name: phepy-orchestrator-env
version: "1.0"
image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest
conda_file:
  name: phepy-env
  channels:
    - defaults
  dependencies:
    - python=3.11
    - pip:
      - pandas>=2.0.0
      - azure-identity>=1.15.0
      - azure-kusto-data
EOF
```

### Step 5: Create Agent Endpoint
```powershell
# Create online endpoint for the agent
az ml online-endpoint create \
  --name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG"

# Check endpoint status
az ml online-endpoint show \
  --name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --output table
```

### Step 6: Create Deployment Configuration

Create a deployment YAML file:

```powershell
# Create deployment config
@"
\$schema: https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json
name: phepy-v1
endpoint_name: phepy-orchestrator
model:
  path: .
  name: phepy-orchestrator-model
  version: 1
environment:
  name: phepy-orchestrator-env
  version: 1
code_configuration:
  code: .
  scoring_script: agent_entry.py
instance_type: Standard_DS3_v2
instance_count: 1
"@ | Out-File -FilePath "deployment.yml" -Encoding utf8
```

### Step 7: Deploy the Agent
```powershell
# Deploy to the endpoint
az ml online-deployment create \
  --file deployment.yml \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --all-traffic

# Check deployment status
az ml online-deployment show \
  --name "phepy-v1" \
  --endpoint-name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG"
```

### Step 8: Configure Environment Variables
```powershell
# Update deployment with environment variables
az ml online-deployment update \
  --name "phepy-v1" \
  --endpoint-name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --set environment_variables.OAP_TENANT_ID="<YOUR_TENANT_ID>" \
  --set environment_variables.OAP_CLIENT_ID="<YOUR_CLIENT_ID>"
```

### Step 9: Test Deployment
```powershell
# Get endpoint URI
$endpointUri = az ml online-endpoint show \
  --name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --query scoring_uri -o tsv

Write-Host "Endpoint URI: $endpointUri"

# Test with a sample request
$testData = @{
    query = "List all available sub-agents"
} | ConvertTo-Json

# Invoke the endpoint
az ml online-endpoint invoke \
  --name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --request-file test_request.json
```

---

## 🔧 Alternative: Use Azure AI Foundry CLI (Preview)

Azure AI Foundry has its own CLI (in preview):

```powershell
# Install Foundry CLI extension
az extension add --name ai-foundry

# Create Foundry project
az ai-foundry project create \
  --name "PHEPy-Orchestrator" \
  --workspace "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --location "westus2" \
  --description "Multi-agent orchestration for Purview support operations"

# Upload project files
az ai-foundry project upload \
  --name "PHEPy-Orchestrator" \
  --workspace "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --source-path "."

# Deploy as agent
az ai-foundry agent create \
  --name "phepy-orchestrator" \
  --project "PHEPy-Orchestrator" \
  --workspace "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --instructions-file "docs/project/AGENT_INSTRUCTIONS.md" \
  --model "gpt-4" \
  --temperature 0.7
```

---

## 📊 Monitoring Commands

### Check Deployment Status
```powershell
# Get deployment status
az ml online-deployment get-logs \
  --name "phepy-v1" \
  --endpoint-name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --lines 100
```

### Check Metrics
```powershell
# Get endpoint metrics
az monitor metrics list \
  --resource "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/CxESharedServicesAI-Prod-RG/providers/Microsoft.MachineLearningServices/workspaces/CxESharedServicesAI-Prod/onlineEndpoints/phepy-orchestrator" \
  --metric "RequestLatency" \
  --start-time "2026-02-11T00:00:00Z" \
  --end-time "2026-02-11T23:59:59Z" \
  --interval PT1H
```

---

## 🆘 Troubleshooting

### Issue: Workspace Not Found
```powershell
# Search more broadly
az resource list --query "[?contains(name, 'CxE')]" --output table

# Or list all AI workspaces in subscription
az ml workspace list --query "[].{Name:name, Location:location, ResourceGroup:resourceGroup}" --output table
```

### Issue: Access Denied
```powershell
# Check your role assignments
az role assignment list \
  --assignee "carterryan@microsoft.com" \
  --query "[?contains(roleDefinitionName, 'Contributor') || contains(roleDefinitionName, 'Owner')]" \
  --output table

# Request access if needed
Write-Host "Contact: cxe-ai-admins@microsoft.com"
```

### Issue: Extension Not Available
```powershell
# If ai-foundry extension doesn't exist, use portal
Write-Host "Azure AI Foundry CLI is in preview"
Write-Host "Use portal: https://ai.azure.com"
Write-Host "Or use Azure ML CLI: az ml"
```

---

## ⚡ Quick Deployment Script

Save as `deploy-to-foundry.ps1`:

```powershell
#!/usr/bin/env pwsh
# PHEPy Foundry Deployment Script

param(
    [string]$SubscriptionName = "CxE Shared Services",
    [string]$ResourceGroup = "CxESharedServicesAI-Prod-RG",
    [string]$WorkspaceName = "CxESharedServicesAI-Prod",
    [string]$EndpointName = "phepy-orchestrator"
)

Write-Host "🚀 PHEPy Foundry Deployment" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Step 1: Login
Write-Host "`n1️⃣  Logging in to Azure..." -ForegroundColor Yellow
az login
if ($LASTEXITCODE -ne 0) { throw "Login failed" }

# Step 2: Set subscription
Write-Host "`n2️⃣  Setting subscription..." -ForegroundColor Yellow
az account set --subscription $SubscriptionName
if ($LASTEXITCODE -ne 0) { throw "Subscription not found" }

# Step 3: Verify workspace
Write-Host "`n3️⃣  Verifying workspace..." -ForegroundColor Yellow
$workspace = az ml workspace show `
    --name $WorkspaceName `
    --resource-group $ResourceGroup `
    --output json 2>$null
    
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Workspace not found" -ForegroundColor Red
    Write-Host "Available workspaces:" -ForegroundColor Yellow
    az ml workspace list --output table
    exit 1
}

Write-Host "✅ Workspace found: $WorkspaceName" -ForegroundColor Green

# Step 4: Create endpoint
Write-Host "`n4️⃣  Creating endpoint..." -ForegroundColor Yellow
az ml online-endpoint create `
    --name $EndpointName `
    --workspace-name $WorkspaceName `
    --resource-group $ResourceGroup 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Endpoint created: $EndpointName" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Endpoint may already exist" -ForegroundColor Cyan
}

# Step 5: Get endpoint URL
Write-Host "`n5️⃣  Getting endpoint URL..." -ForegroundColor Yellow
$endpointUrl = az ml online-endpoint show `
    --name $EndpointName `
    --workspace-name $WorkspaceName `
    --resource-group $ResourceGroup `
    --query scoring_uri -o tsv

if ($endpointUrl) {
    Write-Host "✅ Endpoint URL: $endpointUrl" -ForegroundColor Green
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Upload project files via portal: https://ai.azure.com" -ForegroundColor White
Write-Host "2. Configure MCP servers in Foundry" -ForegroundColor White
Write-Host "3. Test the agent" -ForegroundColor White
```

Run it:
```powershell
.\deploy-to-foundry.ps1
```

---

## 📚 Additional CLI Commands

### List All Resources
```powershell
# List all ML resources
az ml workspace list --output table
az ml compute list --workspace-name "CxESharedServicesAI-Prod" --resource-group "CxESharedServicesAI-Prod-RG" --output table
az ml online-endpoint list --workspace-name "CxESharedServicesAI-Prod" --resource-group "CxESharedServicesAI-Prod-RG" --output table
```

### Update Deployment
```powershell
# Update existing deployment
az ml online-deployment update \
  --name "phepy-v1" \
  --endpoint-name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --set instance_count=2
```

### Delete Resources
```powershell
# Delete deployment
az ml online-deployment delete \
  --name "phepy-v1" \
  --endpoint-name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --yes

# Delete endpoint
az ml online-endpoint delete \
  --name "phepy-orchestrator" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --yes
```

---

## ⚠️ Important Notes

### Portal vs CLI

**Best Approach**: **Hybrid**
- Use CLI for: Authentication, workspace discovery, endpoint creation
- Use Portal for: File upload, MCP configuration, sub-agent setup, testing

**Why?**
- Foundry's agent orchestration features are better in portal
- CLI is better for automation and CI/CD
- Portal has visual MCP server configuration
- CLI requires manual YAML for complex configs

### Recommended Workflow
1. **CLI**: Login, find workspace, create endpoint
2. **Portal**: Upload files, configure MCP servers, set up sub-agents
3. **CLI**: Monitor, scale, update deployments
4. **Portal**: Test, debug, iterate

---

## 🎯 Next Steps

After CLI setup, continue in portal:
1. Navigate to: https://ai.azure.com
2. Find your endpoint/project
3. Upload PHEPy files
4. Configure MCP servers from mcp.json
5. Test and iterate

---

*Generated: February 11, 2026*
