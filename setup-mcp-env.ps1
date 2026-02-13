#!/usr/bin/env pwsh
# PHEPy MCP Environment Configuration
# Edit this file with your actual tokens before running

param(
    [switch]$ShowCurrent,
    [switch]$Test
)

if ($ShowCurrent) {
    Write-Host "`n📋 Current MCP Environment Variables:" -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Cyan
    
    Write-Host "`nICM MCP:" -ForegroundColor Yellow
    Write-Host "  ICM_MCP_API_KEY: $(if($env:ICM_MCP_API_KEY) {'✅ Set'} else {'❌ Not set'})"
    Write-Host "  ICM_API_ENDPOINT: $env:ICM_API_ENDPOINT"
    
    Write-Host "`nAzure DevOps:" -ForegroundColor Yellow
    Write-Host "  AZURE_DEVOPS_ORG_URL: $env:AZURE_DEVOPS_ORG_URL"
    Write-Host "  AZURE_DEVOPS_PAT: $(if($env:AZURE_DEVOPS_PAT) {'✅ Set'} else {'❌ Not set'})"
    
    Write-Host "`nKusto:" -ForegroundColor Yellow
    Write-Host "  KUSTO_CLUSTER_URL: $env:KUSTO_CLUSTER_URL"
    Write-Host "  KUSTO_DATABASE: $env:KUSTO_DATABASE"
    Write-Host "  KUSTO_AUTH_MODE: $env:KUSTO_AUTH_MODE"
    
    Write-Host "`nOAP:" -ForegroundColor Yellow
    Write-Host "  OAP_API_KEY: $(if($env:OAP_API_KEY) {'✅ Set'} else {'❌ Not set'})"
    Write-Host "  OAP_ENDPOINT: $env:OAP_ENDPOINT"
    
    Write-Host "`nEnterprise MCP:" -ForegroundColor Yellow
    Write-Host "  ENTERPRISE_SCIM_TOKEN: $(if($env:ENTERPRISE_SCIM_TOKEN) {'✅ Set'} else {'❌ Not set'})"
    
    exit 0
}

Write-Host "`n🔧 PHEPy MCP Environment Setup" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

Write-Host "`n⚠️  WARNING: This will set USER-level environment variables" -ForegroundColor Yellow
Write-Host "   These persist across terminal sessions" -ForegroundColor Gray

$confirm = Read-Host "`nContinue? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "❌ Setup cancelled" -ForegroundColor Red
    exit 1
}

Write-Host "`n📝 Setting environment variables..." -ForegroundColor Cyan

# ICM MCP
Write-Host "`n1️⃣  ICM MCP Configuration" -ForegroundColor Yellow
$icmKey = Read-Host "   Enter ICM MCP API Key (or press Enter to skip)"
if ($icmKey) {
    [System.Environment]::SetEnvironmentVariable('ICM_MCP_API_KEY', $icmKey, 'User')
    [System.Environment]::SetEnvironmentVariable('ICM_API_ENDPOINT', 'https://icm-mcp-prod.azure-api.net/v1/', 'User')
    Write-Host "   ✅ ICM MCP configured" -ForegroundColor Green
} else {
    Write-Host "   ⏭️  Skipped" -ForegroundColor Gray
}

# Azure DevOps
Write-Host "`n2️⃣  Azure DevOps Configuration" -ForegroundColor Yellow
$adoOrg = Read-Host "   Enter ADO Org URL (e.g., https://dev.azure.com/myorg) or press Enter to skip"
if ($adoOrg) {
    [System.Environment]::SetEnvironmentVariable('AZURE_DEVOPS_ORG_URL', $adoOrg, 'User')
    
    $adoPat = Read-Host "   Enter ADO Personal Access Token (PAT)"
    if ($adoPat) {
        [System.Environment]::SetEnvironmentVariable('AZURE_DEVOPS_PAT', $adoPat, 'User')
        Write-Host "   ✅ Azure DevOps configured" -ForegroundColor Green
    }
} else {
    Write-Host "   ⏭️  Skipped" -ForegroundColor Gray
}

# Kusto
Write-Host "`n3️⃣  Kusto Configuration" -ForegroundColor Yellow
$kustoCluster = Read-Host "   Enter Kusto Cluster URL (e.g., https://cluster.kusto.windows.net) or press Enter to skip"
if ($kustoCluster) {
    [System.Environment]::SetEnvironmentVariable('KUSTO_CLUSTER_URL', $kustoCluster, 'User')
    
    $kustoDb = Read-Host "   Enter Kusto Database name"
    [System.Environment]::SetEnvironmentVariable('KUSTO_DATABASE', $kustoDb, 'User')
    
    Write-Host "   Select auth mode:"
    Write-Host "   1. AzureCLI (recommended for dev)"
    Write-Host "   2. InteractiveBrowser"
    Write-Host "   3. ManagedIdentity (for Azure resources)"
    Write-Host "   4. ServicePrincipal"
    $authChoice = Read-Host "   Choice (1-4)"
    
    $authMode = switch ($authChoice) {
        "1" { "AzureCLI" }
        "2" { "InteractiveBrowser" }
        "3" { "ManagedIdentity" }
        "4" { "ServicePrincipal" }
        default { "AzureCLI" }
    }
    
    [System.Environment]::SetEnvironmentVariable('KUSTO_AUTH_MODE', $authMode, 'User')
    
    if ($authMode -eq "ServicePrincipal") {
        $clientId = Read-Host "   Enter Azure Client ID"
        $clientSecret = Read-Host "   Enter Azure Client Secret" -AsSecureString
        $tenantId = Read-Host "   Enter Azure Tenant ID"
        
        [System.Environment]::SetEnvironmentVariable('AZURE_CLIENT_ID', $clientId, 'User')
        [System.Environment]::SetEnvironmentVariable('AZURE_CLIENT_SECRET', [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($clientSecret)), 'User')
        [System.Environment]::SetEnvironmentVariable('AZURE_TENANT_ID', $tenantId, 'User')
    }
    
    Write-Host "   ✅ Kusto configured ($authMode)" -ForegroundColor Green
} else {
    Write-Host "   ⏭️  Skipped" -ForegroundColor Gray
}

# OAP
Write-Host "`n4️⃣  One Agentic Platform (OAP) Configuration" -ForegroundColor Yellow
$oapKey = Read-Host "   Enter OAP API Key (or press Enter to skip)"
if ($oapKey) {
    [System.Environment]::SetEnvironmentVariable('OAP_API_KEY', $oapKey, 'User')
    [System.Environment]::SetEnvironmentVariable('OAP_ENDPOINT', 'https://oap.microsoft.com/api/v1/', 'User')
    Write-Host "   ✅ OAP configured" -ForegroundColor Green
} else {
    Write-Host "   ⏭️  Skipped" -ForegroundColor Gray
}

# Enterprise MCP (optional)
Write-Host "`n5️⃣  Enterprise MCP (Legacy - Optional)" -ForegroundColor Yellow
$enterpriseToken = Read-Host "   Enter Enterprise SCIM Token (or press Enter to skip)"
if ($enterpriseToken) {
    [System.Environment]::SetEnvironmentVariable('ENTERPRISE_SCIM_TOKEN', $enterpriseToken, 'User')
    [System.Environment]::SetEnvironmentVariable('ENTERPRISE_API_ENDPOINT', 'https://enterprise.microsoft.com/api', 'User')
    Write-Host "   ✅ Enterprise MCP configured" -ForegroundColor Green
} else {
    Write-Host "   ⏭️  Skipped" -ForegroundColor Gray
}

# Summary
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "✅ MCP ENVIRONMENT SETUP COMPLETE" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "`n📋 Configuration Summary:" -ForegroundColor Yellow
Write-Host "   ICM MCP: $(if($icmKey) {'✅ Configured'} else {'❌ Not configured'})"
Write-Host "   Azure DevOps: $(if($adoOrg) {'✅ Configured'} else {'❌ Not configured'})"
Write-Host "   Kusto: $(if($kustoCluster) {'✅ Configured'} else {'❌ Not configured'})"
Write-Host "   OAP: $(if($oapKey) {'✅ Configured'} else {'❌ Not configured'})"
Write-Host "   Enterprise MCP: $(if($enterpriseToken) {'✅ Configured'} else {'❌ Not configured'})"

Write-Host "`n⚠️  IMPORTANT: Restart your terminal for changes to take effect!" -ForegroundColor Yellow

Write-Host "`n💡 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Close this terminal" -ForegroundColor White
Write-Host "   2. Open a new terminal" -ForegroundColor White
Write-Host "   3. Run: .\test-mcp-servers.ps1" -ForegroundColor Yellow
Write-Host "   4. Test agent: .\test-agent-cli.ps1" -ForegroundColor Yellow

Write-Host "`n📖 Documentation: MCP_SETUP_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
