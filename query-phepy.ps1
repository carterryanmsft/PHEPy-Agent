#!/usr/bin/env pwsh
# PHEPy Foundry Query Script - Easy CLI Usage

param(
    [Parameter(Mandatory=$true)]
    [string]$Query,
    [int]$MaxTokens = 1000
)

# Get API key from Azure CLI (no hardcoded secrets!)
$apiKey = az cognitiveservices account keys list `
    --name "phepy-resource" `
    --resource-group "rg-PHEPy" `
    --query "key1" -o tsv 2>$null

if (-not $apiKey) {
    Write-Host "❌ Failed to get API key. Run: az login" -ForegroundColor Red
    exit 1
}

$endpoint = "https://phepy-resource.cognitiveservices.azure.com/" -replace 'cognitiveservices', 'openai'
$deploymentName = "phepy-gpt4o"
$systemPrompt = Get-Content "foundry_system_prompt.txt" -Raw

$chatEndpoint = "$endpoint/openai/deployments/$deploymentName/chat/completions?api-version=2024-08-01-preview"

$payload = @{
    messages = @(
        @{ role = "system"; content = $systemPrompt }
        @{ role = "user"; content = $Query }
    )
    max_tokens = $MaxTokens
    temperature = 0.3
} | ConvertTo-Json -Depth 10

$headers = @{
    "api-key" = $apiKey
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri $chatEndpoint -Method Post -Headers $headers -Body $payload
    Write-Host "$($response.choices[0].message.content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
