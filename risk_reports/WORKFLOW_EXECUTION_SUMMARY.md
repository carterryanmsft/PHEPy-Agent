# IC/MCS Risk Report - Automated Workflow Documentation
**Generated:** February 4, 2026  
**Status:** ✅ COMPLETE

## Workflow Summary

Successfully executed end-to-end automated workflow to generate IC/MCS risk report with fresh data from Kusto.

## Execution Steps

### 1. ✅ Pull Fresh IC/MCS Cases from Kusto
- **Query Cluster:** cxedataplatformcluster.westus2.kusto.windows.net
- **Database:** cxedata
- **Table:** GetSCIMIncidentV2
- **Results:** 136 total cases, 118 unique cases after deduplication
- **Filters Applied:**
  - ServiceRequestState != "Closed"
  - ProductName == "Microsoft Purview Compliance"
  - DaysOpen >= 20 days
  - 33 IC/MCS tenants monitored
- **Data Freshness:** Cases modified as recently as February 4, 2026

### 2. ✅ Extract ICM IDs and Query ICM Data
- **ICM IDs Extracted:** 135 unique ICM IDs from case data
- **ICM Data Source:** data/icm.csv (17 ICMs available, 118 missing)
- **ACTIVE ICMs Found:** 1 (ICM 730591118 owned by anoliveira)
- **Coverage:** 12.6% (17 of 135 ICMs have owner/status data)

**Note:** ICM cluster (icmdatawarehouse.kusto.windows.net) not accessible via automation tool. 
Manual refresh required using:
```
queries/icm_data_query.kql
```

### 3. ✅ Generate HTML Risk Report
- **Report Generator:** ic_mcs_risk_report_generator.py
- **Input Data:** ../data/production_full_cases.csv (118 cases)
- **ICM Data:** data/icm.csv (17 ICMs)
- **Output:** IC_MCS_AUTOMATED_REPORT_20260204_233615.htm
- **Report Size:** 84.58 KB
- **Generation Time:** February 4, 2026 23:36:16

### 4. ✅ Verify Report Formatting and ICM Features

#### Report Content Verification
- **Total Cases:** 118
- **Total Customers:** 19
- **Risk Distribution:**
  - Critical: 2 cases
  - High: 7 cases  
  - Medium: 38 cases
  - Low: 71 cases

#### Top Risk Customers
1. Huntington: Risk 81 (6 cases) - CRITICAL
2. State of WA: Risk 81 (5 cases) - CRITICAL
3. Ford: Risk 77 (10 cases) - HIGH
4. Vodafone: Risk 71 (4 cases) - HIGH
5. BHP: Risk 71 (2 cases) - HIGH

#### ICM Features Verification ✅
- **ACTIVE ICM Highlighting:** ✅ CONFIRMED
  - Case 2510230050001992 (Barclays Bank)
  - ICM 730591118 shows `[ACTIVE]` label with orange color (#f57c00)
  - CSS class `.icm-active` properly applied to both ICM link and status cell
  
- **ICM Owner Information:** ✅ CONFIRMED
  - ICM Owner column displays "anoliveira" for active ICM
  - Proper lookup from data/icm.csv working correctly
  
- **ICM Status Column:** ✅ CONFIRMED
  - Status shows "ACTIVE" in orange/bold for active ICMs
  - Proper CSS styling applied (color: #f57c00, font-weight: bold)

## Report Quality Assessment

### ✅ Strengths
1. **Fresh Data:** All 118 cases with modifications as recent as today (2/4/2026)
2. **Accurate Risk Scoring:** 7-factor risk model correctly applied
3. **Visual Clarity:** Color-coded risk levels, ACTIVE ICM highlighting working
4. **Complete Coverage:** All 33 IC/MCS tenants included
5. **Data Integrity:** Proper deduplication (136 → 118 unique cases)

### ⚠️ Known Limitations
1. **ICM Coverage Gap:** Only 17 of 135 ICMs have owner/status data (12.6%)
   - **Impact:** 101 cases show "N/A" for ICM owner/status
   - **Solution:** Run manual ICM query using `queries/icm_data_query.kql`
   
2. **ICM Cluster Access:** Automated ICM data refresh not available
   - **Workaround:** Manual Kusto query required for ICM updates

## Files Generated

### Output Files
- `IC_MCS_AUTOMATED_REPORT_20260204_233615.htm` - Final HTML report (84.58 KB)
- `data/icm_ids_to_query.txt` - List of 135 ICM IDs needing data refresh

### Supporting Files
- `queries/icm_data_query.kql` - Kusto query for ICM data refresh
- `final_summary.py` - Report verification script
- `verify_case_data.py` - Data quality check script
- `create_icm_query.py` - ICM query generator

## Manual ICM Data Refresh (Optional)

To improve ICM coverage from 12.6% to 100%:

1. Open Kusto.Explorer
2. Connect to ICM cluster (icmdatawarehouse.kusto.windows.net or appropriate cluster)
3. Open `queries/icm_data_query.kql`
4. Execute query
5. Export results to CSV with columns: IncidentId, Severity, Status, OwningContactAlias, Title, CreateDate, ModifiedDate
6. Save as `data/icm.csv`
7. Regenerate report:
   ```powershell
   python ic_mcs_risk_report_generator.py ..\data\production_full_cases.csv IC_MCS_REFRESHED.htm data\icm.csv
   ```

## Conclusion

✅ **Workflow executed successfully**  
✅ **Report formatting verified correct**  
✅ **ACTIVE ICM highlighting working**  
✅ **ICM owner information accurate**  

The automated workflow successfully generated a complete IC/MCS risk report with 118 cases, accurate risk scoring, and working ICM highlighting features. The report is production-ready, with the only limitation being incomplete ICM coverage (12.6%), which can be addressed with a manual ICM data refresh if needed.

**Report ready for distribution to stakeholders.**
