# Troubleshoot sensitivity label visibility issues

**Applies to:**
- Microsoft Purview Information Protection
- Microsoft 365 E3/E5/A3/A5/G3/G5
- Office 365 E3/E5/A3/A5/G3/G5

**Estimated reading time:** 12 minutes

This article helps you diagnose and resolve common issues where sensitivity labels are not visible or not behaving as expected across Microsoft 365 applications and services.

## Overview

Sensitivity labels protect your organization's data by classifying and protecting documents and emails. When labels don't appear or behave correctly, it can disrupt your information protection strategy and confuse users. This article addresses the most common visibility issues reported by organizations deploying sensitivity labels.

## Prerequisites

- Global Administrator, Compliance Administrator, or Security Administrator role
- Sensitivity labels published in Microsoft Purview compliance portal
- Appropriate licenses assigned to users
- [Azure Information Protection unified labeling client](https://www.microsoft.com/download/details.aspx?id=53018) (for File Explorer scenarios)

## Common label visibility issues

### Issue 1: Sensitivity labels not visible in File Explorer

**Symptoms:**
- Users don't see sensitivity labels as columns in File Explorer
- Right-click context menu doesn't show "Classify and Protect"
- Existing labels on files aren't displayed

**Root causes:**
- Azure Information Protection (AIP) unified labeling client not installed
- File Explorer integration disabled in AIP client settings
- Label policies not downloaded to the client
- Office files stored in unsupported locations (mapped drives, certain cloud sync folders)

**Resolution steps:**

1. **Verify AIP unified labeling client installation**

   ```powershell
   # Check if AIP client is installed
   Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | 
       Select-Object DisplayName, DisplayVersion, Publisher | 
       Where-Object {$_.DisplayName -like "*Azure Information Protection*"}
   ```

   Expected output should show "Microsoft Azure Information Protection" with version 2.x or higher.

   If not installed, download and install from: https://www.microsoft.com/download/details.aspx?id=53018

2. **Enable File Explorer integration**

   Check registry setting:
   ```powershell
   # Check File Explorer integration
   Get-ItemProperty -Path "HKCU:\Software\Microsoft\MSIP" -Name "EnableShellExt" -ErrorAction SilentlyContinue
   ```

   If the value is 0 or missing, enable it:
   ```powershell
   # Enable File Explorer integration
   New-ItemProperty -Path "HKCU:\Software\Microsoft\MSIP" -Name "EnableShellExt" -PropertyType DWord -Value 1 -Force
   ```

   Restart File Explorer:
   ```powershell
   Stop-Process -Name explorer -Force
   ```

3. **Force label policy download**

   ```powershell
   # Reset and download policies
   Remove-Item -Path "$env:LOCALAPPDATA\Microsoft\MSIP\mip" -Recurse -Force -ErrorAction SilentlyContinue
   Remove-Item -Path "$env:LOCALAPPDATA\Microsoft\MSIP\TokenCache" -Recurse -Force -ErrorAction SilentlyContinue
   ```

   Then open any Office application and go to **File > Account > Update Options > Update Now** or wait for automatic policy refresh (24 hours by default).

4. **Verify supported file locations**

   File Explorer integration works best with:
   - Local drives (C:\, D:\, etc.)
   - UNC network paths (\\server\share)
   - OneDrive sync folders (after sync completes)

   **Not supported:**
   - Mapped network drives (workaround: use UNC path instead)
   - SharePoint libraries opened in browser
   - Some third-party cloud sync folders

5. **Check event logs for errors**

   ```powershell
   # Check AIP client logs
   Get-WinEvent -LogName "Application" -MaxEvents 50 | 
       Where-Object {$_.ProviderName -like "*MSIP*" -or $_.ProviderName -like "*Azure Information Protection*"} |
       Format-Table TimeCreated, Id, LevelDisplayName, Message -Wrap
   ```

> [!NOTE]
> File Explorer integration requires the AIP unified labeling client. Native Office label support does not include File Explorer functionality.

---

### Issue 2: Label inheritance not working in SharePoint Online

**Symptoms:**
- New files uploaded to labeled folders don't inherit the parent label
- Document libraries with default labels don't apply labels automatically
- Sub-folders don't inherit parent folder labels

**Root causes:**
- Label inheritance feature not enabled for the tenant
- Document library doesn't have default sensitivity label configured
- User uploading files doesn't have permissions to apply the label
- Existing files uploaded before feature enablement

**Resolution steps:**

1. **Enable label inheritance for SharePoint Online**

   Connect to SharePoint Online Management Shell:
   ```powershell
   # Install module if needed
   Install-Module -Name Microsoft.Online.SharePoint.PowerShell -Scope CurrentUser

   # Connect to SharePoint Online
   $adminUrl = "https://contoso-admin.sharepoint.com"
   Connect-SPOService -Url $adminUrl

   # Enable label inheritance
   Set-SPOTenant -EnableAutoLabelingInSharePoint $true
   ```

   > [!IMPORTANT]
   > Changes may take up to 24 hours to propagate across all SharePoint sites.

2. **Configure default sensitivity label for document library**

   In SharePoint Online:
   - Navigate to the document library
   - Click **Settings** (gear icon) > **Library settings**
   - Under **Permissions and Management**, click **Information Rights Management**
   - Select **Restrict downloads for documents in this library to users with access**
   - Choose the default sensitivity label from the dropdown
   - Click **OK**

   Alternative PowerShell method:
   ```powershell
   # Connect to PnP PowerShell
   Install-Module -Name PnP.PowerShell -Scope CurrentUser
   Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/yoursite" -Interactive

   # Set default sensitivity label for library
   $labelGuid = "12345678-1234-1234-1234-123456789abc"  # Get from Purview portal
   Set-PnPList -Identity "Documents" -DefaultSensitivityLabelForLibrary $labelGuid
   ```

3. **Verify user permissions**

   Users must have:
   - **Edit** permissions on the document library
   - License that includes sensitivity labels
   - Label policy that includes the inherited label

   Check user license:
   ```powershell
   # Connect to Microsoft Graph
   Connect-MgGraph -Scopes "User.Read.All"

   # Check user license
   Get-MgUserLicenseDetail -UserId "user@contoso.com" | 
       Select-Object SkuPartNumber | 
       Where-Object {$_.SkuPartNumber -like "*E5*" -or $_.SkuPartNumber -like "*COMPLIANCE*"}
   ```

4. **Understand inheritance behavior**

   | Scenario | Inheritance Behavior |
   |----------|---------------------|
   | New file created in browser | ✅ Inherits library/folder label |
   | File uploaded via browser | ✅ Inherits library/folder label |
   | File uploaded via OneDrive sync | ✅ Inherits after sync completes |
   | File uploaded via API/third-party app | ⚠️ May not inherit (depends on app) |
   | Existing files before feature enabled | ❌ No automatic labeling (see Theme 2 article) |
   | File moved from another location | ❌ Retains original label |
   | File copied to folder | ✅ New copy inherits folder label |

5. **Troubleshoot inheritance failures**

   Enable diagnostic logging:
   ```powershell
   # Enable SharePoint audit logging
   Connect-ExchangeOnlineManagement
   Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true

   # Search for label application events
   Search-UnifiedAuditLog -StartDate (Get-Date).AddDays(-7) -EndDate (Get-Date) `
       -Operations "SensitivityLabelApplied" `
       -UserIds "user@contoso.com" |
       Select-Object CreationDate, Operations, AuditData
   ```

> [!TIP]
> To label existing files in bulk, see [Label existing files with auto-labeling policies](./article_2_autolabel_existing_files.md).

---

### Issue 3: Sensitivity labels missing in Outlook Web Access (OWA)

**Symptoms:**
- Label selector not visible when composing emails in OWA
- Labels visible in Outlook desktop but not in OWA
- "Sensitivity" button missing from ribbon

**Root causes:**
- Label policy not applied to Outlook on the web
- Browser caching issues
- Regional compliance boundary restrictions
- User accessing OWA before label policy propagation
- Labels configured for files only (not email)

**Resolution steps:**

1. **Verify label policy includes Outlook on the web**

   In Microsoft Purview compliance portal:
   ```plaintext
   https://compliance.microsoft.com/informationprotection
   ```

   - Navigate to **Information protection > Label policies**
   - Select the policy applied to the user
   - Click **Edit policy**
   - Under **Choose where to apply the policy**, verify:
     - ✅ **Outlook** is selected
     - ✅ User/group is in the policy scope
   - Save changes

   Verify via PowerShell:
   ```powershell
   # Connect to Security & Compliance PowerShell
   Connect-IPPSSession

   # Get label policy details
   Get-LabelPolicy -Identity "Global Policy" | 
       Select-Object Name, Enabled, Settings, @{Name="Users";Expression={$_.ExchangeLocation}}

   # Check if specific user is in policy
   (Get-LabelPolicy -Identity "Global Policy").ExchangeLocation -contains "user@contoso.com"
   ```

2. **Configure labels for email workloads**

   Each label must support email:
   - Navigate to **Information protection > Labels**
   - Select the label
   - Click **Edit label > Scope**
   - Ensure **Items** is checked (includes email and calendar items)
   - Click **Next** through wizard and **Save**

   PowerShell verification:
   ```powershell
   # Check label scope
   Get-Label | Select-Object DisplayName, Tooltip, ContentType | Format-Table -AutoSize
   ```

3. **Clear browser cache and cookies**

   For Microsoft Edge:
   ```plaintext
   1. Press Ctrl+Shift+Delete
   2. Select "Cookies and other site data" and "Cached images and files"
   3. Choose "All time"
   4. Click "Clear now"
   5. Close all browser windows
   6. Navigate to https://outlook.office.com
   ```

   Test in browser private/incognito mode to rule out caching issues.

4. **Force label policy update**

   ```powershell
   # Connect to Security & Compliance PowerShell
   Connect-IPPSSession

   # Force policy distribution
   Set-LabelPolicy -Identity "Global Policy" -AdvancedSettings @{EnableLabelByDefault="True"}
   Set-LabelPolicy -Identity "Global Policy" -AdvancedSettings @{EnableLabelByDefault="False"}
   ```

   Wait 24 hours for policy propagation, or use this user-side workaround:
   - Have user sign out of OWA completely
   - Clear browser cache
   - Sign back in after 10 minutes

5. **Check service health and known issues**

   ```powershell
   # Check Microsoft 365 service health
   Connect-MgGraph -Scopes "ServiceHealth.Read.All"
   Get-MgServiceAnnouncementIssue | 
       Where-Object {$_.Service -eq "Exchange Online" -and $_.IsResolved -eq $false} |
       Select-Object Title, Status, Classification, Summary
   ```

   Check the Microsoft 365 Service Health Dashboard:
   ```plaintext
   https://admin.microsoft.com/Adminportal/Home#/servicehealth
   ```

> [!NOTE]
> Label changes in OWA typically require 24 hours to propagate. Desktop Outlook may show labels sooner due to different policy refresh intervals.

---

### Issue 4: Custom sensitivity label templates not supported in Teams

**Symptoms:**
- Custom label templates work in Office apps but not in Teams
- Teams channels/files don't show custom labels
- SharePoint-based custom templates not visible in Teams

**Root causes:**
- Teams label support has feature parity gaps with Office apps
- Custom permissions templates not fully supported in Teams
- Teams uses simplified label picker
- Container-level labels vs. content-level labels confusion

**Resolution steps:**

1. **Understand Teams label support limitations**

   | Label Feature | Teams Files | Teams Meetings | Teams Channels |
   |--------------|-------------|----------------|----------------|
   | Standard sensitivity labels | ✅ Supported | ✅ Supported | ✅ Supported |
   | Custom permissions | ⚠️ Limited | ❌ Not supported | ⚠️ Limited |
   | Encryption | ✅ Supported | ✅ Supported | ❌ Not supported |
   | Header/footer/watermark | ✅ Supported | ❌ Not supported | ❌ Not supported |
   | Auto-labeling | ✅ Supported | ❌ Not supported | ❌ Not supported |
   | User-defined permissions | ❌ Not supported | ❌ Not supported | ❌ Not supported |

2. **Create Teams-compatible labels**

   For labels to work in Teams, configure them with predefined permissions:

   In Purview compliance portal:
   - Navigate to **Information protection > Labels**
   - Click **Create a label**
   - Under **Encryption**, select **Configure encryption settings**
   - Choose **Assign permissions now** (not "Let users assign permissions")
   - Add specific users/groups or use role-based permissions:
     - ✅ "Add any authenticated users"
     - ✅ "Add specific users or groups"
     - ❌ Avoid "Let users assign permissions" (not supported in Teams)

3. **Apply labels at the team/channel level**

   Use container labels for Teams sites:
   ```powershell
   # Connect to Security & Compliance PowerShell
   Connect-IPPSSession

   # Create container label
   $labelName = "Confidential Team"
   New-Label -DisplayName $labelName `
       -Name $labelName `
       -Tooltip "For confidential team collaboration" `
       -EncryptionEnabled $true `
       -ContentType "TeamworkContainer" `
       -EncryptionRightsDefinitions @("All@contoso.com:VIEW,EDIT")

   # Apply label to Teams site
   Set-SPOSite -Identity "https://contoso.sharepoint.com/sites/TeamSiteName" `
       -SensitivityLabel "12345678-1234-1234-1234-123456789abc"
   ```

4. **Migrate custom templates to predefined permissions**

   If you have existing custom templates:
   ```powershell
   # Export existing label configuration
   Connect-IPPSSession
   Get-Label | Where-Object {$_.Tooltip -like "*custom*"} | 
       Select-Object DisplayName, Tooltip, EncryptionEnabled, EncryptionRightsDefinitions |
       Export-Csv -Path "C:\Temp\existing_labels.csv" -NoTypeInformation

   # Review and recreate with predefined permissions
   # (Manual process - review each label's requirements)
   ```

5. **Alternative: Use Teams policies for governance**

   For scenarios unsupported by sensitivity labels:
   ```powershell
   # Connect to Teams PowerShell
   Connect-MicrosoftTeams

   # Configure Teams app permission policy
   New-CsTeamsAppPermissionPolicy -Identity "RestrictedTeams" `
       -DefaultCatalogApps "Core" `
       -GlobalCatalogApps @()

   # Assign to users
   Grant-CsTeamsAppPermissionPolicy -PolicyName "RestrictedTeams" -Identity "user@contoso.com"
   ```

> [!IMPORTANT]
> Teams uses the underlying SharePoint site for file labeling. Labels applied in Teams files are visible in SharePoint and vice versa.

**Workaround for complex permission scenarios:**
- Define security groups with specific members
- Create labels with predefined permissions pointing to those groups
- Manage access by updating group membership instead of label permissions

---

### Issue 5: Label protection settings not syncing across devices

**Symptoms:**
- Label shows correctly but protection (encryption) is removed
- Different devices show different label states for same file
- Label applied on mobile doesn't show on desktop
- Protection applied on desktop removed when opened on mobile

**Root causes:**
- Multi-factor authentication (MFA) requirements blocking Rights Management
- Rights Management service (RMS) templates not syncing
- Device not connected to Internet during label application
- Offline mode causing local-only label application
- Azure Rights Management service not activated

**Resolution steps:**

1. **Verify Azure Rights Management is activated**

   ```powershell
   # Install AIPService module
   Install-Module -Name AIPService -Scope CurrentUser

   # Connect to Azure RMS
   Connect-AipService

   # Check activation status
   Get-AipService

   # If disabled, activate it
   Enable-AipService
   ```

   Expected output: `Enabled: True`

2. **Force RMS template synchronization on devices**

   **Windows:**
   ```powershell
   # Clear cached RMS templates
   Remove-Item -Path "$env:LOCALAPPDATA\Microsoft\MSIPC\*" -Recurse -Force -ErrorAction SilentlyContinue
   Remove-Item -Path "$env:LOCALAPPDATA\Microsoft\DRM\*" -Recurse -Force -ErrorAction SilentlyContinue

   # Force template download
   Import-Module AIPService
   (Get-AipServiceTemplate).Count  # This triggers template sync
   ```

   **macOS:**
   ```bash
   # Clear Office cache
   rm -rf ~/Library/Containers/com.microsoft.*/Data/Library/Application\ Support/Microsoft/Office/CLP
   rm -rf ~/Library/Group\ Containers/UBF8T346G9.Office/mip_policy/mip/logs/*
   ```

   **iOS/Android:**
   - Go to Office app settings
   - Select account
   - Tap "Sign out"
   - Force close app
   - Sign back in

3. **Check network connectivity to RMS endpoints**

   ```powershell
   # Test connectivity to Azure RMS
   $rmsEndpoints = @(
       "api.aadrm.com",
       "*.aadrm.com",
       "*.azurerms.com"
   )

   foreach ($endpoint in $rmsEndpoints) {
       $testResult = Test-NetConnection -ComputerName $endpoint -Port 443 -InformationLevel Quiet
       Write-Output "$endpoint : $testResult"
   }
   ```

   If connections fail, check:
   - Firewall rules
   - Proxy configuration
   - SSL inspection settings
   - VPN connectivity

4. **Configure offline grace period**

   Allow offline use for specified duration:
   ```powershell
   # Set offline policy (max 30 days)
   Set-AipServiceOnboardingControlPolicy -UseRmsUserLicense $true
   Set-AipServiceMaxUseLicenseValidityTime -MaximumValidityDuration 30
   ```

5. **Troubleshoot with Azure RMS diagnostics**

   ```powershell
   # Get RMS licensing details for user
   Get-AipServiceUserLog -FromDate (Get-Date).AddDays(-7) -ToDate (Get-Date) `
       | Where-Object {$_.UserId -eq "user@contoso.com"} `
       | Select-Object TimeStamp, UserId, Rights, ContentId
   ```

6. **Verify label protection configuration**

   Ensure label encryption is configured correctly:
   ```powershell
   Connect-IPPSSession

   # Review label encryption settings
   Get-Label | Where-Object {$_.EncryptionEnabled -eq $true} |
       Select-Object DisplayName, EncryptionEnabled, EncryptionRightsDefinitions, ContentType |
       Format-List
   ```

> [!TIP]
> For users working offline frequently, consider:
> - Extending the offline grace period
> - Using labels without encryption for offline scenarios
> - Implementing device-based conditional access policies

**Device-specific considerations:**

| Device | Sync Method | Typical Delay | Notes |
|--------|-------------|---------------|-------|
| Windows Desktop | Active Directory + Cloud | 24 hours | Fastest with cloud-only users |
| macOS | Cloud only | 24 hours | Requires Office 365 subscription |
| iOS | Cloud only | Real-time | Requires Outlook mobile or Office mobile apps |
| Android | Cloud only | Real-time | Requires Outlook mobile or Office mobile apps |
| Web (OWA/ODB) | Cloud only | Real-time | Always current |

---

## Decision flowchart for troubleshooting label visibility

```plaintext
Is the label visible in ANY application?
│
├─[NO]─> Check label publication status
│        │
│        ├─ Is label published? ─[NO]─> Publish label in Purview portal
│        │                              Wait 24 hours
│        │
│        └─[YES]─> Is user in policy scope? ─[NO]─> Add user to label policy
│                                                   Wait 24 hours
│                                           [YES]
│                                            │
│                                            └─> Check user license
│                                                Has E3/E5/Compliance license? ─[NO]─> Assign license
│
└─[YES]─> Where is the label not visible?
          │
          ├─[File Explorer]─> Is AIP unified labeling client installed? ─[NO]─> Install AIP client
          │                                                             [YES]
          │                                                              │
          │                                                              └─> Enable File Explorer integration
          │                                                                  (See Issue 1, Step 2)
          │
          ├─[SharePoint/OneDrive]─> Are you checking existing files? ─[YES]─> Labels don't apply retroactively
          │                                                                    Use bulk labeling methods
          │                                                          [NO]
          │                                                           │
          │                                                           └─> Is inheritance enabled? ─[NO]─> Enable SPO inheritance
          │                                                                                              (See Issue 2, Step 1)
          │
          ├─[Outlook Web]─> Clear browser cache
          │                 Wait 24 hours for policy sync
          │                 Check label scope includes "Items"
          │                 (See Issue 3)
          │
          ├─[Teams]─> Does label use custom permissions? ─[YES]─> Recreate with predefined permissions
          │                                                        (See Issue 4, Step 2)
          │            [NO]
          │             │
          │             └─> Apply container label to Teams site
          │
          └─[Mobile Device]─> Does label use encryption? ─[YES]─> Check RMS activation
                                                                   Test network connectivity
                                                                   Force template sync
                                                                   (See Issue 5)
```

## PowerShell script: Comprehensive label visibility diagnostic

```powershell
<#
.SYNOPSIS
    Diagnoses sensitivity label visibility issues across Microsoft 365.

.DESCRIPTION
    This script checks common causes of label visibility problems and generates
    a diagnostic report with remediation steps.

.PARAMETER UserPrincipalName
    The UPN of the user experiencing label visibility issues.

.EXAMPLE
    .\Test-LabelVisibility.ps1 -UserPrincipalName "user@contoso.com"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$UserPrincipalName
)

# Output file
$outputFile = "C:\Temp\LabelDiagnostics_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
New-Item -Path "C:\Temp" -ItemType Directory -Force | Out-Null

function Write-DiagnosticLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path $outputFile -Value $logMessage
}

Write-DiagnosticLog "=== Sensitivity Label Visibility Diagnostic ===" "INFO"
Write-DiagnosticLog "User: $UserPrincipalName" "INFO"
Write-DiagnosticLog ""

# Check 1: User License
Write-DiagnosticLog "Checking user license..." "INFO"
try {
    Import-Module Microsoft.Graph.Users -ErrorAction Stop
    Connect-MgGraph -Scopes "User.Read.All" -NoWelcome
    
    $licenses = Get-MgUserLicenseDetail -UserId $UserPrincipalName
    $hasComplianceLicense = $licenses | Where-Object {
        $_.SkuPartNumber -match "E5|E3|COMPLIANCE"
    }
    
    if ($hasComplianceLicense) {
        Write-DiagnosticLog "✅ User has appropriate license: $($hasComplianceLicense.SkuPartNumber -join ', ')" "PASS"
    } else {
        Write-DiagnosticLog "❌ User missing required license (E3/E5 or Compliance)" "FAIL"
        Write-DiagnosticLog "   Action: Assign Microsoft 365 E3/E5 or Compliance license" "ACTION"
    }
} catch {
    Write-DiagnosticLog "⚠️ Unable to check license: $($_.Exception.Message)" "WARN"
}

# Check 2: Label Policies
Write-DiagnosticLog "`nChecking label policies..." "INFO"
try {
    Import-Module ExchangeOnlineManagement -ErrorAction Stop
    Connect-IPPSSession -ErrorAction Stop
    
    $policies = Get-LabelPolicy
    $userPolicies = $policies | Where-Object {
        $_.ExchangeLocation -contains $UserPrincipalName -or
        $_.ExchangeLocation -contains "All"
    }
    
    if ($userPolicies) {
        Write-DiagnosticLog "✅ User assigned to $($userPolicies.Count) label policies" "PASS"
        foreach ($policy in $userPolicies) {
            Write-DiagnosticLog "   - $($policy.Name)" "INFO"
        }
    } else {
        Write-DiagnosticLog "❌ User not assigned to any label policies" "FAIL"
        Write-DiagnosticLog "   Action: Add user to label policy in Purview portal" "ACTION"
    }
    
    # Check individual labels
    $labels = Get-Label
    Write-DiagnosticLog "`n   Available labels: $($labels.Count)" "INFO"
    
} catch {
    Write-DiagnosticLog "⚠️ Unable to check policies: $($_.Exception.Message)" "WARN"
    Write-DiagnosticLog "   Ensure you have Compliance Administrator role" "ACTION"
}

# Check 3: AIP Client (File Explorer)
Write-DiagnosticLog "`nChecking Azure Information Protection client..." "INFO"
$aipInstalled = Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* |
    Where-Object {$_.DisplayName -like "*Azure Information Protection*"}

if ($aipInstalled) {
    Write-DiagnosticLog "✅ AIP client installed: $($aipInstalled.DisplayVersion)" "PASS"
    
    # Check File Explorer integration
    $shellExtEnabled = Get-ItemProperty -Path "HKCU:\Software\Microsoft\MSIP" -Name "EnableShellExt" -ErrorAction SilentlyContinue
    if ($shellExtEnabled.EnableShellExt -eq 1) {
        Write-DiagnosticLog "✅ File Explorer integration enabled" "PASS"
    } else {
        Write-DiagnosticLog "⚠️ File Explorer integration disabled" "WARN"
        Write-DiagnosticLog "   Action: Enable via registry (see Issue 1, Step 2)" "ACTION"
    }
} else {
    Write-DiagnosticLog "⚠️ AIP client not installed (required for File Explorer)" "WARN"
    Write-DiagnosticLog "   Action: Install from https://aka.ms/aipclient" "ACTION"
}

# Check 4: Azure RMS Activation
Write-DiagnosticLog "`nChecking Azure Rights Management..." "INFO"
try {
    Import-Module AIPService -ErrorAction Stop
    Connect-AipService -ErrorAction Stop
    
    $rmsStatus = Get-AipService
    if ($rmsStatus.Enabled) {
        Write-DiagnosticLog "✅ Azure RMS is activated" "PASS"
    } else {
        Write-DiagnosticLog "❌ Azure RMS is not activated" "FAIL"
        Write-DiagnosticLog "   Action: Run Enable-AipService" "ACTION"
    }
} catch {
    Write-DiagnosticLog "⚠️ Unable to check RMS status: $($_.Exception.Message)" "WARN"
}

# Check 5: Network Connectivity
Write-DiagnosticLog "`nChecking network connectivity to RMS endpoints..." "INFO"
$endpoints = @("api.aadrm.com", "informationprotection.azure.com")
foreach ($endpoint in $endpoints) {
    $canConnect = Test-NetConnection -ComputerName $endpoint -Port 443 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($canConnect) {
        Write-DiagnosticLog "✅ Can connect to $endpoint" "PASS"
    } else {
        Write-DiagnosticLog "❌ Cannot connect to $endpoint" "FAIL"
        Write-DiagnosticLog "   Action: Check firewall/proxy settings" "ACTION"
    }
}

# Check 6: SharePoint Online Label Inheritance
Write-DiagnosticLog "`nChecking SharePoint Online settings..." "INFO"
try {
    Import-Module Microsoft.Online.SharePoint.PowerShell -ErrorAction Stop
    $adminUrl = "https://$((Get-MgOrganization).VerifiedDomains[0].Name.Split('.')[0])-admin.sharepoint.com"
    Connect-SPOService -Url $adminUrl -ErrorAction Stop
    
    $spoTenant = Get-SPOTenant
    if ($spoTenant.EnableAutoLabelingInSharePoint) {
        Write-DiagnosticLog "✅ Auto-labeling enabled in SharePoint Online" "PASS"
    } else {
        Write-DiagnosticLog "⚠️ Auto-labeling disabled in SharePoint Online" "WARN"
        Write-DiagnosticLog "   Action: Run Set-SPOTenant -EnableAutoLabelingInSharePoint `$true" "ACTION"
    }
} catch {
    Write-DiagnosticLog "⚠️ Unable to check SharePoint settings: $($_.Exception.Message)" "WARN"
}

# Summary
Write-DiagnosticLog "`n=== DIAGNOSTIC COMPLETE ===" "INFO"
Write-DiagnosticLog "Report saved to: $outputFile" "INFO"
Write-DiagnosticLog "`nNext Steps:" "INFO"
Write-DiagnosticLog "1. Review all FAIL and WARN items above" "INFO"
Write-DiagnosticLog "2. Complete recommended actions" "INFO"
Write-DiagnosticLog "3. Wait 24 hours for policy propagation" "INFO"
Write-DiagnosticLog "4. Re-test label visibility" "INFO"

# Open report
Start-Process notepad.exe $outputFile
```

## Performance considerations

| Scenario | Expected Delay | Accelerate By |
|----------|---------------|---------------|
| New label publication | 24 hours | No manual acceleration available |
| Label policy change | 24 hours | Force token refresh in Office apps |
| RMS template sync | 7 days (default) | Clear local cache and force download |
| SharePoint inheritance enablement | 24 hours | No manual acceleration available |
| File Explorer label refresh | Immediate | Restart explorer.exe process |

## Related configuration settings

### Advanced label policy settings

```powershell
# Configure policy for better visibility

# Require users to apply label before saving
Set-LabelPolicy -Identity "Global Policy" -AdvancedSettings @{RequireDowngradeJustification="True"}

# Set default label for new documents
Set-LabelPolicy -Identity "Global Policy" -AdvancedSettings @{DefaultLabelId="12345678-1234-1234-1234-123456789abc"}

# Show label colors in Office apps
Set-LabelPolicy -Identity "Global Policy" -AdvancedSettings @{EnableLabelByDefault="True"}

# Enable custom permissions in Outlook
Set-LabelPolicy -Identity "Global Policy" -AdvancedSettings @{EnableCustomPermissions="True"}
```

### Registry settings for AIP client

```powershell
# Common AIP client registry tweaks

# Enable advanced logging
New-ItemProperty -Path "HKCU:\Software\Microsoft\MSIP" -Name "LogLevel" -PropertyType String -Value "Debug" -Force

# Reduce policy refresh interval (minimum 1 hour)
New-ItemProperty -Path "HKCU:\Software\Microsoft\MSIP" -Name "PolicyRefreshInterval" -PropertyType DWord -Value 3600 -Force

# Enable offline mode
New-ItemProperty -Path "HKCU:\Software\Microsoft\MSIP" -Name "EnableOfflineMode" -PropertyType DWord -Value 1 -Force
```

## Known issues and limitations

> [!WARNING]
> The following scenarios are not supported and require workarounds:

1. **File Explorer on mapped network drives**: Use UNC paths instead
2. **User-defined permissions in Teams**: Use predefined permission groups
3. **Label visibility in third-party PDF readers**: Use Adobe Acrobat or built-in Office PDF viewer
4. **Real-time label sync across devices**: Allow up to 24 hours for propagation
5. **Labels on files opened from email attachments**: Save to OneDrive/SharePoint first

## Update instructions for existing articles

### Article: [Get started with sensitivity labels](https://learn.microsoft.com/purview/get-started-with-sensitivity-labels)

**Section:** "Phase 4: Deploy labels to clients and apps"
**After paragraph:** "Consider the time it takes for changes to replicate..."
**Add new section:**

```markdown
### Troubleshooting label visibility

If users report that labels aren't visible after deployment, see [Troubleshoot sensitivity label visibility issues](link-to-new-article) for comprehensive diagnostic steps covering:
- File Explorer integration issues
- SharePoint inheritance problems  
- Outlook web access label display
- Teams compatibility
- Cross-device sync problems
```

### Article: [Sensitivity labels in Office apps](https://learn.microsoft.com/purview/sensitivity-labels-office-apps)

**Section:** "Support for sensitivity label capabilities in Office apps"
**After the capability table**
**Add note:**

```markdown
> [!TIP]
> If users don't see labels in specific Office apps or platforms, see the detailed troubleshooting guide at [Troubleshoot sensitivity label visibility issues](link-to-new-article).
```

### Article: [Enable sensitivity labels for files in SharePoint and OneDrive](https://learn.microsoft.com/purview/sensitivity-labels-sharepoint-onedrive-files)

**Section:** "Default sensitivity labels for document libraries"
**At end of section**
**Add subsection:**

```markdown
#### Troubleshoot inheritance issues

If default labels aren't being applied to new or uploaded files:
1. Verify inheritance is enabled tenant-wide: `Set-SPOTenant -EnableAutoLabelingInSharePoint $true`
2. Confirm users have Edit permissions on the library
3. Check that users are assigned licenses with sensitivity label support
4. Allow 24 hours after configuration changes

For comprehensive troubleshooting steps, see [Troubleshoot sensitivity label visibility issues - Issue 2](link-to-new-article#issue-2).
```

## SEO keywords and search optimization

**Primary keywords:**
- sensitivity label not showing
- sensitivity label missing
- sensitivity labels not visible
- can't see sensitivity labels
- sensitivity labels not appearing
- label not showing in file explorer
- sensitivity label not in outlook
- sharepoint label inheritance not working

**Long-tail keywords:**
- why aren't my sensitivity labels showing up
- sensitivity labels not showing in teams
- how to make sensitivity labels visible
- troubleshoot sensitivity label visibility
- sensitivity labels missing from ribbon
- file explorer sensitivity label integration
- outlook web access missing labels
- sharepoint folder label inheritance

**Related search terms:**
- azure information protection labels not showing
- microsoft purview label visibility
- mip labels not appearing
- information protection labels missing
- document classification labels not visible

## Monitoring and ongoing maintenance

### Set up alerts for label application failures

```powershell
# Create alert policy for label failures
Connect-IPPSSession

$alertParams = @{
    Name = "Sensitivity Label Application Failures"
    Category = "DataGovernance"
    NotifyUser = @("admin@contoso.com")
    Operation = @("SensitivityLabelApplied", "SensitivityLabelUpdated")
    Threshold = 100
    TimeWindow = 60
}

New-ProtectionAlert @alertParams
```

### Regular health checks

Schedule monthly checks:
1. Review audit logs for failed label applications
2. Monitor support tickets for label visibility issues
3. Test label visibility in each platform (desktop, mobile, web)
4. Verify RMS template synchronization
5. Check for new Office versions affecting label compatibility

## See also

- [Learn about sensitivity labels](https://learn.microsoft.com/purview/sensitivity-labels)
- [Get started with sensitivity labels](https://learn.microsoft.com/purview/get-started-with-sensitivity-labels)
- [Sensitivity labels in Office apps](https://learn.microsoft.com/purview/sensitivity-labels-office-apps)
- [Enable sensitivity labels in SharePoint and OneDrive](https://learn.microsoft.com/purview/sensitivity-labels-sharepoint-onedrive-files)
- [Manage sensitivity labels in Office apps](https://learn.microsoft.com/purview/sensitivity-labels-office-apps)
- [Use sensitivity labels with Microsoft Teams](https://learn.microsoft.com/purview/sensitivity-labels-teams-groups-sites)
- [Restrict access to content by using encryption](https://learn.microsoft.com/purview/encryption-sensitivity-labels)
- [Apply a sensitivity label automatically](https://learn.microsoft.com/purview/apply-sensitivity-label-automatically)
- [Common scenarios for sensitivity labels](https://learn.microsoft.com/purview/get-started-with-sensitivity-labels#common-scenarios-for-sensitivity-labels)
- [Azure Information Protection unified labeling client](https://learn.microsoft.com/azure/information-protection/rms-client/aip-clientv2)

---

**Feedback:** Was this article helpful? Let us know at [mippfeedback@microsoft.com](mailto:mippfeedback@microsoft.com)

**Last updated:** February 2026
