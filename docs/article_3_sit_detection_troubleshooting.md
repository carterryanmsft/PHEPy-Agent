# Troubleshoot sensitive information type detection issues

**Applies to:**
- Microsoft Purview Data Loss Prevention
- Microsoft Purview Information Protection
- Microsoft 365 E3/E5/A3/A5/G3/G5
- Office 365 E3/E5/A3/A5/G3/G5

**Estimated reading time:** 18 minutes

This article helps you understand how sensitive information types (SITs) work and diagnose why content isn't being detected as expected. You'll learn about detection logic, confidence levels, pattern matching, and how to create custom SITs when built-in types don't meet your needs.

## Overview

Sensitive information types (SITs) are pattern-based classifiers that detect sensitive data like credit card numbers, social security numbers, and passport numbers. When SITs fail to detect content you expect them to catch—or detect content you don't expect—it's usually due to misunderstanding how the detection logic works.

> [!IMPORTANT]
> SIT detection is **not** artificial intelligence or machine learning (in most cases). It's deterministic pattern matching using:
> - Regular expressions (regex)
> - Keywords and keyword lists
> - Checksums and validation functions
> - Proximity requirements (corroborative evidence)
> - Confidence levels

## How sensitive information type detection works

### Detection architecture

```plaintext
                    ┌─────────────────────────────────────┐
                    │    Document Submitted for Scan      │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │  Content Extraction & Normalization  │
                    │  - Text extraction                   │
                    │  - Remove formatting                 │
                    │  - Normalize whitespace              │
                    │  - OCR for images (if enabled)       │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │    Primary Pattern Matching         │
                    │  - Regex pattern evaluation         │
                    │  - Checksum validation              │
                    │  - Format verification              │
                    └──────────────┬──────────────────────┘
                                   │
                           ┌───────┴────────┐
                           │                │
                    ┌──────▼─────┐   ┌─────▼──────┐
                    │   Match    │   │  No Match  │
                    │   Found    │   │            │
                    └──────┬─────┘   └─────┬──────┘
                           │                │
                           │                └─────> Document passes (no SIT detected)
                           │
                    ┌──────▼──────────────────────────────┐
                    │  Corroborative Evidence Check       │
                    │  - Proximity keyword search         │
                    │  - Context validation               │
                    │  - Additional pattern checks        │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │    Confidence Level Calculation     │
                    │  - Low confidence (65-74%)          │
                    │  - Medium confidence (75-84%)       │
                    │  - High confidence (85-100%)        │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │    Policy Action Triggered          │
                    │  (if confidence meets threshold)    │
                    └─────────────────────────────────────┘
```

### Key detection components

1. **Primary Pattern**: The main regex or pattern that identifies potential matches
2. **Checksum/Validation**: Mathematical validation (e.g., Luhn algorithm for credit cards)
3. **Corroborative Evidence**: Keywords within character proximity that increase confidence
4. **Confidence Level**: Calculated score based on pattern match + evidence
5. **Instance Count**: Number of distinct matches required to trigger policy

## Understanding confidence levels

### How confidence is calculated

| Match Criteria | Confidence Level |
|----------------|------------------|
| Pattern match only | 65% (Low) |
| Pattern + checksum valid | 75% (Medium) |
| Pattern + checksum + 1 keyword nearby | 85% (High) |
| Pattern + checksum + multiple keywords nearby | 95% (High) |

**Example: Credit Card Detection**

```plaintext
Content: "Card number 4532-1234-5678-9010 expires 12/25"

Step 1: Pattern Match
- Regex: \d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}
- Matches: "4532-1234-5678-9010"
- Confidence: 65%

Step 2: Checksum Validation (Luhn Algorithm)
- Digits: 4532123456789010
- Luhn check: VALID ✅
- Confidence: 75%

Step 3: Proximity Keywords (300 characters)
- Found: "Card number", "expires"
- Keyword matches: 2
- Confidence: 95% ✅

Result: HIGH CONFIDENCE DETECTION
```

### Configuring confidence in policies

When creating DLP or auto-labeling policies:

```powershell
# DLP policy rule with confidence level
New-DlpComplianceRule -Name "Block Credit Cards" `
    -Policy "Financial Data Protection" `
    -ContentContainsSensitiveInformation @(
        @{
            Name="Credit Card Number"
            MinCount=1
            MinConfidence=85  # Only trigger on high confidence
        }
    ) `
    -BlockAccess $true
```

**Confidence level recommendations:**

| Use Case | Recommended Confidence | Rationale |
|----------|----------------------|-----------|
| Email blocking (user-facing) | High (85%) | Minimize false positives that disrupt users |
| Audit/monitoring | Low (65%) | Catch all potential matches for review |
| Auto-labeling | Medium (75%) | Balance between coverage and accuracy |
| Financial regulatory compliance | High (85-95%) | Ensure accuracy for legal/audit purposes |
| Internal policy monitoring | Medium (75%) | Broader detection for internal governance |

---

## Built-in SIT examples and patterns

### Credit Card Number detection

**SIT Name**: `Credit Card Number`  
**SIT GUID**: `50842eb7-edc8-4019-85dd-5a5c1f2bb085`

**Primary Pattern (Regex)**:
```regex
# Visa (starts with 4)
4[0-9]{12}(?:[0-9]{3})?

# Mastercard (starts with 51-55 or 2221-2720)
(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}

# American Express (starts with 34 or 37)
3[47][0-9]{13}

# Discover (starts with 6011, 622126-622925, 644-649, 65)
6(?:011|5[0-9]{2})[0-9]{12}

# Combined pattern with optional separators
(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})(?:[-\s])?
```

**Checksum Validation**: Luhn Algorithm (Mod 10)

**Proximity Keywords** (within 300 characters):
```plaintext
credit card, card#, card num, card number, cc#, cc no, acct nbr, 
account number, american express, amex, card holder, cardholder, 
card holders, creditcard, credit cards, expiry date, exp date, expiration
```

**Testing credit card detection**:

```powershell
# Test content
$testContent = @"
Customer payment details:
Card Number: 4532-1234-5678-9010
Expiration: 12/25
CVV: 123
"@

# Save to test file
Set-Content -Path "C:\Temp\test_creditcard.txt" -Value $testContent

# Upload to SharePoint and check DLP evaluation
# (Manual verification in DLP reports after ~24 hours)
```

**Why credit cards might not be detected:**
- ❌ Invalid checksum (e.g., random 16 digits)
- ❌ Missing proximity keywords for high confidence
- ❌ Too much whitespace between digits (>1 space)
- ❌ Numbers split across lines or pages
- ❌ Embedded in images without OCR enabled

---

### U.S. Social Security Number (SSN) detection

**SIT Name**: `U.S. Social Security Number (SSN)`  
**SIT GUID**: `a44669fe-0d48-453d-a9b1-2cc83f2cba77`

**Primary Pattern (Regex)**:
```regex
# Format: ###-##-####
(?!000|666|9\d{2})([0-7]\d{2}|7([0-6]\d|7[012]))([-\s]?)(?!00)\d{2}\3(?!0000)\d{4}

# Breakdown:
# - First 3 digits: Not 000, 666, or 900-999
# - Middle 2 digits: Not 00
# - Last 4 digits: Not 0000
# - Separator: Optional hyphen or space (consistent)
```

**Valid SSN examples:**
```plaintext
✅ 123-45-6789
✅ 123 45 6789
✅ 123456789
❌ 000-12-3456 (invalid area number)
❌ 123-00-4567 (invalid group number)
❌ 123-45-0000 (invalid serial number)
❌ 666-12-3456 (reserved area number)
```

**Proximity Keywords** (within 300 characters):
```plaintext
SSN, social security, social security#, soc sec, 
social sec#, SSNS, SSN#, SS#, SSID
```

**Confidence levels for SSN**:
- **65% (Low)**: Pattern match only (e.g., `123456789` with no context)
- **75% (Medium)**: Pattern match + valid format
- **85% (High)**: Pattern match + proximity keywords like "SSN:" or "Social Security Number:"

---

### International Passport Number detection

**SIT Name**: `All Full Names`  
**SIT Name**: `EU Passport Number`  
**SIT Name**: `U.S./U.K./Germany/France Passport Number` (country-specific)

**Pattern varies by country:**

**U.S. Passport**:
```regex
# Format: 9 digits (newer format)
[0-9]{9}

# Format: 1 letter + 8 digits (older format)
[A-Z][0-9]{8}
```

**UK Passport**:
```regex
# Format: 9 digits
[0-9]{9}
```

**German Passport**:
```regex
# Format: C + 8 alphanumeric (e.g., C01X0006F)
C[0-9A-Z]{8}
```

**Proximity Keywords** (multi-language):
```plaintext
# English
passport, passport number, travel document, passport#, passport no

# German
reisepass, reisepassnummer, reisepass-nr, pass-nr

# French
passeport, numéro de passeport, passeport non

# Spanish
pasaporte, número de pasaporte, pasaporte no
```

**Challenge with passport detection**: 
Passport numbers are often just digits without special formatting or checksums, leading to **high false positive rates** unless:
- Strong proximity keywords are present
- Combined with country/region context
- Used with name + passport number combination

---

### Email Address detection

**SIT Name**: `Email Address`  
**SIT GUID**: `e1d4457b-00e7-4fc5-a9c7-65b1a6c2d0e0`

**Primary Pattern (Regex)**:
```regex
# Standard email format
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b

# More comprehensive pattern
(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])
```

**No checksum validation** (emails don't have checksums)

**No proximity keywords required** (email format is distinctive enough)

**Common false positives:**
- Programming code (e.g., `user@localhost`, `test@example.com`)
- XML namespaces (e.g., `xmlns:xsi="http://example.com"`)
- Documentation examples

**To reduce false positives:**
```powershell
# Create custom SIT with domain exclusions
New-DlpSensitiveInformationType -Name "Corporate Email Addresses" `
    -Description "Email addresses excluding test domains" `
    -Patterns @(
        @{
            Pattern = '\b[A-Za-z0-9._%+-]+@contoso\.com\b'
            Confidence = 85
        }
    ) `
    -NotPatterns @('test@', 'example@', 'demo@')
```

---

## Common SIT detection failures and solutions

### Issue 1: Credit cards not detected in PDFs

**Symptom**: DLP policy doesn't catch credit card numbers in scanned PDF documents

**Root cause**: PDF contains image of text (not searchable text)

**Solution**: Enable OCR (Optical Character Recognition)

#### Enable OCR for Microsoft Purview

OCR is automatically enabled for:
- ✅ SharePoint Online
- ✅ OneDrive for Business
- ✅ Exchange Online (email attachments)
- ✅ Teams (shared files)

**OCR supported file types:**
- Images: .jpg, .jpeg, .png, .bmp, .tiff, .gif
- PDFs: Image-based PDFs (scanned documents)

**OCR limitations:**
- **File size limit**: 20 MB
- **Image resolution**: Minimum 50 DPI, maximum 300 DPI (optimal: 150-200 DPI)
- **Performance**: OCR adds 2-5 seconds processing time per page
- **Accuracy**: 95%+ with clear text, lower with poor scans

#### Test OCR functionality

```powershell
# Create test image with credit card number
# (Use Paint or PowerShell to generate test image)

Add-Type -AssemblyName System.Drawing

$bitmap = New-Object System.Drawing.Bitmap(800, 200)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.Clear([System.Drawing.Color]::White)

$font = New-Object System.Drawing.Font("Arial", 24)
$brush = [System.Drawing.Brushes]::Black
$graphics.DrawString("Credit Card: 4532-1234-5678-9010", $font, $brush, 10, 80)

$bitmap.Save("C:\Temp\creditcard_image.png")
$graphics.Dispose()
$bitmap.Dispose()

Write-Host "Test image created: C:\Temp\creditcard_image.png"
Write-Host "Upload to SharePoint and wait 24 hours for DLP scan"
```

**Verify OCR is working:**
1. Upload image with sensitive data to SharePoint
2. Wait 24-48 hours for processing
3. Check DLP reports in compliance portal:
   ```plaintext
   https://compliance.microsoft.com/datalossprevention?viewid=reports
   ```
4. Search for the file in Activity Explorer

#### Improve OCR accuracy

| Factor | Recommendation |
|--------|----------------|
| **Image quality** | Use 150-200 DPI, avoid compression artifacts |
| **Text size** | Minimum 10pt font size in final image |
| **Contrast** | High contrast (black text on white background) |
| **Orientation** | Text should be horizontal (not rotated) |
| **Background** | Solid color, avoid patterns or watermarks |
| **File format** | PNG or TIFF for best quality, avoid heavily compressed JPG |

---

### Issue 2: SSN detected in employee IDs (false positives)

**Symptom**: DLP policy blocks documents with employee IDs that happen to match SSN pattern

**Root cause**: Employee ID format coincidentally matches SSN pattern

**Example false positive:**
```plaintext
Employee ID: 123-45-6789  (happens to be valid SSN format)
Badge Number: 234-56-7890  (also matches pattern)
```

**Solution 1: Use pattern exclusions**

```powershell
# Create custom SIT with exclusions
New-DlpSensitiveInformationType -Name "SSN Excluding Employee IDs" `
    -Description "Detects SSNs but excludes employee IDs" `
    -Patterns @(
        @{
            Pattern = '(?!000|666|9\d{2})([0-7]\d{2}|7([0-6]\d|7[012]))([-\s]?)(?!00)\d{2}\3(?!0000)\d{4}'
            Confidence = 75
        }
    ) `
    -NotPatterns @('Employee ID:', 'Badge:', 'EMP#', 'Worker ID')

# Create policy rule using custom SIT
New-DlpComplianceRule -Name "Block Real SSNs Only" `
    -Policy "Personal Data Protection" `
    -ContentContainsSensitiveInformation @(
        @{
            Name="SSN Excluding Employee IDs"
            MinCount=1
            MinConfidence=75
        }
    )
```

**Solution 2: Adjust confidence requirements**

```powershell
# Require higher confidence (needs proximity keywords)
Set-DlpComplianceRule -Identity "Block SSN" `
    -ContentContainsSensitiveInformation @(
        @{
            Name="U.S. Social Security Number (SSN)"
            MinCount=1
            MinConfidence=85  # High confidence requires keywords
        }
    )
```

**Solution 3: Create allow override with business justification**

```powershell
# Allow user override with justification
Set-DlpComplianceRule -Identity "Block SSN" `
    -NotifyUser Owner `
    -NotifyUserType NotSet `
    -UserNotificationTitle "Potential SSN Detected" `
    -UserNotificationText "If this is an employee ID, provide justification to override." `
    -AllowUserOverride $true `
    -UserOverrideRequiresJustification $true
```

---

### Issue 3: Multi-line or formatted content not detected

**Symptom**: Sensitive data split across lines or with unusual formatting not detected

**Example problems:**
```plaintext
❌ Credit card split across lines:
Card Number: 4532-1234
-5678-9010

❌ Excessive whitespace:
SSN: 123    45    6789

❌ Mixed separators:
Card: 4532.1234-5678 9010

❌ Tables with cells:
| Field | Value |
| Card  | 4532  |
| -     | 1234  |
| -     | 5678  |
| -     | 9010  |
```

**Solution 1: Content normalization (automatic in Microsoft Purview)**

Microsoft Purview automatically normalizes:
- Extra whitespace → single space
- Newlines within patterns → removed
- Mixed separators → standardized

But this has limits: very complex formatting may still break detection.

**Solution 2: Create custom SIT with flexible patterns**

```powershell
# Custom SIT with more flexible separators
$flexibleCreditCard = @{
    Name = "Credit Card Flexible Format"
    Description = "Detects credit cards with various formatting"
    Patterns = @(
        @{
            # Allow any separator or whitespace
            Pattern = '(?:4[0-9]{3}|5[1-5][0-9]{2}|3[47][0-9]{2}|6(?:011|5[0-9]{2}))[\s\.\-_]*[0-9]{4}[\s\.\-_]*[0-9]{4}[\s\.\-_]*[0-9]{4}'
            Confidence = 75
        }
    )
}

New-DlpSensitiveInformationType @flexibleCreditCard
```

**Solution 3: Use document fingerprinting**

For highly structured documents (forms, templates):

```powershell
# Create document fingerprint from template
$templateFile = "C:\Temp\CreditCardForm_Template.docx"
$fingerprint = New-DlpFingerprint -FileData ([System.IO.File]::ReadAllBytes($templateFile)) `
    -Description "Credit card application form template"

# Create SIT based on document structure
New-DlpSensitiveInformationType -Name "Credit Card Application Form" `
    -Fingerprints $fingerprint `
    -Description "Detects credit card application forms by structure"
```

---

### Issue 4: International data formats not detected

**Symptom**: UK phone numbers, Canadian SINs, or other non-US formats not detected by policies

**Root cause**: DLP policy using U.S.-specific SITs only

**Solution: Use international SIT variants**

Microsoft provides 200+ SITs for different countries:

| Data Type | Countries Supported |
|-----------|---------------------|
| Credit cards | Universal (Visa, MC, Amex, etc.) |
| National IDs | 50+ countries |
| Passport numbers | 40+ countries |
| Tax IDs | 30+ countries |
| Bank accounts | 25+ countries |
| Driver licenses | 20+ countries |

**Find international SITs:**

```powershell
# List all available SITs
Connect-IPPSSession
Get-DlpSensitiveInformationType | 
    Select-Object Name, Publisher, Description |
    Where-Object {$_.Name -like "*canada*" -or $_.Name -like "*UK*"} |
    Format-Table -AutoSize

# Example output:
# Name: Canada Social Insurance Number
# Name: U.K. National Insurance Number (NINO)
# Name: Canada Passport Number
# Name: Canada Bank Account Number
```

**Create multi-region policy:**

```powershell
# DLP policy covering multiple countries
New-DlpComplianceRule -Name "Global PII Protection" `
    -Policy "International Data Protection" `
    -ContentContainsSensitiveInformation @(
        @{Name="U.S. Social Security Number (SSN)"; MinCount=1},
        @{Name="Canada Social Insurance Number"; MinCount=1},
        @{Name="U.K. National Insurance Number (NINO)"; MinCount=1},
        @{Name="Germany Identity Card Number"; MinCount=1},
        @{Name="France National ID Card (CNI)"; MinCount=1}
    )
```

---

### Issue 5: Custom data patterns not recognized

**Symptom**: Organization-specific identifiers (project codes, customer IDs, internal account numbers) not detected

**Root cause**: No built-in SIT for custom organization patterns

**Solution: Create custom sensitive information types**

#### Example: Custom project code format

**Business requirement**: Detect project codes in format `PROJ-YYYY-####`
- PROJ (literal text)
- YYYY (year: 2020-2030)
- #### (4 digits: 0001-9999)

**Example codes**: `PROJ-2024-0001`, `PROJ-2025-1234`

#### Step-by-step custom SIT creation

**Method 1: Using Purview Compliance Portal (recommended for simple patterns)**

1. Navigate to **Microsoft Purview compliance portal** > **Data classification** > **Classifiers** > **Sensitive info types**

2. Click **Create sensitive info type**

3. Configure:
   ```plaintext
   Name: Internal Project Code
   Description: Detects company project codes in format PROJ-YYYY-####
   ```

4. Add pattern:
   ```plaintext
   Primary element: Regular expression
   
   Pattern: PROJ-(202[0-9]|203[0-9])-[0-9]{4}\b
   
   Confidence level: Medium (75%)
   
   Character proximity: 300 characters
   
   Supporting element: Keyword list (optional)
   Keywords: project, project code, project#, project number
   ```

5. Test the pattern:
   ```plaintext
   Test string: "Working on PROJ-2024-0123 for Q1 deliverables"
   Expected: Match ✅
   
   Test string: "PROJ-2019-9999"
   Expected: No match (year out of range)
   ```

6. Click **Create**

**Method 2: Using PowerShell (recommended for complex patterns)**

```powershell
# Connect to Security & Compliance PowerShell
Connect-IPPSSession

# Define the custom SIT
$sitParams = @{
    Name = "Internal Project Code"
    Description = "Detects project codes in format PROJ-YYYY-####"
    Locale = "en-US"
}

# Create the SIT
New-DlpSensitiveInformationType @sitParams

# Add pattern to the SIT
$patternParams = @{
    Identity = "Internal Project Code"
    Patterns = @(
        @{
            Pattern = 'PROJ-(202[0-9]|203[0-9])-[0-9]{4}\b'
            Confidence = 75
        }
    )
    ProximityKeywords = @{
        Keywords = @("project", "project code", "proj#")
        ProximityInCharacters = 300
    }
}

Set-DlpSensitiveInformationType @patternParams

# Verify creation
Get-DlpSensitiveInformationType -Identity "Internal Project Code" | Format-List
```

#### Advanced: Multiple patterns with different confidence levels

```powershell
# Custom SIT with multiple patterns
$patterns = @(
    # High confidence: Pattern + keywords
    @{
        Pattern = 'PROJ-(202[0-9]|203[0-9])-[0-9]{4}\b'
        ProximityKeywords = @{
            Keywords = @("project", "project code")
            ProximityInCharacters = 100
        }
        Confidence = 95
    },
    # Medium confidence: Pattern only with strict proximity
    @{
        Pattern = 'PROJ-(202[0-9]|203[0-9])-[0-9]{4}\b'
        Confidence = 75
    },
    # Low confidence: More flexible year range
    @{
        Pattern = 'PROJ-[0-9]{4}-[0-9]{4}\b'
        Confidence = 65
    }
)

New-DlpSensitiveInformationType -Name "Internal Project Code Advanced" `
    -Description "Multi-confidence project code detection" `
    -Patterns $patterns
```

#### Complex example: Customer account number with checksum

```powershell
<#
    Custom SIT with validation function
    Format: CUST-XXXXXXX (7 digits with Luhn checksum)
#>

# Note: Custom validation functions require on-premises DLP or Azure Information Protection scanner
# For cloud-only, use regex to approximate validation

$accountNumberSIT = @{
    Name = "Customer Account Number"
    Description = "7-digit account number with CUST prefix"
    Patterns = @(
        @{
            # Pattern matches CUST-#######
            Pattern = 'CUST-[0-9]{7}\b'
            Confidence = 75
            ProximityKeywords = @{
                Keywords = @("account", "account number", "acct#", "customer")
                ProximityInCharacters = 300
            }
        }
    )
}

New-DlpSensitiveInformationType @accountNumberSIT

# To add actual Luhn validation, would need custom scanner implementation
```

---

## Testing and validating SIT detection

### Test harness: Create sample documents

```powershell
<#
.SYNOPSIS
    Creates test documents with various sensitive information patterns
    
.DESCRIPTION
    Generates test files to validate SIT detection in DLP policies
#>

$testCases = @{
    "CreditCard_HighConfidence.txt" = @"
Customer Payment Information
Card Number: 4532-1234-5678-9010
Expiration Date: 12/25
Cardholder: John Smith
"@
    
    "CreditCard_LowConfidence.txt" = @"
Product SKU: 4532-1234-5678-9010
Serial Number: ABC123
"@
    
    "SSN_HighConfidence.txt" = @"
Employee Personal Data
Social Security Number: 123-45-6789
Date of Birth: 01/01/1980
"@
    
    "SSN_FalsePositive.txt" = @"
Employee Information
Employee ID: 123-45-6789
Badge Number: EMP001
"@
    
    "CustomProjectCode.txt" = @"
Project Details
Project Code: PROJ-2024-0123
Budget: $50,000
"@
    
    "Email_Detection.txt" = @"
Contact Information
Email: john.smith@contoso.com
Phone: 555-1234
"@
}

# Create test directory
$testDir = "C:\Temp\SIT_Tests"
New-Item -Path $testDir -ItemType Directory -Force | Out-Null

# Generate test files
foreach ($fileName in $testCases.Keys) {
    $filePath = Join-Path $testDir $fileName
    Set-Content -Path $filePath -Value $testCases[$fileName]
    Write-Host "Created: $filePath" -ForegroundColor Green
}

Write-Host "`nTest files created in: $testDir" -ForegroundColor Cyan
Write-Host "Upload these to SharePoint to test DLP detection`n" -ForegroundColor Yellow
```

### Monitor detection results

```powershell
# Query DLP incidents for test files
Connect-IPPSSession

# Get recent DLP detections
$startDate = (Get-Date).AddDays(-7)
$incidents = Get-DlpIncidentDetail -StartDate $startDate

# Filter for our test files
$testResults = $incidents | Where-Object {
    $_.FileName -like "*SIT_Tests*"
} | Select-Object FileName, SensitiveInformationType, Confidence, DetectionTime

$testResults | Format-Table -AutoSize

# Export for analysis
$testResults | Export-Csv -Path "C:\Temp\SIT_Detection_Results.csv" -NoTypeInformation
```

### Use Activity Explorer for validation

1. Navigate to **Microsoft Purview compliance portal** > **Reports** > **Activity explorer**

2. Filter by:
   ```plaintext
   Activity: SensitivityLabelApplied, DLP policy matched
   Date range: Last 7 days
   File name: (your test files)
   ```

3. Review:
   - Which SITs were detected
   - Confidence levels
   - Match counts
   - Policy actions taken

4. Adjust policies based on results

---

## Alternative: Trainable classifiers for complex scenarios

When pattern-based SITs are insufficient, use trainable classifiers (machine learning).

### When to use trainable classifiers

| Scenario | Use Trainable Classifier? |
|----------|--------------------------|
| Detecting credit card numbers | ❌ No - Use SIT (deterministic) |
| Detecting financial contracts | ✅ Yes - Requires context understanding |
| Detecting source code | ✅ Yes - Complex patterns |
| Detecting resumes | ✅ Yes - Varied formats |
| Detecting offensive language | ✅ Yes - Context-dependent |
| Detecting medical records | ✅ Yes - Requires understanding of medical context |

### Pre-built trainable classifiers

Microsoft provides:
- Source code
- Resumes
- Financial documents
- Legal documents
- Medical records
- Offensive language
- Threat/violence language

```powershell
# List available classifiers
Get-DlpSensitiveInformationType | 
    Where-Object {$_.ClassifierType -eq "Trainable"} |
    Select-Object Name, Description
```

### Create custom trainable classifier

**Requirements:**
- Minimum 50 positive examples (seed documents)
- Minimum 500 additional documents for training
- Microsoft 365 E5 or Compliance add-on license

**Steps:**

1. **Prepare training data**:
   - Collect 50+ examples of documents YOU WANT to detect (positive examples)
   - Collect 50+ examples of documents YOU DON'T WANT to detect (negative examples)
   - More examples = better accuracy (recommended: 200-500 each)

2. **Create classifier in Purview portal**:
   ```plaintext
   Navigate to: Data classification > Trainable classifiers > Create trainable classifier
   
   Name: Financial Contracts
   Description: Detects financial service agreements and contracts
   
   Upload seed content: (50+ positive examples)
   ```

3. **Train the model**:
   - Initial training: 7-14 days
   - Review model predictions on test set
   - Provide feedback (correct/incorrect)
   - Re-train as needed

4. **Publish and use in policies**:
   ```powershell
   # After classifier is trained and published
   New-DlpComplianceRule -Name "Protect Financial Contracts" `
       -Policy "Contract Protection" `
       -ContentContainsClassifier @{
           Name="Financial Contracts"
           MinConfidence=75
       }
   ```

**Performance expectations:**
- **Accuracy**: 85-95% with good training data
- **Processing time**: 2-5 seconds per document
- **False positive rate**: 5-15% (varies by classifier quality)

**Best practices:**
- Start with high-quality, representative examples
- Include edge cases in training data
- Regularly review false positives and retrain
- Combine classifiers with SITs for best accuracy

---

## Troubleshooting workflow decision tree

```plaintext
Is the sensitive data being detected at all?
│
├─[NO]─> What type of data?
│        │
│        ├─[Standard types like credit cards, SSN]
│        │  │
│        │  ├─> Is the format correct?
│        │  │   ├─[NO]─> Fix format or create flexible custom SIT
│        │  │   │        (see Issue 3)
│        │  │   └─[YES]
│        │  │        │
│        │  │        ├─> Are proximity keywords present?
│        │  │        │   ├─[NO]─> Lower confidence threshold
│        │  │        │   │        OR add keywords to content
│        │  │        │   └─[YES]
│        │  │        │        │
│        │  │        │        └─> Is data in image/PDF?
│        │  │        │            ├─[YES]─> Enable OCR (Issue 1)
│        │  │        │            └─[NO]─> Check policy configuration
│        │  │
│        │  └─> Is checksum valid?
│        │      ├─[NO]─> Not a real credit card number
│        │      │        (consider if test data is valid)
│        │      └─[YES]─> Check OCR, formatting
│        │
│        └─[Custom organization data]
│           │
│           └─> Does a built-in SIT exist?
│               ├─[NO]─> Create custom SIT (Issue 5)
│               └─[YES]─> Check pattern matches
│
├─[YES, but too many false positives]
│   │
│   ├─> Increase confidence threshold (High = 85%+)
│   ├─> Add pattern exclusions (Issue 2)
│   ├─> Use more specific proximity keywords
│   └─> Consider combining multiple SITs with AND logic
│
└─[YES, but missing some instances]
    │
    ├─> Lower confidence threshold (Low = 65%+)
    ├─> Add more flexible patterns (Issue 3)
    ├─> Check international variants (Issue 4)
    └─> Consider trainable classifier for complex cases
```

---

## PowerShell diagnostic script

```powershell
<#
.SYNOPSIS
    Comprehensive SIT detection diagnostic tool
    
.DESCRIPTION
    Tests SIT detection against sample content and diagnoses configuration issues
    
.PARAMETER TestContent
    Content to test for SIT detection
    
.PARAMETER SITName
    Name of the sensitive information type to test
    
.EXAMPLE
    .\Test-SITDetection.ps1 -TestContent "Card: 4532-1234-5678-9010" -SITName "Credit Card Number"
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$TestContent,
    
    [Parameter(Mandatory=$false)]
    [string]$SITName
)

# Connect to compliance center
Write-Host "Connecting to Security & Compliance PowerShell..." -ForegroundColor Yellow
try {
    Connect-IPPSSession -ErrorAction Stop
    Write-Host "✅ Connected successfully`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Connection failed: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# List all available SITs
Write-Host "Available Sensitive Information Types:" -ForegroundColor Cyan
$allSITs = Get-DlpSensitiveInformationType | 
    Select-Object Name, Publisher, @{Name="Type";Expression={if($_.ClassifierType){"Classifier"}else{"Pattern-Based"}}}

$allSITs | Format-Table -AutoSize | Out-String | Write-Host

# If specific SIT specified, show details
if ($SITName) {
    Write-Host "`n=== Details for: $SITName ===" -ForegroundColor Cyan
    
    $sit = Get-DlpSensitiveInformationType -Identity $SITName
    
    if ($sit) {
        Write-Host "Name: $($sit.Name)"
        Write-Host "Publisher: $($sit.Publisher)"
        Write-Host "Description: $($sit.Description)"
        Write-Host "Recommended Confidence: $($sit.RecommendedConfidence)"
        
        # Show patterns if available
        if ($sit.Patterns) {
            Write-Host "`nPatterns:" -ForegroundColor Yellow
            foreach ($pattern in $sit.Patterns) {
                Write-Host "  Pattern: $($pattern.Value)"
                Write-Host "  Confidence: $($pattern.Confidence)%"
            }
        }
        
        # Test against content if provided
        if ($TestContent) {
            Write-Host "`n=== Testing Detection ===" -ForegroundColor Cyan
            Write-Host "Test content: $TestContent`n"
            
            # Create test file
            $testFile = "C:\Temp\SIT_Test_$(Get-Date -Format 'HHmmss').txt"
            Set-Content -Path $testFile -Value $TestContent
            
            Write-Host "Test file created: $testFile" -ForegroundColor Yellow
            Write-Host "Next steps:" -ForegroundColor Yellow
            Write-Host "1. Upload this file to SharePoint/OneDrive"
            Write-Host "2. Wait 24-48 hours for DLP scan"
            Write-Host "3. Check Activity Explorer for results"
            Write-Host "4. Review DLP incidents (if policy exists)`n"
            
            # Show how to create test policy
            Write-Host "Create test DLP policy:" -ForegroundColor Cyan
            Write-Host "New-DlpCompliancePolicy -Name 'SIT Test Policy' -SharePointLocation All -Mode TestWithoutNotifications" -ForegroundColor Gray
            Write-Host "New-DlpComplianceRule -Name 'Detect $SITName' -Policy 'SIT Test Policy' -ContentContainsSensitiveInformation @(@{Name='$SITName';MinCount=1;MinConfidence=65})" -ForegroundColor Gray
        }
        
    } else {
        Write-Host "❌ SIT not found: $SITName" -ForegroundColor Red
    }
}

# Show DLP policies using SITs
Write-Host "`n=== Active DLP Policies ===" -ForegroundColor Cyan
$policies = Get-DlpCompliancePolicy | Where-Object {$_.Enabled -eq $true}

foreach ($policy in $policies) {
    Write-Host "`nPolicy: $($policy.Name)" -ForegroundColor Yellow
    Write-Host "  Mode: $($policy.Mode)"
    Write-Host "  Locations: $($policy.SharePointLocation -join ', ')"
    
    $rules = Get-DlpComplianceRule -Policy $policy.Name
    foreach ($rule in $rules) {
        if ($rule.ContentContainsSensitiveInformation) {
            Write-Host "  Rule: $($rule.Name)"
            foreach ($sit in $rule.ContentContainsSensitiveInformation) {
                Write-Host "    - $($sit.Name) (MinCount: $($sit.MinCount), MinConfidence: $($sit.MinConfidence)%)"
            }
        }
    }
}

# Check  recent DLP detections
Write-Host "`n=== Recent DLP Detections (Last 7 Days) ===" -ForegroundColor Cyan
try {
    $startDate = (Get-Date).AddDays(-7)
    $detections = Search-UnifiedAuditLog -StartDate $startDate -EndDate (Get-Date) `
        -Operations "DlpRuleMatch" `
        -ResultSize 100

    if ($detections) {
        $summary = $detections | ForEach-Object {
            $data = $_.AuditData | ConvertFrom-Json
            [PSCustomObject]@{
                Time = $_.CreationDate
                File = $data.ObjectId
                SIT = $data.SensitiveInfoTypeData.Name
                Confidence = $data.SensitiveInfoTypeData.Confidence
            }
        } | Group-Object SIT | Select-Object Count, Name

        $summary | Format-Table -AutoSize
    } else {
        Write-Host "No recent detections found" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Unable to query audit logs: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n=== Diagnostic Complete ===" -ForegroundColor Cyan
```

**Usage examples:**

```powershell
# List all SITs
.\Test-SITDetection.ps1

# Get details for specific SIT
.\Test-SITDetection.ps1 -SITName "Credit Card Number"

# Test detection with sample content
.\Test-SITDetection.ps1 -TestContent "SSN: 123-45-6789" -SITName "U.S. Social Security Number (SSN)"
```

---

## Update instructions for existing articles

### Article: [Sensitive information type entity definitions](https://learn.microsoft.com/purview/sensitive-information-type-entity-definitions)

**Section:** Top of article (after intro paragraph)
**Add callout:**

```markdown
> [!TIP]
> Having trouble with SIT detection? See [Troubleshoot sensitive information type detection issues](link-to-new-article) for:
> - Understanding how confidence levels work
> - Resolving common detection failures
> - Creating custom SITs for organization-specific data
> - Testing and validating detection accuracy
```

### Article: [Create a custom sensitive information type](https://learn.microsoft.com/purview/create-a-custom-sensitive-information-type)

**Section:** "Before you begin"
**Add paragraph:**

```markdown
Before creating a custom SIT, review common troubleshooting scenarios in [Troubleshoot sensitive information type detection issues](link-to-new-article#issue-5-custom-data-patterns-not-recognized). You may find that adjusting confidence levels or proximity keywords on built-in SITs resolves your needs without creating custom types.
```

### Article: [Learn about data loss prevention](https://learn.microsoft.com/purview/dlp-learn-about-dlp)

**Section:** "Sensitive information types"
**Add subsection:**

```markdown
#### Troubleshooting SIT detection

If your DLP policies aren't detecting sensitive content as expected:

1. **Verify the data format**: SITs use regex patterns that may not match all formatting variations
2. **Check confidence levels**: Policies may require high confidence (85%+) which needs proximity keywords
3. **Test with known samples**: Create test files with known sensitive data and verify detection
4. **Review OCR requirements**: Image-based content requires OCR enablement

For comprehensive troubleshooting, see [Troubleshoot sensitive information type detection issues](link-to-new-article).
```

---

## SEO keywords and search optimization

**Primary keywords:**
- sensitive information type not working
- sit not detecting
- dlp not detecting credit cards
- sensitive information type troubleshooting
- custom sensitive information type
- sit detection issues
- why isn't dlp detecting

**Long-tail keywords:**
- credit card number not being detected by dlp
- how to test sensitive information type detection
- create custom sensitive information type regex
- dlp policy not catching ssn
- sensitivity information types confidence levels
- troubleshoot sit detection in purview
- enable ocr for dlp scanning

**Question-based keywords:**
- why is dlp not detecting credit cards
- how do sensitive information types work
- what is sit confidence level
- how to create custom sit for organization
- why does dlp have false positives
- how to improve sit detection accuracy

**Technical keywords:**
- sit regex patterns
- proximity keywords
- checksum validation
- luhn algorithm credit cards
- ocr enabled dlp
- trainable classifier vs sit
- dlp confidence threshold

---

## Performance benchmarks

### SIT detection processing times

| Content Type | File Size | Processing Time | SIT Count |
|--------------|-----------|----------------|-----------|
| Plain text file | 10 KB | <1 second | 1-5 SITs |
| Office document | 100 KB | 1-2 seconds | 1-10 SITs |
| PDF (text) | 500 KB | 2-3 seconds | 1-10 SITs |
| PDF (image/OCR) | 500 KB | 5-10 seconds | 1-5 SITs |
| Large document | 5 MB | 10-15 seconds | 1-20 SITs |
| Email with attachments | Variable | 2-20 seconds | 1-20 SITs |

### Scale considerations

| Metric | Limit | Notes |
|--------|-------|-------|
| SITs per policy | 500 | Recommended: <50 for performance |
| Custom SITs per tenant | 500 | No practical limit, but management overhead |
| Regex complexity | N/A | Complex patterns slow processing |
| Proximity keyword distance | 300 characters (default) | Increasing decreases accuracy |
| Document size for DLP | 30 MB | Larger files time out |
| OCR image resolution | 50-300 DPI | Higher = slower but more accurate |

---

## See also

- [Sensitive information type entity definitions](https://learn.microsoft.com/purview/sensitive-information-type-entity-definitions)
- [Create a custom sensitive information type](https://learn.microsoft.com/purview/create-a-custom-sensitive-information-type)
- [Credit card number entity definition](https://learn.microsoft.com/purview/sit-defn-credit-card-number)
- [Learn about trainable classifiers](https://learn.microsoft.com/purview/classifier-learn-about)
- [Get started with trainable classifiers](https://learn.microsoft.com/purview/classifier-get-started-with)
- [Learn about exact data match based sensitive information types](https://learn.microsoft.com/purview/sit-learn-about-exact-data-match-based-sits)
- [Learn about document fingerprinting](https://learn.microsoft.com/purview/document-fingerprinting)
- [Test a data loss prevention policy](https://learn.microsoft.com/purview/dlp-test-dlp-policies)
- [Use data loss prevention policies for non-Microsoft cloud apps](https://learn.microsoft.com/purview/dlp-use-policies-non-microsoft-cloud-apps)
- [Activity explorer](https://learn.microsoft.com/purview/data-classification-activity-explorer)
- [Apply a sensitivity label to content automatically](https://learn.microsoft.com/purview/apply-sensitivity-label-automatically)
- [Troubleshoot sensitivity label visibility issues](./article_1_label_visibility_troubleshooting.md)
- [Label existing files with auto-labeling policies](./article_2_autolabel_existing_files.md)

---

**Feedback:** Was this article helpful? Let us know at [dlpfeedback@microsoft.com](mailto:dlpfeedback@microsoft.com)

**Last updated:** February 2026
