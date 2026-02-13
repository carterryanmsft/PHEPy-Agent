#!/usr/bin/env pwsh
# PHEPy Copilot Studio CLI Deployment
# Uses Azure CLI and Microsoft Graph API to deploy declarative copilot

param(
    [string]$TenantId = "",
    [switch]$DownloadPACTool,
    [switch]$UseGraphAPI
)

Write-Host "🤖 PHEPy Copilot Studio - CLI Deployment" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Check if manifest exists
if (-not (Test-Path "copilot-studio-manifest.json")) {
    Write-Host "❌ Manifest not found. Run: .\deploy-to-copilot-studio.ps1 first" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found manifest file" -ForegroundColor Green

# Option 1: Download Power Platform CLI
if ($DownloadPACTool) {
    Write-Host "`n📥 Downloading Power Platform CLI..." -ForegroundColor Yellow
    
    $installerUrl = "https://aka.ms/PowerAppsCLI"
    $installerPath = "$env:TEMP\powerapps-cli.msi"
    
    Write-Host "  Downloading from: $installerUrl" -ForegroundColor White
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
    
    Write-Host "  Installing..." -ForegroundColor White
    Start-Process msiexec.exe -Wait -ArgumentList "/i `"$installerPath`" /quiet /qn"
    
    Write-Host "✅ Power Platform CLI installed" -ForegroundColor Green
    Write-Host "  Restart your terminal and run: pac auth create" -ForegroundColor Yellow
    exit 0
}

# Option 2: Use Graph API
if ($UseGraphAPI) {
    Write-Host "`n🔑 Logging in to Azure..." -ForegroundColor Yellow
    
    # Login to Azure CLI
    $account = az account show 2>$null | ConvertFrom-Json
    if (-not $account) {
        Write-Host "  Not logged in. Logging in..." -ForegroundColor White
        az login --allow-no-subscriptions
    } else {
        Write-Host "  ✅ Logged in as: $($account.user.name)" -ForegroundColor Green
    }
    
    # Get access token for Microsoft Graph
    Write-Host "`n🔐 Getting access token..." -ForegroundColor Yellow
    $token = az account get-access-token --resource https://graph.microsoft.com --query accessToken -o tsv
    
    if (-not $token) {
        Write-Host "❌ Failed to get access token" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Access token obtained" -ForegroundColor Green
    
    # Read manifest
    $manifest = Get-Content "copilot-studio-manifest.json" -Raw | ConvertFrom-Json
    
    # Prepare copilot configuration
    Write-Host "`n📝 Preparing copilot configuration..." -ForegroundColor Yellow
    
    $copilotConfig = @{
        displayName = $manifest.name
        description = $manifest.description
        instructions = $manifest.instructions
        conversationStarters = $manifest.conversation_starters | ForEach-Object {
            @{
                title = $_.title
                text = $_.text
            }
        }
    }
    
    $body = $copilotConfig | ConvertTo-Json -Depth 10
    
    # Note: Copilot Studio API might require specific endpoints
    Write-Host "`n⚠️  Direct Graph API for Copilot Studio is limited" -ForegroundColor Yellow
    Write-Host "    Alternative: Use Dataverse API or Portal upload" -ForegroundColor White
    
    Write-Host "`n📋 Your configuration is ready:" -ForegroundColor Cyan
    Write-Host $body -ForegroundColor White
    
    Write-Host "`n📖 Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Go to: https://copilotstudio.microsoft.com" -ForegroundColor White
    Write-Host "  2. Create New Copilot → From description" -ForegroundColor White
    Write-Host "  3. Use the configuration above" -ForegroundColor White
    
    # Save for reference
    $copilotConfig | ConvertTo-Json -Depth 10 | Set-Content "copilot-config-processed.json"
    Write-Host "`n✅ Configuration saved to: copilot-config-processed.json" -ForegroundColor Green
    
    exit 0
}

# Option 3: Step-by-step CLI instructions
Write-Host "`n📋 CLI Deployment Options:" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Cyan

Write-Host "`n1️⃣  Install Power Platform CLI (Recommended):" -ForegroundColor Yellow
Write-Host "   Run: .\deploy-copilot-cli.ps1 -DownloadPACTool" -ForegroundColor White
Write-Host "   Then:" -ForegroundColor White
Write-Host "     pac auth create" -ForegroundColor Cyan
Write-Host "     pac copilot create --manifest copilot-studio-manifest.json" -ForegroundColor Cyan

Write-Host "`n2️⃣  Use Graph API Preparation:" -ForegroundColor Yellow
Write-Host "   Run: .\deploy-copilot-cli.ps1 -UseGraphAPI" -ForegroundColor White
Write-Host "   This prepares your config for API submission" -ForegroundColor White

Write-Host "`n3️⃣  Direct Teams CLI (If available):" -ForegroundColor Yellow
Write-Host "   Teams Toolkit CLI commands:" -ForegroundColor White
Write-Host "     teamsfx new --interactive false --app-name PHEPy" -ForegroundColor Cyan
Write-Host "     teamsfx deploy" -ForegroundColor Cyan

Write-Host "`n4️⃣  Portal with CLI prep (Fastest):" -ForegroundColor Yellow
Write-Host "   a. Manifest ready: copilot-studio-manifest.json ✅" -ForegroundColor Green
Write-Host "   b. Open portal: " -ForegroundColor White -NoNewline
Write-Host "https://copilotstudio.microsoft.com" -ForegroundColor Cyan
Write-Host "   c. Create → Upload manifest" -ForegroundColor White

Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan
Write-Host "💡 Recommendation: Option 4 (Portal + manifest file)" -ForegroundColor Green
Write-Host "   Fastest path: 2 minutes to working copilot" -ForegroundColor White

Write-Host "`n🎯 Quick Command:" -ForegroundColor Cyan
Write-Host "   Start-Process 'https://copilotstudio.microsoft.com'" -ForegroundColor White
Write-Host "   # Then drag-and-drop: copilot-studio-manifest.json" -ForegroundColor White

Write-Host "`n❓ Which option do you prefer?" -ForegroundColor Yellow
Write-Host "   1 = Download PAC CLI (5 min)" -ForegroundColor White
Write-Host "   2 = Use Graph API (tech preview)" -ForegroundColor White
Write-Host "   4 = Open portal now (recommended)" -ForegroundColor Green

$choice = Read-Host "`nEnter choice (1/2/4)"

switch ($choice) {
    "1" {
        Write-Host "`n🚀 Downloading Power Platform CLI..." -ForegroundColor Cyan
        & $PSCommandPath -DownloadPACTool
    }
    "2" {
        Write-Host "`n🚀 Preparing Graph API deployment..." -ForegroundColor Cyan
        & $PSCommandPath -UseGraphAPI
    }
    "4" {
        Write-Host "`n🚀 Opening Copilot Studio portal..." -ForegroundColor Cyan
        Start-Process "https://copilotstudio.microsoft.com"
        Write-Host "`n📁 Upload this file: copilot-studio-manifest.json" -ForegroundColor Yellow
        Write-Host "✅ Ready to deploy!" -ForegroundColor Green
    }
    default {
        Write-Host "`n💡 No problem! Run anytime:" -ForegroundColor Yellow
        Write-Host "   .\deploy-copilot-cli.ps1" -ForegroundColor Cyan
    }
}
