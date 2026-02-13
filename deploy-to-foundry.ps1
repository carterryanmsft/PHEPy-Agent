#!/usr/bin/env pwsh
# PHEPy Foundry Deployment Script
# Quick CLI deployment to CxESharedServicesAI-Prod

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
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Login failed" -ForegroundColor Red
    exit 1 
}

# Step 2: Set subscription
Write-Host "`n2️⃣  Setting subscription..." -ForegroundColor Yellow
az account set --subscription $SubscriptionName
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Subscription not found. Available subscriptions:" -ForegroundColor Red
    az account list --query "[].{Name:name, SubscriptionId:id}" --output table
    exit 1
}

$currentSub = az account show --query "{Name:name, SubscriptionId:id}" --output json | ConvertFrom-Json
Write-Host "✅ Using subscription: $($currentSub.Name)" -ForegroundColor Green

# Step 3: Verify workspace exists
Write-Host "`n3️⃣  Searching for workspace..." -ForegroundColor Yellow

# Try to find workspace (may not have ml extension)
$found = $false
try {
    az ml workspace show `
        --name $WorkspaceName `
        --resource-group $ResourceGroup `
        --output json 2>$null | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        $found = $true
        Write-Host "✅ Workspace found: $WorkspaceName" -ForegroundColor Green
    }
}
catch {
    Write-Host "ℹ️  ML extension not available" -ForegroundColor Yellow
}

if (-not $found) {
    Write-Host "`n🔍 Searching for AI Foundry workspaces..." -ForegroundColor Yellow
    Write-Host "Checking resource group: $ResourceGroup" -ForegroundColor White
    
    # Search using generic resource commands
    $resources = az resource list --resource-group $ResourceGroup --query "[?contains(type, 'MachineLearningServices') || contains(type, 'AIServices')].{Name:name, Type:type, Location:location}" --output json 2>$null | ConvertFrom-Json
    
    if ($resources) {
        Write-Host "`n⚠️  Found these AI resources:" -ForegroundColor Cyan
        $resources | Format-Table -AutoSize
    }
    else {
        Write-Host "⚠️  No workspace found via CLI" -ForegroundColor Yellow
        Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
        Write-Host "1. Verify resource group name: $ResourceGroup" -ForegroundColor White
        Write-Host "2. Check workspace name: $WorkspaceName" -ForegroundColor White
        Write-Host "3. You may need to use the Azure Portal:" -ForegroundColor White
        Write-Host "   → https://ai.azure.com" -ForegroundColor Cyan
        Write-Host "4. Or check available resource groups:" -ForegroundColor White
        az group list --query "[?contains(name, 'CxE') || contains(name, 'AI')].{Name:name, Location:location}" --output table
    }
}

# Step 4: Provide portal link
Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "📌 RECOMMENDED APPROACH:" -ForegroundColor Yellow
Write-Host "`nFor Foundry agent deployment, use the portal:" -ForegroundColor White
Write-Host "1. Navigate to: https://ai.azure.com" -ForegroundColor Cyan
Write-Host "2. Find workspace: $WorkspaceName" -ForegroundColor White
Write-Host "3. Create new Agent project" -ForegroundColor White
Write-Host "4. Upload PHEPy folder (drag & drop)" -ForegroundColor White
Write-Host "5. Configure MCP servers from mcp.json" -ForegroundColor White

Write-Host "`n📚 Documentation:" -ForegroundColor Yellow
Write-Host "→ FOUNDRY_DEPLOYMENT_GUIDE.md (full guide)" -ForegroundColor White
Write-Host "→ FOUNDRY_CLI_DEPLOYMENT.md (CLI reference)" -ForegroundColor White
Write-Host "→ FOUNDRY_QUICK_START.md (5-minute quick start)" -ForegroundColor White

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
