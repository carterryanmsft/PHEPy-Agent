# PHEPy Foundry Deployment - Quick Commands

**Environment**: CxESharedServicesAI-Prod  
**Date**: February 11, 2026

---

## 🚀 Quick Start Commands

### 1. Login to Azure
```powershell
# Install Azure CLI if needed
winget install Microsoft.AzureCLI

# Login
az login

# Set subscription
az account set --subscription "CxE Shared Services"

# Verify
az account show
```

### 2. Install Azure AI Extension
```powershell
az extension add --name ml
az extension update --name ml
```

### 3. Access Foundry Workspace
```powershell
# List available workspaces
az ml workspace list --resource-group "CxESharedServicesAI-Prod-RG"

# Show workspace details
az ml workspace show \
  --name "CxESharedServicesAI-Prod" \
  --resource-group "CxESharedServicesAI-Prod-RG"
```

### 4. Create Agent Project (If not exists)
```powershell
# Navigate to PHEPy directory
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy"

# Create project
az ml project create \
  --name "PHEPy-Orchestrator" \
  --display-name "Purview Health & Escalation Agent" \
  --description "Multi-agent orchestration for Purview support operations" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --workspace-name "CxESharedServicesAI-Prod"
```

### 5. Upload Project Files
```powershell
# Make sure you're in PHEPy root directory
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy"

# Upload all files (respects .gitignore)
az ml project upload \
  --name "PHEPy-Orchestrator" \
  --path . \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --workspace-name "CxESharedServicesAI-Prod"
```

---

## 🌐 Web Portal Access

### Foundry Portal
```
https://ai.azure.com
```

### Azure Portal
```
https://portal.azure.com
-> Search: "CxESharedServicesAI-Prod"
```

### Direct Workspace Link (after finding workspace ID)
```
https://ai.azure.com/workspaces/{workspace-id}
```

---

## 📦 Pre-Deployment Security Check

### Scan for PII (Run before upload)
```powershell
# Check for common PII patterns in markdown files
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy"

# Search for tenant IDs
Get-ChildItem -Recurse -Include *.md,*.py | Select-String -Pattern "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}" | Select-Object Path, LineNumber, Line

# Search for email addresses
Get-ChildItem -Recurse -Include *.md,*.py | Select-String -Pattern "\w+@\w+\.\w+" | Where-Object { $_.Line -notmatch "example\.com|contoso\.com|microsoft\.com" } | Select-Object Path, LineNumber, Line

# Search for customer names (add your customers)
$customers = @("Ford", "Amazon", "CIBC", "GE", "Santander", "Zurich", "Barclays", "Desjardins")
$customers | ForEach-Object {
    Write-Host "`nSearching for: $_" -ForegroundColor Yellow
    Get-ChildItem -Recurse -Include *.md | Select-String -Pattern $_ | Select-Object Path, LineNumber -First 3
}
```

---

## 🔍 Verify Deployment

### Check Files Uploaded
```powershell
az ml project show \
  --name "PHEPy-Orchestrator" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --workspace-name "CxESharedServicesAI-Prod"
```

### List Project Files
```powershell
az ml project list-files \
  --name "PHEPy-Orchestrator" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --workspace-name "CxESharedServicesAI-Prod"
```

---

## 📊 Monitor Deployment

### View Logs
```powershell
az ml project logs \
  --name "PHEPy-Orchestrator" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --workspace-name "CxESharedServicesAI-Prod"
```

### Check Status
```powershell
az ml project show \
  --name "PHEPy-Orchestrator" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --workspace-name "CxESharedServicesAI-Prod" \
  --query "status"
```

---

## 🧪 Test Agent (After Deployment)

### Via Azure CLI (if supported)
```powershell
az ml agent test \
  --name "PHEPy-Orchestrator" \
  --query "List all available sub-agents" \
  --resource-group "CxESharedServicesAI-Prod-RG" \
  --workspace-name "CxESharedServicesAI-Prod"
```

### Via Portal
```
https://ai.azure.com/agents/phepy-orchestrator/playground
```

---

## 🔐 Environment Variables (Set in Foundry Portal)

**After creating project, add these in Portal:**

1. Navigate to: Agent Settings → Environment Variables
2. Add:

```
OAP_TENANT_ID = [Get from OAP team]
OAP_CLIENT_ID = [Get from OAP team]
OAP_CLIENT_SECRET = [Get from OAP team]
```

---

## 📝 Quick Test Queries

**Copy/paste these into Foundry playground:**

```
Test 1: Basic
"List all available agents"

Test 2: MCP
"How many active ICMs does Purview have?"

Test 3: Support Cases
"Show me at-risk support cases"

Test 4: Grounding Docs
"What is the SLA for P0 cases?"

Test 5: Multi-Agent
"Analyze ICM 693849812 and find related cases"
```

---

## 🆘 Troubleshooting

### Can't Find Workspace
```powershell
# List all subscriptions
az account list --output table

# Search for workspace in all subscriptions
az ml workspace list --output table
```

### Access Denied
```powershell
# Check your role assignments
az role assignment list --assignee "carterryan@microsoft.com" --output table

# Request access
# Contact: cxe-ai-admins@microsoft.com
```

### Upload Failed
```powershell
# Check file size
Get-ChildItem -Recurse | Measure-Object -Property Length -Sum | Select-Object @{Name="Size(MB)";Expression={[math]::Round($_.Sum/1MB,2)}}

# If too large (>100MB), check for large files
Get-ChildItem -Recurse | Where-Object {$_.Length -gt 10MB} | Select-Object FullName, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}}
```

---

## 📞 Quick Contacts

| Issue | Contact |
|-------|---------|
| Foundry Access | cxe-ai-admins@microsoft.com |
| MCP Servers | Your team |
| OAP Credentials | oap-support@microsoft.com |
| Azure Support | azureai-support@microsoft.com |

---

## ✅ Deployment Checklist

```powershell
# Quick checklist commands

# 1. Login
az login
Write-Host "✅ Logged in" -ForegroundColor Green

# 2. Set subscription
az account set --subscription "CxE Shared Services"
Write-Host "✅ Subscription set" -ForegroundColor Green

# 3. Verify workspace access
az ml workspace show --name "CxESharedServicesAI-Prod" --resource-group "CxESharedServicesAI-Prod-RG" > $null
if ($?) { Write-Host "✅ Workspace accessible" -ForegroundColor Green } else { Write-Host "❌ Workspace not found" -ForegroundColor Red }

# 4. Check PHEPy directory
cd "c:\Users\carterryan\OneDrive - Microsoft\PHEPy"
Write-Host "✅ In PHEPy directory" -ForegroundColor Green

# 5. Check file count
$fileCount = (Get-ChildItem -File).Count
Write-Host "✅ Root files: $fileCount (target: ~16)" -ForegroundColor Green

# 6. Ready to deploy
Write-Host "`n🚀 Ready to deploy to Foundry!" -ForegroundColor Cyan
```

---

## 🎯 Next Step

**Use the Portal (Easiest):**
1. Go to: https://ai.azure.com
2. Find workspace: CxESharedServicesAI-Prod
3. Create new agent
4. Upload PHEPy folder (drag & drop)
5. Configure MCP servers from mcp.json
6. Test & publish

**OR use CLI (shown above)**

---

*Generated: February 11, 2026*
