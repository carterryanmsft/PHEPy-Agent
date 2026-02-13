#!/usr/bin/env pwsh
# PHEPy Copilot Studio Deployment Guide
# Deploys PHEPy Orchestrator Agent to Microsoft Copilot Studio

param(
    [string]$Environment = "Production",
    [switch]$GenerateManifest,
    [switch]$OpenPortal
)

Write-Host "🤖 PHEPy Copilot Studio Deployment" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Step 1: Prerequisites Check
Write-Host "`n📋 Checking Prerequisites..." -ForegroundColor Yellow

$prerequisites = @(
    @{Name="Power Platform CLI"; Command="pac"; Url="https://aka.ms/PowerPlatformCLI"},
    @{Name="Azure CLI"; Command="az"; Url="https://aka.ms/azure-cli"},
    @{Name="Node.js"; Command="node"; Url="https://nodejs.org"}
)

$allInstalled = $true
foreach ($prereq in $prerequisites) {
    try {
        $null = Get-Command $prereq.Command -ErrorAction Stop
        Write-Host "  ✅ $($prereq.Name)" -ForegroundColor Green
    }
    catch {
        Write-Host "  ❌ $($prereq.Name) not found - Install from: $($prereq.Url)" -ForegroundColor Red
        $allInstalled = $false
    }
}

if (-not $allInstalled) {
    Write-Host "`n⚠️  Please install missing prerequisites and try again" -ForegroundColor Yellow
    exit 1
}

# Step 2: Generate Agent Manifest
Write-Host "`n📝 Generating Copilot Studio Agent Manifest..." -ForegroundColor Yellow

$manifest = @{
    schema = "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.0/schema.json"
    version = "v1.0"
    name = "PHEPy Orchestrator"
    description = "Comprehensive Purview Product Health & Escalation Orchestrator Agent with ICM, ADO, Kusto, and case management capabilities"
    instructions = @"
You are the PHEPy Orchestrator - a specialized support engineering assistant for Microsoft Purview.

# Core Capabilities
- 🎫 **ICM Management**: Query incidents, escalations, customer impact
- 🐛 **ADO Integration**: Bug tracking, feature requests, work item queries
- 📊 **Kusto Analytics**: Telemetry analysis, diagnostic queries
- 💼 **Case Management**: Support case lifecycle and customer context
- 📚 **Knowledge Base**: TSG lookup and troubleshooting guidance

# Available Tools
- ICM MCP Server: Incident and escalation data
- ADO MCP Servers: o365exchange and ASIM-Security work items
- Kusto MCP: Query execution for telemetry
- OAP/Enterprise MCP: Support case management

# Response Style
- Be precise and technical when discussing product issues
- Include incident/bug IDs when referencing work items
- Provide actionable next steps and escalation paths
- Use data-driven insights from Kusto when available

# Escalation Awareness
- Sev 0/1: Immediate attention, customer-impacting outages
- Sev 2: High priority, degraded service
- Track P0/P1 bugs linked to customer cases
"@
    conversation_starters = @(
        @{title="Show critical incidents"; text="What are the current Sev 0/1 ICM incidents?"},
        @{title="Recent P0 bugs"; text="Show me recent P0 bugs from ADO"},
        @{title="Customer case trends"; text="Analyze support case trends for last week"},
        @{title="Query telemetry"; text="Help me write a Kusto query for DLP telemetry"}
    )
    capabilities = @{
        web_search = @{enabled = $false}
        file_upload = @{enabled = $false; max_size_mb = 10; accepted_mime_types = @("text/plain", "application/json", "text/csv")}
    }
    actions = @(
        @{
            id = "icm-mcp"
            name = "ICM Incident Management"
            description = "Query ICM incidents, escalations, and customer impact data"
            file = "actions/icm-action.json"
        },
        @{
            id = "ado-mcp"
            name = "Azure DevOps Integration"
            description = "Search bugs, features, and work items across multiple ADO projects"
            file = "actions/ado-action.json"
        },
        @{
            id = "kusto-mcp"
            name = "Kusto Query Engine"
            description = "Execute Kusto queries for telemetry analysis and diagnostics"
            file = "actions/kusto-action.json"
        },
        @{
            id = "oap-mcp"
            name = "Case Management"
            description = "Support case lifecycle, customer context, and ML-powered insights"
            file = "actions/oap-action.json"
        }
    )
}

# Save manifest
$manifestPath = "copilot-studio-manifest.json"
$manifest | ConvertTo-Json -Depth 10 | Set-Content $manifestPath -Encoding UTF8
Write-Host "  ✅ Manifest saved: $manifestPath" -ForegroundColor Green

# Step 3: Create Action Definitions
Write-Host "`n🔌 Creating Action Definitions..." -ForegroundColor Yellow

$actionsDir = "actions"
if (-not (Test-Path $actionsDir)) {
    New-Item -ItemType Directory -Path $actionsDir | Out-Null
}

# ICM Action
$icmAction = @{
    type = "http"
    name = "ICM MCP"
    description = "ICM incident and escalation management"
    base_url = "https://icm-mcp-prod.azure-api.net/v1/"
    authentication = @{
        type = "microsoft_entra"
        scope = "api://icm-mcp/.default"
    }
    operations = @(
        @{
            operation_id = "get_incident"
            name = "Get Incident Details"
            description = "Retrieve full details for an ICM incident by ID"
            http_method = "GET"
            path = "/incidents/{incidentId}"
        },
        @{
            operation_id = "search_incidents"
            name = "Search Incidents"
            description = "Search ICM incidents with filters"
            http_method = "POST"
            path = "/incidents/search"
        }
    )
}

$icmAction | ConvertTo-Json -Depth 10 | Set-Content "actions/icm-action.json" -Encoding UTF8
Write-Host "  ✅ ICM action created" -ForegroundColor Green

# ADO Action
$adoAction = @{
    type = "http"
    name = "Azure DevOps MCP"
    description = "ADO work items, bugs, and features"
    base_url = "https://dev.azure.com/"
    authentication = @{
        type = "oauth2"
        authorization_url = "https://app.vssps.visualstudio.com/oauth2/authorize"
        token_url = "https://app.vssps.visualstudio.com/oauth2/token"
        scope = "vso.work vso.code vso.build"
    }
}

$adoAction | ConvertTo-Json -Depth 10 | Set-Content "actions/ado-action.json" -Encoding UTF8
Write-Host "  ✅ ADO action created" -ForegroundColor Green

# Step 4: Deployment Instructions
Write-Host "`n📖 Deployment Steps:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

Write-Host "`n1️⃣  Login to Power Platform:" -ForegroundColor Yellow
Write-Host "   pac auth create --environment <your-environment-url>" -ForegroundColor White

Write-Host "`n2️⃣  Navigate to Copilot Studio Portal:" -ForegroundColor Yellow
Write-Host "   https://copilotstudio.microsoft.com" -ForegroundColor Cyan

Write-Host "`n3️⃣  Create New Copilot:" -ForegroundColor Yellow
Write-Host "   • Select 'New Copilot' → 'Declarative Agent'" -ForegroundColor White
Write-Host "   • Upload manifest: $manifestPath" -ForegroundColor White
Write-Host "   • Configure each action with proper authentication" -ForegroundColor White

Write-Host "`n4️⃣  Configure Actions:" -ForegroundColor Yellow
Write-Host "   For each action in the 'actions' folder:" -ForegroundColor White
Write-Host "   • Add as Custom Action/Connector" -ForegroundColor White
Write-Host "   • Set up Microsoft Entra ID authentication" -ForegroundColor White
Write-Host "   • Test connection before publishing" -ForegroundColor White

Write-Host "`n5️⃣  Test Agent:" -ForegroundColor Yellow
Write-Host "   • Use conversation starters to validate" -ForegroundColor White
Write-Host "   • Test each data source connection" -ForegroundColor White
Write-Host "   • Verify response quality" -ForegroundColor White

Write-Host "`n6️⃣  Publish:" -ForegroundColor Yellow
Write-Host "   • Publish to Teams, Web, or other channels" -ForegroundColor White
Write-Host "   • Set up permissions and access controls" -ForegroundColor White

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "📁 Generated Files:" -ForegroundColor Yellow
Write-Host "   • $manifestPath - Main agent manifest" -ForegroundColor White
Write-Host "   • actions/icm-action.json - ICM connector" -ForegroundColor White  
Write-Host "   • actions/ado-action.json - ADO connector" -ForegroundColor White

Write-Host "`n🔗 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Review and customize manifest if needed" -ForegroundColor White
Write-Host "   2. Open Copilot Studio portal (add -OpenPortal flag)" -ForegroundColor White
Write-Host "   3. Follow deployment instructions above" -ForegroundColor White
Write-Host "   4. Configure MCP server endpoints as Custom Actions" -ForegroundColor White

if ($OpenPortal) {
    Write-Host "`n🌐 Opening Copilot Studio Portal..." -ForegroundColor Yellow
    Start-Process "https://copilotstudio.microsoft.com"
}

Write-Host "`n✅ Setup complete! Ready for Copilot Studio deployment" -ForegroundColor Green
