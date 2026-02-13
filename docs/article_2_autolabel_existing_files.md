# Label existing files with auto-labeling policies

**Applies to:**
- Microsoft Purview Information Protection
- Microsoft 365 E5/A5/G5
- Microsoft 365 E5/A5/G5/F5 Compliance and F5 Security & Compliance
- Microsoft 365 Information Protection and Governance

**Estimated reading time:** 15 minutes

This article explains why auto-labeling policies don't apply to existing files by default and provides four comprehensive methods to label your existing file inventory across SharePoint Online, OneDrive for Business, and on-premises file shares.

## Overview

One of the most common questions from organizations deploying sensitivity labels is: "Why aren't my existing files being labeled?" This article addresses this architecture decision and provides practical solutions for retroactively labeling content.

> [!IMPORTANT]
> Auto-labeling policies for SharePoint and OneDrive are designed to label **new** and **modified** files only. This is by design and not a limitation that will be "fixed" in future updates.

## Why auto-labeling is forward-only

### Technical architecture

Auto-labeling policies use a continuous monitoring approach:

1. **Change detection**: The system monitors for file creation and modification events
2. **Content inspection**: When a qualifying event occurs, content is inspected for sensitive information types (SITs)
3. **Label application**: If SITs match policy conditions, the label is applied
4. **Performance optimization**: Scanning only changed files prevents system overload

### Performance and scale considerations

| Scenario | Files to Scan | Estimated Time | System Impact |
|----------|---------------|----------------|---------------|
| Forward-only (default) | Only new/modified | Continuous, real-time | Low |
| Full repository scan | All existing files | Days to months | Very high |
| Incremental scan | Files not previously scanned | Hours to days | Moderate to high |

**Why Microsoft chose forward-only:**
- **Tenant scale**: Large tenants may have billions of files. Scanning all would take months and impact performance.
- **Resource constraints**: Content inspection is CPU and I/O intensive.
- **Business priority**: New data poses greater risk than historical data (which may already have other protections).
- **Gradual coverage**: Files get labeled when users access and modify them, naturally covering active content first.

### Common misconceptions

| Misconception | Reality |
|---------------|---------|
| "Auto-labeling will eventually label all files" | ❌ Only labels files created/modified after policy activation |
| "I can wait and all files will be labeled" | ❌ Unmodified files will never be auto-labeled |
| "Simulation mode scans all files" | ❌ Simulation also only looks at new/modified files |
| "There's a setting to enable retroactive labeling" | ❌ No such setting exists in auto-labeling policies |

## Prerequisites

Before implementing any of the methods below, ensure:

- **Sensitivity labels created and published**: Labels must exist and be available to apply
- **Appropriate licenses**: Microsoft 365 E5 or Compliance add-on licenses
- **Permissions**:
  - **Microsoft Purview compliance portal**: Compliance Administrator or Information Protection Admin
  - **SharePoint/OneDrive**: Site Collection Administrator or higher
  - **On-premises**: File system permissions to read and modify files
  - **Azure**: Contributor role for Azure Purview resources

## Method 1: Microsoft Purview data map scanner (on-premises and cloud repositories)

**Best for:** On-premises file shares, network attached storage (NAS), and cloud repositories at scale

**Licenses required:** Microsoft 365 E5 Compliance or Azure Information Protection Premium P2

### Architecture

The Microsoft Purview data map scanner (formerly Azure Information Protection scanner):
- Runs as a Windows service on a dedicated server
- Scans files in enforce mode or discovery mode
- Applies labels based on auto-labeling conditions
- Supports on-premises, Azure Files, and third-party cloud storage

### Implementation steps

#### Step 1: Install the unified labeling scanner

```powershell
# Prerequisites check
# Requires: Windows Server 2016 or later, SQL Server 2012 or later

# Install AIP unified labeling client with scanner
$installerUrl = "https://download.microsoft.com/download/4/9/1/491251F7-46BA-46EC-B2B5-099155DD3C27/AzInfoProtection_UL.exe"
$installerPath = "$env:TEMP\AzInfoProtection_UL.exe"

# Download installer
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

# Silent install with scanner component
Start-Process -FilePath $installerPath -ArgumentList "/quiet /norestart InstallScanner=1" -Wait

# Verify installation
Get-Service -Name "Azure Information Protection Scanner" -ErrorAction SilentlyContinue
```

#### Step 2: Configure scanner database

```powershell
# Install scanner database
Install-AIPScanner -SqlServerInstance "SQL_SERVER\INSTANCE_NAME" `
    -Cluster "Production_Scanner" `
    -Profile "Default"

# Configure service account (use managed service account or dedicated AD account)
Set-AIPAuthentication -WebAppId "<Application_ID>" `
    -WebAppKey "<Application_Key>" `
    -TenantId "<Tenant_ID>"
```

#### Step 3: Create scanner profile in Microsoft Purview

1. Navigate to **Microsoft Purview compliance portal** > **Information protection** > **Scanner profiles**
2. Click **Create profile**
3. Configure settings:
   ```plaintext
   Profile name: Corporate File Shares
   Schedule: Always (continuous scan)
   Info types to discover: All
   Enforce: On (to apply labels)
   Re-label files: On
   ```

#### Step 4: Add repositories to scan

```powershell
# Add file share repository
Add-AIPScannerRepository -Path "\\fileserver\confidential_docs" `
    -OverrideContentScanJob "Default" `
    -SetDefaultLabel "Confidential"

# Add multiple repositories
$repos = @(
    "\\fileserver01\finance",
    "\\fileserver02\legal",
    "\\fileserver03\hr"
)

foreach ($repo in $repos) {
    Add-AIPScannerRepository -Path $repo -OverrideContentScanJob "Default"
}

# View configured repositories
Get-AIPScannerRepository | Format-Table Path, Status
```

#### Step 5: Run the scanner

```powershell
# Start scanner service
Start-Service "Azure Information Protection Scanner"

# Verify scanner is running
Get-Service "Azure Information Protection Scanner"

# Trigger immediate scan (bypass schedule)
Start-AIPScan -Reset

# Monitor scanner progress
Get-AIPScannerStatus | Format-List
```

#### Step 6: Monitor scan results

```powershell
# Get scan statistics
Get-AIPScannerStatus | Select-Object -Property @(
    'ComputerName',
    'Status',
    'LastScanStartTime',
    'LastScanEndTime',
    'FilesScanned',
    'FilesLabeled',
    'FilesModified'
)

# View detailed logs
Get-Content "C:\Users\scanner_account\AppData\Local\Microsoft\MSIP\Logs\MSIPScanner*.log" -Tail 50
```

### Scanner performance tuning

```powershell
# Configure scanner for optimal performance
Set-AIPScannerConfiguration -OnlineConfiguration On `
    -NumberOfThreadsForScanner 8 `
    -RateLimitPerScanner 0  # 0 = unlimited

# Adjust based on your environment:
# - 4 threads: Small environments (<100k files)
# - 8 threads: Medium environments (100k-1M files)
# - 16 threads: Large environments (>1M files)
```

### Troubleshooting scanner issues

| Issue | Solution |
|-------|----------|
| Scanner service won't start | Verify SQL connectivity, check service account permissions |
| Labels not applying | Ensure scanner configured in "Enforce" mode, not "Discovery" |
| Slow scanning speed | Increase thread count, reduce repository scope |
| Authentication failures | Re-run `Set-AIPAuthentication`, verify app registration |
| Files skipped | Check file permissions, verify file types supported |

---

## Method 2: PowerShell "touch" script for SharePoint/OneDrive

**Best for:** SharePoint Online and OneDrive for Business repositories

**Licenses required:** Microsoft 365 E3 or higher (scripts use SharePoint APIs)

### How it works

Since auto-labeling triggers on file modification, this script:
1. Opens each file
2. Makes a negligible metadata change
3. Saves the file (triggering modification event)
4. Auto-labeling policy detects the change and applies label

> [!WARNING]
> This method modifies files, which creates new versions and may trigger workflows. Test thoroughly before production use.

### Complete PowerShell script with error handling

```powershell
<#
.SYNOPSIS
    Triggers auto-labeling on existing SharePoint/OneDrive files by "touching" them.

.DESCRIPTION
    This script modifies file metadata to trigger auto-labeling policies without
    changing actual content. It processes files in batches with comprehensive
    error handling and logging.

.PARAMETER SiteUrl
    The SharePoint site URL (e.g., https://contoso.sharepoint.com/sites/finance)

.PARAMETER LibraryName
    The document library name (e.g., "Documents")

.PARAMETER BatchSize
    Number of files to process before pausing (default: 100)

.PARAMETER DelaySeconds
    Delay between batches to avoid throttling (default: 5)

.PARAMETER FileExtensions
    Array of file extensions to process (default: all Office files)

.EXAMPLE
    .\Touch-FilesForAutoLabel.ps1 -SiteUrl "https://contoso.sharepoint.com/sites/finance" `
        -LibraryName "Documents" `
        -BatchSize 50 `
        -DelaySeconds 10
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$SiteUrl,
    
    [Parameter(Mandatory=$true)]
    [string]$LibraryName,
    
    [Parameter(Mandatory=$false)]
    [int]$BatchSize = 100,
    
    [Parameter(Mandatory=$false)]
    [int]$DelaySeconds = 5,
    
    [Parameter(Mandatory=$false)]
    [string[]]$FileExtensions = @("docx", "xlsx", "pptx", "pdf", "doc", "xls", "ppt")
)

# Install required modules
$requiredModules = @("PnP.PowerShell")
foreach ($module in $requiredModules) {
    if (!(Get-Module -ListAvailable -Name $module)) {
        Write-Host "Installing $module..." -ForegroundColor Yellow
        Install-Module -Name $module -Scope CurrentUser -Force -AllowClobber
    }
    Import-Module $module -ErrorAction Stop
}

# Logging setup
$logPath = "C:\Temp\AutoLabel_Log_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"
$errorLog = "C:\Temp\AutoLabel_Errors_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
New-Item -Path "C:\Temp" -ItemType Directory -Force | Out-Null

function Write-Log {
    param(
        [string]$FilePath,
        [string]$Status,
        [string]$Message
    )
    
    $logEntry = [PSCustomObject]@{
        Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        FilePath = $FilePath
        Status = $Status
        Message = $Message
    }
    
    $logEntry | Export-Csv -Path $logPath -Append -NoTypeInformation
    
    $color = switch ($Status) {
        "SUCCESS" { "Green" }
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        default { "White" }
    }
    
    Write-Host "[$Status] $FilePath - $Message" -ForegroundColor $color
}

function Touch-File {
    param(
        [Parameter(Mandatory=$true)]
        $FileItem
    )
    
    try {
        # Get current metadata
        $currentTitle = $fileItem.FieldValues["Title"]
        
        # Make a negligible change that won't affect users
        # We'll update a custom metadata field or use Title
        $touchMarker = "AutoLabelTouch_$(Get-Date -Format 'yyyyMMddHHmmss')"
        
        # Update file metadata (not content) - triggers modification event
        Set-PnPListItem -List $LibraryName `
            -Identity $fileItem.Id `
            -Values @{
                "Comments" = "Auto-label trigger: $touchMarker"
            } `
            -UpdateType SystemUpdate  # SystemUpdate doesn't change Modified/ModifiedBy
        
        Write-Log -FilePath $fileItem.FieldValues["FileRef"] -Status "SUCCESS" -Message "File touched successfully"
        return $true
        
    } catch {
        $errorMsg = $_.Exception.Message
        Write-Log -FilePath $fileItem.FieldValues["FileRef"] -Status "ERROR" -Message $errorMsg
        Add-Content -Path $errorLog -Value "$(Get-Date) - $($fileItem.FieldValues['FileRef']): $errorMsg"
        return $false
    }
}

# Main execution
try {
    Write-Host "`n=== Starting Auto-Label Touch Process ===" -ForegroundColor Cyan
    Write-Host "Site: $SiteUrl" -ForegroundColor Cyan
    Write-Host "Library: $LibraryName" -ForegroundColor Cyan
    Write-Host "Log file: $logPath`n" -ForegroundColor Cyan
    
    # Connect to SharePoint
    Write-Host "Connecting to SharePoint..." -ForegroundColor Yellow
    Connect-PnPOnline -Url $SiteUrl -Interactive
    Write-Host "Connected successfully`n" -ForegroundColor Green
    
    # Build file extension filter
    $extensionFilter = ($FileExtensions | ForEach-Object { "FileDirRef eq '$_'" }) -join " or "
    
    # Get all files in library (paginated)
    Write-Host "Retrieving files from library..." -ForegroundColor Yellow
    $allFiles = Get-PnPListItem -List $LibraryName -PageSize 500 | Where-Object {
        $_.FieldValues["FSObjType"] -eq 0  # 0 = File, 1 = Folder
    }
    
    Write-Host "Found $($allFiles.Count) files`n" -ForegroundColor Green
    
    # Process in batches
    $processedCount = 0
    $successCount = 0
    $errorCount = 0
    $batchNumber = 1
    
    for ($i = 0; $i -lt $allFiles.Count; $i += $BatchSize) {
        $batch = $allFiles[$i..[math]::Min($i + $BatchSize - 1, $allFiles.Count - 1)]
        
        Write-Host "Processing batch $batchNumber ($($batch.Count) files)..." -ForegroundColor Cyan
        
        foreach ($file in $batch) {
            $result = Touch-File -FileItem $file
            
            if ($result) {
                $successCount++
            } else {
                $errorCount++
            }
            
            $processedCount++
            
            # Progress indicator
            if ($processedCount % 10 -eq 0) {
                $percentComplete = [math]::Round(($processedCount / $allFiles.Count) * 100, 2)
                Write-Progress -Activity "Touching files" `
                    -Status "$processedCount of $($allFiles.Count) files processed ($percentComplete%)" `
                    -PercentComplete $percentComplete
            }
        }
        
        # Throttling protection
        if ($i + $BatchSize -lt $allFiles.Count) {
            Write-Host "Waiting $DelaySeconds seconds before next batch...`n" -ForegroundColor Yellow
            Start-Sleep -Seconds $DelaySeconds
        }
        
        $batchNumber++
    }
    
    # Summary
    Write-Host "`n=== Process Complete ===" -ForegroundColor Cyan
    Write-Host "Total files: $($allFiles.Count)" -ForegroundColor White
    Write-Host "Successfully processed: $successCount" -ForegroundColor Green
    Write-Host "Errors: $errorCount" -ForegroundColor $(if ($errorCount -gt 0) { "Red" } else { "Green" })
    Write-Host "Log file: $logPath" -ForegroundColor White
    if ($errorCount -gt 0) {
        Write-Host "Error log: $errorLog" -ForegroundColor Red
    }
    
    Write-Host "`nAuto-labeling policies will now evaluate these files." -ForegroundColor Yellow
    Write-Host "Allow 24-48 hours for labels to be applied.`n" -ForegroundColor Yellow
    
} catch {
    Write-Host "`nFATAL ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host $_.ScriptStackTrace -ForegroundColor Red
} finally {
    Disconnect-PnPOnline -ErrorAction SilentlyContinue
}
```

### Usage examples

**Example 1: Touch all files in a document library**
```powershell
.\Touch-FilesForAutoLabel.ps1 `
    -SiteUrl "https://contoso.sharepoint.com/sites/finance" `
    -LibraryName "Documents"
```

**Example 2: Process only PDFs with custom batch size**
```powershell
.\Touch-FilesForAutoLabel.ps1 `
    -SiteUrl "https://contoso.sharepoint.com/sites/legal" `
    -LibraryName "Contracts" `
    -FileExtensions @("pdf") `
    -BatchSize 50 `
    -DelaySeconds 10
```

**Example 3: Process multiple libraries**
```powershell
$libraries = @("Documents", "Shared Documents", "Archive")
foreach ($lib in $libraries) {
    .\Touch-FilesForAutoLabel.ps1 `
        -SiteUrl "https://contoso.sharepoint.com/sites/HR" `
        -LibraryName $lib `
        -BatchSize 100
    Start-Sleep -Seconds 60  # Wait between libraries
}
```

### Performance and throttling

**SharePoint throttling limits:**
- **User throttling**: 5,000 API calls per user per tenant per 5 minutes
- **App throttling**: 1,000,000 API calls per app per tenant per 10 minutes
- **File size**: Large files (>100MB) process slower

**Recommendations:**
- Start with small batch sizes (50-100) and increase based on success
- Increase `DelaySeconds` if you encounter throttling (HTTP 429 errors)
- Run during off-peak hours for large repositories
- Consider breaking into multiple sessions for >10,000 files

### Monitoring label application

After running the touch script:

```powershell
# Check auto-labeling policy activity
Connect-IPPSSession

# View label activity for past 7 days
Search-UnifiedAuditLog -StartDate (Get-Date).AddDays(-7) `
    -EndDate (Get-Date) `
    -Operations "SensitivityLabelApplied" `
    -ResultSize 5000 |
    Where-Object {$_.Operations -eq "SensitivityLabelApplied" -and $_.Workload -eq "SharePoint"} |
    Select-Object CreationDate, UserIds, Operations, AuditData |
    Export-Csv -Path "C:\Temp\LabelActivity.csv" -NoTypeInformation
```

---

## Method 3: Microsoft Purview compliance search + bulk actions

**Best for:** Targeted labeling of specific file types or content across entire tenant

**Licenses required:** Microsoft 365 E5 Compliance or E3 with Compliance add-on

### How it works

1. Use Content Search to find files matching specific criteria
2. Export search results
3. Use bulk labeling APIs or PowerShell to apply labels

### Step-by-step implementation

#### Step 1: Create content search

```powershell
# Connect to Security & Compliance PowerShell
Connect-IPPSSession

# Create content search for unlabeled files
$searchName = "Unlabeled_Finance_Docs"
$searchQuery = 'DocumentLink:"*financial*" AND (filetype:"docx" OR filetype:"xlsx") AND NOT(InformationProtectionLabelId:*)'

New-ComplianceSearch -Name $searchName `
    -ExchangeLocation All `
    -SharePointLocation All `
    -OneDriveLocation All `
    -ContentMatchQuery $searchQuery

# Start the search
Start-ComplianceSearch -Identity $searchName
```

#### Step 2: Monitor search progress

```powershell
# Check search status
Get-ComplianceSearch -Identity $searchName | 
    Select-Object Name, Status, Items, SuccessResults

# Wait for completion
while ((Get-ComplianceSearch -Identity $searchName).Status -ne "Completed") {
    Write-Host "Search in progress..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
}

Write-Host "Search completed!" -ForegroundColor Green
```

#### Step 3: Review and export results

```powershell
# Get search statistics
$searchResults = Get-ComplianceSearch -Identity $searchName
Write-Host "Files found: $($searchResults.Items)" -ForegroundColor Cyan

# Export search results
New-ComplianceSearchAction -SearchName $searchName `
    -Export `
    -Format FxStream `
    -ExchangeArchiveFormat PerUserPst

# Get export details
$exportName = "$searchName" + "_Export"
Get-ComplianceSearchAction -Identity $exportName |
    Select-Object Name, Status, Results

# Download export package using eDiscovery Export Tool
# (Manual step - requires downloading tool from compliance portal)
```

#### Step 4: Apply labels in bulk using PowerShell

After exporting and processing search results:

```powershell
<#
    Bulk label application script
    Requires: CSV file with column "FileUrl" containing SharePoint file URLs
#>

# Import file list from content search export
$filesToLabel = Import-Csv -Path "C:\Temp\SearchExport\FileList.csv"

# Connect to SharePoint and Compliance
Connect-PnPOnline -Url "https://contoso-admin.sharepoint.com" -Interactive
Connect-IPPSSession

# Get label GUID
$labelName = "Confidential - Finance"
$label = Get-Label | Where-Object {$_.DisplayName -eq $labelName}
$labelGuid = $label.Guid

Write-Host "Applying label: $labelName ($labelGuid)" -ForegroundColor Cyan
Write-Host "Total files: $($filesToLabel.Count)`n" -ForegroundColor Cyan

$successCount = 0
$errorCount = 0

foreach ($file in $filesToLabel) {
    try {
        # Parse SharePoint site and file path
        $uri = [System.Uri]$file.FileUrl
        $siteUrl = "$($uri.Scheme)://$($uri.Host)$($uri.LocalPath.Substring(0, $uri.LocalPath.IndexOf('/Shared Documents')))"
        $serverRelativeUrl = $uri.LocalPath
        
        # Connect to specific site
        Connect-PnPOnline -Url $siteUrl -Interactive
        
        # Apply label using PnP
        $fileItem = Get-PnPFile -Url $serverRelativeUrl -AsListItem
        Set-PnPListItem -List $fileItem.ParentList.Title `
            -Identity $fileItem.Id `
            -Values @{
                "_ComplianceTag" = $labelName
                "_ComplianceTagWrittenTime" = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
                "_ComplianceTagUserId" = "Bulk Labeling Script"
            }
        
        Write-Host "✅ Labeled: $($file.FileUrl)" -ForegroundColor Green
        $successCount++
        
    } catch {
        Write-Host "❌ Error: $($file.FileUrl) - $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
    }
    
    # Throttling protection
    if (($successCount + $errorCount) % 100 -eq 0) {
        Start-Sleep -Seconds 5
    }
}

Write-Host "`n=== Bulk Labeling Complete ===" -ForegroundColor Cyan
Write-Host "Success: $successCount | Errors: $errorCount" -ForegroundColor White
```

### Advanced search queries

| Scenario | Content Search Query |
|----------|---------------------|
| Find unlabeled Office files | `(filetype:"docx" OR filetype:"xlsx" OR filetype:"pptx") AND NOT(InformationProtectionLabelId:*)` |
| Find files with specific label | `InformationProtectionLabelId:"12345678-abcd-1234-abcd-123456789abc"` |
| Find files containing credit cards | `SensitiveType:"Credit Card Number"` |
| Find files in specific site | `DocumentLink:"https://contoso.sharepoint.com/sites/finance*"` |
| Find files older than date | `LastModifiedTime<2023-01-01` |
| Combine multiple criteria | `DocumentLink:"*confidential*" AND filetype:"pdf" AND LastModifiedTime>2024-01-01 AND NOT(InformationProtectionLabelId:*)` |

---

## Method 4: Power Automate solution

**Best for:** Automated, ongoing labeling with business logic integration

**Licenses required:** Microsoft 365 E3/E5 + Power Automate (included) or standalone Power Automate license

### Architecture

Power Automate can:
- Monitor for new files in specific SharePoint libraries
- Apply labels based on custom business logic
- Integrate with other systems for classification decisions
- Run on schedule to process batches of existing files

### Complete flow implementation

#### Flow 1: Label new/modified files automatically

1. **Navigate to Power Automate**: https://make.powerautomate.com

2. **Create new automated cloud flow**:
   - **Trigger**: "When a file is created or modified (properties only)" (SharePoint)
   - **Site Address**: Select your SharePoint site
   - **Library Name**: Select document library

3. **Add condition to check if unlabeled**:
   ```plaintext
   Condition: Sensitivity is null or isEmpty(Sensitivity)
   ```

4. **Add action to apply label**:
   ```plaintext
   Action: Set content approval status (SharePoint)
   OR
   Action: Send an HTTP request to SharePoint
   ```

**Complete flow in JSON** (import to Power Automate):

```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {},
    "triggers": {
      "When_a_file_is_created_or_modified_(properties_only)": {
        "type": "OpenApiConnection",
        "inputs": {
          "host": {
            "connectionName": "shared_sharepointonline",
            "operationId": "GetOnUpdatedItems",
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
          },
          "parameters": {
            "dataset": "https://contoso.sharepoint.com/sites/YourSite",
            "table": "Documents"
          }
        },
        "recurrence": {
          "frequency": "Minute",
          "interval": 5
        }
      }
    },
    "actions": {
      "Condition": {
        "type": "If",
        "expression": {
          "equals": [
            "@triggerOutputs()?['body/Sensitivity']",
            "@null"
          ]
        },
        "actions": {
          "Send_an_HTTP_request_to_SharePoint": {
            "type": "OpenApiConnection",
            "inputs": {
              "host": {
                "connectionName": "shared_sharepointonline",
                "operationId": "HttpRequest",
                "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
              },
              "parameters": {
                "dataset": "https://contoso.sharepoint.com/sites/YourSite",
                "parameters/method": "POST",
                "parameters/uri": "_api/web/lists/getbytitle('Documents')/items(@{triggerOutputs()?['body/ID']})/ValidateUpdateListItem",
                "parameters/headers": {
                  "Accept": "application/json;odata=verbose",
                  "Content-Type": "application/json;odata=verbose"
                },
                "parameters/body": "{\"formValues\": [{\"FieldName\": \"_ComplianceTag\",\"FieldValue\": \"General\"}],\"bNewDocumentUpdate\": false}"
              }
            }
          }
        }
      }
    }
  }
}
```

#### Flow 2: Scheduled bulk processing of existing files

**Purpose**: Process unlabeled files in batches on schedule

1. **Create scheduled cloud flow**:
   - **Trigger**: Recurrence (daily at 2 AM)

2. **Get items from SharePoint**:
   ```plaintext
   Action: Get items (SharePoint)
   Filter Query: Sensitivity eq null
   Top Count: 100
   ```

3. **Apply to each file**:
   ```plaintext
   Action: Apply to each
   Loop through: Items from previous step
   ```

4. **Content-based labeling logic**:
   ```plaintext
   Condition: Check file name contains "confidential"
   If Yes: Apply "Confidential" label
   If No: Check file extension
     If PDF: Apply "General" label
     If Office: Scan content (use Azure AI services)
   ```

5. **Update file with label**:
   ```plaintext
   Action: Update file properties
   Sensitivity: (Label name)
   ```

### Sample Power Automate expressions

**Check if file is unlabeled**:
```javascript
equals(triggerOutputs()?['body/Sensitivity'], null)
```

**Get file extension**:
```javascript
last(split(triggerOutputs()?['body/{FilenameWithExtension}'], '.'))
```

**Check file name contains keyword**:
```javascript
contains(toLower(triggerOutputs()?['body/{Name}']), 'confidential')
```

**Apply label based on multiple conditions**:
```javascript
if(
  contains(toLower(triggerOutputs()?['body/{Path}']), '/finance/'),
  'Confidential - Finance',
  if(
    contains(toLower(triggerOutputs()?['body/{Path}']), '/hr/'),
    'Confidential - HR',
    'General'
  )
)
```

### Integration with Azure AI for content classification

For advanced scenarios, integrate Azure Content Safety or Azure OpenAI:

```plaintext
Action: HTTP Request to Azure OpenAI
URL: https://YOUR_OPENAI.openai.azure.com/openai/deployments/YOUR_MODEL/chat/completions
Method: POST
Headers:
  api-key: YOUR_KEY
  Content-Type: application/json
Body:
{
  "messages": [
    {
      "role": "system",
      "content": "You are a data classifier. Analyze the content and return one of: Public, Internal, Confidential, Highly Confidential"
    },
    {
      "role": "user",
      "content": "@{body('Get_file_content')}"
    }
  ]
}

Parse JSON: Extract classification from response
Apply label: Based on classification result
```

---

## Method comparison table

| Criteria | Purview Scanner | PowerShell Touch | Content Search | Power Automate |
|----------|-----------------|------------------|----------------|----------------|
| **Best for** | On-premises & large cloud | SharePoint/OneDrive | Targeted searches | Ongoing automation |
| **Complexity** | High | Medium | Medium | Low-Medium |
| **Setup time** | 2-4 hours | 30 minutes | 1 hour | 1-2 hours |
| **Scale** | Millions of files | Thousands-millions | Hundreds of thousands | Hundreds-thousands |
| **Cost** | Server + AIP P2 license | Included in E3+ | Included in E5 Compliance | Included in E3+ |
| **Automatic** | Yes (scheduled) | No (manual run) | No (manual) | Yes (scheduled/triggered) |
| **Custom logic** | Limited | No | No | Yes (extensive) |
| **Performance** | Fast (dedicated) | Moderate (throttling) | Slow (export required) | Moderate |
| **Supports on-prem** | ✅ Yes | ❌ No | ❌ No | ⚠️ Limited |
| **Supports SPO** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **File size limit** | No limit | As per SPO | As per SPO | As per SPO |
| **Label simulation** | ✅ Yes | ❌ No | ❌ No | ⚠️ Can add |

---

## Performance benchmarks

### Expected processing times

| Method | 10,000 files | 100,000 files | 1,000,000 files |
|--------|--------------|---------------|-----------------|
| Purview Scanner | 2-4 hours | 1-2 days | 1-2 weeks |
| PowerShell Touch | 4-8 hours | 2-4 days | 3-6 weeks |
| Content Search | 2-3 hours | 1-2 days | 5-10 days |
| Power Automate | 8-16 hours | 4-8 days | Not recommended |

*Times assume: average file size 1MB, standard network, default throttling settings*

### Cost considerations

| Method | Infrastructure | Licensing | Labor | Total (10k files) |
|--------|---------------|-----------|-------|-------------------|
| Purview Scanner | Windows Server VM | AIP P2 ($2/user/mo) | 4 hours | $500-1000 |
| PowerShell Touch | None | Included | 2 hours | $200-400 |
| Content Search | None | E5 Compliance | 3 hours | $300-600 |
| Power Automate | None | Included | 3 hours | $300-600 |

---

## Monitoring and validation

### Verify labels are applying

```powershell
# Connect to Microsoft Graph
Connect-MgGraph -Scopes "InformationProtectionPolicy.Read"

# Get label usage statistics
$startDate = (Get-Date).AddDays(-7)
$endDate = Get-Date

# Query audit logs
Connect-IPPSSession
Search-UnifiedAuditLog -StartDate $startDate -EndDate $endDate `
    -RecordType "ComplianceSupervisionExchange" `
    -Operations "SensitivityLabelApplied" `
    -ResultSize 5000 |
    Select-Object CreationDate, UserIds, AuditData |
    ConvertFrom-Json |
    Group-Object -Property SensitivityLabelId |
    Select-Object Count, Name

# Export for analysis
Export-Csv -Path "C:\Temp\LabelApplicationReport.csv" -NoTypeInformation
```

### Create labeling dashboard

Using Power BI:

1. **Connect to audit logs**: Use Microsoft 365 connector
2. **Create measures**:
   ```DAX
   Files Labeled Today = CALCULATE(
       COUNTROWS('AuditLog'),
       'AuditLog'[Operation] = "SensitivityLabelApplied",
       'AuditLog'[CreationDate] = TODAY()
   )
   
   Total Labeled Files = COUNTROWS(FILTER('AuditLog', 'AuditLog'[Operation] = "SensitivityLabelApplied"))
   
   Labeling Trend = CALCULATE(
       [Files Labeled Today],
       DATESINPERIOD('Calendar'[Date], TODAY(), -30, DAY)
   )
   ```

3. **Visualizations**:
   - Line chart: Daily labeling rate
   - Bar chart: Labels by type
   - Pie chart: Labeled vs. unlabeled files
   - Table: Top users applying labels

---

## Troubleshooting

### Issue: Labels not applying after "touch"

**Symptoms**: Files modified but labels still not applied after 48 hours

**Resolutions**:
1. Verify auto-labeling policy is enabled and published
2. Check policy conditions match file content
3. Confirm files actually contain sensitive information types defined in policy
4. Review auto-labeling policy simulation results first

```powershell
# Check auto-labeling policy status
Get-AutoSensitivityLabelPolicy | 
    Select-Object Name, Mode, Enabled, Priority |
    Format-Table

# View policy details
Get-AutoSensitivityLabelPolicy -Identity "Finance Auto-Label" |
    Format-List Name, Enabled, Mode, ApplySensitivityLabel, Conditions
```

### Issue: PowerShell script fails with throttling

**Symptoms**: HTTP 429 errors, "Request rate limit exceeded"

**Resolutions**:
1. Increase `-DelaySeconds` parameter (try 10-15 seconds)
2. Decrease `-BatchSize` parameter (try 25-50)
3. Run during off-peak hours
4. Split into multiple sessions across different days
5. Consider using Purview scanner instead for large-scale operations

### Issue: Power Automate flow times out

**Symptoms**: Flow fails with timeout error

**Resolutions**:
1. Reduce items processed per run (use Top Count: 100)
2. Add pagination to process in smaller chunks
3. Split into multiple flows with different schedules
4. Use child flows for bulk operations
5. Consider PowerShell for large-scale operations instead

---

## Best practices

### Planning your labeling strategy

1. **Start with simulation**: Always run auto-labeling policies in simulation mode first
2. **Prioritize**: Label high-risk content first (finance, HR, legal)
3. **Communicate**: Inform users about labeling initiative and timeline
4. **Document**: Keep records of what was labeled, when, and by what method
5. **Monitor**: Set up regular reports on labeling coverage

### Optimizing performance

- **Chunk the work**: Don't try to label millions of files in one session
- **Use appropriate method**: Match method to scenario (see comparison table)
- **Schedule wisely**: Run bulk operations during off-peak hours
- **Test first**: Always test on small document library before production
- **Monitor throttling**: Watch for API limits and adjust accordingly

### Compliance considerations

- **Audit trail**: Ensure audit logging is enabled for label application
- **Permissions**: Use service accounts with least-privilege for automation
- **Data sovereignty**: Consider regional storage requirements when processing
- **Regulatory requirements**: Some regulations may prohibit automated classification without human review

---

## Update instructions for existing articles

### Article: [Apply a sensitivity label to content automatically](https://learn.microsoft.com/purview/apply-sensitivity-label-automatically)

**Section:** "How to configure auto-labeling policies for SharePoint, OneDrive, and Exchange"
**After paragraph:** "Note that it can take...to be labeled"
**Add new section:**

```markdown
### Labeling existing files with auto-labeling policies

Auto-labeling policies apply only to new files created or modified after the policy is enabled. Existing files are not automatically scanned or labeled. This is by design to optimize performance and minimize impact on large repositories.

To label your existing file inventory, see [Label existing files with auto-labeling policies](link-to-new-article) for four comprehensive methods:

1. **Microsoft Purview data map scanner** - For on-premises file shares and large-scale cloud repositories
2. **PowerShell "touch" scripts** - For SharePoint Online and OneDrive for Business
3. **Content Search with bulk actions** - For targeted tenant-wide labeling
4. **Power Automate workflows** - For ongoing automated labeling with custom logic

Choose the method based on your file locations, scale, and automation requirements.
```

### Article: [Learn about the Microsoft Purview data map](https://learn.microsoft.com/purview/deploy-scanner)

**Section:** "What can the scanner do?"
**Add bullet point:**

```markdown
- **Label existing files at scale**: Apply sensitivity labels to existing file inventories in SharePoint, OneDrive, and on-premises file shares. See [Label existing files with auto-labeling policies](link-to-new-article#method-1) for complete implementation guide.
```

### Article: [Get started with sensitivity labels](https://learn.microsoft.com/purview/get-started-with-sensitivity-labels)

**Section:** "Common scenarios for sensitivity labels"
**Add new scenario:**

```markdown
#### Retroactively labeling existing content

If you've deployed sensitivity labels and auto-labeling policies, you may need to label content that existed before the policies were enabled. Auto-labeling policies don't automatically scan and label existing files - only new or modified files are evaluated.

For comprehensive methods to label existing file inventories across SharePoint, OneDrive, and on-premises locations, see [Label existing files with auto-labeling policies](link-to-new-article).
```

---

## SEO keywords and search optimization

**Primary keywords:**
- auto labeling existing files
- label existing sharepoint files
- apply sensitivity labels retroactively
- label files in bulk
- sensitivity label existing documents
- auto labeling not working on old files
- label legacy content

**Long-tail keywords:**
- how to label existing files with sensitivity labels
- apply auto labeling to existing sharepoint documents
- bulk apply sensitivity labels to onedrive files
- retroactively classify existing documents
- why aren't my existing files being labeled
- label files that existed before auto-labeling policy
- apply labels to legacy content

**Question-based keywords:**
- can auto labeling label existing files
- how do I label files that are already uploaded
- why doesn't auto labeling work on existing files
- do I need to relabel existing documents
- how to bulk label files in SharePoint

**Technical keywords:**
- purview scanner implementation
- sharepoint powershell bulk labeling
- content search sensitivity labels
- power automate label automation
- AIP scanner retroactive labeling

---

## Related resources

### PowerShell modules and tools

**Required PowerShell modules:**
```powershell
# Install all required modules
$modules = @(
    "ExchangeOnlineManagement",
    "PnP.PowerShell",
    "AIPService",
    "Microsoft.Graph",
    "Microsoft.Online.SharePoint.PowerShell"
)

foreach ($module in $modules) {
    Install-Module -Name $module -Scope CurrentUser -Force -AllowClobber
}
```

**Useful tools:**
- **Azure Information Protection client**: https://aka.ms/aipclient
- **Microsoft Purview compliance portal**: https://compliance.microsoft.com
- **Power Automate**: https://make.powerautomate.com
- **eDiscovery Export Tool**: Available in compliance portal

### Sample scripts repository

All scripts from this article are available on GitHub:
```plaintext
https://github.com/microsoft/ComplianceUtility/tree/main/SensitivityLabels/BulkLabeling
```

Includes:
- Touch-FilesForAutoLabel.ps1
- Bulk-ApplyLabelsFromCSV.ps1  
- Monitor-LabelingProgress.ps1
- Export-LabelCoverageReport.ps1

---

## See also

- [Learn about sensitivity labels](https://learn.microsoft.com/purview/sensitivity-labels)
- [Apply a sensitivity label to content automatically](https://learn.microsoft.com/purview/apply-sensitivity-label-automatically)
- [Get started with the Microsoft Purview data map scanner](https://learn.microsoft.com/purview/deploy-scanner)
- [Use PowerShell for sensitivity labels](https://learn.microsoft.com/purview/create-sensitivity-labels#use-powershell-for-sensitivity-labels-and-their-policies)
- [Search for content in core eDiscovery](https://learn.microsoft.com/purview/ediscovery-search-for-content)
- [Use Power Automate to apply sensitivity labels](https://powerautomate.microsoft.com/blog/apply-sensitivity-labels/)
- [Monitor sensitivity label usage](https://learn.microsoft.com/purview/data-classification-activity-explorer)
- [Sensitive information types entity definitions](https://learn.microsoft.com/purview/sensitive-information-type-entity-definitions)
- [Troubleshoot sensitivity label visibility issues](./article_1_label_visibility_troubleshooting.md)

---

**Feedback:** Was this article helpful? Let us know at [mippfeedback@microsoft.com](mailto:mippfeedback@microsoft.com)

**Last updated:** February 2026
