#!/usr/bin/env pwsh
# PHEPy Azure AI Studio Deployment Script
# Deploys to existing phepy-resource workspace

param(
    [string]$WorkspaceName = "phepy-resource",
    [string]$ResourceGroup = "rg-PHEPy",
    [string]$ProjectName = "PHEPy",
    [string]$Location = "eastus2"
)

Write-Host "`n🚀 PHEPy Azure AI Studio Deployment" -ForegroundColor Cyan
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

# Step 2: Verify workspace exists
Write-Host "`n2️⃣  Verifying workspace: $WorkspaceName" -ForegroundColor Yellow
$workspace = az ml workspace show --name $WorkspaceName --resource-group $ResourceGroup 2>$null | ConvertFrom-Json
if (-not $workspace) {
    Write-Host "❌ Workspace '$WorkspaceName' not found in resource group '$ResourceGroup'" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Found workspace: $WorkspaceName" -ForegroundColor Green
Write-Host "   Location: $($workspace.location)" -ForegroundColor White

# Step 3: Open project in Azure AI Studio
Write-Host "`n3️⃣  Opening Azure AI Studio project..." -ForegroundColor Yellow
$projectUrl = "https://phepy-resource.services.ai.azure.com/api/projects/PHEPy"
Write-Host "   Project URL: $projectUrl" -ForegroundColor White
Start-Process "https://ai.azure.com"
Start-Sleep -Seconds 2

# Step 4: Check GitHub repo status
Write-Host "`n4️⃣  Checking GitHub repository..." -ForegroundColor Yellow
$gitRemote = git remote get-url origin 2>$null
if ($gitRemote) {
    Write-Host "✅ GitHub repo: $gitRemote" -ForegroundColor Green
} else {
    Write-Host "⚠️  No Git remote configured" -ForegroundColor Yellow
}

# Step 5: Get latest from GitHub
Write-Host "`n5️⃣  Ensuring latest code is pushed to GitHub..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "   Found uncommitted changes:" -ForegroundColor Yellow
    git status --short
    
    $response = Read-Host "`n   Commit and push changes? (Y/n)"
    if ($response -ne 'n' -and $response -ne 'N') {
        Write-Host "   Committing changes..." -ForegroundColor White
        git add .
        $commitMsg = "Deployment update: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        git commit -m $commitMsg
        git push origin master
        Write-Host "✅ Changes pushed to GitHub" -ForegroundColor Green
    }
} else {
    Write-Host "✅ Repository is up to date" -ForegroundColor Green
}

# Step 6: Display deployment instructions
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "📋 COMPLETE DEPLOYMENT IN AZURE AI STUDIO" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "`n🌐 Azure AI Studio should now be open in your browser." -ForegroundColor Cyan
Write-Host "   If not, navigate to: https://ai.azure.com" -ForegroundColor White

Write-Host "`n📍 Navigate to Your Project:" -ForegroundColor Yellow
Write-Host "   1. In Azure AI Studio, find workspace: `"$WorkspaceName`"" -ForegroundColor White
Write-Host "   2. Click on project: `"$ProjectName`"" -ForegroundColor White

Write-Host "`n🔗 Connect GitHub Repository (if not already connected):" -ForegroundColor Yellow
Write-Host "   1. Go to: Settings → Source control" -ForegroundColor White
Write-Host "   2. Click 'Connect repository'" -ForegroundColor White
Write-Host "   3. Select GitHub and authorize" -ForegroundColor White
Write-Host "   4. Repository: carterryanmsft/PHEPy-Agent" -ForegroundColor Green
Write-Host "   5. Branch: master" -ForegroundColor White

Write-Host "`n🤖 Create/Update Agent:" -ForegroundColor Yellow
Write-Host "   1. Go to: Playground → Agents (or Chat)" -ForegroundColor White
Write-Host "   2. Click '+ New agent' or select existing agent" -ForegroundColor White
Write-Host "   3. Configure:" -ForegroundColor White
Write-Host "      • Name: PHEPy Orchestrator" -ForegroundColor Green
Write-Host "      • Model: GPT-4o or GPT-4" -ForegroundColor Green
Write-Host "      • Temperature: 0.3" -ForegroundColor Green

Write-Host "`n📝 Update System Instructions:" -ForegroundColor Yellow
Write-Host "   1. Click 'Edit system message' in Playground" -ForegroundColor White
Write-Host "   2. Copy content from: " -ForegroundColor White
$systemInstructionsPath = Join-Path $PSScriptRoot "system-instructions.txt"
if (Test-Path $systemInstructionsPath) {
    Write-Host "      $systemInstructionsPath" -ForegroundColor Green
    Write-Host "`n   Quick copy: " -ForegroundColor Cyan
    Write-Host "      Get-Content `"$systemInstructionsPath`" | clip" -ForegroundColor Yellow
} else {
    Write-Host "      ⚠️  system-instructions.txt not found" -ForegroundColor Yellow
}

Write-Host "`n📚 Add Knowledge Base:" -ForegroundColor Yellow
Write-Host "   1. In Playground, click '+ Add your data'" -ForegroundColor White
Write-Host "   2. Select 'GitHub' as source" -ForegroundColor White
Write-Host "   3. Add these files from your repo:" -ForegroundColor White
@(
    "GETTING_STARTED.md",
    "CAPABILITY_MATRIX.md",
    "ADVANCED_CAPABILITIES.md",
    "QUICK_REFERENCE.md",
    "INDEX.md"
) | ForEach-Object {
    Write-Host "      • $_" -ForegroundColor Green
}

Write-Host "`n🧪 Test the Agent:" -ForegroundColor Yellow
Write-Host "   In the Playground chat, try:" -ForegroundColor White
Write-Host '      "What capabilities does PHEPy have?"' -ForegroundColor Cyan
Write-Host '      "List all available MCP agents"' -ForegroundColor Cyan
Write-Host '      "Show me example prompts for incident investigation"' -ForegroundColor Cyan

Write-Host "`n🚀 Deploy:" -ForegroundColor Yellow
Write-Host "   1. Click 'Deploy' button in Playground" -ForegroundColor White
Write-Host "   2. Choose deployment target:" -ForegroundColor White
Write-Host "      • Web app (for testing)" -ForegroundColor White
Write-Host "      • API endpoint (for programmatic access)" -ForegroundColor White
Write-Host "      • Microsoft Teams (for org access)" -ForegroundColor White

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "✅ DEPLOYMENT SCRIPT COMPLETE" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "`n📖 Additional Resources:" -ForegroundColor Cyan
Write-Host "   • FOUNDRY_QUICK_REFERENCE.md - Quick commands" -ForegroundColor White
Write-Host "   • FOUNDRY_DEPLOYMENT_COMPLETE_GUIDE.md - Full guide" -ForegroundColor White
Write-Host "   • GitHub: $gitRemote" -ForegroundColor White

Write-Host "`n🎉 Ready to complete deployment in Azure AI Studio!" -ForegroundColor Green
Write-Host ""
