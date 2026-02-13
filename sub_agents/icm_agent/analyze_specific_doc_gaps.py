"""
Specific Documentation Gap Analysis
Analyzes actual customer confusion from ICM descriptions to identify precise doc gaps

Author: Carter Ryan
Created: February 11, 2026
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def extract_specific_gaps(icms):
    """Extract specific documentation gaps from ICM descriptions"""
    
    gaps = {
        "Licensing & Feature Coverage": [],
        "Metrics & Portal Data": [],
        "Policy Distribution & Status": [],
        "Size Limits & Performance": [],
        "Configuration Examples": [],
        "URL & Pattern Matching": [],
        "Feature Scope & Behavior": [],
        "UI/UX Clarity": [],
        "Troubleshooting & Diagnostics": [],
        "API & Automation": []
    }
    
    for icm in icms:
        desc = icm.get('description', '').lower()
        title = icm.get('title', '').lower()
        combined = f"{title} {desc}"
        
        # Licensing gaps
        if any(x in combined for x in ['license', 'licensing', 'add-on', 'e5', 'e3', 'which license']):
            if 'teams' in combined and 'chat' in combined:
                gaps["Licensing & Feature Coverage"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'DLP for Teams licensing unclear - which license covers Teams chat vs files',
                    'current_state': 'No clear documentation on DLP coverage differences between E5 base and E5 Information Protection add-on for Teams chat messages',
                    'needed': 'License comparison table showing Teams chat, Teams files, and channel message coverage by license type'
                })
            elif 'coverage' in combined or 'cover' in combined:
                gaps["Licensing & Feature Coverage"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'Feature coverage by license unclear',
                    'current_state': 'Documentation does not clearly map features to license types',
                    'needed': 'Comprehensive license-to-feature matrix with workload coverage'
                })
        
        # Metrics and portal data
        if any(x in combined for x in ['metric', 'portal', 'dashboard', 'activity explorer', 'content explorer']):
            if 'files labeled' in combined or 'files to' in combined or 'value' in combined and ('0' in combined or 'zero' in combined):
                gaps["Metrics & Portal Data"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'Auto-labeling portal metrics reliability not documented',
                    'current_state': 'No documentation on metric update frequency, accuracy, or known limitations',
                    'needed': 'Clear documentation on: 1) How often metrics refresh 2) Why counts may show 0 temporarily 3) Difference between portal metrics vs Activity Explorer 4) Known delays/limitations'
                })
            elif 'delay' in combined or 'update' in combined:
                gaps["Metrics & Portal Data"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'Data refresh timing not documented',
                    'current_state': 'No information on expected delays for portal data',
                    'needed': 'Service-level timing documentation for each portal/report type'
                })
        
        # Policy distribution and status
        if 'pending' in combined and ('distribution' in combined or 'policy' in combined):
            gaps["Policy Distribution & Status"].append({
                'icm': icm['id'],
                'title': icm['title'][:100],
                'gap': 'Policy distribution "Pending" status meaning unclear',
                'current_state': 'No documentation explaining what "Pending" means, expected duration, or when to be concerned',
                'needed': 'Status definitions with: 1) Expected time in each status 2) What triggers status changes 3) When to escalate vs wait 4) Troubleshooting steps for stuck policies'
            })
        
        # Size limits
        if any(x in combined for x in ['file size', 'large file', 'thousands of records', 'volume', 'size limit']):
            if 'not detect' in combined or 'not block' in combined or 'not work' in combined:
                gaps["Size Limits & Performance"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'File size limits for DLP/classification not documented',
                    'current_state': 'No clear documentation on file size limits that affect DLP detection or classification accuracy',
                    'needed': 'Comprehensive limits documentation: 1) File size limits by workload 2) Record count limits for SITs 3) Performance degradation thresholds 4) Workarounds for large files'
                })
        
        # Configuration examples
        if any(x in combined for x in ['example', 'sample', 'xml', 'rule package', 'regex', 'pattern']):
            if 'checksum' in combined:
                gaps["Configuration Examples"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'Advanced checksum XML examples missing',
                    'current_state': 'Documentation explains concepts but lacks working XML examples',
                    'needed': 'Complete working XML examples for: 1) Lead digit replacement 2) Two-digit number handling 3) Post-computation replacement 4) Common checksum algorithms'
                })
            elif 'regex' in combined or 'regular expression' in combined:
                gaps["Configuration Examples"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'Regex pattern examples insufficient',
                    'current_state': 'Limited examples for complex regex patterns',
                    'needed': 'More real-world regex examples with explanations and common pitfalls'
                })
        
        # URL and pattern matching
        if 'url' in combined or 'whitelist' in combined or 'domain' in combined:
            if 'query parameter' in combined or '?' in desc or 'auth=' in combined or 'copilot' in combined:
                gaps["URL & Pattern Matching"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'URL matching with query parameters not documented',
                    'current_state': 'No documentation on how DLP handles URLs with dynamic query parameters',
                    'needed': 'Clear documentation on: 1) How URL matching works 2) Query parameter handling 3) Wildcard behaviors 4) Parent domain whitelisting implications 5) Best practices for dynamic URLs'
                })
        
        # Feature scope and behavior
        if 'scope' in combined or 'in-transit' in combined or 'at-rest' in combined:
            if 'exchange' in combined and 'auto' in combined:
                gaps["Feature Scope & Behavior"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'Auto-labeling scope (in-transit vs at-rest) not clear',
                    'current_state': 'Confusion about when auto-labeling applies to emails',
                    'needed': 'Clear documentation: 1) Exchange auto-labeling applies only to in-transit messages 2) Does not apply to existing mailbox content 3) Simulation behavior differences 4) Timeline for label application'
                })
        
        # DLP conditions
        if 'condition' in combined and 'dlp' in combined:
            if 'document created by' in combined or 'what conditions do' in combined:
                gaps["Feature Scope & Behavior"].append({
                    'icm': icm['id'],
                    'title': icm['title'][:100],
                    'gap': 'DLP conditions not fully explained',
                    'current_state': 'Conditions are listed but behavior/source of match not explained',
                    'needed': 'Enhanced conditions documentation: 1) What each condition checks 2) Data source (file metadata vs content) 3) Matching logic 4) Examples for each condition 5) SharePoint/OneDrive-specific behavior'
                })
        
        # UI/UX clarity
        if 'dke' in combined and ('option' in combined or 'configure' in combined):
            gaps["UI/UX Clarity"].append({
                'icm': icm['id'],
                'title': icm['title'][:100],
                'gap': 'Mutually exclusive label options not clear in UI',
                'current_state': 'DKE encryption and user-defined permissions are mutually exclusive but UI allows both to be selected',
                'needed': '1) UI should disable incompatible options 2) Tooltip/help text explaining why 3) Documentation of all mutually exclusive options'
            })
        
        # Site/URL limits
        if 'maximum number' in combined and 'sharepoint' in combined:
            gaps["Configuration Examples"].append({
                'icm': icm['id'],
                'title': icm['title'][:100],
                'gap': 'Site selection limits not documented',
                'current_state': 'No documentation on maximum number of SharePoint sites for DLP policies',
                'needed': 'Limits documentation: 1) Max sites per policy 2) Max locations total 3) Performance implications 4) Alternatives for large-scale deployment'
            })
        
        # Notification behavior
        if 'multiple notification' in combined or 'email' in combined and 'sent' in combined:
            gaps["Feature Scope & Behavior"].append({
                'icm': icm['id'],
                'title': icm['title'][:100],
                'gap': 'Notification email behavior not documented',
                'current_state': 'Unclear when/why multiple notification emails are sent',
                'needed': 'Documentation on: 1) Notification triggers 2) Expected number of emails 3) Deduplication logic 4) How to configure notification frequency'
            })
    
    return gaps


def generate_specific_recommendations_report(gaps, icms, output_file):
    """Generate detailed report with specific, actionable recommendations"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Specific Documentation Gap Analysis\n")
        f.write("## Actionable Recommendations Based on Customer Confusion\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**ICMs Analyzed:** {len(icms)}\n\n")
        f.write("---\n\n")
        
        f.write("## 🎯 Executive Summary\n\n")
        f.write("This analysis identifies **specific** documentation gaps based on actual customer ")
        f.write("confusion and questions from ICMs marked as 'By Design' with prevention type ")
        f.write("'Public Documentation'. Each gap includes:\n\n")
        f.write("- **Current State:** What's missing or unclear\n")
        f.write("- **Impact:** Real customer ICM demonstrating the gap\n")
        f.write("- **Needed:** Specific content to add\n\n")
        
        total_gaps = sum(len(g) for g in gaps.values())
        f.write(f"**Total Specific Gaps Identified:** {total_gaps}\n\n")
        
        f.write("---\n\n")
        
        # Generate detailed sections
        for category, gap_list in gaps.items():
            if not gap_list:
                continue
            
            f.write(f"## 📋 {category}\n\n")
            f.write(f"**Gaps Identified:** {len(gap_list)}\n\n")
            
            # Group by gap type
            gap_groups = defaultdict(list)
            for gap in gap_list:
                gap_groups[gap['gap']].append(gap)
            
            for gap_type, instances in gap_groups.items():
                f.write(f"### ⚠️ {gap_type}\n\n")
                
                # Show first instance in detail
                first = instances[0]
                
                f.write(f"**Impact:** {len(instances)} customer incident(s)\n\n")
                f.write(f"**Example ICM:** [{first['icm']}](https://portal.microsofticm.com/imp/v3/incidents/details/{first['icm']})\n\n")
                f.write(f"**Issue Title:** {first['title']}\n\n")
                
                f.write("#### 📊 Current State\n\n")
                f.write(f"{first['current_state']}\n\n")
                
                f.write("#### ✅ What's Needed\n\n")
                f.write(f"{first['needed']}\n\n")
                
                f.write("#### 🎬 Recommended Actions\n\n")
                
                # Generate specific action items based on gap type
                if 'license' in gap_type.lower():
                    f.write("1. **Create License Comparison Matrix**\n")
                    f.write("   - Side-by-side comparison of E3, E5, and add-on licenses\n")
                    f.write("   - Indicate feature availability by workload (Exchange, SharePoint, Teams, etc.)\n")
                    f.write("   - Clarify chat vs file coverage in Teams\n")
                    f.write("   - Add to main DLP licensing page with prominent placement\n\n")
                    f.write("2. **Update Product Page**\n")
                    f.write("   - Add licensing section to each feature page\n")
                    f.write("   - Link to license comparison from feature descriptions\n\n")
                    f.write("3. **Create FAQ Section**\n")
                    f.write("   - \"Do I need E5 or the add-on for Teams DLP?\"\n")
                    f.write("   - \"What's included in each license tier?\"\n\n")
                
                elif 'metric' in gap_type.lower() or 'portal' in gap_type.lower():
                    f.write("1. **Create Portal Data Reference Page**\n")
                    f.write("   - Document refresh intervals for each report/metric\n")
                    f.write("   - Explain known limitations and edge cases\n")
                    f.write("   - Clarify difference between portal metrics and Activity Explorer\n\n")
                    f.write("2. **Add In-Portal Help Text**\n")
                    f.write("   - Hover tooltips explaining what each metric shows\n")
                    f.write("   - \"Last updated\" timestamp on metrics\n")
                    f.write("   - Warning when data may be incomplete\n\n")
                    f.write("3. **Troubleshooting Guide**\n")
                    f.write("   - \"Why do my metrics show 0?\"\n")
                    f.write("   - \"How long until I see results?\"\n")
                    f.write("   - When to wait vs escalate\n\n")
                
                elif 'pending' in gap_type.lower():
                    f.write("1. **Create Policy Status Reference**\n")
                    f.write("   - Define each status (Pending, Distributing, Success, Error)\n")
                    f.write("   - Expected duration in each status\n")
                    f.write("   - What triggers status transitions\n\n")
                    f.write("2. **Add Status Indicators**\n")
                    f.write("   - Contextual help next to status in UI\n")
                    f.write("   - Progress indicator when available\n")
                    f.write("   - Action buttons (\"Check status\", \"Refresh\")\n\n")
                    f.write("3. **Troubleshooting Flow**\n")
                    f.write("   - Decision tree for stuck policies\n")
                    f.write("   - PowerShell commands to check status\n")
                    f.write("   - When 30+ days pending is OK vs concerning\n\n")
                
                elif 'size' in gap_type.lower() or 'limit' in gap_type.lower():
                    f.write("1. **Create Limits and Boundaries Page**\n")
                    f.write("   - File size limits by workload\n")
                    f.write("   - Record/row count limits for SITs\n")
                    f.write("   - Performance degradation thresholds\n")
                    f.write("   - Impact on classification accuracy\n\n")
                    f.write("2. **Update Troubleshooting Docs**\n")
                    f.write("   - \"Why isn't DLP detecting in large files?\"\n")
                    f.write("   - Workarounds for files exceeding limits\n")
                    f.write("   - Best practices for large datasets\n\n")
                    f.write("3. **Add Warning in UI**\n")
                    f.write("   - Alert when policy may not work on large files\n")
                    f.write("   - Suggest alternatives (EDM, fingerprinting)\n\n")
                
                elif 'xml' in gap_type.lower() or 'example' in gap_type.lower():
                    f.write("1. **Create Code Sample Repository**\n")
                    f.write("   - Complete, working XML examples for each feature\n")
                    f.write("   - Commented code explaining each section\n")
                    f.write("   - Common variations (e.g., different checksum algorithms)\n\n")
                    f.write("2. **Add to GitHub**\n")
                    f.write("   - Create microsoft/compliance-samples repo\n")
                    f.write("   - Include test data and validation scripts\n")
                    f.write("   - Link from docs to repo\n\n")
                    f.write("3. **Interactive Examples**\n")
                    f.write("   - Consider XML builder tool\n")
                    f.write("   - Validation sandbox for testing\n\n")
                
                elif 'url' in gap_type.lower():
                    f.write("1. **Create URL Matching Reference**\n")
                    f.write("   - Explain URL matching logic in detail\n")
                    f.write("   - How query parameters are handled\n")
                    f.write("   - Wildcard behavior and limitations\n\n")
                    f.write("2. **Best Practices Guide**\n")
                    f.write("   - When to whitelist parent domain vs specific URLs\n")
                    f.write("   - Security implications of broad whitelisting\n")
                    f.write("   - Handling dynamic URLs (like Copilot)\n\n")
                    f.write("3. **Examples Library**\n")
                    f.write("   - Common scenarios (Microsoft services, cloud apps)\n")
                    f.write("   - Testing methodology\n\n")
                
                elif 'condition' in gap_type.lower():
                    f.write("1. **Enhance Conditions Documentation**\n")
                    f.write("   - Add detailed explanation for each condition\n")
                    f.write("   - Specify data source (metadata vs content)\n")
                    f.write("   - Include behavior differences by workload\n\n")
                    f.write("2. **Add Visual Examples**\n")
                    f.write("   - Screenshots showing where data comes from\n")
                    f.write("   - Flowcharts for condition evaluation\n\n")
                    f.write("3. **Create Comparison Table**\n")
                    f.write("   - Exchange vs SharePoint vs OneDrive condition behavior\n")
                    f.write("   - Note any workload-specific limitations\n\n")
                
                elif 'scope' in gap_type.lower():
                    f.write("1. **Clarify Scope Documentation**\n")
                    f.write("   - Explicitly state in-transit vs at-rest behavior\n")
                    f.write("   - Add prominent callouts on feature pages\n")
                    f.write("   - Explain simulation behavior differences\n\n")
                    f.write("2. **Update UI Text**\n")
                    f.write("   - Add scope information during policy creation\n")
                    f.write("   - Clarify timing in simulation results\n\n")
                    f.write("3. **Create Scope Comparison Page**\n")
                    f.write("   - What's covered by each policy type\n")
                    f.write("   - When labels apply (creation, modification, etc.)\n\n")
                
                else:
                    f.write("1. **Review and Update Documentation**\n")
                    f.write("   - Address specific gap identified\n")
                    f.write("   - Add examples and explanations\n")
                    f.write("   - Include common edge cases\n\n")
                    f.write("2. **Consider UI Improvements**\n")
                    f.write("   - Contextual help where users encounter confusion\n")
                    f.write("   - Validation/warnings for common mistakes\n\n")
                    f.write("3. **Update FAQ/Troubleshooting**\n")
                    f.write("   - Add section based on customer questions\n")
                    f.write("   - Link to from related pages\n\n")
                
                # Show other ICMs with same gap
                if len(instances) > 1:
                    f.write(f"#### 📎 Other ICMs with Same Gap\n\n")
                    for inst in instances[1:5]:  # Show up to 4 more
                        f.write(f"- [{inst['icm']}](https://portal.microsofticm.com/imp/v3/incidents/details/{inst['icm']}) - {inst['title']}\n")
                    if len(instances) > 5:
                        f.write(f"- *...and {len(instances) - 5} more*\n")
                    f.write("\n")
                
                f.write("#### 📖 Affected Documentation Pages\n\n")
                
                # Suggest specific doc pages that need updates
                if 'license' in gap_type.lower():
                    f.write("- `/purview/dlp-licensing`\n")
                    f.write("- `/purview/dlp-microsoft-teams` (add licensing section)\n")
                    f.write("- `/purview/information-protection` (license comparison)\n")
                elif 'auto-label' in gap_type.lower():
                    f.write("- `/purview/apply-sensitivity-label-automatically`\n")
                    f.write("- `/purview/auto-labeling-exchange`\n")
                    f.write("- `/purview/auto-labeling-sharepoint-onedrive`\n")
                elif 'condition' in gap_type.lower():
                    f.write("- `/purview/dlp-conditions-actions-reference`\n")
                    f.write("- `/purview/dlp-exchange-conditions-actions`\n")
                    f.write("- `/purview/dlp-sharepoint-onedrive-conditions`\n")
                elif 'endpoint' in gap_type.lower():
                    f.write("- `/purview/endpoint-dlp-getting-started`\n")
                    f.write("- `/purview/endpoint-dlp-using`\n")
                elif 'metric' in gap_type.lower() or 'portal' in gap_type.lower():
                    f.write("- `/purview/data-classification-activity-explorer`\n")
                    f.write("- `/purview/data-classification-content-explorer`\n")
                    f.write("- `/purview/auto-labeling-policies` (add metrics section)\n")
                else:
                    f.write("- *(To be determined based on specific gap)*\n")
                
                f.write("\n---\n\n")
        
        # Priority matrix
        f.write("## 🎯 Priority Matrix\n\n")
        f.write("| Priority | Gap | Impact | Effort | ICMs |\n")
        f.write("|----------|-----|--------|--------|------|\n")
        
        # Calculate priorities
        all_gaps_flat = []
        for category, gap_list in gaps.items():
            gap_groups = defaultdict(list)
            for gap in gap_list:
                gap_groups[gap['gap']].append(gap)
            for gap_type, instances in gap_groups.items():
                all_gaps_flat.append({
                    'category': category,
                    'gap': gap_type,
                    'count': len(instances),
                    'instances': instances
                })
        
        # Sort by count (impact)
        all_gaps_flat.sort(key=lambda x: x['count'], reverse=True)
        
        priorities = ['🔴 HIGH', '🟡 MEDIUM', '🟢 LOW']
        for i, gap in enumerate(all_gaps_flat[:15]):  # Top 15
            if i < 5:
                priority = priorities[0]
                effort = "Low-Medium"
            elif i < 10:
                priority = priorities[1]
                effort = "Medium"
            else:
                priority = priorities[2]
                effort = "Medium"
            
            gap_short = gap['gap'][:60] + "..." if len(gap['gap']) > 60 else gap['gap']
            f.write(f"| {priority} | {gap_short} | {gap['count']} customers | {effort} | ")
            
            icm_links = ", ".join([f"[{inst['icm']}](https://portal.microsofticm.com/imp/v3/incidents/details/{inst['icm']})" 
                                   for inst in gap['instances'][:3]])
            if len(gap['instances']) > 3:
                icm_links += f", +{len(gap['instances']) - 3}"
            f.write(f"{icm_links} |\n")
        
        f.write("\n---\n\n")
        
        # Implementation roadmap
        f.write("## 🗺️ Suggested Implementation Roadmap\n\n")
        f.write("### Phase 1: Quick Wins (1-2 weeks)\n\n")
        f.write("Focus on high-impact, low-effort improvements:\n\n")
        f.write("- Add missing definitions and explanations to existing pages\n")
        f.write("- Create FAQ sections for common questions\n")
        f.write("- Add tooltips/help text in UI where confusion occurs\n\n")
        
        f.write("### Phase 2: Documentation Updates (2-4 weeks)\n\n")
        f.write("- Create new reference pages (limits, status definitions, etc.)\n")
        f.write("- Enhance existing pages with examples and clarifications\n")
        f.write("- Add troubleshooting guides\n\n")
        
        f.write("### Phase 3: Enhanced Content (1-2 months)\n\n")
        f.write("- Develop code sample repositories\n")
        f.write("- Create video walkthroughs for complex scenarios\n")
        f.write("- Build interactive tools where helpful\n\n")
        
        f.write("### Phase 4: Product Improvements (2-3 months)\n\n")
        f.write("- UI changes to prevent common errors\n")
        f.write("- In-product guidance and validation\n")
        f.write("- Enhanced portal information displays\n\n")
        
        f.write("---\n\n")
        f.write("*Generated from analysis of real customer incidents. ")
        f.write("Each recommendation is backed by actual customer confusion and questions.*\n")


def main():
    print("="*80)
    print("SPECIFIC DOCUMENTATION GAP ANALYSIS")
    print("="*80)
    print()
    
    # Load ICM data
    data_file = Path(__file__).parent / "data" / "public_doc_icms" / "icm_details_with_themes.json"
    
    print(f"📂 Loading ICM data from: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        icms = json.load(f)
    
    print(f"✓ Loaded {len(icms)} ICMs")
    print()
    
    print("🔍 Analyzing incident descriptions for specific gaps...")
    gaps = extract_specific_gaps(icms)
    
    total_gaps = sum(len(g) for g in gaps.values())
    print(f"✓ Identified {total_gaps} specific documentation gaps")
    print()
    
    # Generate report
    report_file = Path(__file__).parent / "reports" / f"specific_doc_gaps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    print("📝 Generating detailed recommendations report...")
    generate_specific_recommendations_report(gaps, icms, report_file)
    
    print(f"✅ Report generated: {report_file}")
    print()
    
    # Summary
    print("="*80)
    print("GAP SUMMARY BY CATEGORY")
    print("="*80)
    for category, gap_list in gaps.items():
        if gap_list:
            unique_gaps = len(set(g['gap'] for g in gap_list))
            print(f"📌 {category}: {len(gap_list)} instances ({unique_gaps} unique gaps)")
    
    print()
    print("="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
