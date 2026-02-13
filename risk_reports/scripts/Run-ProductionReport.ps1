# IC/MCS Production Risk Report - One-Command Generation
# Executes the full workflow: Query → Process → Report

param(
    [switch]$UseTestData = $false
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -NoNewline -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan
Write-Host "  IC/MCS PRODUCTION RISK REPORT GENERATOR" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -NoNewline -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

# Check if we have query results already
$jsonFile = "production_cases_131.json"
$testFile = "test_output_cases.csv"

if (-not (Test-Path $jsonFile) -and -not $UseTestData) {
    Write-Host "⚠️  No saved production query results found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You have two options:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Option 1: Generate with test data (9 cases)" -ForegroundColor White
    Write-Host "    Run: .\generate_production_report.ps1 -UseTestData" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Option 2: Execute query and save results first" -ForegroundColor White
    Write-Host "    1. Execute the Kusto query via MCP tool" -ForegroundColor Gray
    Write-Host "    2. Save results to: $jsonFile" -ForegroundColor Gray
    Write-Host "    3. Run this script again" -ForegroundColor Gray
    Write-Host ""
    Write-Host "For demonstration, I'll use test data..." -ForegroundColor Yellow
    Write-Host ""
    $UseTestData = $true
    Start-Sleep -Seconds 2
}

# Run the Python automation script
Write-Host "🚀 Starting report generation..." -ForegroundColor Green
Write-Host ""

try {
    python generate_production_report.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ REPORT GENERATION COMPLETE!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📄 Report saved to: IC_MCS_Production_Report.htm" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "💡 Next steps:" -ForegroundColor Yellow
        Write-Host "   • Open IC_MCS_Production_Report.htm in your browser" -ForegroundColor White
        Write-Host "   • Review high-risk cases (Critical/High risk levels)" -ForegroundColor White
        Write-Host "   • Check ICM status for ACTIVE escalations" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "❌ Report generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error: $_" -ForegroundColor Red
    exit 1
}
