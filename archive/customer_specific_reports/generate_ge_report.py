#!/usr/bin/env python3
"""
Generate General Electric Purview Case History Report
"""
import json
from datetime import datetime
from pathlib import Path
from collections import Counter

# Load case data
with open("data/purview_case_history_GE_6mo.json", "r", encoding="utf-8") as f:
    content = f.read()
    if content.startswith("Query results:"):
        content = content.replace("Query results:", "").strip()
    data = json.loads(content)

cases = data["data"]

# Calculate metrics
total_cases = len(cases)
open_cases = [c for c in cases if c["ServiceRequestState"] == "Open"]
closed_cases = [c for c in cases if c["ServiceRequestState"] == "Closed"]
open_count = len(open_cases)
closed_count = len(closed_cases)

# Severity breakdown
sev_counts = Counter(c["ServiceRequestCurrentSeverity"] for c in cases)

# ICM escalations
with_icm = len([c for c in cases if c["RelatedICM_Id"] and c["RelatedICM_Id"] != ""])

# Averages
avg_days_open = round(sum(c["DaysOpen"] for c in open_cases) / len(open_cases), 1) if open_cases else 0
oldest_open = round(max((c["DaysOpen"] for c in open_cases), default=0), 1)
avg_ownership = round(sum(c["OwnershipCount"] for c in cases) / total_cases, 1)
avg_transfers = round(sum(c["TransferCount"] for c in cases) / total_cases, 1)

# Top 10 oldest
top_oldest = sorted(open_cases, key=lambda x: x["DaysOpen"], reverse=True)[:10]

# Product breakdown
product_counts = Counter(c["ProductName"] for c in cases)
top_products = product_counts.most_common(5)

# Agent distribution
agent_counts = Counter(c["AgentAlias"] for c in cases)
top_agents = agent_counts.most_common(5)

# Severity groups
sev_groups = {}
for c in cases:
    sev = c["ServiceRequestCurrentSeverity"]
    if sev not in sev_groups:
        sev_groups[sev] = []
    sev_groups[sev].append(c)

# Generate HTML
report_date = datetime.now().strftime("%B %d, %Y")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>General Electric Purview Case History - 6 Month Analysis</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px 40px;
            border-bottom: 4px solid #ffd700;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        
        .header .meta {{
            font-size: 14px;
            opacity: 0.8;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}
        
        .card h3 {{
            font-size: 14px;
            color: #555;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .card .value {{
            font-size: 36px;
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 5px;
        }}
        
        .card .label {{
            font-size: 13px;
            color: #666;
        }}
        
        .card.success {{
            border-left-color: #10b981;
        }}
        
        .card.warning {{
            border-left-color: #f59e0b;
        }}
        
        .card.danger {{
            border-left-color: #ef4444;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            font-size: 24px;
            color: #1e3c72;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e5e7eb;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        thead {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e5e7eb;
            font-size: 14px;
        }}
        
        tr:hover {{
            background-color: #f9fafb;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge.open {{
            background-color: #fef3c7;
            color: #92400e;
        }}
        
        .badge.closed {{
            background-color: #d1fae5;
            color: #065f46;
        }}
        
        .badge.sev-a {{
            background-color: #fee2e2;
            color: #991b1b;
        }}
        
        .badge.sev-b {{
            background-color: #fed7aa;
            color: #9a3412;
        }}
        
        .badge.sev-c {{
            background-color: #dbeafe;
            color: #1e40af;
        }}
        
        .case-link {{
            color: #2563eb;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .case-link:hover {{
            text-decoration: underline;
        }}
        
        .chart-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .chart-item {{
            background: #f9fafb;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
        }}
        
        .chart-item h4 {{
            font-size: 14px;
            color: #374151;
            margin-bottom: 10px;
        }}
        
        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .bar-row {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .bar-label {{
            min-width: 150px;
            font-size: 13px;
            color: #6b7280;
        }}
        
        .bar {{
            flex: 1;
            height: 24px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
            display: flex;
            align-items: center;
            padding: 0 8px;
            color: white;
            font-size: 12px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 General Electric Purview Case History</h1>
            <div class="subtitle">General Electric Co. - 6 Month Case Review</div>
            <div class="subtitle">Tenant: d584a4b7-b1f2-4714-a578-fd4d43c146a6</div>
            <div class="meta">
                <strong>Report Generated:</strong> {report_date}<br>
                <strong>Analysis Period:</strong> August 8, 2025 - February 6, 2026 (180 days)<br>
                <strong>Data Source:</strong> CxE Data Platform / GetSCIMIncidentV2
            </div>
        </div>
        
        <div class="content">
            <!-- Summary Cards -->
            <div class="summary-cards">
                <div class="card">
                    <h3>Total Cases</h3>
                    <div class="value">{total_cases}</div>
                    <div class="label">Last 6 months</div>
                </div>
                <div class="card danger">
                    <h3>Open Cases</h3>
                    <div class="value">{open_count}</div>
                    <div class="label">{round(open_count/total_cases*100,1) if total_cases else 0}% of total</div>
                </div>
                <div class="card success">
                    <h3>Closed Cases</h3>
                    <div class="value">{closed_count}</div>
                    <div class="label">{round(closed_count/total_cases*100,1) if total_cases else 0}% resolution rate</div>
                </div>
                <div class="card warning">
                    <h3>Avg Open Age</h3>
                    <div class="value">{avg_days_open}</div>
                    <div class="label">Days (oldest: {oldest_open} days)</div>
                </div>
                <div class="card">
                    <h3>Cases with ICM</h3>
                    <div class="value">{with_icm}</div>
                    <div class="label">{round(with_icm/total_cases*100,1) if total_cases else 0}% escalated</div>
                </div>
                <div class="card">
                    <h3>Avg Ownership</h3>
                    <div class="value">{avg_ownership}</div>
                    <div class="label">Transfers: {avg_transfers} avg</div>
                </div>
            </div>
            
            <!-- Top 10 Oldest Open Cases -->
            <div class="section">
                <h2>🚨 Top 10 Oldest Open Cases</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Case #</th>
                            <th>Title</th>
                            <th>Status</th>
                            <th>Sev</th>
                            <th>Age (Days)</th>
                            <th>Owner</th>
                            <th>ICM</th>
                        </tr>
                    </thead>
                    <tbody>
"""

for case in top_oldest:
    title = case["Title"][:80] + "..." if len(case["Title"]) > 80 else case["Title"]
    sev = case["ServiceRequestCurrentSeverity"]
    sev_class = f"sev-{sev.lower()}"
    has_icm = "✓" if case["RelatedICM_Id"] and case["RelatedICM_Id"] != "" else "-"
    days_open = round(case["DaysOpen"], 1)
    
    html += f"""                        <tr>
                            <td><a href="{case['CaseUri']}" class="case-link" target="_blank">{case['ServiceRequestNumber']}</a></td>
                            <td>{title}</td>
                            <td><span class="badge open">{case['ServiceRequestStatus']}</span></td>
                            <td><span class="badge {sev_class}">{sev}</span></td>
                            <td><strong>{days_open}</strong></td>
                            <td>{case['AgentAlias']}</td>
                            <td>{has_icm}</td>
                        </tr>
"""

html += """                    </tbody>
                </table>
            </div>
            
            <!-- Product & Agent Breakdown -->
            <div class="section">
                <h2>📈 Distribution Analysis</h2>
                <div class="chart-container">
                    <div class="chart-item">
                        <h4>Product Breakdown (Top 5)</h4>
                        <div class="bar-chart">
"""

for product, count in top_products:
    pct = round(count / total_cases * 100, 1)
    width = pct
    display_name = product.replace("Microsoft ", "")
    html += f"""                            <div class="bar-row">
                                <div class="bar-label">{display_name}</div>
                                <div class="bar" style="width: {width}%;">{count}</div>
                            </div>
"""

html += """                        </div>
                    </div>
                    <div class="chart-item">
                        <h4>Top Case Owners</h4>
                        <div class="bar-chart">
"""

for agent, count in top_agents:
    pct = round(count / total_cases * 100, 1)
    width = pct * 2
    html += f"""                            <div class="bar-row">
                                <div class="bar-label">{agent}</div>
                                <div class="bar" style="width: {width}%;">{count}</div>
                            </div>
"""

html += """                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Severity Distribution -->
            <div class="section">
                <h2>⚠️ Severity Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Severity</th>
                            <th>Count</th>
                            <th>Percentage</th>
                            <th>Open</th>
                            <th>Closed</th>
                        </tr>
                    </thead>
                    <tbody>
"""

for sev in sorted(sev_groups.keys()):
    sev_cases = sev_groups[sev]
    count = len(sev_cases)
    open_sev = len([c for c in sev_cases if c["ServiceRequestState"] == "Open"])
    closed_sev = len([c for c in sev_cases if c["ServiceRequestState"] == "Closed"])
    pct = round(count / total_cases * 100, 1)
    
    html += f"""                        <tr>
                            <td><span class="badge sev-{sev.lower()}">Severity {sev}</span></td>
                            <td><strong>{count}</strong></td>
                            <td>{pct}%</td>
                            <td>{open_sev}</td>
                            <td>{closed_sev}</td>
                        </tr>
"""

html += """                    </tbody>
                </table>
            </div>
            
            <!-- All Cases Table -->
            <div class="section">
                <h2>📋 All Cases (Most Recent First)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Case #</th>
                            <th>Title</th>
                            <th>State</th>
                            <th>Sev</th>
                            <th>Created</th>
                            <th>Days Open</th>
                            <th>Owner</th>
                        </tr>
                    </thead>
                    <tbody>
"""

# Sort by created time desc
sorted_cases = sorted(cases, key=lambda x: x["CreatedTime"], reverse=True)
for case in sorted_cases:
    title = case["Title"][:60] + "..." if len(case["Title"]) > 60 else case["Title"]
    state_class = "open" if case["ServiceRequestState"] == "Open" else "closed"
    sev = case["ServiceRequestCurrentSeverity"]
    sev_class = f"sev-{sev.lower()}"
    created = datetime.strptime(case["CreatedTime"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b %d, %Y")
    days_open = round(case["DaysOpen"], 1)
    
    html += f"""                        <tr>
                            <td><a href="{case['CaseUri']}" class="case-link" target="_blank">{case['ServiceRequestNumber']}</a></td>
                            <td>{title}</td>
                            <td><span class="badge {state_class}">{case['ServiceRequestState']}</span></td>
                            <td><span class="badge {sev_class}">{sev}</span></td>
                            <td>{created}</td>
                            <td>{days_open}</td>
                            <td>{case['AgentAlias']}</td>
                        </tr>
"""

html += """                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Save report
output_path = Path("risk_reports/GE_Purview_Case_History_6mo.htm")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Report generated: {output_path}")
print(f"   Total Cases: {total_cases}")
print(f"   Open: {open_count} | Closed: {closed_count}")
print(f"   Avg Open Age: {avg_days_open} days")
