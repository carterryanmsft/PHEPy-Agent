# ========================================
# PHEPy Foundry Preparation Script
# ========================================
# Automates cleanup and organization for Foundry deployment
# Date: February 11, 2026

param(
    [switch]$DryRun,
    [switch]$SkipBackup
)

$ErrorActionPreference = "Continue"
$workspaceRoot = "c:\Users\carterryan\OneDrive - Microsoft\PHEPy"

# Colors for output
function Write-Success { param($msg) Write-Host "✅ $msg" -ForegroundColor Green }
function Write-Info { param($msg) Write-Host "ℹ️  $msg" -ForegroundColor Cyan }
function Write-Warning { param($msg) Write-Host "⚠️  $msg" -ForegroundColor Yellow }
function Write-Error { param($msg) Write-Host "❌ $msg" -ForegroundColor Red }

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "PHEPy Foundry Preparation Script" -ForegroundColor Magenta
Write-Host "========================================`n" -ForegroundColor Magenta

if ($DryRun) {
    Write-Warning "DRY RUN MODE - No files will be moved"
}

Set-Location $workspaceRoot

# ========================================
# Step 1: Create Backup
# ========================================
if (-not $SkipBackup -and -not $DryRun) {
    Write-Info "Creating backup..."
    $backupDate = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = "c:\Users\carterryan\OneDrive - Microsoft\PHEPy_BACKUP_$backupDate"
    
    try {
        Copy-Item $workspaceRoot -Destination $backupPath -Recurse -Force
        Write-Success "Backup created: $backupPath"
    } catch {
        Write-Error "Backup failed: $_"
        exit 1
    }
} elseif ($SkipBackup) {
    Write-Warning "Skipping backup (use at your own risk!)"
}

# ========================================
# Step 2: Create Archive Structure
# ========================================
Write-Info "Creating archive structure..."

$archiveFolders = @(
    "archive/one_off_analyses/bug_icm_analysis",
    "archive/one_off_analyses/validation",
    "archive/one_off_analyses/data_checking",
    "archive/one_off_analyses/mapping",
    "archive/customer_specific_reports",
    "archive/utilities",
    "archive/analysis_reports",
    "docs/project/workspace",
    "docs/reference"
)

foreach ($folder in $archiveFolders) {
    if ($DryRun) {
        Write-Info "Would create: $folder"
    } else {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Success "Created: $folder"
    }
}

# ========================================
# Step 3: Move Root Scripts to Archive
# ========================================
Write-Info "`nMoving root scripts to archive..."

$moveOperations = @{
    "archive/one_off_analyses/bug_icm_analysis" = @(
        "analyze_bug_linkage.py",
        "analyze_by_design_icms.py",
        "analyze_by_design_real_icms.py",
        "analyze_by_design_report.py",
        "analyze_icm_owners.py",
        "analyze_ic_mcs_bugs_from_icm.py",
        "analyze_ic_mcs_tenants_bugs.py",
        "analyze_ic_risk_report.py",
        "comprehensive_icm_bug_analysis.py",
        "parse_icm_bug_mentions.py",
        "extract_bugs_for_fetch.py",
        "extract_icm_from_ado_bugs.py",
        "extract_icm_ids_for_ado.py",
        "fetch_icm_hyperlinks.py",
        "process_ado_search_results.py",
        "process_ic_filtered.py"
    )
    "archive/one_off_analyses/validation" = @(
        "validate_90day_threshold.py",
        "validate_bug_summary.py",
        "validate_critical_table.py",
        "validate_final_report.py",
        "validate_unassigned_flag.py",
        "final_validation.py"
    )
    "archive/one_off_analyses/data_checking" = @(
        "check_active_unassigned.py",
        "check_bug_data.py",
        "check_icm_data.py",
        "check_scim_cases.py",
        "filter_scim_cases.py"
    )
    "archive/customer_specific_reports" = @(
        "generate_cibc_report.py",
        "generate_ge_report.py",
        "generate_santander_zurich_report.py",
        "show_barclays_details.py"
    )
    "archive/one_off_analyses/mapping" = @(
        "map_ado_bugs_to_ic_mcs.py",
        "map_ic_mcs_bugs_to_customers.py",
        "match_bugs_to_customers.py",
        "match_bugs_to_customers_final.py",
        "final_bug_linkage_analysis.py"
    )
    "archive/utilities" = @(
        "config_email_credentials.py",
        "convert_timeline_to_pptx.py",
        "create_icm_owner_query.py",
        "display_bug_matches_table.py",
        "fix_ic_csv.py",
        "find_unassigned_case.py",
        "SOLUTION_STEPS.py",
        "send_email_graph.py",
        "continuous_improvement_tracker.py"
    )
    "archive/analysis_reports" = @(
        "by_design_analysis_real_data.md",
        "by_design_analysis_report.md",
        "COMPREHENSIVE_BUG_LINKAGE_REPORT.md",
        "GEMBA_ANALYSIS_2512120040008759_Desjardins.md",
        "INCIDENT_TIMELINE_2512120040008759_Desjardins.md",
        "INCIDENT_TIMELINE_2512120040008759_Desjardins_Full.md",
        "IC_REPORT_UPDATES_2026-02-09.md",
        "Desjardins_Incident_Timeline.pptx",
        "icm_by_design_analysis_with_customers.xlsx"
    )
}

$movedCount = 0
$skippedCount = 0

foreach ($destination in $moveOperations.Keys) {
    foreach ($file in $moveOperations[$destination]) {
        if (Test-Path $file) {
            if ($DryRun) {
                Write-Info "Would move: $file -> $destination/"
                $movedCount++
            } else {
                try {
                    Move-Item $file -Destination "$destination/" -Force
                    Write-Success "Moved: $file"
                    $movedCount++
                } catch {
                    Write-Warning "Failed to move $file : $_"
                    $skippedCount++
                }
            }
        } else {
            $skippedCount++
        }
    }
}

Write-Info "Moved: $movedCount files, Skipped: $skippedCount files (already moved or missing)"

# ========================================
# Step 4: Organize Documentation
# ========================================
Write-Info "`nOrganizing documentation..."

$docMoves = @{
    "docs/project/workspace" = @(
        "CLEANUP_PLAN.md",
        "CLEANUP_QUICK_REFERENCE.md",
        "DOCUMENTATION_MAP.md",
        "OPTIMIZATION_GUIDE.md",
        "WHATS_NEW.md",
        "WORKSPACE_ORGANIZATION.md",
        "WORKSPACE_REVIEW_SUMMARY.md"
    )
    "docs/reference" = @(
        "DSCGP Squad Map.csv"
    )
}

foreach ($destination in $docMoves.Keys) {
    foreach ($file in $docMoves[$destination]) {
        if (Test-Path $file) {
            if ($DryRun) {
                Write-Info "Would move: $file -> $destination/"
            } else {
                try {
                    Move-Item $file -Destination "$destination/" -Force
                    Write-Success "Moved: $file"
                } catch {
                    Write-Warning "Failed to move $file : $_"
                }
            }
        }
    }
}

# ========================================
# Step 5: Clean Up Temp Files
# ========================================
Write-Info "`nCleaning up temp files..."

$tempFiles = @(
    "export (9).csv"
)

foreach ($file in $tempFiles) {
    if (Test-Path $file) {
        if ($DryRun) {
            Write-Info "Would remove: $file"
        } else {
            try {
                Remove-Item $file -Force
                Write-Success "Removed: $file"
            } catch {
                Write-Warning "Failed to remove $file : $_"
            }
        }
    }
}

# Remove Copilot scratch folder
if (Test-Path "Copilot") {
    if ($DryRun) {
        Write-Info "Would remove: Copilot/ folder"
    } else {
        try {
            Remove-Item "Copilot" -Recurse -Force
            Write-Success "Removed: Copilot/ folder"
        } catch {
            Write-Warning "Failed to remove Copilot folder: $_"
        }
    }
}

# ========================================
# Step 6: Create .gitkeep Files
# ========================================
Write-Info "`nCreating .gitkeep files for empty directories..."

$keepFolders = @("data", "output")

foreach ($folder in $keepFolders) {
    if (Test-Path $folder) {
        $gitkeepPath = "$folder/.gitkeep"
        if ($DryRun) {
            Write-Info "Would create: $gitkeepPath"
        } else {
            "" | Out-File $gitkeepPath -Encoding utf8
            Write-Success "Created: $gitkeepPath"
        }
    }
}

# ========================================
# Step 7: Verify Structure
# ========================================
Write-Info "`nVerifying essential folders..."

$essentialFolders = @(
    "agent_memory",
    "sub_agents",
    "docs",
    "grounding_docs",
    "purview_analysis",
    "tsg_system",
    "risk_reports",
    "data",
    "output",
    "archive"
)

$allPresent = $true
foreach ($folder in $essentialFolders) {
    if (Test-Path $folder) {
        Write-Success "$folder"
    } else {
        Write-Error "$folder MISSING"
        $allPresent = $false
    }
}

# ========================================
# Step 8: Count Root Files
# ========================================
Write-Info "`nRoot directory file count..."

$rootFiles = Get-ChildItem -File | Where-Object { -not $_.Name.StartsWith('.') }
$rootFileCount = $rootFiles.Count

Write-Info "Root files: $rootFileCount"

if ($rootFileCount -le 15) {
    Write-Success "Root directory is clean! ($rootFileCount files)"
} else {
    Write-Warning "Root directory still has $rootFileCount files (target: ≤15)"
    Write-Info "Remaining files:"
    $rootFiles | Select-Object Name | Format-Table
}

# ========================================
# Summary
# ========================================
Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "SUMMARY" -ForegroundColor Magenta
Write-Host "========================================`n" -ForegroundColor Magenta

if ($DryRun) {
    Write-Warning "DRY RUN COMPLETE - No files were actually moved"
    Write-Info "Run without -DryRun to execute the cleanup"
} else {
    if ($allPresent -and $rootFileCount -le 15) {
        Write-Success "✅ Cleanup completed successfully!"
        Write-Success "✅ All essential folders present"
        Write-Success "✅ Root directory is clean"
        Write-Info "`nNext steps:"
        Write-Info "1. Review moved files in archive/"
        Write-Info "2. Update documentation links if needed"
        Write-Info "3. Test agent functionality"
        Write-Info "4. Review FOUNDRY_PREPARATION_PLAN.md for deployment checklist"
    } else {
        Write-Warning "⚠️  Cleanup completed with warnings"
        Write-Info "Review the output above for details"
    }
}

Write-Host "`n" 
