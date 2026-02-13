"""
Enhanced Documentation Gap Analysis with Specific Customer Questions
Extracts actual customer questions and confusion points from ICM descriptions

Author: Carter Ryan
Created: February 11, 2026
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def extract_customer_questions(icm):
    """Extract actual customer questions and confusion from ICM"""
    desc = icm.get('description', '')
    title = icm.get('title', '')
    
    questions = []
    confusion_points = []
    
    # Extract questions
    question_patterns = [
        r'["\']([^"\']*\?)["\']',  # Questions in quotes
        r'(?:question|ask|clarification|confirm|help).{0,20}:\s*([^.!]{10,200}\?)',  # After "question:", "ask:", etc.
        r'(?:customer|cx|client).{0,30}(?:ask|want|need|report).{0,30}:([^.!]{10,200})',
        r'(?:why|how|what|when|where|which|can|does|is|are).{10,150}\?',  # Direct questions
    ]
    
    for pattern in question_patterns:
        matches = re.findall(pattern, desc, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0] if match else ""
            match = match.strip()
            if len(match) > 20 and match not in questions:
                questions.append(match)
    
    # Extract confusion points
    confusion_indicators = [
        r'(?:confus|unclear|not clear|doesn\'t understand|cannot find|missing|gap).{10,200}',
        r'(?:expected|thought|assume).{10,100}(?:but|however).{10,100}',
        r'(?:documentation|doc|article).{0,30}(?:doesn\'t|does not|missing|no information).{10,150}',
    ]
    
    for pattern in confusion_indicators:
        matches = re.findall(pattern, desc, re.IGNORECASE)
        for match in matches:
            match = match.strip()
            if len(match) > 20 and match not in confusion_points:
                confusion_points.append(match)
    
    return questions[:5], confusion_points[:5]  # Limit to top 5 each


def extract_expected_vs_actual(desc):
    """Extract expected vs actual behavior from description"""
    expected = ""
    actual = ""
    
    # Look for Expected behavior
    expected_patterns = [
        r'expected(?:\s+behavior)?:\s*([^.!]{20,300})',
        r'expected:\s*([^.!]{20,300})',
        r'customer(?:\'s)? expectation:\s*([^.!]{20,300})',
        r'should(?:\s+be)?:\s*([^.!]{20,300})',
    ]
    
    for pattern in expected_patterns:
        match = re.search(pattern, desc, re.IGNORECASE)
        if match:
            expected = match.group(1).strip()
            break
    
    # Look for Actual behavior
    actual_patterns = [
        r'actual(?:\s+behavior)?:\s*([^.!]{20,300})',
        r'current(?:\s+behavior)?:\s*([^.!]{20,300})',
        r'(?:however|but),?\s*([^.!]{20,300})',
        r'issue:\s*([^.!]{20,300})',
    ]
    
    for pattern in actual_patterns:
        match = re.search(pattern, desc, re.IGNORECASE)
        if match:
            actual = match.group(1).strip()
            break
    
    return expected, actual


def generate_enhanced_report(icms, output_file):
    """Generate enhanced report with specific customer details"""
    
    # Group ICMs by major themes
    theme_groups = {
        "Licensing & Feature Availability": [],
        "Portal Metrics & Data Visibility": [],
        "Policy Status & Distribution": [],
        "Size Limits & Scale": [],
        "Configuration & Examples": [],
        "URL Matching & Whitelisting": [],
        "Feature Scope & Timing": [],
        "UI/UX & Validation": [],
        "Conditions & Rules Behavior": [],
        "Notifications & Alerts": []
    }
    
    # Categorize ICMs
    for icm in icms:
        desc = icm.get('description', '').lower()
        title = icm.get('title', '').lower()
        combined = f"{title} {desc}"
        
        if any(x in combined for x in ['license', 'licensing', 'e5', 'e3', 'add-on', 'coverage']):
            theme_groups["Licensing & Feature Availability"].append(icm)
        
        if any(x in combined for x in ['metric', 'portal', 'dashboard', 'files labeled', 'activity explorer', 'content explorer']):
            theme_groups["Portal Metrics & Data Visibility"].append(icm)
        
        if 'pending' in combined and ('distribution' in combined or 'status' in combined):
            theme_groups["Policy Status & Distribution"].append(icm)
        
        if any(x in combined for x in ['size', 'limit', 'maximum', 'scale', 'large', 'thousands', 'volume']):
            theme_groups["Size Limits & Scale"].append(icm)
        
        if any(x in combined for x in ['example', 'sample', 'xml', 'regex', 'pattern', 'checksum']):
            theme_groups["Configuration & Examples"].append(icm)
        
        if any(x in combined for x in ['url', 'whitelist', 'domain', 'query parameter']):
            theme_groups["URL Matching & Whitelisting"].append(icm)
        
        if any(x in combined for x in ['scope', 'in-transit', 'at-rest', 'simulation', 'when', 'timing']):
            theme_groups["Feature Scope & Timing"].append(icm)
        
        if any(x in combined for x in ['ui', 'ux', 'mutually exclusive', 'disable', 'option']):
            theme_groups["UI/UX & Validation"].append(icm)
        
        if 'condition' in combined and any(x in combined for x in ['dlp', 'rule', 'behavior', 'check']):
            theme_groups["Conditions & Rules Behavior"].append(icm)
        
        if any(x in combined for x in ['notification', 'email', 'alert', 'multiple']):
            theme_groups["Notifications & Alerts"].append(icm)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Enhanced Documentation Gap Analysis\n")
        f.write("## Detailed Customer Questions & Confusion Points\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**ICMs Analyzed:** {len(icms)}\n\n")
        f.write("---\n\n")
        
        f.write("## 🎯 Executive Summary\n\n")
        f.write("This analysis extracts **actual customer questions and confusion points** from ICM descriptions ")
        f.write("to identify specific documentation gaps. Each section includes:\n\n")
        f.write("- **Real Customer Questions** - Actual questions asked by customers\n")
        f.write("- **Confusion Points** - What customers misunderstood or couldn't find\n")
        f.write("- **Expected vs Actual** - What customers expected vs what happened\n")
        f.write("- **Specific Documentation Needs** - Exactly what content is missing\n\n")
        f.write("---\n\n")
        
        # Process each theme
        for theme, icm_list in theme_groups.items():
            if not icm_list:
                continue
            
            f.write(f"## 📋 {theme}\n\n")
            f.write(f"**ICMs in this category:** {len(icm_list)}\n\n")
            
            for icm in icm_list:
                f.write(f"### ICM [{icm['id']}](https://portal.microsofticm.com/imp/v3/incidents/details/{icm['id']})\n\n")
                f.write(f"**Title:** {icm['title']}\n\n")
                f.write(f"**Team:** {icm['owning_team']}\n\n")
                
                # Extract customer questions
                questions, confusion = extract_customer_questions(icm)
                
                if questions:
                    f.write("#### ❓ Customer Questions\n\n")
                    for q in questions:
                        f.write(f"- {q}\n")
                    f.write("\n")
                
                # Expected vs Actual
                expected, actual = extract_expected_vs_actual(icm.get('description', ''))
                
                if expected or actual:
                    f.write("#### 🔍 Expected vs Actual\n\n")
                    if expected:
                        f.write(f"**Expected:** {expected}\n\n")
                    if actual:
                        f.write(f"**Actual:** {actual}\n\n")
                
                if confusion:
                    f.write("#### 😕 Confusion Points\n\n")
                    for c in confusion[:3]:  # Limit to 3
                        f.write(f"- {c}\n")
                    f.write("\n")
                
                # Extract key issues from description
                desc = icm.get('description', '')
                
                # Look for "Issue:" or "Problem:" sections
                issue_match = re.search(r'(?:Issue|Problem):\s*(.{50,500})', desc, re.IGNORECASE)
                if issue_match:
                    issue_text = issue_match.group(1).strip()
                    # Clean up and truncate
                    issue_text = re.sub(r'\s+', ' ', issue_text)
                    if len(issue_text) > 300:
                        issue_text = issue_text[:297] + "..."
                    f.write(f"#### 📝 Issue Summary\n\n")
                    f.write(f"{issue_text}\n\n")
                
                # What's missing in documentation
                f.write("#### 📖 What's Missing in Current Documentation\n\n")
                
                desc_lower = desc.lower()
                title_lower = icm['title'].lower()
                combined = f"{title_lower} {desc_lower}"
                
                if 'license' in combined:
                    f.write("**Missing Content:**\n")
                    f.write("- Clear license comparison showing which features are included in each tier\n")
                    f.write("- Specific coverage for Teams chat vs Teams files\n")
                    f.write("- License requirements for each workload and feature\n\n")
                    f.write("**Where to Add:**\n")
                    f.write("- `/purview/dlp-licensing` - Add comprehensive comparison table\n")
                    f.write("- `/purview/dlp-microsoft-teams` - Add license requirements section\n")
                    f.write("- Add FAQ: \"Which license do I need for Teams DLP?\"\n\n")
                
                elif 'metric' in combined or 'files labeled' in combined or 'portal' in combined:
                    f.write("**Missing Content:**\n")
                    f.write("- Refresh intervals for portal metrics (how often data updates)\n")
                    f.write("- Why metrics might show 0 temporarily\n")
                    f.write("- Difference between portal metrics and Activity Explorer data\n")
                    f.write("- Expected delays and data consistency information\n\n")
                    f.write("**Where to Add:**\n")
                    f.write("- Create new page: `/purview/portal-metrics-reference`\n")
                    f.write("- Add tooltips in UI next to each metric\n")
                    f.write("- `/purview/auto-labeling-policies` - Add \"Understanding Metrics\" section\n\n")
                
                elif 'pending' in combined and 'distribution' in combined:
                    f.write("**Missing Content:**\n")
                    f.write("- Definition of each policy status (Pending, Distributing, Success, Error)\n")
                    f.write("- Expected time in each status\n")
                    f.write("- When 30+ days pending is normal vs concerning\n")
                    f.write("- Troubleshooting steps for stuck policies\n\n")
                    f.write("**Where to Add:**\n")
                    f.write("- Create new page: `/purview/policy-distribution-status-reference`\n")
                    f.write("- `/purview/dlp-policy-design` - Add section on policy distribution\n")
                    f.write("- Add PowerShell examples to check policy status\n\n")
                
                elif 'url' in combined or 'whitelist' in combined:
                    f.write("**Missing Content:**\n")
                    f.write("- How URL matching works with query parameters\n")
                    f.write("- Wildcard behavior and limitations\n")
                    f.write("- When to whitelist parent domain vs specific URL\n")
                    f.write("- Security implications of broad whitelisting\n")
                    f.write("- Specific guidance for dynamic URLs (e.g., Copilot, Microsoft services)\n\n")
                    f.write("**Where to Add:**\n")
                    f.write("- `/purview/endpoint-dlp-using` - Add \"URL Matching Reference\" section\n")
                    f.write("- Create new page: `/purview/dlp-url-matching-guide`\n")
                    f.write("- Add examples for common Microsoft services\n\n")
                
                elif 'size' in combined or 'limit' in combined or 'large' in combined:
                    f.write("**Missing Content:**\n")
                    f.write("- File size limits by workload (Exchange, SharePoint, OneDrive)\n")
                    f.write("- Record/row count limits for SIT detection\n")
                    f.write("- How large files affect classification accuracy\n")
                    f.write("- Performance thresholds and degradation points\n")
                    f.write("- Workarounds for files exceeding limits\n\n")
                    f.write("**Where to Add:**\n")
                    f.write("- Create new page: `/purview/service-limits-dlp-classification`\n")
                    f.write("- `/purview/dlp-conditions-actions-reference` - Add limits section\n")
                    f.write("- Add warning in UI when policy may not work on large files\n\n")
                
                elif 'example' in combined or 'xml' in combined or 'checksum' in combined:
                    f.write("**Missing Content:**\n")
                    f.write("- Complete, working XML examples for advanced features\n")
                    f.write("- Commented code explaining each XML element\n")
                    f.write("- Common checksum algorithm implementations\n")
                    f.write("- Test data and validation scripts\n\n")
                    f.write("**Where to Add:**\n")
                    f.write("- Create GitHub repository: `microsoft/purview-samples`\n")
                    f.write("- `/purview/sit-custom-get-started` - Link to examples\n")
                    f.write("- Add interactive XML builder tool in documentation\n\n")
                
                elif 'scope' in combined or 'in-transit' in combined or 'simulation' in combined:
                    f.write("**Missing Content:**\n")
                    f.write("- Clear explanation of in-transit vs at-rest application\n")
                    f.write("- When auto-labeling applies (creation, modification, in-flight)\n")
                    f.write("- Simulation behavior vs actual deployment\n")
                    f.write("- Timeline expectations for label application\n\n")
                    f.write("**Where to Add:**\n")
                    f.write("- `/purview/apply-sensitivity-label-automatically` - Add prominent callout\n")
                    f.write("- `/purview/auto-labeling-exchange` - Clarify in-transit only behavior\n")
                    f.write("- Add UI text during policy creation explaining scope\n\n")
                
                elif 'condition' in combined:
                    f.write("**Missing Content:**\n")
                    f.write("- Detailed explanation of what each condition checks\n")
                    f.write("- Data source for each condition (file metadata vs content)\n")
                    f.write("- Behavior differences by workload (Exchange, SharePoint, OneDrive)\n")
                    f.write("- Matching logic and examples\n\n")
                    f.write("**Where to Add:**\n")
                    f.write("- `/purview/dlp-conditions-actions-reference` - Expand each condition\n")
                    f.write("- Add comparison table: Exchange vs SharePoint vs OneDrive conditions\n")
                    f.write("- Include screenshots showing where data comes from\n\n")
                
                else:
                    f.write("**Missing Content:**\n")
                    f.write("- Clear documentation addressing the specific scenario\n")
                    f.write("- Step-by-step examples\n")
                    f.write("- Troubleshooting guide for common issues\n\n")
                    f.write("**Where to Add:**\n")
                    f.write("- Update relevant feature documentation page\n")
                    f.write("- Add to FAQ section\n\n")
                
                f.write("---\n\n")
        
        # Add quick reference table
        f.write("## 📊 Quick Reference: Documentation Pages to Update\n\n")
        f.write("| Documentation Page | Updates Needed | Priority | ICMs |\n")
        f.write("|-------------------|----------------|----------|------|\n")
        
        doc_pages = {
            "/purview/dlp-licensing": ("Add license comparison table with Teams chat/file coverage", "🔴 HIGH"),
            "/purview/portal-metrics-reference": ("Create new page with refresh intervals and metric definitions", "🔴 HIGH"),
            "/purview/policy-distribution-status-reference": ("Create new page with status definitions and troubleshooting", "🔴 HIGH"),
            "/purview/dlp-url-matching-guide": ("Create new page explaining URL matching with examples", "🔴 HIGH"),
            "/purview/service-limits-dlp-classification": ("Create new page with all size and scale limits", "🟡 MEDIUM"),
            "/purview/dlp-conditions-actions-reference": ("Expand condition explanations with data sources and examples", "🟡 MEDIUM"),
            "/purview/apply-sensitivity-label-automatically": ("Add scope clarification (in-transit vs at-rest)", "🟡 MEDIUM"),
            "GitHub: microsoft/purview-samples": ("Create sample repository with XML examples and test data", "🟡 MEDIUM"),
        }
        
        for page, (update, priority) in doc_pages.items():
            f.write(f"| `{page}` | {update} | {priority} | Multiple |\n")
        
        f.write("\n")


def main():
    print("="*80)
    print("ENHANCED DOCUMENTATION GAP ANALYSIS")
    print("="*80)
    print()
    
    # Load ICM data
    data_file = Path(__file__).parent / "data" / "public_doc_icms" / "icm_details_with_themes.json"
    
    print(f"📂 Loading ICM data from: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        icms = json.load(f)
    
    print(f"✓ Loaded {len(icms)} ICMs")
    print()
    
    print("🔍 Extracting customer questions and confusion points...")
    
    # Generate report
    report_file = Path(__file__).parent / "reports" / f"enhanced_doc_gaps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    print("📝 Generating enhanced report with specific details...")
    generate_enhanced_report(icms, report_file)
    
    print(f"✅ Enhanced report generated: {report_file}")
    print()
    print("="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
