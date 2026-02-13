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
    
    # If ICM data provided, join it
    has_icm_data = False
    if icm_results_csv:
        try:
            icm_df = pd.read_csv(icm_results_csv)
            # Build ICM lookup dictionary for multi-ICM cases - include bug data
            icm_columns = ['IcmOwner', 'IcmSeverity', 'IcmStatus']
            if 'BugExternalIds' in icm_df.columns:
                icm_columns.extend(['BugExternalIds', 'BugDescriptions', 'BugStatuses'])
            icm_dict = icm_df.set_index('IncidentId')[icm_columns].to_dict('index')
            
            # Function to look up ICM data (handles multiple ICM IDs - comma or semicolon separated)
            # Prioritizes ACTIVE, then MITIGATED, then others for owner/status display
            def get_icm_data(icm_ids_str, field):
                if pd.isna(icm_ids_str) or not str(icm_ids_str).strip():
                    return None
                # Split by both comma and semicolon to handle different formats
                icm_ids_str = str(icm_ids_str).replace(',', ';')
                icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
                if icm_ids:
                    # First, look for an ACTIVE ICM
                    for icm_id_str in icm_ids:
                        try:
                            icm_id = int(icm_id_str)
                            if icm_id in icm_dict:
                                if icm_dict[icm_id].get('IcmStatus') == 'ACTIVE':
                                    return icm_dict[icm_id].get(field)
                        except ValueError:
                            pass
                    # If no ACTIVE, look for MITIGATED
                    for icm_id_str in icm_ids:
                        try:
                            icm_id = int(icm_id_str)
                            if icm_id in icm_dict:
                                if icm_dict[icm_id].get('IcmStatus') == 'MITIGATED':
                                    return icm_dict[icm_id].get(field)
                        except ValueError:
                            pass
                    # If no ACTIVE or MITIGATED, return first available
                    try:
                        first_icm_id = int(icm_ids[0])
                        if first_icm_id in icm_dict:
                            return icm_dict[first_icm_id].get(field)
                    except ValueError:
                        pass
                return None
            
            # Function to get all bugs for all ICMs (not just ACTIVE)
            def get_all_bugs(icm_ids_str):
                if pd.isna(icm_ids_str) or not str(icm_ids_str).strip():
                    return None
                icm_ids_str = str(icm_ids_str).replace(',', ';')
                icm_ids = [id.strip() for id in icm_ids_str.split(';') if id.strip()]
                all_bugs = set()
                bug_info = []
                for icm_id_str in icm_ids:
                    try:
                        icm_id = int(icm_id_str)
                        if icm_id in icm_dict:
                            bug_ids = icm_dict[icm_id].get('BugExternalIds')
                            bug_statuses = icm_dict[icm_id].get('BugStatuses')
                            if bug_ids and not pd.isna(bug_ids) and str(bug_ids).strip():
                                bug_id_list = str(bug_ids).split(',')
                                status_list = str(bug_statuses).split(',') if bug_statuses and not pd.isna(bug_statuses) else []
                                for i, bug_id in enumerate(bug_id_list):
                                    bug_id = bug_id.strip()
                                    if bug_id and bug_id not in all_bugs:
                                        all_bugs.add(bug_id)
                                        status = status_list[i].strip() if i < len(status_list) else 'Unknown'
                                        bug_info.append(f"{bug_id} ({status})")
                    except ValueError:
                        pass
                return '; '.join(bug_info) if bug_info else None
            
            # Function to convert bug info to HTML links
            def format_bug_links(bug_info_str):
                if not bug_info_str or pd.isna(bug_info_str):
                    return None
                bug_links = []
                # Parse "bug_id (status); bug_id (status)" format
                bug_entries = bug_info_str.split(';')
                for entry in bug_entries:
                    entry = entry.strip()
                    if entry:
                        # Extract bug ID and status
                        if '(' in entry and ')' in entry:
                            bug_id = entry.split('(')[0].strip()
                            status = entry.split('(')[1].split(')')[0].strip()
                            bug_url = f"https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug_id}"
                            bug_links.append(f'<a href="{bug_url}" target="_blank">{bug_id}</a> ({status})')
                        else:
                            bug_links.append(entry)
                return '; '.join(bug_links) if bug_links else None
            
            df['IcmOwner'] = df['RelatedICM_Id'].apply(lambda x: get_icm_data(x, 'IcmOwner'))
            df['IcmStatus'] = df['RelatedICM_Id'].apply(lambda x: get_icm_data(x, 'IcmStatus'))
            df['BugInfo'] = df['RelatedICM_Id'].apply(get_all_bugs)
            df['BugInfoLinked'] = df['BugInfo'].apply(format_bug_links)
            has_icm_data = True
        except Exception as e:
            print(f"Warning: Could not load ICM data: {e}")
    
    # Ensure ICM columns exist
    if 'IcmOwner' not in df.columns:
        df['IcmOwner'] = None
    if 'IcmStatus' not in df.columns:
        df['IcmStatus'] = None
    if 'BugInfo' not in df.columns:
        df['BugInfo'] = None
    if 'BugInfoLinked' not in df.columns:
        df['BugInfoLinked'] = None
    
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
<style>
body { font-family: Segoe UI, sans-serif; margin: 20px; }
h1 { font-size: 18pt; color: #1F4E78; font-weight: bold; margin-top: 20px; }
h2 { font-size: 14pt; color: #2E75B5; font-weight: bold; margin-top: 15px; margin-bottom: 10px; }
table { width: 100%; background: white; border-collapse: collapse; margin-bottom: 20px; table-layout: fixed; }
thead td { background: #B7D9F7; border: solid #7EA8F8 1.0pt; padding: 4pt 6pt; font-weight: bold; font-size: 10pt; text-align: center; vertical-align: middle; }
tbody td { border: solid #7EA8F8 1.0pt; padding: 4pt 6pt; font-size: 9pt; text-align: center; vertical-align: middle; word-wrap: break-word; }
tbody td.left-align { text-align: left; }
tbody td.nowrap { white-space: nowrap; }
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
/* Column widths for case tables - equal widths */
table.case-table td:nth-child(1) { width: 11%; } /* Case ID */
table.case-table td:nth-child(2) { width: 11%; } /* Status */
table.case-table td:nth-child(3) { width: 11%; } /* Age */
table.case-table td:nth-child(4) { width: 11%; } /* Owner */
table.case-table td:nth-child(5) { width: 11%; } /* Manager */
table.case-table td:nth-child(6) { width: 11%; } /* Risk */
table.case-table td:nth-child(7) { width: 12%; } /* Summary (with bugs) */
table.case-table td:nth-child(8) { width: 11%; } /* ICM (with status) */
table.case-table td:nth-child(9) { width: 11%; } /* ICM Owner */
/* Critical cases table has 10 columns (includes Customer) */
table.critical-cases-table td:nth-child(1) { width: 10%; } /* Case ID */
table.critical-cases-table td:nth-child(2) { width: 10%; } /* Customer */
table.critical-cases-table td:nth-child(3) { width: 10%; } /* Status */
table.critical-cases-table td:nth-child(4) { width: 10%; } /* Age */
table.critical-cases-table td:nth-child(5) { width: 10%; } /* Owner */
table.critical-cases-table td:nth-child(6) { width: 10%; } /* Manager */
table.critical-cases-table td:nth-child(7) { width: 10%; } /* Risk */
table.critical-cases-table td:nth-child(8) { width: 10%; } /* Summary */
table.critical-cases-table td:nth-child(9) { width: 10%; } /* ICM IDs */
table.critical-cases-table td:nth-child(10) { width: 10%; } /* ICM Owner */
.bug-info { font-size: 8pt; color: #d32f2f; font-weight: bold; }
/* ICM Status color coding */
.icm-active { color: #f57c00; font-weight: bold; }
.icm-unassigned { background: #FFC7CE; color: #9C0006; font-weight: bold; }
</style>
</head>

<body>

<h1>IC/MCS Case Risk Report - ''' + datetime.now().strftime('%B %d, %Y') + '''</h1>

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
    
    # Add Critical Cases section at the top
    critical_cases = df[df['RiskLevel'] == 'Critical'].sort_values('RiskScore', ascending=False)
    if len(critical_cases) > 0:
        html_parts.append(f'''
<h2>🚨 Critical Cases ({len(critical_cases)} cases - ALL cases over 90 days old)</h2>
<table class="critical-cases-table">
<thead>
<tr>
<td>Case ID</td>
<td>Customer</td>
<td>Status</td>
<td>Age (Days)</td>
<td>Owner</td>
<td>Manager</td>
<td>Risk</td>
<td>Summary</td>
<td>ICM IDs</td>
<td>ICM Owner</td>
</tr>
</thead>
<tbody>
''')
        
        for _, row in critical_cases.iterrows():
            case_owner = row['AgentAlias'] if not pd.isna(row['AgentAlias']) else 'N/A'
            owner_manager = row['ManagerEmail'] if not pd.isna(row['ManagerEmail']) else 'N/A'
            
            # Format ICM ID with link if present
            if not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip():
                icm_id_value = str(row['RelatedICM_Id']).strip()
                icm_id_value = icm_id_value.replace(',', ';')
                icm_ids = [id.strip() for id in icm_id_value.split(';') if id.strip()]
                
                # Sort ICMs: ACTIVE first, then MITIGATED, then RESOLVED
                active_icms = []
                mitigated_icms = []
                other_icms = []
                for icm_id in icm_ids:
                    if has_icm_data:
                        try:
                            icm_id_int = int(icm_id)
                            if icm_id_int in icm_dict:
                                status = icm_dict[icm_id_int].get('IcmStatus')
                                if status == 'ACTIVE':
                                    active_icms.append(icm_id)
                                elif status == 'MITIGATED':
                                    mitigated_icms.append(icm_id)
                                else:
                                    other_icms.append(icm_id)
                            else:
                                other_icms.append(icm_id)
                        except ValueError:
                            other_icms.append(icm_id)
                    else:
                        other_icms.append(icm_id)
                
                sorted_icm_ids = active_icms + mitigated_icms + other_icms
                
                icm_links = []
                for icm_id in sorted_icm_ids:
                    icm_url = f"https://portal.microsofticm.com/imp/v5/incidents/details/{icm_id}/home"
                    status_class = ''
                    status_text = ''
                    if has_icm_data:
                        try:
                            icm_id_int = int(icm_id)
                            if icm_id_int in icm_dict:
                                icm_status_check = icm_dict[icm_id_int].get('IcmStatus', '')
                                if icm_status_check:
                                    status_text = f' ({icm_status_check})'
                                    if icm_status_check == 'ACTIVE':
                                        status_class = 'icm-active'
                        except ValueError:
                            pass
                    icm_links.append(f'<a href="{icm_url}" class="{status_class}">{icm_id}{status_text}</a>')
                icm_display = '<br>'.join(icm_links)
            else:
                icm_display = 'None'
            
            # ICM Owner - show only for ACTIVE or MITIGATED
            icm_owner = ''
            icm_status = 'N/A'
            icm_owner_class = ''
            if has_icm_data:
                if 'IcmStatus' in df.columns and not pd.isna(row['IcmStatus']):
                    icm_status = str(row['IcmStatus'])
                # Only show owner for ACTIVE or MITIGATED ICMs
                if icm_status in ['ACTIVE', 'MITIGATED']:
                    if 'IcmOwner' in df.columns and not pd.isna(row['IcmOwner']):
                        icm_owner = str(row['IcmOwner']).strip()
                    # Flag ACTIVE ICMs with no owner as UNASSIGNED
                    if icm_status == 'ACTIVE' and not icm_owner:
                        icm_owner = 'UNASSIGNED'
                        icm_owner_class = ' class="icm-unassigned"'
            
            # Bug information - from ICM data, add to summary only
            summary_with_bugs = row['Summary']
            if 'BugInfoLinked' in df.columns and not pd.isna(row['BugInfoLinked']):
                summary_with_bugs = f'{row["Summary"]} <strong>Linked Bugs:</strong> {row["BugInfoLinked"]}'
            
            html_parts.append(f'''
<tr>
<td class="nowrap"><a href="{row['CaseUrl']}">{row['ServiceRequestNumber']}</a></td>
<td>{row['TopParentName']}</td>
<td>{row['ServiceRequestStatus']}</td>
<td>{row['DaysOpen']:.0f}</td>
<td>{case_owner}</td>
<td>{owner_manager}</td>
<td class="critical">{row['RiskScore']:.0f}</td>
<td class="left-align">{summary_with_bugs}</td>
<td>{icm_display}</td>
<td{icm_owner_class}>{icm_owner}</td>
</tr>
''')
        
        html_parts.append('''
</tbody>
</table>

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
        html_parts.append(f'''
<h2>{customer_name} ({program}) - {case_count} Case(s) - Max Risk: {max_risk:.0f}</h2>
<p><strong>PHE:</strong> {phe} | <strong>CLE:</strong> {cle}</p>

<table class="case-table">
<thead>
<tr>
<td>Case ID</td>
<td>Status</td>
<td>Age (Days)</td>
<td>Owner</td>
<td>Manager</td>
<td>Risk</td>
<td>Summary</td>
<td>ICM IDs</td>
<td>ICM Owner</td>
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
            
            case_url = f"https://servicedesk.microsoft.com/incidents/{row['ServiceRequestNumber']}"
            case_owner = row['AgentAlias'] if not pd.isna(row['AgentAlias']) else 'N/A'
            owner_manager = row['ManagerEmail'] if not pd.isna(row['ManagerEmail']) else 'N/A'
            
            # Format ICM ID with link if present - handle both comma and semicolon separated IDs
            if not pd.isna(row['RelatedICM_Id']) and str(row['RelatedICM_Id']).strip():
                icm_id_value = str(row['RelatedICM_Id']).strip()
                # Normalize to semicolon separator and split
                icm_id_value = icm_id_value.replace(',', ';')
                icm_ids = [id.strip() for id in icm_id_value.split(';') if id.strip()]
                
                # Sort ICMs: ACTIVE first, then MITIGATED, then RESOLVED
                active_icms = []
                mitigated_icms = []
                other_icms = []
                for icm_id in icm_ids:
                    if has_icm_data:
                        try:
                            icm_id_int = int(icm_id)
                            if icm_id_int in icm_dict:
                                status = icm_dict[icm_id_int].get('IcmStatus')
                                if status == 'ACTIVE':
                                    active_icms.append(icm_id)
                                elif status == 'MITIGATED':
                                    mitigated_icms.append(icm_id)
                                else:
                                    other_icms.append(icm_id)
                            else:
                                other_icms.append(icm_id)
                        except ValueError:
                            other_icms.append(icm_id)
                    else:
                        other_icms.append(icm_id)
                
                # Combine: ACTIVE, MITIGATED, then others
                sorted_icm_ids = active_icms + mitigated_icms + other_icms
                
                icm_links = []
                for icm_id in sorted_icm_ids:
                    icm_url = f"https://portal.microsofticm.com/imp/v5/incidents/details/{icm_id}/home"
                    # Show status inline for all ICMs, highlight ACTIVE in orange
                    status_class = ''
                    status_text = ''
                    if has_icm_data:
                        try:
                            icm_id_int = int(icm_id)
                            if icm_id_int in icm_dict:
                                icm_status = icm_dict[icm_id_int].get('IcmStatus', '')
                                if icm_status:
                                    status_text = f' ({icm_status})'
                                    if icm_status == 'ACTIVE':
                                        status_class = 'icm-active'
                        except ValueError:
                            pass
                    icm_links.append(f'<a href="{icm_url}" class="{status_class}">{icm_id}{status_text}</a>')
                icm_display = '<br>'.join(icm_links)  # Use line break for multiple IDs
            else:
                icm_display = 'None'
            
            # ICM Owner - show only for ACTIVE or MITIGATED
            icm_owner = ''
            icm_status = 'N/A'
            icm_owner_class = ''
            if has_icm_data:
                if 'IcmStatus' in df.columns and not pd.isna(row['IcmStatus']):
                    icm_status = str(row['IcmStatus'])
                # Only show owner for ACTIVE or MITIGATED ICMs
                if icm_status in ['ACTIVE', 'MITIGATED']:
                    if 'IcmOwner' in df.columns and not pd.isna(row['IcmOwner']):
                        icm_owner = str(row['IcmOwner']).strip()
                    # Flag ACTIVE ICMs with no owner as UNASSIGNED
                    if icm_status == 'ACTIVE' and not icm_owner:
                        icm_owner = 'UNASSIGNED'
                        icm_owner_class = ' class="icm-unassigned"'
            
            # Bug information - from ICM data, add to summary only
            summary_with_bugs = row['Summary']
            if 'BugInfoLinked' in df.columns and not pd.isna(row['BugInfoLinked']):
                summary_with_bugs = f'{row["Summary"]} <strong>Linked Bugs:</strong> {row["BugInfoLinked"]}'
            
            html_parts.append(f'''
<tr>
<td class="nowrap"><a href="{row['CaseUrl']}">{row['ServiceRequestNumber']}</a></td>
<td>{row['ServiceRequestStatus']}</td>
<td>{row['DaysOpen']:.0f}</td>
<td>{case_owner}</td>
<td>{owner_manager}</td>
<td class="{risk_class}">{row['RiskScore']:.0f}</td>
<td class="left-align">{summary_with_bugs}</td>
<td>{icm_display}</td>
<td{icm_owner_class}>{icm_owner}</td>
</tr>
''')
        
        html_parts.append('''
</tbody>
</table>
''')
    
    # Footer
    html_parts.append('''
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
        output_file = "IC_MCS_Risk_Report.htm"
        
        # Check if second arg is ICM data or output file
        if len(sys.argv) > 2:
            if sys.argv[2].endswith('.csv') or sys.argv[2].endswith('.json'):
                icm_file = sys.argv[2]
                output_file = sys.argv[3] if len(sys.argv) > 3 else "IC_MCS_Risk_Report.htm"
            else:
                output_file = sys.argv[2]
        
        generate_risk_report_html(input_file, icm_file, output_file)
    else:
        print("Usage: python ic_mcs_risk_report_generator.py <cases.csv|cases.json> [icm.csv] [output.htm]")
        print("\\nExamples:")
        print("  python ic_mcs_risk_report_generator.py cases.csv report.htm")
        print("  python ic_mcs_risk_report_generator.py cases.json icm.csv report.htm")
        print("  python ic_mcs_risk_report_generator.py query_results.json report.htm")

