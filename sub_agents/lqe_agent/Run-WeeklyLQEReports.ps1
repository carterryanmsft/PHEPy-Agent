<#
.SYNOPSIS
    Automated Weekly Regional LQE Report Generation

.DESCRIPTION
    Fetches fresh LQE data from Kusto and generates regional reports for:
    - Americas
    - EMEA
    - APAC
    
    This script should be run weekly (recommended: Friday afternoon or Monday morning)
    to ensure stakeholders have visibility into low quality escalations.

.PARAMETER SkipDataFetch
    Use existing data file instead of fetching fresh data from Kusto

.PARAMETER DataFile
    Path to specific data file to use (skips fetch)

.PARAMETER SendEmail
    Send generated reports via email (requires email configuration)

.PARAMETER TestMode
    Run in test mode (generates reports but doesn't send emails)

.EXAMPLE
    .\Run-WeeklyLQEReports.ps1
    Fetches fresh data and generates all regional reports

.EXAMPLE
    .\Run-WeeklyLQEReports.ps1 -SkipDataFetch
    Uses most recent data file without fetching from Kusto

.EXAMPLE
    .\Run-WeeklyLQEReports.ps1 -SendEmail -FromEmail "your.email@microsoft.com"
    Generates reports and sends via email

.NOTES
    Author: Carter Ryan
    Created: February 13, 2026
    
    Prerequisites:
    - Python 3.8+
    - Azure authentication (az login)
    - Kusto access to icmcluster
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$SkipDataFetch,
    
    [Parameter(Mandatory=$false)]
    [string]$DataFile,
    
    [Parameter(Mandatory=$false)]
    [switch]$SendEmail,
    
    [Parameter(Mandatory=$false)]
    [string]$FromEmail,
    
    [Parameter(Mandatory=$false)]
    [switch]$TestMode
)

# Script configuration
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ReportsDir = Join-Path $ScriptDir "reports\regional_reports"

# Banner
Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "WEEKLY REGIONAL LQE REPORT AUTOMATION" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""
Write-Host "📅 Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor White
Write-Host "📂 Location: $ScriptDir" -ForegroundColor White
Write-Host ""

# Check Python
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check Azure authentication
try {
    $azAccount = az account show 2>&1 | ConvertFrom-Json
    Write-Host "✓ Azure authenticated: $($azAccount.user.name)" -ForegroundColor Green
} catch {
    Write-Host "⚠ Azure not authenticated. Run: az login" -ForegroundColor Yellow
    Write-Host "  Attempting interactive authentication during script execution..." -ForegroundColor Yellow
}

Write-Host ""

# Build Python command
$pythonArgs = @("run_weekly_regional_reports.py")

if ($SkipDataFetch) {
    Write-Host "📝 Mode: Using existing data (skip fetch)" -ForegroundColor Cyan
    $pythonArgs += "--skip-fetch"
}
elseif ($DataFile) {
    Write-Host "📝 Mode: Using specified data file" -ForegroundColor Cyan
    Write-Host "   File: $DataFile" -ForegroundColor White
    $pythonArgs += "--use-data"
    $pythonArgs += $DataFile
}
else {
    Write-Host "📝 Mode: Fetching fresh data from Kusto" -ForegroundColor Cyan
}

Write-Host ""

# Execute report generation
Write-Host ("=" * 80) -ForegroundColor Yellow
Write-Host "STEP 1: GENERATE REGIONAL REPORTS" -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor Yellow
Write-Host ""

try {
    Push-Location $ScriptDir
    
    # Run Python script
    $process = Start-Process -FilePath "python" `
        -ArgumentList $pythonArgs `
        -NoNewWindow `
        -Wait `
        -PassThru
    
    if ($process.ExitCode -ne 0) {
        Write-Host ""
        Write-Host "✗ Report generation failed (exit code: $($process.ExitCode))" -ForegroundColor Red
        Pop-Location
        exit $process.ExitCode
    }
    
    Pop-Location
    
    Write-Host ""
    Write-Host "✓ Reports generated successfully!" -ForegroundColor Green
    
} catch {
    Write-Host ""
    Write-Host "✗ Error during report generation:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Pop-Location
    exit 1
}

# Send emails if requested
if ($SendEmail) {
    Write-Host ""
    Write-Host ("=" * 80) -ForegroundColor Yellow
    Write-Host "STEP 2: SEND EMAIL REPORTS" -ForegroundColor Yellow
    Write-Host ("=" * 80) -ForegroundColor Yellow
    Write-Host ""
    
    if (-not $FromEmail) {
        Write-Host "✗ --FromEmail required for sending emails" -ForegroundColor Red
        Write-Host "   Example: -FromEmail 'your.email@microsoft.com'" -ForegroundColor Yellow
        exit 1
    }
    
    try {
        Push-Location $ScriptDir
        
        $emailArgs = @(
            "send_regional_lqe_emails.py",
            "--from-email", $FromEmail
        )
        
        if ($TestMode) {
            Write-Host "🧪 Running in TEST MODE (no emails will be sent)" -ForegroundColor Cyan
            $emailArgs += "--test"
        }
        
        $process = Start-Process -FilePath "python" `
            -ArgumentList $emailArgs `
            -NoNewWindow `
            -Wait `
            -PassThru
        
        Pop-Location
        
        if ($process.ExitCode -ne 0) {
            Write-Host ""
            Write-Host "✗ Email sending failed (exit code: $($process.ExitCode))" -ForegroundColor Red
            exit $process.ExitCode
        }
        
        Write-Host ""
        Write-Host "✓ Emails sent successfully!" -ForegroundColor Green
        
    } catch {
        Write-Host ""
        Write-Host "✗ Error sending emails:" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        Pop-Location
        exit 1
    }
}

# Summary
Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Green
Write-Host "✓✓✓ WEEKLY LQE REPORTS COMPLETE ✓✓✓" -ForegroundColor Green
Write-Host ("=" * 80) -ForegroundColor Green
Write-Host ""
Write-Host "📂 Reports available at:" -ForegroundColor White
Write-Host "   $ReportsDir" -ForegroundColor Cyan
Write-Host ""

# List generated reports
$htmlReports = Get-ChildItem -Path $ReportsDir -Filter "*.htm" -ErrorAction SilentlyContinue | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 3

if ($htmlReports) {
    Write-Host "📊 Latest reports:" -ForegroundColor White
    foreach ($report in $htmlReports) {
        $age = (Get-Date) - $report.LastWriteTime
        $ageStr = if ($age.TotalMinutes -lt 60) {
            "$([math]::Floor($age.TotalMinutes)) minutes ago"
        } else {
            "$([math]::Floor($age.TotalHours)) hours ago"
        }
        Write-Host "   • $($report.Name)" -ForegroundColor White -NoNewline
        Write-Host " ($ageStr)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review HTML reports in: $ReportsDir" -ForegroundColor White
Write-Host "  2. Share with regional stakeholders" -ForegroundColor White
if (-not $SendEmail) {
    Write-Host "  3. (Optional) Run with -SendEmail to distribute via email" -ForegroundColor White
}

Write-Host ""
Write-Host "Schedule this script weekly: PowerShell Task Scheduler or cron" -ForegroundColor Cyan
Write-Host ""
