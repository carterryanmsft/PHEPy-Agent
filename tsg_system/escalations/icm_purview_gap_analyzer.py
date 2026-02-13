"""
ICM Purview Escalation Gap Analyzer
Analyzes ICM incidents for Purview service to identify TSG gaps

This script:
1. Searches ICM for Purview-related escalations
2. Identifies patterns that indicate TSG gaps
3. Compares against existing wiki TSG baseline
4. Recommends new/updated TSGs based on escalation frequency
"""

import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Set

# Gap indicators - signals that a better TSG could have prevented escalation
TSG_GAP_INDICATORS = {
    'repeated_issue': [
        'this is a recurring issue',
        'similar to previous case',
        'same problem as',
        'happens frequently',
        'multiple customers affected'
    ],
    'missing_documentation': [
        'no TSG available',
        'no documentation found',
        'unclear how to troubleshoot',
        'missing troubleshooting steps',
        'no guidance in wiki'
    ],
    'unclear_process': [
        'not sure how to proceed',
        'escalation path unclear',
        'unsure which team',
        'where should this go',
        'who owns this'
    ],
    'missing_diagnostic_steps': [
        'no diagnostic query',
        'missing kusto query',
        'how do I check',
        'what logs to collect',
        'need investigation steps'
    ],
    'incomplete_tsg': [
        'TSG doesn\'t cover this',
        'not in existing TSG',
        'TSG is outdated',
        'TSG missing scenario',
        'documentation incomplete'
    ]
}

# Purview product areas to track
PURVIEW_PRODUCTS = [
    'Auditing',
    'Communication Compliance',
    'Data Lifecycle Management',
    'Data Loss Prevention',
    'DLP',
    'Data Security Investigations',
    'DSPM for AI',
    'eDiscovery',
    'Information Barriers',
    'Information Protection',
    'Sensitivity Labels',
    'Ingestion',
    'Insider Risk Management',
    'IRM',
    'Purview Compliance Shared Components',
    'Copilot',
    'Agents'
]


class ICMGapAnalyzer:
    """Analyzes ICM incidents to find TSG gaps"""
    
    def __init__(self):
        self.incidents: List[Dict] = []
        self.gap_patterns: Dict[str, List] = defaultdict(list)
        self.product_gaps: Dict[str, int] = defaultdict(int)
        self.existing_tsgs: Set[str] = set()
        
    def load_existing_tsgs(self, tsg_baseline_path: str):
        """Load existing TSGs from baseline analysis"""
        try:
            with open(tsg_baseline_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract TSG titles/paths from baseline
                for line in content.split('\n'):
                    if 'TSG' in line or 'Scenario:' in line:
                        self.existing_tsgs.add(line.strip())
            print(f"✓ Loaded {len(self.existing_tsgs)} existing TSGs from baseline")
        except Exception as e:
            print(f"⚠️ Could not load TSG baseline: {e}")
    
    def analyze_incident_description(self, incident: Dict) -> Dict:
        """Analyze incident description for gap indicators"""
        description = incident.get('Description', '') + ' ' + incident.get('Title', '')
        description = description.lower()
        
        gaps_found = {
            'gap_types': [],
            'gap_score': 0,
            'product_area': None,
            'issue_pattern': None
        }
        
        # Check for gap indicators
        for gap_type, keywords in TSG_GAP_INDICATORS.items():
            for keyword in keywords:
                if keyword in description:
                    gaps_found['gap_types'].append(gap_type)
                    gaps_found['gap_score'] += 1
                    break
        
        # Identify product area
        for product in PURVIEW_PRODUCTS:
            if product.lower() in description:
                gaps_found['product_area'] = product
                break
        
        # Extract issue pattern (simplified)
        if 'sync' in description or 'synchronization' in description:
            gaps_found['issue_pattern'] = 'Sync/Replication Issue'
        elif 'performance' in description or 'slow' in description or 'timeout' in description:
            gaps_found['issue_pattern'] = 'Performance/Latency'
        elif 'configuration' in description or 'setup' in description:
            gaps_found['issue_pattern'] = 'Configuration/Setup'
        elif 'permission' in description or 'access' in description or 'rbac' in description:
            gaps_found['issue_pattern'] = 'Permissions/Access'
        elif 'ui' in description or 'portal' in description or 'interface' in description:
            gaps_found['issue_pattern'] = 'UI/Portal Issue'
        
        return gaps_found
    
    def score_tsg_opportunity(self, incident: Dict, analysis: Dict) -> int:
        """Score how beneficial a TSG would be (0-100)"""
        score = 0
        
        # Base score from gap indicators
        score += analysis['gap_score'] * 10
        
        # Repeated incidents (check severity and duration)
        severity = incident.get('Severity', 3)
        if severity <= 2:
            score += 20
        
        # Long resolution time indicates complexity
        created = incident.get('CreatedDate')
        resolved = incident.get('ResolvedDate')
        if created and resolved:
            duration_hours = (resolved - created).total_seconds() / 3600
            if duration_hours > 24:
                score += 15
            elif duration_hours > 8:
                score += 10
        
        # Customer impact
        if 'customer' in incident.get('Description', '').lower():
            score += 15
        
        # Missing TSG explicit mention
        if 'missing_documentation' in analysis['gap_types']:
            score += 20
        
        return min(score, 100)
    
    def analyze_incidents(self, incidents: List[Dict]) -> Dict:
        """Main analysis function"""
        self.incidents = incidents
        
        results = {
            'total_incidents': len(incidents),
            'tsg_gap_incidents': [],
            'high_priority_gaps': [],
            'product_gap_summary': {},
            'pattern_recommendations': []
        }
        
        for incident in incidents:
            analysis = self.analyze_incident_description(incident)
            
            if analysis['gap_score'] > 0:
                tsg_score = self.score_tsg_opportunity(incident, analysis)
                
                gap_incident = {
                    'incident_id': incident.get('Id', 'Unknown'),
                    'title': incident.get('Title', 'No Title'),
                    'severity': incident.get('Severity', 'Unknown'),
                    'created_date': incident.get('CreatedDate', 'Unknown'),
                    'gap_types': analysis['gap_types'],
                    'product_area': analysis['product_area'],
                    'issue_pattern': analysis['issue_pattern'],
                    'tsg_opportunity_score': tsg_score,
                    'recommendation': self.generate_tsg_recommendation(incident, analysis)
                }
                
                results['tsg_gap_incidents'].append(gap_incident)
                
                if tsg_score >= 60:
                    results['high_priority_gaps'].append(gap_incident)
                
                # Track by product
                if analysis['product_area']:
                    self.product_gaps[analysis['product_area']] += 1
        
        results['product_gap_summary'] = dict(self.product_gaps)
        results['tsg_gap_incidents'].sort(key=lambda x: x['tsg_opportunity_score'], reverse=True)
        
        return results
    
    def generate_tsg_recommendation(self, incident: Dict, analysis: Dict) -> str:
        """Generate specific TSG recommendation"""
        product = analysis['product_area'] or 'General Purview'
        pattern = analysis['issue_pattern'] or 'Common Issue'
        
        recommendation = f"Create TSG: {product} - {pattern}\n"
        
        if 'missing_documentation' in analysis['gap_types']:
            recommendation += "• Priority: HIGH - No existing documentation found\n"
        
        if 'repeated_issue' in analysis['gap_types']:
            recommendation += "• Include common scenarios section\n"
        
        if 'missing_diagnostic_steps' in analysis['gap_types']:
            recommendation += "• Add diagnostic Kusto queries\n"
            recommendation += "• Include log collection steps\n"
        
        if 'unclear_process' in analysis['gap_types']:
            recommendation += "• Define clear escalation path\n"
            recommendation += "• Add decision tree diagram\n"
        
        return recommendation
    
    def generate_report(self, results: Dict, output_path: str):
        """Generate markdown report"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# Purview ICM Escalation Gap Analysis Report
**Generated:** {timestamp}
**Total Incidents Analyzed:** {results['total_incidents']}
**TSG Gap Incidents Found:** {len(results['tsg_gap_incidents'])}
**High Priority Gaps:** {len(results['high_priority_gaps'])}

---

## Executive Summary

This report analyzes Purview-related ICM escalations to identify gaps in troubleshooting documentation.
Incidents were scored based on gap indicators such as missing TSGs, repeated issues, and unclear processes.

### Top Findings:

"""
        # High priority gaps
        if results['high_priority_gaps']:
            report += "### 🔴 High Priority TSG Gaps (Score >= 60)\n\n"
            for gap in results['high_priority_gaps'][:10]:  # Top 10
                report += f"""
#### {gap['title']}
- **ICM ID:** {gap['incident_id']}
- **Product:** {gap['product_area'] or 'Unknown'}
- **Pattern:** {gap['issue_pattern'] or 'Unclassified'}
- **TSG Opportunity Score:** {gap['tsg_opportunity_score']}/100
- **Gap Types:** {', '.join(gap['gap_types'])}

**Recommendation:**
```
{gap['recommendation']}
```

---
"""
        
        # Product breakdown
        report += "\n## Gap Analysis by Product\n\n"
        report += "| Product Area | Gap Count | Priority |\n"
        report += "|--------------|-----------|----------|\n"
        
        sorted_products = sorted(
            results['product_gap_summary'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for product, count in sorted_products:
            priority = "🔴 HIGH" if count >= 10 else "🟡 MEDIUM" if count >= 5 else "🟢 LOW"
            report += f"| {product} | {count} | {priority} |\n"
        
        # All gaps
        report += "\n## All TSG Gap Incidents\n\n"
        for gap in results['tsg_gap_incidents']:
            report += f"- **{gap['incident_id']}** [{gap['tsg_opportunity_score']}/100] - {gap['title'][:80]}...\n"
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Report saved to: {output_path}")
        return report


def main():
    """Main execution"""
    print("=" * 80)
    print("ICM Purview Escalation Gap Analyzer")
    print("=" * 80)
    
    # Initialize analyzer
    analyzer = ICMGapAnalyzer()
    
    # Load existing TSG baseline
    baseline_path = 'c:/Users/carterryan/OneDrive - Microsoft/PHEPy/tsg_system/purview_wiki_tsg_baseline.md'
    analyzer.load_existing_tsgs(baseline_path)
    
    print("\n📊 To analyze ICM incidents, you need to:")
    print("1. Use ICM MCP to search for Purview incidents")
    print("2. Query: owning service contains 'Purview'")
    print("3. Date range: Last 90 days")
    print("4. Export results and pass to this script\n")
    
    # Example usage with mock data
    print("Example: Mock analysis with sample incident")
    sample_incidents = [
        {
            'Id': 'INC123456',
            'Title': 'DLP Policy not syncing to endpoints - no TSG available',
            'Description': 'Customer reports DLP policies created 48 hours ago still not applied to Windows endpoints. Missing troubleshooting steps in documentation. This is a recurring issue for multiple customers.',
            'Severity': 2,
            'CreatedDate': datetime.now() - timedelta(days=2),
            'ResolvedDate': datetime.now(),
            'OwningService': 'Purview / DLP'
        }
    ]
    
    results = analyzer.analyze_incidents(sample_incidents)
    
    output_path = 'c:/Users/carterryan/OneDrive - Microsoft/PHEPy/tsg_system/escalations/icm_gap_analysis_report.md'
    analyzer.generate_report(results, output_path)
    
    print("\n✅ Analysis complete!")
    print(f"   - Found {len(results['tsg_gap_incidents'])} incidents with TSG gaps")
    print(f"   - {len(results['high_priority_gaps'])} high-priority recommendations")


if __name__ == '__main__':
    main()
