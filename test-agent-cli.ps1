#!/usr/bin/env pwsh
# Test PHEPy Agent via CLI

param(
    [string]$ResourceName = "phepy-resource",
    [string]$ResourceGroup = "rg-PHEPy",
    [string]$AgentId = "asst_Oybm3OHCwVHWSk3bUb9oF9le",
    [string]$Message = "What capabilities does PHEPy have?"
)

Write-Host "`n🧪 Testing PHEPy Agent" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Get resource details
$resource = az cognitiveservices account show `
    --name $ResourceName `
    --resource-group $ResourceGroup `
    --query "{endpoint:properties.endpoint}" -o json | ConvertFrom-Json

$keys = az cognitiveservices account keys list `
    --name $ResourceName `
    --resource-group $ResourceGroup `
    --query "{key1:key1}" -o json | ConvertFrom-Json

$endpoint = $resource.endpoint
$apiKey = $keys.key1
$apiVersion = "2024-05-01-preview"

Write-Host "`n1️⃣  Creating thread..." -ForegroundColor Yellow
$headers = @{
    "api-key" = $apiKey
    "Content-Type" = "application/json"
}

# Create thread
$threadUri = "${endpoint}openai/threads?api-version=$apiVersion"
$thread = Invoke-RestMethod -Uri $threadUri -Method Post -Headers $headers -Body "{}"
Write-Host "✅ Thread created: $($thread.id)" -ForegroundColor Green

# Add message to thread
Write-Host "`n2️⃣  Sending message..." -ForegroundColor Yellow
Write-Host "   User: $Message" -ForegroundColor White

$messagePayload = @{
    role = "user"
    content = $Message
} | ConvertTo-Json

$messageUri = "${endpoint}openai/threads/$($thread.id)/messages?api-version=$apiVersion"
$message = Invoke-RestMethod -Uri $messageUri -Method Post -Headers $headers -Body $messagePayload
Write-Host "✅ Message sent" -ForegroundColor Green

# Run the assistant
Write-Host "`n3️⃣  Running agent..." -ForegroundColor Yellow
$runPayload = @{
    assistant_id = $AgentId
} | ConvertTo-Json

$runUri = "${endpoint}openai/threads/$($thread.id)/runs?api-version=$apiVersion"
$run = Invoke-RestMethod -Uri $runUri -Method Post -Headers $headers -Body $runPayload
Write-Host "✅ Run started: $($run.id)" -ForegroundColor Green

# Poll for completion
Write-Host "`n4️⃣  Waiting for response..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$runStatus = $run

do {
    Start-Sleep -Seconds 1
    $attempt++
    
    $statusUri = "${endpoint}openai/threads/$($thread.id)/runs/$($run.id)?api-version=$apiVersion"
    $runStatus = Invoke-RestMethod -Uri $statusUri -Method Get -Headers $headers
    
    Write-Host "   Status: $($runStatus.status) ($attempt/$maxAttempts)" -ForegroundColor Gray
    
    if ($runStatus.status -in @("completed", "failed", "cancelled", "expired")) {
        break
    }
} while ($attempt -lt $maxAttempts)

if ($runStatus.status -eq "completed") {
    Write-Host "✅ Agent completed successfully!" -ForegroundColor Green
    
    # Get messages
    Write-Host "`n5️⃣  Retrieving response..." -ForegroundColor Yellow
    $messagesUri = "${endpoint}openai/threads/$($thread.id)/messages?api-version=$apiVersion"
    $messages = Invoke-RestMethod -Uri $messagesUri -Method Get -Headers $headers
    
    # Display response
    Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
    Write-Host "🤖 AGENT RESPONSE" -ForegroundColor Green
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host ""
    
    foreach ($msg in $messages.data) {
        if ($msg.role -eq "assistant") {
            foreach ($content in $msg.content) {
                if ($content.type -eq "text") {
                    Write-Host $content.text.value -ForegroundColor White
                }
            }
            break
        }
    }
    
    Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
    
} else {
    Write-Host "❌ Agent run failed with status: $($runStatus.status)" -ForegroundColor Red
    if ($runStatus.last_error) {
        Write-Host "   Error: $($runStatus.last_error.message)" -ForegroundColor Gray
    }
}

Write-Host "`n✅ Test complete!" -ForegroundColor Green
Write-Host ""
