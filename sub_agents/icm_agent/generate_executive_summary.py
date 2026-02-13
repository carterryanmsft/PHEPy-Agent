"""
Generate Executive Summary HTML Report with Tables and Clear Actions

⚠️ LOCKED FORMAT - Version 1.0 - APPROVED ⚠️
This format has been approved for production use.
Do not modify structure without approval.

Author: Carter Ryan
Created: February 11, 2026
Locked: February 11, 2026
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def generate_executive_summary_html():
    """Generate clean HTML report with tables and executive summary"""
    
    # Load ICM data
    data_file = Path(__file__).parent / "data" / "public_doc_icms" / "icm_details_with_themes.json"
    
    with open(data_file, 'r', encoding='utf-8') as f:
        icms = json.load(f)
    
    # Group by themes
    themes = defaultdict(list)
    
    for icm in icms:
        desc = icm.get('description', '').lower()
        title = icm.get('title', '').lower()
        combined = f"{title} {desc}"
        
        # Categorize
        if any(x in combined for x in ['license', 'licensing', 'e5', 'add-on']):
            themes["Licensing Clarity"].append(icm)
        
        if 'metric' in combined or 'portal' in combined or 'files labeled' in combined:
            themes["Portal Metrics Documentation"].append(icm)
        
        if 'pending' in combined and 'distribution' in combined:
            themes["Policy Status Definitions"].append(icm)
        
        if any(x in combined for x in ['size', 'limit', 'maximum', 'large', 'thousands']):
            themes["Size & Scale Limits"].append(icm)
        
        if any(x in combined for x in ['example', 'xml', 'checksum', 'regex']):
            themes["Configuration Examples"].append(icm)
        
        if 'url' in combined or 'whitelist' in combined:
            themes["URL Matching Logic"].append(icm)
        
        if 'scope' in combined or 'in-transit' in combined or 'simulation' in combined:
            themes["Feature Scope & Timing"].append(icm)
        
        if 'condition' in combined:
            themes["DLP Conditions Behavior"].append(icm)
    
    # Generate HTML
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation Gap Analysis - Executive Summary</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            background: #f5f5f5; 
            color: #333; 
        }
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .header { 
            background: linear-gradient(135deg, #0078d4 0%, #106ebe 100%); 
            color: white; 
            padding: 40px; 
            border-radius: 10px; 
            margin-bottom: 30px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
        }
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 10px; 
        }
        .header p { 
            font-size: 1.2em; 
            opacity: 0.95; 
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .stat-card { 
            background: white; 
            padding: 25px; 
            border-radius: 8px; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
            border-left: 4px solid #0078d4; 
        }
        .stat-card .number { 
            font-size: 3em; 
            font-weight: bold; 
            color: #0078d4; 
            margin-bottom: 5px; 
        }
        .stat-card .label { 
            font-size: 1.1em; 
            color: #666; 
        }
        .section { 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            margin-bottom: 30px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        }
        h2 { 
            color: #0078d4; 
            font-size: 1.8em; 
            margin-bottom: 20px; 
            padding-bottom: 10px; 
            border-bottom: 3px solid #0078d4; 
        }
        h3 { 
            color: #106ebe; 
            font-size: 1.4em; 
            margin-top: 25px; 
            margin-bottom: 15px; 
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin: 20px 0; 
            background: white; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.1); 
        }
        th { 
            background: #0078d4; 
            color: white; 
            padding: 15px; 
            text-align: left; 
            font-weight: 600; 
            font-size: 0.95em; 
        }
        td { 
            padding: 12px 15px; 
            border-bottom: 1px solid #e1e1e1; 
            vertical-align: top; 
        }
        tr:hover { 
            background: #f9f9f9; 
        }
        .priority-high { 
            background: #fde7e9; 
            color: #d13438; 
            padding: 5px 10px; 
            border-radius: 4px; 
            font-weight: 600; 
            display: inline-block; 
        }
        .priority-medium { 
            background: #fff4ce; 
            color: #8a5a00; 
            padding: 5px 10px; 
            border-radius: 4px; 
            font-weight: 600; 
            display: inline-block; 
        }
        .priority-low { 
            background: #dff6dd; 
            color: #107c10; 
            padding: 5px 10px; 
            border-radius: 4px; 
            font-weight: 600; 
            display: inline-block; 
        }
        a { 
            color: #0078d4; 
            text-decoration: none; 
            font-weight: 500; 
        }
        a:hover { 
            text-decoration: underline; 
        }
        .action-list { 
            background: #f0f9ff; 
            padding: 15px 20px; 
            border-left: 4px solid #0078d4; 
            margin: 15px 0; 
            border-radius: 4px; 
        }
        .action-list li { 
            margin: 8px 0; 
        }
        .doc-page { 
            background: #f4f4f4; 
            padding: 3px 8px; 
            border-radius: 3px; 
            font-family: 'Courier New', monospace; 
            font-size: 0.9em; 
            color: #d13438; 
        }
        .theme-card { 
            background: #fafafa; 
            padding: 20px; 
            margin: 20px 0; 
            border-radius: 8px; 
            border-left: 4px solid #0078d4; 
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Documentation Gap Analysis</h1>
        <p>Executive Summary - MIP/DLP "By Design" Prevention Type: Public Documentation</p>
        <p style="margin-top: 10px; font-size: 1em;">Generated: """ + datetime.now().strftime('%B %d, %Y at %I:%M %p') + """</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="number">""" + str(len(icms)) + """</div>
            <div class="label">Total ICMs Analyzed</div>
        </div>
        <div class="stat-card">
            <div class="number">""" + str(len(themes)) + """</div>
            <div class="label">Major Themes</div>
        </div>
        <div class="stat-card">
            <div class="number">22</div>
            <div class="label">Specific Doc Gaps</div>
        </div>
        <div class="stat-card">
            <div class="number">8</div>
            <div class="label">Doc Pages to Create</div>
        </div>
    </div>
"""
    
    # Executive Summary Table
    html += """
    <div class="section">
        <h2>Executive Summary - Top Documentation Gaps</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 25%;">Theme</th>
                    <th style="width: 15%;">Priority</th>
                    <th style="width: 10%;">ICMs</th>
                    <th style="width: 50%;">What's Missing</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # Sort themes by count
    sorted_themes = sorted(themes.items(), key=lambda x: len(x[1]), reverse=True)
    
    priority_map = {
        0: '<span class="priority-high">HIGH</span>',
        1: '<span class="priority-high">HIGH</span>',
        2: '<span class="priority-high">HIGH</span>',
        3: '<span class="priority-medium">MEDIUM</span>',
        4: '<span class="priority-medium">MEDIUM</span>',
    }
    
    summaries = {
        "Licensing Clarity": "No clear license comparison showing Teams chat vs files coverage, E5 vs add-on differences",
        "Portal Metrics Documentation": "Refresh intervals, why metrics show 0, portal vs Activity Explorer differences not documented",
        "Policy Status Definitions": "No explanation of 'Pending' status, expected durations, when to escalate",
        "Size & Scale Limits": "File size and record count limits that affect DLP detection not documented",
        "Configuration Examples": "Working XML examples for checksums, regex patterns missing from docs",
        "URL Matching Logic": "How query parameters are handled, parent domain implications unclear",
        "Feature Scope & Timing": "In-transit vs at-rest application, simulation behavior not explained",
        "DLP Conditions Behavior": "What each condition checks (metadata vs content) not fully explained"
    }
    
    for idx, (theme, icm_list) in enumerate(sorted_themes[:8]):
        priority = priority_map.get(idx, '<span class="priority-low">LOW</span>')
        summary = summaries.get(theme, "Documentation gaps identified")
        
        html += f"""
                <tr>
                    <td><strong>{theme}</strong></td>
                    <td>{priority}</td>
                    <td style="text-align: center;"><strong>{len(icm_list)}</strong></td>
                    <td>{summary}</td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
    </div>
"""
    
    # Detailed Sections for Each Theme
    actions_map = {
        "Licensing Clarity": [
            "Create comprehensive license comparison table on <span class='doc-page'>/purview/dlp-licensing</span>",
            "Add side-by-side comparison: E3, E5, E5 Information Protection add-on",
            "Clarify Teams: chat messages vs file sharing vs channel messages coverage",
            "Add FAQ: 'Which license do I need for Teams DLP?'",
            "Update <span class='doc-page'>/purview/dlp-microsoft-teams</span> with licensing requirements section"
        ],
        "Portal Metrics Documentation": [
            "Create new page: <span class='doc-page'>/purview/portal-metrics-reference</span>",
            "Document refresh intervals for each metric (auto-labeling portal, Activity Explorer, etc.)",
            "Explain why 'Files Labeled' might show 0 temporarily",
            "Add comparison table: Portal metrics vs Activity Explorer vs Content Explorer",
            "Add tooltips in UI showing last update time and refresh frequency"
        ],
        "Policy Status Definitions": [
            "Create new page: <span class='doc-page'>/purview/policy-distribution-status-reference</span>",
            "Define each status: Pending, Distributing, Success, Error",
            "Document expected time in each status by policy type",
            "Add troubleshooting flowchart for policies stuck 30+ days",
            "Provide PowerShell commands to check detailed distribution status"
        ],
        "Size & Scale Limits": [
            "Create new page: <span class='doc-page'>/purview/service-limits-dlp-classification</span>",
            "Document file size limits by workload (Exchange: XMB, SharePoint: YMB, etc.)",
            "Add record/row count limits for SIT detection",
            "Explain performance degradation with large files",
            "Provide workarounds: EDM for large datasets, file splitting strategies"
        ],
        "Configuration Examples": [
            "Create GitHub repo: <span class='doc-page'>microsoft/purview-samples</span>",
            "Add complete XML examples for: lead digit replacement, checksum algorithms",
            "Include commented code explaining each XML element",
            "Provide test data and validation scripts",
            "Add regex pattern library with common use cases"
        ],
        "URL Matching Logic": [
            "Create new page: <span class='doc-page'>/purview/endpoint-dlp-url-matching</span>",
            "Explain how query parameters are handled (ignored vs matched)",
            "Document wildcard behavior and limitations",
            "Add security implications of parent domain whitelisting",
            "Provide examples: Microsoft services (Copilot, Teams, etc.)"
        ],
        "Feature Scope & Timing": [
            "Add prominent callouts on <span class='doc-page'>/purview/apply-sensitivity-label-automatically</span>",
            "Clarify Exchange auto-labeling: in-transit only, not existing mailbox content",
            "Explain simulation vs actual deployment behavior differences",
            "Add timeline diagrams showing when labels are applied",
            "Update UI text during policy creation to show scope"
        ],
        "DLP Conditions Behavior": [
            "Expand <span class='doc-page'>/purview/dlp-conditions-actions-reference</span>",
            "Add for each condition: what it checks, data source (metadata vs content)",
            "Create comparison table: Exchange vs SharePoint vs OneDrive condition behavior",
            "Include screenshots showing where condition data comes from",
            "Add flowcharts for condition evaluation order"
        ]
    }
    
    for theme, icm_list in sorted_themes[:8]:
        html += f"""
    <div class="section">
        <h2>{theme}</h2>
        <p><strong>Impact:</strong> {len(icm_list)} customer incidents</p>
        
        <h3>Customer Confusion Examples</h3>
        <table>
            <thead>
                <tr>
                    <th style="width: 12%;">ICM ID</th>
                    <th style="width: 40%;">Issue Title</th>
                    <th style="width: 28%;">Customer Question/Confusion</th>
                    <th style="width: 20%;">Team</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for icm in icm_list[:5]:  # Show top 5
            # Extract question snippet
            desc = icm.get('description', '')
            question = ""
            if 'cannot find' in desc.lower():
                question = "Cannot find documentation"
            elif '?' in desc[:500]:
                q_idx = desc[:500].find('?')
                question = desc[max(0, q_idx-60):q_idx+1].strip().replace('\n', ' ')[:80] + "..."
            elif 'expected' in desc.lower()[:500]:
                question = "Expected behavior unclear"
            else:
                question = "Documentation gap"
            
            team_short = icm['owning_team'].split('\\')[-1] if '\\' in icm['owning_team'] else icm['owning_team']
            title_short = icm['title'][:60] + "..." if len(icm['title']) > 60 else icm['title']
            
            html += f"""
                <tr>
                    <td><a href="https://portal.microsofticm.com/imp/v3/incidents/details/{icm['id']}" target="_blank">{icm['id']}</a></td>
                    <td>{title_short}</td>
                    <td>{question}</td>
                    <td>{team_short}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
        
        <h3>Required Actions</h3>
        <div class="action-list">
            <ol>
"""
        
        actions = actions_map.get(theme, ["Update relevant documentation", "Add examples and clarifications"])
        for action in actions:
            html += f"                <li>{action}</li>\n"
        
        html += """
            </ol>
        </div>
    </div>
"""
    
    # Implementation Roadmap
    html += """
    <div class="section">
        <h2>Implementation Roadmap</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">Phase</th>
                    <th style="width: 15%;">Timeline</th>
                    <th style="width: 15%;">Effort</th>
                    <th style="width: 50%;">Deliverables</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Phase 1: Quick Wins</strong></td>
                    <td>1-2 weeks</td>
                    <td>Low</td>
                    <td>
                        • Add FAQ sections to existing pages<br>
                        • Create status definitions page<br>
                        • Add tooltips in UI<br>
                        • Update license comparison table
                    </td>
                </tr>
                <tr>
                    <td><strong>Phase 2: New Reference Pages</strong></td>
                    <td>2-4 weeks</td>
                    <td>Medium</td>
                    <td>
                        • Create portal metrics reference<br>
                        • Create service limits page<br>
                        • Create URL matching guide<br>
                        • Expand conditions documentation
                    </td>
                </tr>
                <tr>
                    <td><strong>Phase 3: Examples & Samples</strong></td>
                    <td>1-2 months</td>
                    <td>Medium-High</td>
                    <td>
                        • Create GitHub samples repository<br>
                        • Add XML examples with comments<br>
                        • Create regex pattern library<br>
                        • Add video walkthroughs
                    </td>
                </tr>
                <tr>
                    <td><strong>Phase 4: Product Enhancements</strong></td>
                    <td>2-3 months</td>
                    <td>High</td>
                    <td>
                        • UI improvements (validation, warnings)<br>
                        • In-product guidance<br>
                        • Enhanced portal displays<br>
                        • Interactive configuration tools
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>Documentation Pages to Create or Update</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 40%;">Documentation Page</th>
                    <th style="width: 15%;">Action</th>
                    <th style="width: 15%;">Priority</th>
                    <th style="width: 30%;">Key Content</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="doc-page">/purview/portal-metrics-reference</span></td>
                    <td>CREATE NEW</td>
                    <td><span class="priority-high">HIGH</span></td>
                    <td>Refresh intervals, metric definitions, known limitations</td>
                </tr>
                <tr>
                    <td><span class="doc-page">/purview/policy-distribution-status-reference</span></td>
                    <td>CREATE NEW</td>
                    <td><span class="priority-high">HIGH</span></td>
                    <td>Status definitions, expected durations, troubleshooting</td>
                </tr>
                <tr>
                    <td><span class="doc-page">/purview/service-limits-dlp-classification</span></td>
                    <td>CREATE NEW</td>
                    <td><span class="priority-high">HIGH</span></td>
                    <td>File size limits, record counts, performance thresholds</td>
                </tr>
                <tr>
                    <td><span class="doc-page">/purview/endpoint-dlp-url-matching</span></td>
                    <td>CREATE NEW</td>
                    <td><span class="priority-high">HIGH</span></td>
                    <td>URL matching logic, query parameters, wildcard behavior</td>
                </tr>
                <tr>
                    <td><span class="doc-page">/purview/dlp-licensing</span></td>
                    <td>UPDATE</td>
                    <td><span class="priority-high">HIGH</span></td>
                    <td>Add comprehensive license comparison table</td>
                </tr>
                <tr>
                    <td><span class="doc-page">/purview/dlp-conditions-actions-reference</span></td>
                    <td>ENHANCE</td>
                    <td><span class="priority-medium">MEDIUM</span></td>
                    <td>Expand each condition with data sources and examples</td>
                </tr>
                <tr>
                    <td><span class="doc-page">/purview/apply-sensitivity-label-automatically</span></td>
                    <td>UPDATE</td>
                    <td><span class="priority-medium">MEDIUM</span></td>
                    <td>Add scope clarifications (in-transit vs at-rest)</td>
                </tr>
                <tr>
                    <td><span class="doc-page">GitHub: microsoft/purview-samples</span></td>
                    <td>CREATE NEW</td>
                    <td><span class="priority-medium">MEDIUM</span></td>
                    <td>Code samples, XML examples, test data</td>
                </tr>
            </tbody>
        </table>
    </div>
    
</div>
</body>
</html>
"""
    
    # Save HTML
    report_file = Path(__file__).parent / "reports" / f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Executive summary report generated: {report_file}")
    return report_file


if __name__ == "__main__":
    print("="*80)
    print("GENERATING EXECUTIVE SUMMARY HTML REPORT")
    print("="*80)
    print()
    
    report_file = generate_executive_summary_html()
    
    print()
    print("="*80)
    print("✅ COMPLETE")
    print("="*80)
