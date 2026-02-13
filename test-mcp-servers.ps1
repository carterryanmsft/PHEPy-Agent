#!/usr/bin/env pwsh
# Test all MCP server connections
# Validates that environment variables are set and servers are accessible

Write-Host "`n🧪 Testing MCP Server Connections" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

$successCount = 0
$failCount = 0
$skipCount = 0

# Helper function to test HTTP endpoint
function Test-HttpEndpoint {
    param(
        [string]$Name,
        [string]$Url,
        [hashtable]$Headers
    )
    
    try {
        $response = Invoke-WebRequest -Uri $Url -Headers $Headers -Method Get -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $Name`: Connected (Status: $($response.StatusCode))" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️  $Name`: Unexpected status $($response.StatusCode)" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "❌ $Name`: Failed - $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# 1. Test ICM MCP
Write-Host "`n1️⃣  Testing ICM MCP Server" -ForegroundColor Yellow
Write-Host "   Endpoint: $env:ICM_API_ENDPOINT" -ForegroundColor Gray

if ($env:ICM_MCP_API_KEY) {
    $headers = @{
        "Ocp-Apim-Subscription-Key" = $env:ICM_MCP_API_KEY
    }
    
    # Try health endpoint first, fallback to incidents endpoint
    $testUrl = if ($env:ICM_API_ENDPOINT.EndsWith('/')) {
        "$($env:ICM_API_ENDPOINT)health"
    } else {
        "$env:ICM_API_ENDPOINT/health"
    }
    
    if (Test-HttpEndpoint -Name "ICM MCP" -Url $testUrl -Headers $headers) {
        $successCount++
    } else {
        # Try incidents endpoint as fallback
        Write-Host "   Trying incidents endpoint..." -ForegroundColor Gray
        $testUrl = "$env:ICM_API_ENDPOINT/incidents?`$top=1"
        if (Test-HttpEndpoint -Name "ICM MCP (fallback)" -Url $testUrl -Headers $headers) {
            $successCount++
        } else {
            $failCount++
        }
    }
} else {
    Write-Host "⏭️  ICM MCP: API key not configured (ICM_MCP_API_KEY)" -ForegroundColor Gray
    $skipCount++
}

# 2. Test Azure DevOps - o365exchange
Write-Host "`n2️⃣  Testing Azure DevOps MCP - o365exchange" -ForegroundColor Yellow
Write-Host "   Org: $env:AZURE_DEVOPS_ORG_URL" -ForegroundColor Gray

if ($env:AZURE_DEVOPS_PAT -and $env:AZURE_DEVOPS_ORG_URL) {
    try {
        # Check if az devops extension is installed
        $null = az devops --version 2>&1
        
        # Test connection with a simple query
        $result = az devops project list --org $env:AZURE_DEVOPS_ORG_URL 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Azure DevOps MCP: Connected" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "❌ Azure DevOps MCP: Failed - $result" -ForegroundColor Red
            $failCount++
        }
    } catch {
        Write-Host "⚠️  Azure DevOps MCP: az devops CLI not available" -ForegroundColor Yellow
        Write-Host "   Install: az extension add --name azure-devops" -ForegroundColor Gray
        $failCount++
    }
} else {
    Write-Host "⏭️  Azure DevOps: Not configured (AZURE_DEVOPS_PAT or AZURE_DEVOPS_ORG_URL missing)" -ForegroundColor Gray
    $skipCount++
}

# 3. Test Kusto MCP
Write-Host "`n3️⃣  Testing Kusto MCP Server" -ForegroundColor Yellow
Write-Host "   Cluster: $env:KUSTO_CLUSTER_URL" -ForegroundColor Gray
Write-Host "   Database: $env:KUSTO_DATABASE" -ForegroundColor Gray
Write-Host "   Auth Mode: $env:KUSTO_AUTH_MODE" -ForegroundColor Gray

if ($env:KUSTO_CLUSTER_URL -and $env:KUSTO_DATABASE) {
    # Check if we're using Azure CLI auth
    if ($env:KUSTO_AUTH_MODE -eq "AzureCLI") {
        # Verify az CLI is logged in
        $account = az account show 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "⚠️  Kusto MCP: Azure CLI not logged in" -ForegroundColor Yellow
            Write-Host "   Run: az login" -ForegroundColor Gray
            $failCount++
        } else {
            Write-Host "✅ Kusto MCP: Azure CLI authenticated" -ForegroundColor Green
            Write-Host "   Note: Full test requires query execution" -ForegroundColor Gray
            $successCount++
        }
    } elseif ($env:KUSTO_AUTH_MODE -eq "ServicePrincipal") {
        if ($env:AZURE_CLIENT_ID -and $env:AZURE_CLIENT_SECRET -and $env:AZURE_TENANT_ID) {
            Write-Host "✅ Kusto MCP: Service Principal configured" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "❌ Kusto MCP: Service Principal credentials incomplete" -ForegroundColor Red
            $failCount++
        }
    } else {
        Write-Host "✅ Kusto MCP: Configured with $env:KUSTO_AUTH_MODE auth" -ForegroundColor Green
        $successCount++
    }
} else {
    Write-Host "⏭️  Kusto: Not configured (KUSTO_CLUSTER_URL or KUSTO_DATABASE missing)" -ForegroundColor Gray
    $skipCount++
}

# 4. Test OAP
Write-Host "`n4️⃣  Testing One Agentic Platform (OAP)" -ForegroundColor Yellow
Write-Host "   Endpoint: $env:OAP_ENDPOINT" -ForegroundColor Gray

if ($env:OAP_API_KEY) {
    $headers = @{
        "Authorization" = "Bearer $env:OAP_API_KEY"
        "Content-Type" = "application/json"
    }
    
    $testUrl = if ($env:OAP_ENDPOINT) {
        "$($env:OAP_ENDPOINT)health"
    } else {
        "https://oap.microsoft.com/api/v1/health"
    }
    
    if (Test-HttpEndpoint -Name "OAP" -Url $testUrl -Headers $headers) {
        $successCount++
    } else {
        $failCount++
    }
} else {
    Write-Host "⏭️  OAP: API key not configured (OAP_API_KEY)" -ForegroundColor Gray
    $skipCount++
}

# 5. Test Enterprise MCP (optional)
Write-Host "`n5️⃣  Testing Enterprise MCP (Legacy)" -ForegroundColor Yellow
if ($env:ENTERPRISE_SCIM_TOKEN) {
    Write-Host "✅ Enterprise MCP: Token configured" -ForegroundColor Green
    Write-Host "   Note: This is a fallback server, prefer OAP" -ForegroundColor Gray
    $successCount++
} else {
    Write-Host "⏭️  Enterprise MCP: Not configured (optional)" -ForegroundColor Gray
    $skipCount++
}

# 6. Test Node.js availability (for stdio servers)
Write-Host "`n6️⃣  Testing Node.js (required for stdio MCP servers)" -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Node.js: Installed ($nodeVersion)" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "❌ Node.js: Not found" -ForegroundColor Red
        Write-Host "   Install: winget install OpenJS.NodeJS" -ForegroundColor Gray
        $failCount++
    }
} catch {
    Write-Host "❌ Node.js: Not available" -ForegroundColor Red
    Write-Host "   Install: winget install OpenJS.NodeJS" -ForegroundColor Gray
    $failCount++
}

# Summary
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "📊 TEST SUMMARY" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan

$total = $successCount + $failCount + $skipCount
Write-Host "   ✅ Passed: $successCount" -ForegroundColor Green
Write-Host "   ❌ Failed: $failCount" -ForegroundColor Red
Write-Host "   ⏭️  Skipped: $skipCount" -ForegroundColor Gray
Write-Host "   📊 Total: $total tests"

if ($failCount -eq 0 -and $successCount -gt 0) {
    Write-Host "`n🎉 All configured MCP servers are working!" -ForegroundColor Green
} elseif ($failCount -gt 0) {
    Write-Host "`n⚠️  Some MCP servers have issues. Check configuration above." -ForegroundColor Yellow
}

if ($skipCount -gt 0) {
    Write-Host "`n💡 To configure skipped servers:" -ForegroundColor Cyan
    Write-Host "   Run: .\setup-mcp-env.ps1" -ForegroundColor Yellow
}

Write-Host "`n📖 Documentation: MCP_SETUP_GUIDE.md" -ForegroundColor Cyan

Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
if ($successCount -gt 0) {
    Write-Host "   ✅ Test your agent: .\test-agent-cli.ps1" -ForegroundColor Green
}
if ($failCount -gt 0) {
    Write-Host "   🔧 Fix failed servers: Check environment variables" -ForegroundColor Red
    Write-Host "   📋 Show current config: .\setup-mcp-env.ps1 -ShowCurrent" -ForegroundColor Yellow
}

Write-Host ""

# Exit code based on results
if ($failCount -gt 0) {
    exit 1
} else {
    exit 0
}
