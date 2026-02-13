#!/usr/bin/env pwsh
# Complete CLI Setup for PHEPy Foundry Project
# No portal required - everything via Azure CLI and REST API

param(
    [switch]$Setup,
    [switch]$UploadFiles,
    [switch]$ConfigureDeployment,
    [switch]$Test,
    [switch]$All
)

$ErrorActionPreference = "Continue"

# Configuration
$subscriptionId = "82b24542-e1a0-441c-845a-f5677d342450"
$resourceGroup = "rg-PHEPy"
$accountName = "phepy-resource"
$deploymentName = "phepy-gpt4o"
$location = "eastus2"

Write-Host "🚀 PHEPy Foundry CLI Setup" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# ============================================================================
# STEP 1: Setup and Authentication
# ============================================================================
function Setup-Environment {
    Write-Host "`n1️⃣  Setting up environment..." -ForegroundColor Yellow
    
    # Set subscription
    az account set --subscription $subscriptionId
    
    # Get API keys
    Write-Host "   Getting API keys..." -ForegroundColor White
    $script:apiKey = az cognitiveservices account keys list `
        --name $accountName `
        --resource-group $resourceGroup `
        --query "key1" -o tsv
    
    # Get endpoint
    $script:endpoint = az cognitiveservices account show `
        --name $accountName `
        --resource-group $resourceGroup `
        --query "properties.endpoint" -o tsv
    
    if ($script:apiKey -and $script:endpoint) {
        Write-Host "   ✅ API Key retrieved" -ForegroundColor Green
        Write-Host "   ✅ Endpoint: $script:endpoint" -ForegroundColor Green
        return $true
    } else {
        Write-Host "   ❌ Failed to get credentials" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# STEP 2: Create Azure AI Search for Knowledge Base
# ============================================================================
function Create-SearchService {
    Write-Host "`n2️⃣  Setting up Azure AI Search for knowledge base..." -ForegroundColor Yellow
    
    $searchName = "phepy-search"
    
    # Check if exists
    $existing = az search service show `
        --name $searchName `
        --resource-group $resourceGroup `
        2>$null
    
    if ($existing) {
        Write-Host "   ✅ Search service exists: $searchName" -ForegroundColor Green
        return $searchName
    }
    
    Write-Host "   Creating search service... (this takes 2-3 minutes)" -ForegroundColor White
    az search service create `
        --name $searchName `
        --resource-group $resourceGroup `
        --location $location `
        --sku basic `
        --partition-count 1 `
        --replica-count 1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Search service created: $searchName" -ForegroundColor Green
        return $searchName
    } else {
        Write-Host "   ⚠️  Search service creation failed (optional)" -ForegroundColor Yellow
        return $null
    }
}

# ============================================================================
# STEP 3: Upload Knowledge Base Files to Blob Storage
# ============================================================================
function Upload-KnowledgeBase {
    Write-Host "`n3️⃣  Uploading knowledge base files..." -ForegroundColor Yellow
    
    $storageName = "phepystorage" + (Get-Random -Minimum 1000 -Maximum 9999)
    
    # Create storage account
    Write-Host "   Creating storage account: $storageName" -ForegroundColor White
    az storage account create `
        --name $storageName `
        --resource-group $resourceGroup `
        --location $location `
        --sku Standard_LRS `
        --kind StorageV2
    
    # Get connection string
    $connString = az storage account show-connection-string `
        --name $storageName `
        --resource-group $resourceGroup `
        --query "connectionString" -o tsv
    
    # Create container
    Write-Host "   Creating blob container..." -ForegroundColor White
    az storage container create `
        --name "knowledge-base" `
        --connection-string $connString `
        --public-access blob
    
    # Upload key files
    $filesToUpload = @(
        "agent_routing_map.json",
        "foundry_agent_config.json",
        "mcp.json",
        "CAPABILITY_MATRIX.md",
        "ADVANCED_CAPABILITIES.md",
        "QUICK_REFERENCE.md"
    )
    
    Write-Host "   Uploading files..." -ForegroundColor White
    foreach ($file in $filesToUpload) {
        if (Test-Path $file) {
            az storage blob upload `
                --container-name "knowledge-base" `
                --file $file `
                --name $file `
                --connection-string $connString `
                --overwrite | Out-Null
            Write-Host "     ✅ $file" -ForegroundColor Green
        }
    }
    
    # Upload sub-agent instructions
    Write-Host "   Uploading sub-agent instructions..." -ForegroundColor White
    Get-ChildItem "sub_agents/*/AGENT_INSTRUCTIONS.md" | ForEach-Object {
        $blobName = "sub_agents/$($_.Directory.Name)/$($_.Name)"
        az storage blob upload `
            --container-name "knowledge-base" `
            --file $_.FullName `
            --name $blobName `
            --connection-string $connString `
            --overwrite | Out-Null
        Write-Host "     ✅ $blobName" -ForegroundColor Green
    }
    
    Write-Host "   ✅ Knowledge base uploaded" -ForegroundColor Green
    return $storageName
}

# ============================================================================
# STEP 4: Configure Deployment with System Instructions
# ============================================================================
function Configure-Deployment {
    Write-Host "`n4️⃣  Configuring deployment with system instructions..." -ForegroundColor Yellow
    
    # Read system prompt
    $systemPrompt = Get-Content "foundry_system_prompt.txt" -Raw
    
    # Build OpenAI endpoint
    $openaiEndpoint = $script:endpoint -replace 'cognitiveservices', 'openai'
    $chatEndpoint = "$openaiEndpoint/openai/deployments/$deploymentName/chat/completions?api-version=2024-08-01-preview"
    
    Write-Host "   Testing deployment with system prompt..." -ForegroundColor White
    
    # Create test payload
    $testPayload = @{
        messages = @(
            @{
                role = "system"
                content = $systemPrompt
            }
            @{
                role = "user"
                content = "List all available sub-agents in bullet points"
            }
        )
        max_tokens = 800
        temperature = 0.3
    } | ConvertTo-Json -Depth 10
    
    # Test the deployment
    $headers = @{
        "api-key" = $script:apiKey
        "Content-Type" = "application/json"
    }
    
    try {
        $response = Invoke-RestMethod -Uri $chatEndpoint -Method Post -Headers $headers -Body $testPayload
        Write-Host "   ✅ Deployment configured and tested!" -ForegroundColor Green
        Write-Host "`n   Response:" -ForegroundColor Cyan
        Write-Host "   $($response.choices[0].message.content)" -ForegroundColor White
        return $true
    } catch {
        Write-Host "   ❌ Test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# STEP 5: Create Wrapper Script for Easy Usage
# ============================================================================
function Create-WrapperScript {
    Write-Host "`n5️⃣  Creating usage wrapper script..." -ForegroundColor Yellow
    
    $wrapperContent = @"
#!/usr/bin/env pwsh
# PHEPy Foundry Query Script - Easy CLI Usage

param(
    [Parameter(Mandatory=`$true)]
    [string]`$Query,
    [int]`$MaxTokens = 1000
)

# Get API key from Azure CLI (no hardcoded secrets!)
`$apiKey = az cognitiveservices account keys list ``
    --name "$accountName" ``
    --resource-group "$resourceGroup" ``
    --query "key1" -o tsv 2>`$null

if (-not `$apiKey) {
    Write-Host "❌ Failed to get API key. Run: az login" -ForegroundColor Red
    exit 1
}

`$endpoint = "$($script:endpoint)" -replace 'cognitiveservices', 'openai'
`$deploymentName = "$deploymentName"
`$systemPrompt = Get-Content "foundry_system_prompt.txt" -Raw

`$chatEndpoint = "`$endpoint/openai/deployments/`$deploymentName/chat/completions?api-version=2024-08-01-preview"

`$payload = @{
    messages = @(
        @{ role = "system"; content = `$systemPrompt }
        @{ role = "user"; content = `$Query }
    )
    max_tokens = `$MaxTokens
    temperature = 0.3
} | ConvertTo-Json -Depth 10

`$headers = @{
    "api-key" = `$apiKey
    "Content-Type" = "application/json"
}

try {
    `$response = Invoke-RestMethod -Uri `$chatEndpoint -Method Post -Headers `$headers -Body `$payload
    Write-Host "`$(`$response.choices[0].message.content)"
} catch {
    Write-Host "Error: `$(`$_.Exception.Message)" -ForegroundColor Red
}
"@
    
    $wrapperContent | Out-File -FilePath "query-phepy.ps1" -Encoding utf8
    Write-Host "   ✅ Created: query-phepy.ps1" -ForegroundColor Green
}

# ============================================================================
# STEP 6: Test Everything
# ============================================================================
function Test-Deployment {
    Write-Host "`n6️⃣  Running test queries..." -ForegroundColor Yellow
    
    $testQueries = @(
        "List all available sub-agents",
        "What can the ICM agent do?",
        "How do I query Kusto for telemetry?"
    )
    
    foreach ($query in $testQueries) {
        Write-Host "`n   Query: $query" -ForegroundColor Cyan
        .\query-phepy.ps1 -Query $query -MaxTokens 500
        Start-Sleep -Seconds 2
    }
}

# ============================================================================
# Main Execution
# ============================================================================

if ($All -or $Setup) {
    if (Setup-Environment) {
        Write-Host "✅ Environment setup complete" -ForegroundColor Green
    } else {
        Write-Host "❌ Environment setup failed" -ForegroundColor Red
        exit 1
    }
}

if ($All -or $UploadFiles) {
    Setup-Environment | Out-Null
    $storageName = Upload-KnowledgeBase
    Write-Host "✅ Knowledge base uploaded to: $storageName" -ForegroundColor Green
}

if ($All -or $ConfigureDeployment) {
    Setup-Environment | Out-Null
    if (Configure-Deployment) {
        Create-WrapperScript
        Write-Host "✅ Deployment configured" -ForegroundColor Green
    }
}

if ($All -or $Test) {
    if (Test-Path "query-phepy.ps1") {
        Test-Deployment
    } else {
        Write-Host "❌ Run with -ConfigureDeployment first to create query script" -ForegroundColor Red
    }
}

if (-not ($All -or $Setup -or $UploadFiles -or $ConfigureDeployment -or $Test)) {
    Write-Host "`n📋 Usage:" -ForegroundColor Yellow
    Write-Host "  .\setup-foundry-cli.ps1 -All              # Complete setup" -ForegroundColor White
    Write-Host "  .\setup-foundry-cli.ps1 -Setup            # Just authentication" -ForegroundColor White
    Write-Host "  .\setup-foundry-cli.ps1 -UploadFiles      # Upload knowledge base" -ForegroundColor White
    Write-Host "  .\setup-foundry-cli.ps1 -ConfigureDeployment  # Configure & test" -ForegroundColor White
    Write-Host "  .\setup-foundry-cli.ps1 -Test             # Run test queries" -ForegroundColor White
}

Write-Host "`n" "=" * 70 -ForegroundColor Cyan
Write-Host "🎯 Quick Usage After Setup:" -ForegroundColor Green
Write-Host "  .\query-phepy.ps1 -Query 'Show me Sev2 ICMs from last week'" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
