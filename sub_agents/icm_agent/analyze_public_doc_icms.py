"""
Public Documentation Gap Analysis - ICM Deep Dive

This script analyzes ICMs flagged with prevention type "Public Documentation"
to identify common themes and documentation gaps in MIP/DLP.

Author: Carter Ryan
Created: February 11, 2026
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re

def extract_keywords(text):
    """Extract key technical terms from incident descriptions"""
    if not text:
        return []
    
    # Common MIP/DLP technical keywords
    keywords_patterns = [
        r'sensitivity label[s]?',
        r'DLP',
        r'data loss prevention',
        r'encryption',
        r'decryption',
        r'rights management',
        r'RMS',
        r'Azure Information Protection',
        r'AIP',
        r'policy[ies]?',
        r'classifier[s]?',
        r'EDM',
        r'exact data match',
        r'file explorer',
        r'office app[s]?',
        r'outlook',
        r'teams',
        r'sharepoint',
        r'onedrive',
        r'exchange',
        r'auto-label[ing]?',
        r'manual label[ing]?',
        r'default label[s]?',
        r'mandatory label[ing]?',
        r'downgrade[ing]?',
        r'removal',
        r'protection',
        r'unprotect',
        r'metadata',
        r'custom permission[s]?',
        r'co-author[ing]?',
        r'inheritance',
        r'container label[s]?',
        r'parent label[s]?',
        r'sub-label[s]?',
        r'scope[d]?',
        r'advanced classifier[s]?',
        r'trainable classifier[s]?',
        r'sensitive info type[s]?',
        r'SIT[s]?',
        r'confidence level[s]?',
        r'threshold[s]?',
        r'override[s]?',
        r'justification[s]?',
        r'audit[ing]?',
        r'activity explorer',
        r'content explorer',
        r'endpoint DLP',
        r'device[s]?',
        r'mac',
        r'windows',
        r'mobile',
        r'PDF',
        r'double key encryption',
        r'DKE',
        r'HYOK',
        r'tenant key',
        r'customer managed key[s]?',
        r'CMK',
    ]
    
    found_keywords = []
    text_lower = text.lower()
    
    for pattern in keywords_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        found_keywords.extend([m.lower() for m in matches])
    
    return list(set(found_keywords))


def categorize_incident(title, description, keywords):
    """Categorize incident into themes based on content analysis"""
    
    text = f"{title} {description}".lower()
    
    # Theme definitions
    themes = {
        "Label Visibility & Display": [
            "not visible", "not showing", "not appear", "not display", 
            "missing label", "label missing", "disappeared", "cannot see",
            "file explorer", "explorer", "right-click"
        ],
        "Encryption & Decryption": [
            "encrypt", "decrypt", "protection", "unprotect", "rights",
            "RMS", "rights management", "unable to open", "access denied",
            "permission", "co-author"
        ],
        "Auto-labeling & Classification": [
            "auto-label", "automatic", "classification", "classifier",
            "trainable", "EDM", "exact data match", "sensitive info type",
            "SIT", "not applied automatically", "not triggering"
        ],
        "Label Policy & Configuration": [
            "policy", "default label", "mandatory", "scope", "setting",
            "configuration", "applied to", "inheritance", "parent label",
            "sub-label", "container"
        ],
        "Label Modification & Downgrade": [
            "downgrade", "removal", "remove label", "change label",
            "override", "justification", "cannot remove", "cannot change",
            "cannot downgrade"
        ],
        "Application-specific Issues": [
            "outlook", "teams", "sharepoint", "onedrive", "office",
            "word", "excel", "powerpoint", "PDF", "app"
        ],
        "Endpoint DLP": [
            "endpoint", "device", "windows", "mac", "mobile",
            "upload", "copy", "print", "USB"
        ],
        "Audit & Reporting": [
            "audit", "activity explorer", "content explorer", "report",
            "log", "tracking", "monitor"
        ],
        "Key Management": [
            "double key", "DKE", "HYOK", "tenant key", "customer managed",
            "CMK", "key"
        ]
    }
    
    categorized_themes = []
    
    for theme, indicators in themes.items():
        for indicator in indicators:
            if indicator in text:
                categorized_themes.append(theme)
                break
    
    # If no theme found, mark as "Other"
    if not categorized_themes:
        categorized_themes.append("Other/Uncategorized")
    
    return categorized_themes


def analyze_icm_data():
    """Main analysis function"""
    
    print("="*80)
    print("PUBLIC DOCUMENTATION GAP ANALYSIS - ICM DEEP DIVE")
    print("="*80)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # ICM IDs to analyze
    icm_ids = [
        730972455, 730867091, 730194018, 729156307, 726209001, 724698812,
        724468498, 724141777, 723572770, 723508987, 722954497, 721238221,
        719793969, 719718596, 716201243, 714797265, 713750747, 713662994,
        712476914, 711972349, 709524522, 706301319, 703921423, 700706744,
        700569939, 700114735, 693130111, 691533110, 681612161, 667236540
    ]
    
    print(f"📊 Analyzing {len(icm_ids)} ICMs flagged as 'Public Documentation' prevention type")
    print()
    
    # Data directory for storing ICM details
    data_dir = Path(__file__).parent / "data" / "public_doc_icms"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Read ICM data from MCP results
    # The data is stored in the temp files from the MCP calls
    icm_data = []
    
    print("📂 Loading ICM data from MCP results...")
    temp_dir = Path(r"c:\Users\carterryan\AppData\Roaming\Code\User\workspaceStorage\03d22f79047fa29145a8c56d4247ce7c\GitHub.copilot-chat\chat-session-resources\0b3a52cb-5056-42f6-b403-95846ca4b223")
    
    # Find all content.json files from today's session
    content_files = sorted(temp_dir.glob("toolu_*__vscode-*/content.json"))
    
    if not content_files:
        print("⚠️ No ICM data files found. Please ensure ICM data was fetched.")
        return
    
    print(f"✓ Found {len(content_files)} ICM data files")
    
    # Parse each ICM
    icm_ids_processed = set()
    for idx, content_file in enumerate(content_files):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Skip if we already processed this ICM
                icm_id = data.get('id')
                if icm_id in icm_ids_processed or icm_id is None:
                    continue
                icm_ids_processed.add(icm_id)
                
                # Extract summary text and strip HTML tags
                summary_html = data.get('summary', '')
                # Basic HTML tag stripping - more robust than regex
                import html
                from html.parser import HTMLParser
                class MLStripper(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.reset()
                        self.strict = False
                        self.convert_charrefs = True
                        self.text = []
                    def handle_data(self, d):
                        self.text.append(d)
                    def get_data(self):
                        return ''.join(self.text)
                
                stripper = MLStripper()
                stripper.feed(summary_html)
                description_text = stripper.get_data()
                
                # Extract relevant fields
                icm_info = {
                    'id': icm_id,
                    'title': data.get('title', ''),
                    'description': description_text,
                    'severity': data.get('severity'),
                    'status': data.get('state'),
                    'owning_team': data.get('owningTeamName', ''),
                    'create_date': data.get('createdDate'),
                    'modified_date': data.get('lastModifiedDate'),
                    'resolution': data.get('howFixed', ''),
                    'resolution_code': '',
                    'source': data.get('type', ''),
                    'customer': data.get('impactedCustomers', [{}])[0].get('customerName', '') if data.get('impactedCustomers') else '',
                }
                
                # Extract keywords
                keywords = extract_keywords(f"{icm_info['title']} {icm_info['description']}")
                icm_info['keywords'] = keywords
                
                # Categorize into themes
                themes = categorize_incident(icm_info['title'], icm_info['description'], keywords)
                icm_info['themes'] = themes
                
                icm_data.append(icm_info)
                
        except Exception as e:
            print(f"⚠️ Error processing {content_file.name}: {e}")
            continue
    
    print(f"✓ Successfully parsed {len(icm_data)} ICMs")
    print()
    
    # Save combined ICM data
    combined_file = data_dir / "icm_details_with_themes.json"
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(icm_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved detailed ICM data to: {combined_file}")
    print()
    
    # Analyze themes
    print("="*80)
    print("THEME ANALYSIS")
    print("="*80)
    print()
    
    theme_to_icms = defaultdict(list)
    
    for icm in icm_data:
        for theme in icm['themes']:
            theme_to_icms[theme].append(icm)
    
    # Sort themes by frequency
    sorted_themes = sorted(theme_to_icms.items(), key=lambda x: len(x[1]), reverse=True)
    
    print(f"📈 Identified {len(sorted_themes)} distinct themes:")
    print()
    
    for theme, incidents in sorted_themes:
        print(f"🔸 {theme}: {len(incidents)} incidents")
    
    print()
    
    # Generate detailed report
    report_file = Path(__file__).parent / "reports" / f"public_doc_gap_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Public Documentation Gap Analysis\n")
        f.write(f"## ICM Deep Dive - Prevention Type: Public Documentation\n\n")
        f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total ICMs Analyzed:** {len(icm_data)}\n\n")
        f.write(f"**Themes Identified:** {len(sorted_themes)}\n\n")
        
        f.write("---\n\n")
        f.write("## Executive Summary\n\n")
        f.write(f"This analysis examines {len(icm_data)} ICMs that were resolved as 'By Design' with ")
        f.write("prevention type 'Public Documentation', indicating these incidents represent gaps ")
        f.write("in customer understanding that could be addressed through better documentation.\n\n")
        
        f.write("### Top Documentation Gap Areas:\n\n")
        for i, (theme, incidents) in enumerate(sorted_themes[:5], 1):
            pct = (len(incidents) / len(icm_data)) * 100
            f.write(f"{i}. **{theme}** - {len(incidents)} incidents ({pct:.1f}%)\n")
        
        f.write("\n---\n\n")
        f.write("## Detailed Theme Analysis\n\n")
        
        for theme, incidents in sorted_themes:
            f.write(f"### {theme}\n\n")
            f.write(f"**Incident Count:** {len(incidents)}\n\n")
            f.write(f"**% of Total:** {(len(incidents) / len(icm_data)) * 100:.1f}%\n\n")
            
            # Count by team
            teams = defaultdict(int)
            for icm in incidents:
                teams[icm['owning_team']] += 1
            
            f.write("**Affected Teams:**\n\n")
            for team, count in sorted(teams.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {team}: {count} incidents\n")
            f.write("\n")
            
            # Common keywords
            all_keywords = []
            for icm in incidents:
                all_keywords.extend(icm['keywords'])
            
            keyword_counts = defaultdict(int)
            for kw in all_keywords:
                keyword_counts[kw] += 1
            
            top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            if top_keywords:
                f.write("**Common Keywords:**\n\n")
                for kw, count in top_keywords:
                    f.write(f"- `{kw}` ({count} occurrences)\n")
                f.write("\n")
            
            # List incidents in this theme
            f.write("**Related ICMs:**\n\n")
            f.write("| ICM ID | Title | Severity | Team | Customer |\n")
            f.write("|--------|-------|----------|------|----------|\n")
            
            for icm in incidents[:20]:  # Limit to first 20
                title_short = icm['title'][:60] + "..." if len(icm['title']) > 60 else icm['title']
                team_short = icm['owning_team'].split('\\')[-1] if '\\' in icm['owning_team'] else icm['owning_team']
                customer_short = icm['customer'][:20] + "..." if len(icm['customer']) > 20 else icm['customer']
                
                f.write(f"| [{icm['id']}](https://portal.microsofticm.com/imp/v3/incidents/details/{icm['id']}) | ")
                f.write(f"{title_short} | {icm['severity']} | {team_short} | {customer_short} |\n")
            
            if len(incidents) > 20:
                f.write(f"\n*... and {len(incidents) - 20} more incidents*\n")
            
            f.write("\n")
            
            # Documentation recommendations
            f.write("#### 📝 Documentation Recommendations\n\n")
            f.write("Based on the incident patterns in this theme, consider:\n\n")
            f.write("- [ ] Create or enhance documentation covering this topic\n")
            f.write("- [ ] Add troubleshooting guide with common scenarios\n")
            f.write("- [ ] Include FAQ section addressing frequent questions\n")
            f.write("- [ ] Add step-by-step configuration examples\n")
            f.write("- [ ] Create video walkthrough if applicable\n")
            f.write("- [ ] Update support articles with clear explanations\n")
            f.write("\n---\n\n")
        
        # Add appendix with all ICMs
        f.write("## Appendix: Complete ICM List\n\n")
        f.write("| ICM ID | Title | Themes | Severity | Team |\n")
        f.write("|--------|-------|--------|----------|------|\n")
        
        for icm in sorted(icm_data, key=lambda x: x.get('id', 0) or 0, reverse=True):
            title_short = icm['title'][:50] + "..." if len(icm['title']) > 50 else icm['title']
            themes_str = ", ".join(icm['themes'][:2])  # First 2 themes
            team_short = icm['owning_team'].split('\\')[-1] if '\\' in icm['owning_team'] else icm['owning_team']
            
            f.write(f"| [{icm['id']}](https://portal.microsofticm.com/imp/v3/incidents/details/{icm['id']}) | ")
            f.write(f"{title_short} | {themes_str} | {icm['severity']} | {team_short} |\n")
        
        f.write("\n")
        
    print(f"📄 Generated detailed report: {report_file}")
    print()
    
    # Generate HTML report
    html_file = report_file.with_suffix('.html')
    generate_html_report(sorted_themes, icm_data, html_file)
    print(f"🌐 Generated HTML report: {html_file}")
    print()
    
    print("="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)


def generate_html_report(sorted_themes, icm_data, output_file):
    """Generate interactive HTML report"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Public Documentation Gap Analysis</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
            margin-top: 10px;
        }}
        .summary {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-card .number {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-card .label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .theme-section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .theme-section h2 {{
            color: #667eea;
            margin-top: 0;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .theme-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .theme-badge {{
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #495057;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        a {{
            color: #667eea;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .keyword-tag {{
            display: inline-block;
            background: #e7f3ff;
            color: #0066cc;
            padding: 4px 10px;
            margin: 3px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        .recommendation {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
        }}
        .recommendation h4 {{
            margin-top: 0;
            color: #856404;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Public Documentation Gap Analysis</h1>
        <div class="subtitle">ICM Deep Dive - Prevention Type: Public Documentation</div>
        <div class="subtitle">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>
    
    <div class="summary">
        <h2>📊 Analysis Summary</h2>
        <p>This analysis examines ICMs resolved as "By Design" with prevention type "Public Documentation", 
        indicating opportunities to improve customer understanding through better documentation.</p>
        
        <div class="stat-grid">
            <div class="stat-card">
                <div class="number">{len(icm_data)}</div>
                <div class="label">Total ICMs</div>
            </div>
            <div class="stat-card">
                <div class="number">{len(sorted_themes)}</div>
                <div class="label">Themes Identified</div>
            </div>
            <div class="stat-card">
                <div class="number">{len([icm for icm in icm_data if icm.get('severity') in [2, 3]])}</div>
                <div class="label">High Impact (Sev 2-3)</div>
            </div>
            <div class="stat-card">
                <div class="number">{len(set([icm.get('customer', '') for icm in icm_data if icm.get('customer')]))}</div>
                <div class="label">Unique Customers</div>
            </div>
        </div>
    </div>
"""
    
    # Add theme sections
    for theme, incidents in sorted_themes:
        pct = (len(incidents) / len(icm_data)) * 100
        
        # Count teams
        teams = defaultdict(int)
        for icm in incidents:
            teams[icm['owning_team']] += 1
        
        # Get keywords
        all_keywords = []
        for icm in incidents:
            all_keywords.extend(icm['keywords'])
        keyword_counts = defaultdict(int)
        for kw in all_keywords:
            keyword_counts[kw] += 1
        top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        
        html_content += f"""
    <div class="theme-section">
        <div class="theme-header">
            <h2>{theme}</h2>
            <span class="theme-badge">{len(incidents)} incidents ({pct:.1f}%)</span>
        </div>
        
        <p><strong>Affected Teams:</strong></p>
        <ul>
"""
        for team, count in sorted(teams.items(), key=lambda x: x[1], reverse=True)[:5]:
            team_short = team.split('\\')[-1] if '\\' in team else team
            html_content += f"            <li>{team_short}: {count} incidents</li>\n"
        
        html_content += "        </ul>\n"
        
        if top_keywords:
            html_content += "        <p><strong>Common Keywords:</strong></p>\n        <div>\n"
            for kw, count in top_keywords:
                html_content += f'            <span class="keyword-tag">{kw} ({count})</span>\n'
            html_content += "        </div>\n"
        
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>ICM ID</th>
                    <th>Title</th>
                    <th>Severity</th>
                    <th>Team</th>
                    <th>Customer</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for icm in incidents[:15]:  # Show top 15
            title_short = icm['title'][:80] + "..." if len(icm['title']) > 80 else icm['title']
            team_short = icm['owning_team'].split('\\')[-1] if '\\' in icm['owning_team'] else icm['owning_team']
            customer_short = icm['customer'][:30] + "..." if len(icm['customer']) > 30 else icm['customer']
            
            html_content += f"""                <tr>
                    <td><a href="https://portal.microsofticm.com/imp/v3/incidents/details/{icm['id']}" target="_blank">{icm['id']}</a></td>
                    <td>{title_short}</td>
                    <td>{icm['severity']}</td>
                    <td>{team_short}</td>
                    <td>{customer_short}</td>
                </tr>
"""
        
        if len(incidents) > 15:
            html_content += f"                <tr><td colspan='5'><em>... and {len(incidents) - 15} more incidents</em></td></tr>\n"
        
        html_content += """            </tbody>
        </table>
        
        <div class="recommendation">
            <h4>📝 Documentation Recommendations</h4>
            <ul>
                <li>Create or enhance documentation covering this topic</li>
                <li>Add troubleshooting guide with common scenarios</li>
                <li>Include FAQ section addressing frequent questions</li>
                <li>Add step-by-step configuration examples with screenshots</li>
                <li>Consider video walkthrough for complex scenarios</li>
            </ul>
        </div>
    </div>
"""
    
    html_content += """
    <div class="footer">
        <p>Generated by PHEPy ICM Analysis Tool</p>
        <p>For questions or feedback, contact the Purview Engineering team</p>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == "__main__":
    analyze_icm_data()
