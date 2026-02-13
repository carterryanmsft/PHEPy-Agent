#!/usr/bin/env pwsh
# Create PHEPy Agent via Azure CLI
# Uses Azure REST API to create agent in Azure AI Studio

param(
    [string]$ResourceName = "phepy-resource",
    [string]$ResourceGroup = "rg-PHEPy",
    [string]$AgentName = "PHEPy-Orchestrator",
    [string]$DeploymentName = "phepy-gpt4o"
)

Write-Host "`n🤖 Creating PHEPy Agent via CLI" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Step 1: Get resource details
Write-Host "`n1️⃣  Getting resource information..." -ForegroundColor Yellow
$resource = az cognitiveservices account show `
    --name $ResourceName `
    --resource-group $ResourceGroup `
    --query "{endpoint:properties.endpoint, id:id, location:location}" -o json | ConvertFrom-Json

Write-Host "✅ Resource endpoint: $($resource.endpoint)" -ForegroundColor Green

# Step 2: Get API key
Write-Host "`n2️⃣  Retrieving API key..." -ForegroundColor Yellow
$keys = az cognitiveservices account keys list `
    --name $ResourceName `
    --resource-group $ResourceGroup `
    --query "{key1:key1}" -o json | ConvertFrom-Json

Write-Host "✅ API key retrieved" -ForegroundColor Green

# Step 3: Read system instructions
Write-Host "`n3️⃣  Loading system instructions..." -ForegroundColor Yellow
$systemInstructionsPath = Join-Path $PSScriptRoot "system-instructions.txt"
if (Test-Path $systemInstructionsPath) {
    $systemInstructions = Get-Content $systemInstructionsPath -Raw
    Write-Host "✅ System instructions loaded ($($systemInstructions.Length) characters)" -ForegroundColor Green
} else {
    Write-Host "❌ system-instructions.txt not found!" -ForegroundColor Red
    exit 1
}

# Step 4: Create agent configuration
Write-Host "`n4️⃣  Creating agent via Azure OpenAI API..." -ForegroundColor Yellow

# Prepare the agent creation payload
$agentPayload = @{
    model = $DeploymentName
    name = $AgentName
    description = "Comprehensive Purview Product Health & Escalation Orchestrator Agent"
    instructions = $systemInstructions
    tools = @()
    metadata = @{
        created_by = "CLI"
        project = "PHEPy"
        github_repo = "https://github.com/carterryanmsft/PHEPy-Agent"
    }
} | ConvertTo-Json -Depth 10

# Save payload for inspection
$agentPayload | Out-File "agent-creation-payload.json" -Encoding UTF8

Write-Host "   Payload saved to: agent-creation-payload.json" -ForegroundColor Gray
Write-Host "   Sending request to Azure OpenAI..." -ForegroundColor White

# Create agent using Azure OpenAI Assistants API
$endpoint = $resource.endpoint
$apiKey = $keys.key1
$apiVersion = "2024-05-01-preview"

$headers = @{
    "api-key" = $apiKey
    "Content-Type" = "application/json"
}

try {
    # Note: Using Invoke-RestMethod for the API call
    $uri = "${endpoint}openai/assistants?api-version=$apiVersion"
    
    Write-Host "   URI: $uri" -ForegroundColor Gray
    
    $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $agentPayload
    
    Write-Host "✅ Agent created successfully!" -ForegroundColor Green
    Write-Host "   Agent ID: $($response.id)" -ForegroundColor White
    Write-Host "   Name: $($response.name)" -ForegroundColor White
    Write-Host "   Model: $($response.model)" -ForegroundColor White
    
    # Save response
    $response | ConvertTo-Json -Depth 10 | Out-File "agent-creation-response.json" -Encoding UTF8
    Write-Host "   Full response saved to: agent-creation-response.json" -ForegroundColor Gray
    
} catch {
    Write-Host "⚠️  Direct API creation failed. Trying alternative method..." -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
    
    # Alternative: Create via az rest command
    Write-Host "`n5️⃣  Trying Azure REST API method..." -ForegroundColor Yellow
    
    $result = az rest `
        --method POST `
        --url "${endpoint}openai/assistants?api-version=$apiVersion" `
        --headers "api-key=$apiKey" "Content-Type=application/json" `
        --body "@agent-creation-payload.json" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Agent created via REST API!" -ForegroundColor Green
        $result | ConvertFrom-Json | ConvertTo-Json -Depth 10 | Out-File "agent-creation-response.json"
        
        $agentInfo = $result | ConvertFrom-Json
        Write-Host "   Agent ID: $($agentInfo.id)" -ForegroundColor White
        Write-Host "   Name: $($agentInfo.name)" -ForegroundColor White
    } else {
        Write-Host "❌ Failed to create agent" -ForegroundColor Red
        Write-Host "   Error output:" -ForegroundColor Gray
        Write-Host $result -ForegroundColor Gray
        
        Write-Host "`n💡 Manual creation required:" -ForegroundColor Yellow
        Write-Host "   The system instructions and deployment are ready." -ForegroundColor White
        Write-Host "   Please create the agent in Azure AI Studio portal." -ForegroundColor White
        Write-Host "   Portal: https://ai.azure.com" -ForegroundColor Cyan
        exit 1
    }
}

# Step 5: List all agents to verify
Write-Host "`n5️⃣  Verifying agent creation..." -ForegroundColor Yellow
try {
    $listUri = "${endpoint}openai/assistants?api-version=$apiVersion"
    $agents = Invoke-RestMethod -Uri $listUri -Method Get -Headers $headers
    
    Write-Host "✅ Current agents:" -ForegroundColor Green
    foreach ($agent in $agents.data) {
        Write-Host "   • $($agent.name) (ID: $($agent.id))" -ForegroundColor White
    }
} catch {
    Write-Host "⚠️  Could not list agents: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "✅ AGENT CREATION COMPLETE" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "`n📋 Agent Details:" -ForegroundColor Yellow
Write-Host "   Name: $AgentName" -ForegroundColor White
Write-Host "   Deployment: $DeploymentName" -ForegroundColor White
Write-Host "   Endpoint: $($resource.endpoint)" -ForegroundColor White

Write-Host "`n🧪 Test Your Agent:" -ForegroundColor Cyan
Write-Host "   Portal: https://ai.azure.com" -ForegroundColor Yellow
Write-Host "   Project: https://phepy-resource.services.ai.azure.com/api/projects/phepy" -ForegroundColor Yellow

Write-Host "`n💡 Test Prompt:" -ForegroundColor Cyan
Write-Host '   "What capabilities does PHEPy have?"' -ForegroundColor White

Write-Host "`n🎉 Agent is ready to use!" -ForegroundColor Green
Write-Host ""
