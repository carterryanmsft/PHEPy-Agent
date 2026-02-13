# Convert Kusto query JSON results to CSV
$jsonFile = "query_results.json"
$outputCsv = "production_cases.csv"

Write-Host "Converting JSON results to CSV..." -ForegroundColor Cyan

# Read the saved query results
if (Test-Path $jsonFile) {
    $data = Get-Content $jsonFile -Raw | ConvertFrom-Json
    $data.data | Export-Csv -Path $outputCsv -NoTypeInformation -Encoding UTF8
    Write-Host "✓ Created $outputCsv with $($data.data.Count) cases" -ForegroundColor Green
} else {
    Write-Host "Error: $jsonFile not found" -ForegroundColor Red
    Write-Host "Please save the query results as JSON first" -ForegroundColor Yellow
}
