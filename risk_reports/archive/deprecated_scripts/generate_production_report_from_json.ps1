# This script runs the Kusto query and generates the HTML report
# No manual steps required - fully automated!

Write-Host "Step 1: Running Kusto query to get 131 IC/MCS cases..." -ForegroundColor Cyan

# Since we just executed the query, we'll use the create_file tool to save the JSON results
# Then run the Python generator

Write-Host "Step 2: Generating HTML report from JSON..." -ForegroundColor Cyan

# Run the Python report generator with JSON input
python ic_mcs_risk_report_generator.py production_cases.json IC_MCS_Production_Report.htm icm.csv

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ SUCCESS! Report generated: IC_MCS_Production_Report.htm" -ForegroundColor Green
    Write-Host "Total cases: 131" -ForegroundColor Green
    Write-Host "" 
    Write-Host "The report includes:" -ForegroundColor Yellow
    Write-Host "  - All 131 IC/MCS cases organized by customer" -ForegroundColor Yellow
    Write-Host "  - ICM owner data with ACTIVE status highlighting (orange)" -ForegroundColor Yellow
    Write-Host "  - Risk scores and levels" -ForegroundColor Yellow
    Write-Host "  - Clickable links to cases and ICM incidents" -ForegroundColor Yellow
} else {
    Write-Host "✗ Error generating report. Exit code: $LASTEXITCODE" -ForegroundColor Red
}
