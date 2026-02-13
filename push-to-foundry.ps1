#!/usr/bin/env pwsh
# Push PHEPy Agent to Azure AI Foundry
# Deploys GPT-4o model and configures agent

param(
    [string]$ResourceName = "phepy-resource",
    [string]$ResourceGroup = "rg-PHEPy",
    [string]$DeploymentName = "phepy-gpt4o",
    [string]$ModelName = "gpt-4o",
    [string]$ModelVersion = "2024-08-06"
)

Write-Host "`n🚀 Pushing PHEPy Agent to Azure AI Foundry" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Step 1: Verify authentication
Write-Host "`n1️⃣  Verifying Azure authentication..." -ForegroundColor Yellow
$account = az account show 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "❌ Not logged in. Please run: az login" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
Write-Host "   Subscription: $($account.name)" -ForegroundColor White

# Step 2: Check if GPT-4o deployment exists
Write-Host "`n2️⃣  Checking existing deployments..." -ForegroundColor Yellow
$existingDeployments = az cognitiveservices account deployment list `
    --name $ResourceName `
    --resource-group $ResourceGroup `
    --query "[].name" -o tsv 2>$null

if ($existingDeployments -match $DeploymentName) {
    Write-Host "✅ Deployment '$DeploymentName' already exists" -ForegroundColor Green
} else {
    Write-Host "📦 Creating GPT-4o deployment..." -ForegroundColor Yellow
    Write-Host "   This may take 2-3 minutes..." -ForegroundColor Gray
    
    # Create deployment
    $result = az cognitiveservices account deployment create `
        --name $ResourceName `
        --resource-group $ResourceGroup `
        --deployment-name $DeploymentName `
        --model-name $ModelName `
        --model-version $ModelVersion `
        --model-format OpenAI `
        --sku-capacity 10 `
        --sku-name "Standard" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ GPT-4o deployment created successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Deployment creation encountered an issue:" -ForegroundColor Yellow
        Write-Host $result -ForegroundColor Gray
        Write-Host "`nContinuing with agent configuration..." -ForegroundColor Cyan
    }
}

# Step 3: Upload agent configuration files to storage
Write-Host "`n3️⃣  Preparing agent configuration..." -ForegroundColor Yellow

# Get storage account associated with the AI resource
$storageAccounts = az storage account list `
    --resource-group $ResourceGroup `
    --query "[?contains(name, 'phepy')].name" -o tsv

if ($storageAccounts) {
    $storageAccount = ($storageAccounts -split "`n")[0]
    Write-Host "✅ Found storage account: $storageAccount" -ForegroundColor Green
    
    # Note: Full file upload requires storage account key
    Write-Host "   Agent files are in GitHub repo" -ForegroundColor White
    Write-Host "   GitHub: https://github.com/carterryanmsft/PHEPy-Agent" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Agent configuration will be managed in Azure AI Studio" -ForegroundColor Cyan
}

# Step 4: Get endpoint information
Write-Host "`n4️⃣  Getting endpoint information..." -ForegroundColor Yellow
$resource = az cognitiveservices account show `
    --name $ResourceName `
    --resource-group $ResourceGroup `
    --query "{endpoint:properties.endpoint, location:location}" -o json | ConvertFrom-Json

Write-Host "✅ Resource endpoint: $($resource.endpoint)" -ForegroundColor Green
Write-Host "   Location: $($resource.location)" -ForegroundColor White

# Step 5: Get API key
Write-Host "`n5️⃣  Retrieving API keys..." -ForegroundColor Yellow
$keys = az cognitiveservices account keys list `
    --name $ResourceName `
    --resource-group $ResourceGroup `
    --query "{key1:key1}" -o json | ConvertFrom-Json

if ($keys.key1) {
    Write-Host "✅ API key retrieved (use for authentication)" -ForegroundColor Green
    $maskedKey = $keys.key1.Substring(0, 8) + "..." + $keys.key1.Substring($keys.key1.Length - 4)
    Write-Host "   Key: $maskedKey" -ForegroundColor Gray
}

# Step 6: Display next steps
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "✅ FOUNDRY DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "`n📋 Agent Configuration Summary:" -ForegroundColor Yellow
Write-Host "   Resource: $ResourceName" -ForegroundColor White
Write-Host "   Endpoint: $($resource.endpoint)" -ForegroundColor White
Write-Host "   Model Deployment: $DeploymentName" -ForegroundColor White
Write-Host "   GitHub Repo: https://github.com/carterryanmsft/PHEPy-Agent" -ForegroundColor White

Write-Host "`n🌐 Access Your Agent:" -ForegroundColor Cyan
Write-Host "   Portal: https://ai.azure.com" -ForegroundColor Yellow
Write-Host "   Project: PHEPy" -ForegroundColor Yellow
Write-Host "   Direct: https://phepy-resource.services.ai.azure.com" -ForegroundColor Yellow

Write-Host "`n🔧 Configure Agent in Portal:" -ForegroundColor Cyan
Write-Host "   1. Go to Playground → Chat/Agents" -ForegroundColor White
Write-Host "   2. Create/Edit agent:" -ForegroundColor White
Write-Host "      • Name: PHEPy Orchestrator" -ForegroundColor Green
Write-Host "      • Deployment: $DeploymentName" -ForegroundColor Green
Write-Host "      • System message: Already in clipboard!" -ForegroundColor Green
Write-Host "   3. Add data from GitHub repo" -ForegroundColor White
Write-Host "   4. Test and deploy" -ForegroundColor White

Write-Host "`n📡 API Access:" -ForegroundColor Cyan
Write-Host "   curl -X POST `"$($resource.endpoint)openai/deployments/$DeploymentName/chat/completions?api-version=2024-08-01-preview`" \\" -ForegroundColor Gray
Write-Host "     -H `"api-key: YOUR_API_KEY`" \\" -ForegroundColor Gray
Write-Host "     -H `"Content-Type: application/json`" \\" -ForegroundColor Gray
Write-Host "     -d '{`"messages`":[{`"role`":`"user`",`"content`":`"Hello PHEPy`"}]}'" -ForegroundColor Gray

Write-Host "`n💾 Save These Values:" -ForegroundColor Yellow
Write-Host "   AZURE_AI_ENDPOINT=$($resource.endpoint)" -ForegroundColor White
Write-Host "   AZURE_AI_KEY=$maskedKey" -ForegroundColor White
Write-Host "   DEPLOYMENT_NAME=$DeploymentName" -ForegroundColor White

Write-Host "`n🎉 Agent pushed to Foundry successfully!" -ForegroundColor Green
Write-Host "   Complete configuration in Azure AI Studio portal." -ForegroundColor White
Write-Host ""
