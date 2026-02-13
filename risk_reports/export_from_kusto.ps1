# Azure Data Explorer - Kusto Query Export Script
# This script helps export IC/MCS risk report data from Kusto

Write-Host "=" * 70
Write-Host "IC/MCS RISK REPORT - KUSTO QUERY EXPORT GUIDE"
Write-Host "=" * 70
Write-Host ""

Write-Host "STEP 1: Open Azure Data Explorer"
Write-Host "  Opening browser now..."
Write-Host ""

Start-Process "https://dataexplorer.azure.com/"

Start-Sleep -Seconds 2

Write-Host "STEP 2: Connect to Cluster"
Write-Host "  Cluster: cxedataplatformcluster.westus2.kusto.windows.net"
Write-Host "  Database: cxedata"
Write-Host ""

Write-Host "STEP 3: Load Query"
Write-Host "  File location: queries\ic_mcs_risk_report.kql"
Write-Host ""

$queryFile = Join-Path $PSScriptRoot "queries\ic_mcs_risk_report.kql"
if (Test-Path $queryFile) {
    Write-Host "  Query file found: $queryFile"
    Write-Host "  Opening query file..."
    Start-Process notepad $queryFile
} else {
    Write-Host "  ERROR: Query file not found at $queryFile"
}

Write-Host ""
Write-Host "STEP 4: Execute Query in Azure Data Explorer"
Write-Host "  1. Copy the query from the opened file"
Write-Host "  2. Paste into Azure Data Explorer"
Write-Host "  3. Click 'Run' or press Shift+Enter"
Write-Host "  4. Wait for query to complete (should return ~118 rows)"
Write-Host ""

Write-Host "STEP 5: Export Results to CSV"
Write-Host "  1. After query completes, click 'Export' button"
Write-Host "  2. Select 'Export to CSV'"
Write-Host "  3. Save file as: production_full_cases.csv"
Write-Host "  4. Move file to: .\data\production_full_cases.csv"
Write-Host ""

Write-Host "STEP 6: Generate Updated Report"
Write-Host "  Run: python ic_mcs_risk_report_generator.py data\production_full_cases.csv IC_MCS_UPDATED data\icm.csv"
Write-Host ""

Write-Host "=" * 70
Write-Host "EXPECTED RESULTS:"
Write-Host "  - Query should return ~118 IC/MCS cases"
Write-Host "  - CSV will have 31 columns"
Write-Host "  - Top risks: Huntington, State of WA, Ford, Vodafone, BHP"
Write-Host "=" * 70
Write-Host ""

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
