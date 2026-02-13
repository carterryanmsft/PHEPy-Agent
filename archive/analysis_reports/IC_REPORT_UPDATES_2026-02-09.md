# IC Risk Report - Updates Completed (February 9, 2026)

## Issues Resolved

### 1. ✅ SCIM Escalation Management Cases Filtered Out
**Problem**: Cases with SCIM Escalation Management ICMs were not being filtered properly.

**Root Cause**: The Kusto query was checking ICM ownership but not filtering cases at the post-processing level.

**Solution**:
- Created ICM ownership lookup query (`risk_reports/queries/get_icm_owners.kql`)
- Executed query to get ownership data for all 85 ICMs
- Identified 4 SCIM ICMs: 693849812, 694041459, 694142803, 694208210
- Created `filter_scim_cases.py` to remove cases with SCIM ICMs
- **Result**: Removed 1 case (2510030040002408 - Huntington) that had SCIM ICMs

**Cases**: 73 → **72 cases** (1 SCIM case removed)

### 2. ✅ ICM Owners Now Populated
**Problem**: ICM Owner and ICM Status columns showed "N/A" for all cases.

**Root Cause**: HTML generator needs ICM ownership data passed as a separate CSV file.

**Solution**:
- Queried ICM cluster for ownership data (OwningContactAlias, Status, Severity)
- Saved to `risk_reports/data/icm_owners.csv`
- Updated report generator command to include ICM CSV: `python risk_reports/scripts/ic_mcs_risk_report_generator.py risk_reports/data/ic_cases.csv risk_reports/data/icm_owners.csv risk_reports/IC_Report_Final.htm`
- **Result**: ICM Owner and ICM Status now display correctly with active ICM prioritization

**ICM Coverage**: 54 of 72 cases have ICM data populated

### 3. ✅ Case ID Formatting Fixed (Previous Session)
**Problem**: Case numbers were splitting across multiple lines in HTML table cells.

**Solution**: Added `class="nowrap"` CSS to case number cells in HTML generator.

### 4. ✅ Age Risk Weighting Increased by 40% (Previous Session)
**Problem**: Risk scoring needed higher weighting for aged cases.

**Solution**: Updated `process_ic_filtered.py` to increase age points from 0-40 to 0-56 (40% increase).

---

## Files Modified

### Queries
- **risk_reports/queries/ic_only_risk_report.kql** - Updated to preserve RelatedICM_Id through mv-expand
- **risk_reports/queries/ic_mcs_risk_report.kql** - Same ICM preservation fix
- **risk_reports/queries/get_icm_owners.kql** - NEW: Query to extract ICM ownership data

### Python Scripts
- **process_ic_filtered.py** - Updated to accept command-line argument for result file
- **risk_reports/scripts/ic_mcs_risk_report_generator.py** - Added CSS `nowrap` class for case numbers

### New Utility Scripts
- **create_icm_owner_query.py** - Generates Kusto query for ICM ownership
- **analyze_icm_owners.py** - Analyzes ICM data and identifies SCIM escalations
- **filter_scim_cases.py** - Removes cases with SCIM ICMs from dataset
- **check_scim_cases.py** - Validates SCIM filtering
- **check_icm_data.py** - Diagnoses ICM data issues

### Data Files
- **risk_reports/data/ic_cases.csv** - Updated with 72 cases (SCIM filtered), includes ICM data
- **risk_reports/data/icm_owners.csv** - NEW: ICM ownership lookup data (85 ICMs)

### Reports
- **risk_reports/IC_Report_Final.htm** - Regenerated with all fixes applied

---

## Final Report Statistics

**Total Cases**: 72 (down from 73 after SCIM filtering)
**Total Customers**: 14

### Risk Distribution
- **Critical** (85+): 5 cases
- **High** (60-84): 19 cases
- **Medium** (40-59): 31 cases
- **Low** (<40): 17 cases

### Top 5 Highest Risk Customers
1. **State of WA** - Risk 95 (5 cases)
2. **BHP** - Risk 87 (2 cases)
3. **Vodafone** - Risk 87 (4 cases)
4. **Ford** - Risk 83 (10 cases)
5. **MUFJ** - Risk 83 (14 cases)

### ICM Data Coverage
- **Cases with ICM**: 54 of 72 (75%)
- **Cases without ICM**: 18 (25%)
- **ICM Owners Populated**: ✅ Active ICMs prioritized
- **ICM Status**: ✅ ACTIVE/RESOLVED shown

### SCIM Filtering
- **SCIM ICMs Identified**: 4 (693849812, 694041459, 694142803, 694208210)
- **Cases Filtered**: 1 (Huntington case 2510030040002408)
- **SCIM ICM Ownership**: 4 out of 85 total ICMs (4.7%)

---

## Verification Checklist

✅ Case numbers do not split across lines (nowrap CSS applied)
✅ ICM IDs display with clickable links to ICM portal
✅ ICM Owners populated from IcmDataWarehouse
✅ ICM Status shows ACTIVE/RESOLVED
✅ SCIM Escalation Management cases filtered out
✅ Age risk weighting at 40% increase (0-56 points)
✅ Risk scores recalculated with updated weights
✅ Report shows 72 cases (1 SCIM case removed)

---

## How to Regenerate Report

To regenerate the report with all fixes:

```powershell
# 1. Run the IC query (with SCIM filtering at Kusto level)
# Use MCP Kusto server with: risk_reports/queries/ic_only_risk_report.kql

# 2. Process query results
python process_ic_filtered.py "<path_to_kusto_result_file>"

# 3. Generate ICM owner query
python create_icm_owner_query.py

# 4. Run ICM query (with ICM cluster)
# Use MCP Kusto server with: risk_reports/queries/get_icm_owners.kql

# 5. Analyze ICM data and save to CSV
python analyze_icm_owners.py

# 6. Filter out SCIM cases
python filter_scim_cases.py

# 7. Generate HTML report with ICM data
python risk_reports/scripts/ic_mcs_risk_report_generator.py risk_reports/data/ic_cases.csv risk_reports/data/icm_owners.csv risk_reports/IC_Report_Final.htm
```

---

## Notes

- The Kusto query filtering logic preserves original ICM IDs through the mv-expand operation
- SCIM filtering happens at the post-processing level after ICM ownership data is retrieved
- ICM ownership data prioritizes ACTIVE ICMs when multiple ICMs exist for a case
- The report generator requires ICM CSV to be passed as the second argument for owner population

---

**Updated By**: GitHub Copilot  
**Date**: February 9, 2026  
**Report Location**: `risk_reports/IC_Report_Final.htm`
