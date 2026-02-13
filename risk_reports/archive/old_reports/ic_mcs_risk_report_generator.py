# IC/MCS Risk Report Generator
# Takes Kusto query results and generates HTML report organized by customer
# Author: Jacques (Kusto Expert)
# Date: February 4, 2026

import pandas as pd
from datetime import datetime
import sys
import json
import os

def generate_risk_report_html(kusto_results_input, icm_results_csv=None, output_html="IC_MCS_Risk_Report.htm"):
    """
    Generate HTML risk report from Kusto query results
    Organized by customer (highest risk first)
    
    Args:
        kusto_results_input: CSV or JSON file with support case data
        icm_results_csv: Optional CSV file with ICM incident data to join
        output_html: Output HTML file path
    """
    
    # Auto-detect input format (CSV or JSON) and read accordingly
    if kusto_results_input.endswith('.json'):
        # Read JSON format (from Kusto MCP tool)
        with open(kusto_results_input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data.get('data', data))  # Handle both wrapped and unwrapped JSON
        print(f"✓ Loaded JSON with {len(df)} cases")
    else:
        # Read CSV format (default)
        df = pd.read_csv(kusto_results_input)
    
    # Deduplicate cases by ServiceRequestNumber (keep first occurrence)
    # This handles cases that appear multiple times due to different DerivedProductName values
    original_count = len(df)
    df = df.drop_duplicates(subset='ServiceRequestNumber', keep='first')
    if original_count > len(df):
        print(f"✓ Removed {original_count - len(df)} duplicate cases")
    
    # If ICM data provided, join it
    has_icm_data = False
    icm_dict = {}
    bug_dict = {}  # Initialize bug_dict in outer scope
    if icm_results_csv:
        try:
            icm_df = pd.read_csv(icm_results_csv)
            # Replace empty strings with NaN for proper handling
            icm_df['IcmOwner'] = icm_df['IcmOwner'].replace('', pd.NA)
            
            # Build ICM lookup dictionary for multi-ICM cases
            icm_dict = icm_df.set_index('IncidentId')[['IcmOwner', 'IcmSeverity', 'IcmStatus']].to_dict('index')
            
            # Load bug data if available
            try:
                # Try relative path from risk_reports folder
                bug_path = 'data/icm_bugs.csv'
                if not os.path.exists(bug_path):
                    # Try absolute path from parent directory
                    bug_path = '../data/icm_bugs.csv'
                bugs_df = pd.read_csv(bug_path)
                for _, bug in bugs_df.iterrows():
                    icm_id = str(bug['IncidentId'])
                    if icm_id not in bug_dict:
                        bug_dict[icm_id] = []
                    bug_dict[icm_id].append({
                        'BugId': bug['BugId'],
                        'Status': bug['Status'],
                        'AdoLink': bug['AdoLink']
                    })
                print(f"✓ Loaded {len(bugs_df)} bugs for {len(bug_dict)} ICMs")
            except FileNotFoundError:
                print("No bug data found")
            
            # Function to look up ICM data (handles multiple ICM IDs - comma or semicolon separated)
            # Prioritizes ACTIVE ICMs for owner/status display
            def get_icm_data(icm_ids_str, field):
                if pd.isna(icm_ids_str) or not str(icm_ids_str).strip():
                    return None
                # Split by both comma and semicolon to handle different formats
                icm_ids_str = str(icm_ids_str).replace(',', ';')
                icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
                if icm_ids:
                    # First, look for an ACTIVE ICM with data
                    for icm_id_str in icm_ids:
                        try:
                            icm_id = int(icm_id_str)
                            if icm_id in icm_dict:
                                if icm_dict[icm_id].get('IcmStatus') == 'ACTIVE':
                                    value = icm_dict[icm_id].get(field)
                                    # Return if value exists and is not NaN
                                    if pd.notna(value) and str(value).strip():
                                        return value
                        except (ValueError, KeyError):
                            pass
                    # If no ACTIVE with data, return first available that exists in the dict
                    for icm_id_str in icm_ids:
                        try:
                            icm_id = int(icm_id_str)
                            if icm_id in icm_dict:
                                value = icm_dict[icm_id].get(field)
                                # Return if value exists and is not NaN
                                if pd.notna(value) and str(value).strip():
                                    return value
                        except (ValueError, KeyError):
                            pass
                return None
            
            # Function to filter out ICMs not in the dictionary
            def filter_icm_ids(icm_ids_str):
                if pd.isna(icm_ids_str) or not str(icm_ids_str).strip():
                    return ''
                icm_ids_str = str(icm_ids_str).replace(',', ';')
                icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
                valid_icms = []
                for icm_id_str in icm_ids:
                    try:
                        icm_id = int(icm_id_str)
                        if icm_id in icm_dict:
                            valid_icms.append(str(icm_id))
                    except (ValueError, KeyError):
                        pass
                return ','.join(valid_icms) if valid_icms else ''
            
            # Filter RelatedICM_Id to only include ICMs in our dictionary
            df['RelatedICM_Id'] = df['RelatedICM_Id'].apply(filter_icm_ids)
            
            df['IcmOwner'] = df['RelatedICM_Id'].apply(lambda x: get_icm_data(x, 'IcmOwner'))
            df['IcmStatus'] = df['RelatedICM_Id'].apply(lambda x: get_icm_data(x, 'IcmStatus'))
            has_icm_data = True
        except Exception as e:
            print(f"Warning: Could not load ICM data: {e}")
    
    # Ensure ICM columns exist
    if 'IcmOwner' not in df.columns:
        df['IcmOwner'] = None
    if 'IcmStatus' not in df.columns:
        df['IcmStatus'] = None
    
    # Recalculate RiskScore with enhanced weighting
    # CRITICAL: >90 days = Critical priority (80+ points)
    # HIGH: >60 days = High priority (60+ points)
    def recalculate_risk_score(row):
        base_score = row['RiskScore']
        days_open = row['DaysOpen']
        
        # Calculate original case age contribution with NEW thresholds
        # Ensure >90 days gets Critical (80+), >60 days gets High (60+)
        if days_open > 180:
            original_age_points = 70  # 70 * 1.4 = 98 (Critical)
        elif days_open > 90:
            original_age_points = 60  # 60 * 1.4 = 84 (Critical)
        elif days_open > 60:
            original_age_points = 45  # 45 * 1.4 = 63 (High)
        elif days_open > 30:
            original_age_points = 20  # 20 * 1.4 = 28 (Medium)
        else:
            original_age_points = 10  # 10 * 1.4 = 14 (Low)
        
        # Increase case age weighting by 40%
        enhanced_age_points = original_age_points * 1.4
        age_adjustment = enhanced_age_points - original_age_points
        
        # Count ICMs and add 10 points for each additional ICM
        icm_bonus = 0
        has_icm = not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip()
        if has_icm:
            icm_ids_str = str(row['RelatedICM_Id']).replace(',', ';')
            icm_count = len([id.strip() for id in icm_ids_str.split(';') if id.strip()])
            if icm_count > 1:
                icm_bonus = (icm_count - 1) * 10
        
        # Add 10 points for cases >30 days without ICM
        no_icm_penalty = 0
        if not has_icm and days_open > 30:
            no_icm_penalty = 10
        
        # Calculate new risk score (capped at 100)
        new_score = min(100, base_score + age_adjustment + icm_bonus + no_icm_penalty)
        return new_score
    
    df['RiskScore'] = df.apply(recalculate_risk_score, axis=1)
    
    # Recalculate risk levels based on new scores
    def get_risk_level(score):
        if score >= 80:
            return 'Critical'
        elif score >= 60:
            return 'High'
        elif score >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    df['RiskLevel'] = df['RiskScore'].apply(get_risk_level)
    
    # Sort by TopParentName (customer) and RiskScore (highest first)
    df = df.sort_values(['TopParentName', 'RiskScore'], ascending=[True, False])
    
    # Group by customer and calculate max risk score per customer
    customer_max_risk = df.groupby('TopParentName')['RiskScore'].max().sort_values(ascending=False)
    
    # Calculate summary statistics by risk level
    risk_summary = df.groupby('RiskLevel').agg({
        'ServiceRequestNumber': 'count',
        'DaysOpen': 'mean',
        'RiskScore': 'mean'
    }).reindex(['Critical', 'High', 'Medium', 'Low'])
    
    # Determine program type for title
    program_type = ''
    if 'Program' in df.columns and len(df['Program'].unique()) == 1:
        program = df['Program'].iloc[0]
        if program == 'IC':
            program_type = ' - Intensive Care (IC)'
        elif program == 'MCS':
            program_type = ' - Mission Critical Support (MCS)'
    
    # Generate HTML
    html_parts = []
    
    # Header
    html_parts.append('''<html xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:w="urn:schemas-microsoft-com:office:word"
xmlns="http://www.w3.org/TR/REC-html40">

<head>
<meta http-equiv=Content-Type content="text/html; charset=unicode">
<meta name=ProgId content=Word.Document>
<meta name=Generator content="Microsoft Word 15">
<title>IC/MCS Case Risk Report - ''' + datetime.now().strftime('%Y-%m-%d') + '''</title>

<!-- DataTables CSS for filtering -->
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css">

<style>
body { font-family: Segoe UI, sans-serif; margin: 20px; }
h1 { font-size: 18pt; color: #1F4E78; font-weight: bold; margin-top: 20px; }
h2 { font-size: 14pt; color: #2E75B5; font-weight: bold; margin-top: 15px; margin-bottom: 10px; }
table { width: 100%; background: white; border-collapse: collapse; margin-bottom: 20px; table-layout: fixed; }
thead td { background: #B7D9F7; border: solid #7EA8F8 1.0pt; padding: 4pt 6pt; font-weight: bold; font-size: 10pt; text-align: center; vertical-align: middle; user-select: none; }
tbody td { border: solid #7EA8F8 1.0pt; padding: 4pt 6pt; font-size: 9pt; text-align: center; vertical-align: middle; word-wrap: break-word; user-select: text; }
tbody td.left-align { text-align: left; }
a { color: #0563C1; text-decoration: underline; }
.critical { background: #FFC7CE; color: #9C0006; font-weight: bold; }
.high { background: #FFF2CC; color: #9C6500; font-weight: bold; }
.medium { background: #C6EFCE; color: #006100; }
.low { background: #F0F0F0; color: #3F3F76; }
/* Column widths for summary table */
table.summary-table { table-layout: auto; }
table.summary-table td:nth-child(1) { width: 15%; }
table.summary-table td:nth-child(2) { width: 15%; }
table.summary-table td:nth-child(3) { width: 20%; }
table.summary-table td:nth-child(4) { width: 20%; }
/* Column widths for case tables - removed Product column, shrunk all */
table.case-table td:nth-child(1) { width: 8%; }  /* Case ID */
table.case-table td:nth-child(2) { width: 12%; } /* Status */
table.case-table td:nth-child(3) { width: 5%; }  /* Age */
table.case-table td:nth-child(4) { width: 8%; }  /* Owner */
table.case-table td:nth-child(5) { width: 8%; }  /* Manager */
table.case-table td:nth-child(6) { width: 7%; }  /* Risk */
table.case-table td:nth-child(7) { width: 25%; } /* Summary */
table.case-table td:nth-child(8) { width: 10%; }  /* ICM */
table.case-table td:nth-child(9) { width: 10%; }  /* ICM Owner */
/* ICM Status color coding */
.icm-active { color: #f57c00; font-weight: bold; }
.icm-resolved { color: #28a745; }
.icm-mitigated { color: #007bff; }
.icm-na { color: #6c757d; font-style: italic; }
.icm-unassigned { color: #dc3545; font-weight: bold; background-color: #ffe6e6; padding: 2px 6px; border-radius: 3px; }
/* Highlight for aged cases without ICM */
.no-icm-aged { background-color: #fff3cd; border: 2px solid #ff9800; padding: 4px; font-weight: bold; }
/* Priority case sections */
.priority-section { border: 3px solid #d32f2f; padding: 15px; margin-bottom: 30px; background-color: #ffebee; border-radius: 5px; }
/* DataTables customizations */
.dataTables_wrapper { margin-top: 15px; }
.dataTables_filter { float: right; }
.dataTables_filter input { border: 1px solid #7EA8F8; padding: 4px 8px; border-radius: 3px; }
div.dataTables_wrapper div.dataTables_length select { border: 1px solid #7EA8F8; padding: 2px; }
/* Better column selection */
td { cursor: text; }
td::selection { background: #B4D5FE; }
</style>

<!-- jQuery and DataTables JS -->
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>

</head>

<body>

<h1>Case Risk Report''' + program_type + ''' - ''' + datetime.now().strftime('%B %d, %Y') + '''</h1>

<p><strong>Report Generated:</strong> ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
<p><strong>Total Cases:</strong> ''' + str(len(df)) + ''' | <strong>Customers:</strong> ''' + str(len(customer_max_risk)) + '''</p>

<h2>Risk Level Summary</h2>
<table class="summary-table" style="width: 60%;">
<thead>
<tr>
<td>Risk Level</td>
<td>Case Count</td>
<td>Avg Days Open</td>
<td>Avg Risk Score</td>
</tr>
</thead>
<tbody>
''')
    
    # Add risk summary rows
    for risk_level in ['Critical', 'High', 'Medium', 'Low']:
        if risk_level in risk_summary.index and not pd.isna(risk_summary.loc[risk_level, 'ServiceRequestNumber']):
            count = int(risk_summary.loc[risk_level, 'ServiceRequestNumber'])
            avg_days = risk_summary.loc[risk_level, 'DaysOpen']
            avg_score = risk_summary.loc[risk_level, 'RiskScore']
            risk_class = risk_level.lower()
            html_parts.append(f'''<tr>
<td class="{risk_class}">{risk_level}</td>
<td>{count}</td>
<td>{avg_days:.1f}</td>
<td>{avg_score:.1f}</td>
</tr>
''')
    
    html_parts.append('''</tbody>
</table>

''')
    
    # Separate Critical and High risk cases into priority section
    critical_high_cases = df[df['RiskScore'] >= 60].copy()
    if len(critical_high_cases) > 0:
        critical_high_cases = critical_high_cases.sort_values(['RiskScore', 'DaysOpen'], ascending=[False, False])
        
        html_parts.append('''<div class="priority-section">
<h2 style="color: #d32f2f; font-size: 18pt; margin-bottom: 10px;">⚠️ CRITICAL & HIGH RISK CASES (Priority View)</h2>
<p style="font-size: 11pt; margin-bottom: 15px;"><strong>Risk Score ≥60 | Total Priority Cases:</strong> ''' + str(len(critical_high_cases)) + '''<br>
<em style="color: #666; font-size: 10pt;">Note: These cases also appear in their respective customer sections below</em></p>

<table id="priorityTable" class="case-table display" style="margin-top: 10px; width: 100%;">
<thead>
<tr>
<th>Case ID</th>
<th>Status</th>
<th>Age (Days)</th>
<th>Owner</th>
<th>Manager</th>
<th>Risk</th>
<th>Summary</th>
<th>ICM IDs</th>
<th>ICM Owner</th>
</tr>
</thead>
<tbody>
''')
        
        for _, row in critical_high_cases.iterrows():
            risk_class = 'critical' if row['RiskScore'] >= 80 else 'high'
            case_url = row['CaseUrl'] if not pd.isna(row['CaseUrl']) else f"https://onesupport.crm.dynamics.com/main.aspx?appid=101acb62-8d00-eb11-a813-000d3a8b3117&pagetype=entityrecord&etn=incident"
            case_owner = row['AgentAlias'] if not pd.isna(row['AgentAlias']) else 'N/A'
            owner_manager = row['ManagerEmail'] if not pd.isna(row['ManagerEmail']) else 'N/A'
            
            # Format ICM ID with link
            icm_display = 'ICM Needed?'
            if not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip():
                icm_id_value = str(row['RelatedICM_Id']).strip().replace(',', ';')
                icm_ids = [id.strip() for id in icm_id_value.split(';') if id.strip()]
                icm_links = []
                
                # Build list of ICMs with their status for sorting
                icm_with_status = []
                for icm_id in icm_ids:
                    icm_url = f"https://portal.microsofticm.com/imp/v3/incidents/details/{icm_id}/home"
                    status_class = ''
                    status_text = ''
                    status_priority = 3  # Default priority (lowest)
                    if has_icm_data:
                        try:
                            icm_id_int = int(icm_id)
                            if icm_id_int in icm_dict:
                                icm_status = icm_dict[icm_id_int].get('IcmStatus', '')
                                if icm_status == 'ACTIVE':
                                    status_class = 'icm-active'
                                    status_text = ' [ACTIVE]'
                                    status_priority = 0
                                elif icm_status == 'MITIGATED':
                                    status_class = 'icm-mitigated'
                                    status_text = ' [MITIGATED]'
                                    status_priority = 1
                                elif icm_status == 'RESOLVED':
                                    status_class = 'icm-resolved'
                                    status_text = ' [RESOLVED]'
                                    status_priority = 2
                        except ValueError:
                            pass
                    icm_with_status.append((status_priority, f'<a href="{icm_url}" class="{status_class}">{icm_id}{status_text}</a>'))
                
                # Sort by status priority (ACTIVE=0, MITIGATED=1, RESOLVED=2)
                icm_with_status.sort(key=lambda x: x[0])
                icm_links = [link for _, link in icm_with_status]
                icm_display = '<br>'.join(icm_links)
            
            # Check if case is >30 days without ICM for highlighting ICM field only
            icm_cell_class = ''
            if row['DaysOpen'] > 30 and (pd.isna(row['RelatedICM_Id']) or not str(row['RelatedICM_Id']).strip()):
                icm_cell_class = ' class="no-icm-aged"'
                icm_display = 'ICM Needed?'
            
            # ICM Owner logic - ROBUST version with ALL RESOLVED check
            icm_owner_display = 'N/A'
            if has_icm_data and not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip():
                # Get owner value, handling all edge cases
                owner_value = ''
                if 'IcmOwner' in df.columns:
                    raw_owner = row['IcmOwner']
                    if pd.notna(raw_owner):
                        owner_str = str(raw_owner).strip()
                        if owner_str and owner_str.lower() not in ['nan', 'none', 'null']:
                            owner_value = owner_str
                
                # Get status value
                icm_status = ''
                if 'IcmStatus' in df.columns:
                    raw_status = row['IcmStatus']
                    if pd.notna(raw_status):
                        status_str = str(raw_status).strip()
                        if status_str and status_str.lower() not in ['nan', 'none', 'null']:
                            icm_status = status_str
                
                # Check if ALL ICMs are RESOLVED
                all_resolved = True
                icm_ids_str = str(row['RelatedICM_Id']).replace(',', ';')
                icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
                for icm_id_str in icm_ids:
                    try:
                        icm_id = int(icm_id_str)
                        if icm_id in icm_dict:
                            if icm_dict[icm_id].get('IcmStatus') != 'RESOLVED':
                                all_resolved = False
                                break
                    except ValueError:
                        pass
                
                # Display logic: N/A if all RESOLVED, show owner if exists, otherwise Unassigned for ACTIVE
                if all_resolved:
                    icm_owner_display = 'N/A'
                elif owner_value:
                    icm_owner_display = owner_value
                    # Add bug links if available
                    bug_links = []
                    for icm_id_str in icm_ids:
                        if icm_id_str in bug_dict:
                            for bug in bug_dict[icm_id_str]:
                                bug_status_color = '#28a745' if bug['Status'] in ['Done', 'Closed'] else '#ffc107' if bug['Status'] in ['Active', 'Resolved'] else '#dc3545'
                                bug_link = f'<a href="{bug["AdoLink"]}" target="_blank" style="color:{bug_status_color};text-decoration:none;" title="Status: {bug["Status"]}">🔧{bug["BugId"]}</a>'
                                bug_links.append(bug_link)
                    if bug_links:
                        icm_owner_display += f'<br><span style="font-size:0.85em;">{" ".join(bug_links)}</span>'
                elif icm_status == 'ACTIVE':
                    icm_owner_display = '<span class="icm-unassigned">Unassigned</span>'
            
            # Build summary with bug links
            summary_text = str(row['Summary'])
            if has_icm_data and not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip():
                icm_ids_str = str(row['RelatedICM_Id']).replace(',', ';')
                icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
                bug_links = []
                for icm_id_str in icm_ids:
                    if icm_id_str in bug_dict:
                        for bug in bug_dict[icm_id_str]:
                            bug_status_color = '#28a745' if bug['Status'] in ['Done', 'Closed'] else '#ffc107' if bug['Status'] in ['Active', 'Resolved'] else '#dc3545'
                            bug_link = f'<a href="{bug["AdoLink"]}" target="_blank" style="color:{bug_status_color};text-decoration:none;font-weight:bold;" title="Status: {bug["Status"]}">[Bug {bug["BugId"]}]</a>'
                            bug_links.append(bug_link)
                if bug_links:
                    summary_text += ' ' + ' '.join(bug_links)
            
            html_parts.append(f'''<tr>
<td><a href="{case_url}">{row['ServiceRequestNumber']}</a></td>
<td>{row['ServiceRequestStatus']}</td>
<td>{row['DaysOpen']:.0f}</td>
<td>{case_owner}</td>
<td>{owner_manager}</td>
<td class="{risk_class}">{row['RiskScore']:.0f}</td>
<td class="left-align">{summary_text}</td>
<td{icm_cell_class}>{icm_display}</td>
<td>{icm_owner_display}</td>
</tr>
''')
        
        html_parts.append('''</tbody>
</table>
</div>

''')
    
    # For each customer (sorted by max risk score)
    for customer_name in customer_max_risk.index:
        customer_cases = df[df['TopParentName'] == customer_name]
        max_risk = customer_cases['RiskScore'].max()
        case_count = len(customer_cases)
        
        # Get PHE and CLE from first row (should be same for all cases of this customer)
        phe = customer_cases.iloc[0]['PHE'] if not pd.isna(customer_cases.iloc[0]['PHE']) else 'N/A'
        cle = customer_cases.iloc[0]['CLE'] if not pd.isna(customer_cases.iloc[0]['CLE']) else 'N/A'
        program = customer_cases.iloc[0]['Program']
        
        # Customer header
        customer_table_id = f"customerTable_{customer_name.replace(' ', '_').replace('.', '_')}"
        html_parts.append(f'''
<h2>{customer_name} ({program}) - {case_count} Case(s) - Max Risk: {max_risk:.0f}</h2>
<p><strong>PHE:</strong> {phe} | <strong>CLE:</strong> {cle}</p>

<table id="{customer_table_id}" class="case-table display" style="width: 100%;">
<thead>
<tr>
<th>Case ID</th>
<th>Status</th>
<th>Age (Days)</th>
<th>Owner</th>
<th>Manager</th>
<th>Risk</th>
<th>Summary</th>
<th>ICM IDs</th>
<th>ICM Owner</th>
</tr>
</thead>
<tbody>
''')
        
        # Cases for this customer
        for _, row in customer_cases.iterrows():
            risk_class = ''
            if row['RiskScore'] >= 80:
                risk_class = 'critical'
            elif row['RiskScore'] >= 60:
                risk_class = 'high'
            elif row['RiskScore'] >= 40:
                risk_class = 'medium'
            else:
                risk_class = 'low'
            
            case_url = row['CaseUrl'] if not pd.isna(row['CaseUrl']) else f"https://onesupport.crm.dynamics.com/main.aspx?appid=101acb62-8d00-eb11-a813-000d3a8b3117&pagetype=entityrecord&etn=incident"
            case_owner = row['AgentAlias'] if not pd.isna(row['AgentAlias']) else 'N/A'
            owner_manager = row['ManagerEmail'] if not pd.isna(row['ManagerEmail']) else 'N/A'
            
            # Format ICM ID with link if present - handle both comma and semicolon separated IDs
            if not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip():
                icm_id_value = str(row['RelatedICM_Id']).strip()
                # Normalize to semicolon separator and split
                icm_id_value = icm_id_value.replace(',', ';')
                icm_ids = [id.strip() for id in icm_id_value.split(';') if id.strip()]
                
                # Build list of ICMs with their status for sorting
                icm_with_status = []
                for icm_id in icm_ids:
                    icm_url = f"https://portal.microsofticm.com/imp/v5/incidents/details/{icm_id}/home"
                    status_class = ''
                    status_text = ''
                    status_priority = 3  # Default priority (lowest)
                    if has_icm_data:
                        try:
                            icm_id_int = int(icm_id)
                            if icm_id_int in icm_dict:
                                icm_status = icm_dict[icm_id_int].get('IcmStatus', '')
                                if icm_status == 'ACTIVE':
                                    status_class = 'icm-active'
                                    status_text = ' [ACTIVE]'
                                    status_priority = 0
                                elif icm_status == 'MITIGATED':
                                    status_class = 'icm-mitigated'
                                    status_text = ' [MITIGATED]'
                                    status_priority = 1
                                elif icm_status == 'RESOLVED':
                                    status_class = 'icm-resolved'
                                    status_text = ' [RESOLVED]'
                                    status_priority = 2
                        except ValueError:
                            pass
                    icm_with_status.append((status_priority, f'<a href="{icm_url}" class="{status_class}">{icm_id}{status_text}</a>'))
                
                # Sort by status priority (ACTIVE=0, MITIGATED=1, RESOLVED=2)
                icm_with_status.sort(key=lambda x: x[0])
                icm_links = [link for _, link in icm_with_status]
                icm_display = '<br>'.join(icm_links)  # Use line break for multiple IDs
            else:
                icm_display = 'ICM Needed?'
            
            # ICM Owner logic - ROBUST version with ALL RESOLVED check
            icm_owner_display = 'N/A'
            if has_icm_data and not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip():
                # Get owner value, handling all edge cases
                owner_value = ''
                if 'IcmOwner' in df.columns:
                    raw_owner = row['IcmOwner']
                    if pd.notna(raw_owner):
                        owner_str = str(raw_owner).strip()
                        if owner_str and owner_str.lower() not in ['nan', 'none', 'null']:
                            owner_value = owner_str
                
                # Get status value
                icm_status = ''
                if 'IcmStatus' in df.columns:
                    raw_status = row['IcmStatus']
                    if pd.notna(raw_status):
                        status_str = str(raw_status).strip()
                        if status_str and status_str.lower() not in ['nan', 'none', 'null']:
                            icm_status = status_str
                
                # Check if ALL ICMs are RESOLVED
                all_resolved = True
                icm_ids_str = str(row['RelatedICM_Id']).replace(',', ';')
                icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
                for icm_id_str in icm_ids:
                    try:
                        icm_id = int(icm_id_str)
                        if icm_id in icm_dict:
                            if icm_dict[icm_id].get('IcmStatus') != 'RESOLVED':
                                all_resolved = False
                                break
                    except ValueError:
                        pass
                
                # Display logic: N/A if all RESOLVED, show owner if exists, otherwise Unassigned for ACTIVE
                if all_resolved:
                    icm_owner_display = 'N/A'
                elif owner_value:
                    icm_owner_display = owner_value
                    # Add bug links if available
                    bug_links = []
                    for icm_id_str in icm_ids:
                        if icm_id_str in bug_dict:
                            for bug in bug_dict[icm_id_str]:
                                bug_status_color = '#28a745' if bug['Status'] in ['Done', 'Closed'] else '#ffc107' if bug['Status'] in ['Active', 'Resolved'] else '#dc3545'
                                bug_link = f'<a href="{bug["AdoLink"]}" target="_blank" style="color:{bug_status_color};text-decoration:none;" title="Status: {bug["Status"]}">🔧{bug["BugId"]}</a>'
                                bug_links.append(bug_link)
                    if bug_links:
                        icm_owner_display += f'<br><span style="font-size:0.85em;">{" ".join(bug_links)}</span>'
                elif icm_status == 'ACTIVE':
                    icm_owner_display = '<span class="icm-unassigned">Unassigned</span>'
            
            # Build summary with bug links
            summary_text = str(row['Summary'])
            if has_icm_data and not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip():
                icm_ids_str = str(row['RelatedICM_Id']).replace(',', ';')
                icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
                bug_links = []
                for icm_id_str in icm_ids:
                    if icm_id_str in bug_dict:
                        for bug in bug_dict[icm_id_str]:
                            bug_status_color = '#28a745' if bug['Status'] in ['Done', 'Closed'] else '#ffc107' if bug['Status'] in ['Active', 'Resolved'] else '#dc3545'
                            bug_link = f'<a href="{bug["AdoLink"]}" target="_blank" style="color:{bug_status_color};text-decoration:none;font-weight:bold;" title="Status: {bug["Status"]}">[Bug {bug["BugId"]}]</a>'
                            bug_links.append(bug_link)
                if bug_links:
                    summary_text += ' ' + ' '.join(bug_links)
            
            # Check if case is >30 days without ICM for highlighting ICM field only
            icm_cell_class = ''
            if row['DaysOpen'] > 30 and (pd.isna(row['RelatedICM_Id']) or not str(row['RelatedICM_Id']).strip()):
                icm_cell_class = ' class="no-icm-aged"'
                if icm_display == 'ICM Needed?':
                    icm_display = 'ICM Needed?'
            
            html_parts.append(f'''
<tr>
<td><a href="{case_url}">{row['ServiceRequestNumber']}</a></td>
<td>{row['ServiceRequestStatus']}</td>
<td>{row['DaysOpen']:.0f}</td>
<td>{case_owner}</td>
<td>{owner_manager}</td>
<td class="{risk_class}">{row['RiskScore']:.0f}</td>
<td class="left-align">{summary_text}</td>
<td{icm_cell_class}>{icm_display}</td>
<td>{icm_owner_display}</td>
</tr>
''')
        
        html_parts.append('''
</tbody>
</table>
''')
    
    # Footer with DataTables initialization
    html_parts.append('''
<script>
$(document).ready(function() {
    // Initialize DataTables for priority table
    $('#priorityTable').DataTable({
        "paging": false,  // Disable pagination
        "lengthChange": false,  // Remove "show entries" dropdown
        "order": [[5, "desc"]],  // Sort by Risk column (index 5) descending
        "columnDefs": [
            { "orderable": true, "targets": "_all" }
        ],
        "language": {
            "search": "Filter cases:",
            "info": "Showing _START_ to _END_ of _TOTAL_ priority cases",
            "infoFiltered": "(filtered from _MAX_ total priority cases)"
        }
    });
    
    // Initialize DataTables for all customer tables
    $('table[id^="customerTable_"]').each(function() {
        $(this).DataTable({
            "paging": false,  // Disable pagination
            "lengthChange": false,  // Remove "show entries" dropdown
            "order": [[5, "desc"]],  // Sort by Risk column descending
            "searching": true,
            "info": true,
            "columnDefs": [
                { "orderable": true, "targets": "_all" }
            ]
        });
    });
});
</script>

</body>
</html>
''')
    
    # Write to file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(''.join(html_parts))
    
    print(f"Report generated: {output_html}")
    print(f"Total customers: {len(customer_max_risk)}")
    print(f"Total cases: {len(df)}")
    print(f"\\nTop 5 Highest Risk Customers:")
    for i, (customer, risk) in enumerate(customer_max_risk.head(5).items(), 1):
        case_count = len(df[df['TopParentName'] == customer])
        print(f"{i}. {customer}: Risk {risk:.0f} ({case_count} cases)")


if __name__ == "__main__":
    # Example usage:
    # 1. Run the support case Kusto query (returns JSON or export to CSV)
    # 2. Optionally run the ICM query and export to CSV
    # 3. Run this script with the file(s)
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]  # Can be CSV or JSON
        icm_file = None
        output_file_base = "IC_MCS_Risk_Report"
        
        # Parse arguments: <cases> <output> [icm] OR <cases> [icm] [output]
        if len(sys.argv) > 2:
            # If second arg ends with .htm, it's the output file
            if sys.argv[2].endswith('.htm') or sys.argv[2].endswith('.html'):
                output_file_base = sys.argv[2].replace('.htm', '').replace('.html', '')
                # Third arg (if present) is ICM file
                if len(sys.argv) > 3:
                    icm_file = sys.argv[3]
            # Otherwise, second arg is ICM file if it ends with .csv
            elif sys.argv[2].endswith('.csv'):
                icm_file = sys.argv[2]
                # Third arg (if present) is output file
                if len(sys.argv) > 3:
                    output_file_base = sys.argv[3].replace('.htm', '').replace('.html', '')
            else:
                # Second arg is output file base, third is ICM file
                output_file_base = sys.argv[2]
                if len(sys.argv) > 3:
                    icm_file = sys.argv[3]
        
        # Load data to check for Program field
        if input_file.endswith('.json'):
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            full_df = pd.DataFrame(data.get('data', data))
        else:
            full_df = pd.read_csv(input_file)
        
        # Check if Program field exists and has both IC and MCS
        if 'Program' in full_df.columns:
            programs = full_df['Program'].unique()
            
            # Generate separate reports for IC and MCS
            if 'IC' in programs:
                ic_df = full_df[full_df['Program'] == 'IC']
                ic_file_temp = 'temp_ic_cases.csv'
                ic_df.to_csv(ic_file_temp, index=False)
                ic_output = f"{output_file_base}_IC.htm"
                print(f"\\n=== Generating IC (Intensive Care) Report ===")
                generate_risk_report_html(ic_file_temp, icm_file, ic_output)
                os.remove(ic_file_temp)
            
            if 'MCS' in programs:
                mcs_df = full_df[full_df['Program'] == 'MCS']
                mcs_file_temp = 'temp_mcs_cases.csv'
                mcs_df.to_csv(mcs_file_temp, index=False)
                mcs_output = f"{output_file_base}_MCS.htm"
                print(f"\\n=== Generating MCS (Mission Critical) Report ===")
                generate_risk_report_html(mcs_file_temp, icm_file, mcs_output)
                os.remove(mcs_file_temp)
            
            print(f"\nGenerated separate reports for IC and MCS programs")
        else:
            # Generate single report if no Program field
            generate_risk_report_html(input_file, icm_file, f"{output_file_base}.htm")
    else:
        print("Usage: python ic_mcs_risk_report_generator.py <cases.csv|cases.json> [icm.csv] [output.htm]")
        print("\\nExamples:")
        print("  python ic_mcs_risk_report_generator.py cases.csv report.htm")
        print("  python ic_mcs_risk_report_generator.py cases.json icm.csv report.htm")
        print("  python ic_mcs_risk_report_generator.py query_results.json report.htm")

