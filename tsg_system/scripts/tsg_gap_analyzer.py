"""
TSG Gap Analyzer - Extract TSG-relevant data from ICM incidents
Analyzes incidents to identify TSG coverage gaps and effectiveness issues
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class TSGIncidentData:
    """Lightweight structure for TSG-relevant incident data"""
    incident_id: int
    title: str
    severity: int
    state: str
    created_date: str
    tsg_link: Optional[str] = None
    tsg_effectiveness: Optional[bool] = None
    escalation_quality: Optional[str] = None
    resolution_summary: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class TSGGapAnalyzer:
    """Analyze ICM incidents for TSG gaps"""
    
    def __init__(self):
        self.incidents: List[TSGIncidentData] = []
        self.tsg_links: Dict[str, int] = defaultdict(int)  # Link -> count
        self.categories: Dict[str, List[int]] = defaultdict(list)  # Category -> incident IDs
        
    def extract_tsg_data(self, incident_json: Dict) -> TSGIncidentData:
        """Extract TSG-relevant fields from full incident JSON"""
        
        # Extract custom fields
        custom_fields = incident_json.get('customFields', [])
        tsg_link = None
        tsg_effectiveness = None
        escalation_quality = None
        
        for field in custom_fields:
            field_name = field.get('name', '')
            if 'TSG' in field_name and 'Link' in field_name:
                tsg_link = field.get('value')
            elif 'TSG Effectiveness' in field_name:
                tsg_effectiveness = field.get('value') == 'true' or field.get('value') is True
            elif 'Escalation Quality' in field_name:
                escalation_quality = field.get('value')
        
        # Extract resolution info
        resolution_summary = None
        if 'resolveData' in incident_json:
            resolution_summary = incident_json.get('resolveData', {}).get('resolutionSteps')
        elif 'mitigateData' in incident_json:
            resolution_summary = incident_json.get('mitigateData', {}).get('mitigationSteps')
        
        return TSGIncidentData(
            incident_id=incident_json.get('id'),
            title=incident_json.get('title', ''),
            severity=incident_json.get('severity', 0),
            state=incident_json.get('state', ''),
            created_date=incident_json.get('createdDate', ''),
            tsg_link=tsg_link,
            tsg_effectiveness=tsg_effectiveness,
            escalation_quality=escalation_quality,
            resolution_summary=resolution_summary,
            tags=incident_json.get('tags', [])
        )
    
    def add_incident(self, incident_data: TSGIncidentData):
        """Add incident to analysis"""
        self.incidents.append(incident_data)
        
        # Track TSG links
        if incident_data.tsg_link:
            self.tsg_links[incident_data.tsg_link] += 1
        
        # Categorize by keywords in title
        title_lower = incident_data.title.lower()
        if 'label' in title_lower or 'classification' in title_lower:
            self.categories['Labeling/Classification'].append(incident_data.incident_id)
        if 'encrypt' in title_lower or 'dlp' in title_lower:
            self.categories['Encryption/DLP'].append(incident_data.incident_id)
        if 'sit' in title_lower or 'sensitive information' in title_lower:
            self.categories['SIT/Detection'].append(incident_data.incident_id)
        if 'scanner' in title_lower or 'scan' in title_lower:
            self.categories['Scanning'].append(incident_data.incident_id)
        if 'policy' in title_lower:
            self.categories['Policy'].append(incident_data.incident_id)
        if 'migration' in title_lower:
            self.categories['Migration'].append(incident_data.incident_id)
    
    def analyze_gaps(self) -> Dict:
        """Perform TSG gap analysis"""
        
        total_incidents = len(self.incidents)
        if total_incidents == 0:
            return {"error": "No incidents to analyze"}
        
        # Calculate metrics
        incidents_with_tsg = sum(1 for i in self.incidents if i.tsg_link)
        incidents_without_tsg = total_incidents - incidents_with_tsg
        
        # TSG effectiveness tracking
        effective_tsgs = sum(1 for i in self.incidents 
                            if i.tsg_effectiveness is True)
        ineffective_tsgs = sum(1 for i in self.incidents 
                              if i.tsg_effectiveness is False)
        
        # Severity breakdown for incidents without TSGs
        sev_breakdown_no_tsg = defaultdict(int)
        for incident in self.incidents:
            if not incident.tsg_link:
                sev_breakdown_no_tsg[incident.severity] += 1
        
        # Category coverage analysis
        category_coverage = {}
        for category, incident_ids in self.categories.items():
            cat_incidents = [i for i in self.incidents if i.incident_id in incident_ids]
            with_tsg = sum(1 for i in cat_incidents if i.tsg_link)
            category_coverage[category] = {
                'total': len(cat_incidents),
                'with_tsg': with_tsg,
                'without_tsg': len(cat_incidents) - with_tsg,
                'coverage_pct': (with_tsg / len(cat_incidents) * 100) if cat_incidents else 0
            }
        
        return {
            'summary': {
                'total_incidents': total_incidents,
                'incidents_with_tsg': incidents_with_tsg,
                'incidents_without_tsg': incidents_without_tsg,
                'tsg_coverage_pct': (incidents_with_tsg / total_incidents * 100),
                'effective_tsgs': effective_tsgs,
                'ineffective_tsgs': ineffective_tsgs
            },
            'severity_breakdown_no_tsg': dict(sev_breakdown_no_tsg),
            'category_coverage': category_coverage,
            'most_used_tsgs': sorted(self.tsg_links.items(), key=lambda x: x[1], reverse=True)[:10],
            'gap_priorities': self._identify_gap_priorities()
        }
    
    def _identify_gap_priorities(self) -> List[Dict]:
        """Identify highest priority TSG gaps"""
        priorities = []
        
        # High severity incidents without TSGs
        high_sev_no_tsg = [i for i in self.incidents 
                          if not i.tsg_link and i.severity <= 3]
        if high_sev_no_tsg:
            priorities.append({
                'priority': 'HIGH',
                'reason': f'{len(high_sev_no_tsg)} high-severity incidents (Sev 0-3) without TSG links',
                'count': len(high_sev_no_tsg),
                'sample_incidents': [i.incident_id for i in high_sev_no_tsg[:5]]
            })
        
        # Incidents with ineffective TSGs
        ineffective = [i for i in self.incidents if i.tsg_effectiveness is False]
        if ineffective:
            priorities.append({
                'priority': 'MEDIUM',
                'reason': f'{len(ineffective)} incidents marked TSG as ineffective',
                'count': len(ineffective),
                'sample_incidents': [i.incident_id for i in ineffective[:5]]
            })
        
        # Categories with low coverage
        for category, incident_ids in self.categories.items():
            cat_incidents = [i for i in self.incidents if i.incident_id in incident_ids]
            with_tsg = sum(1 for i in cat_incidents if i.tsg_link)
            coverage = (with_tsg / len(cat_incidents) * 100) if cat_incidents else 0
            
            if coverage < 50 and len(cat_incidents) >= 5:
                priorities.append({
                    'priority': 'MEDIUM',
                    'reason': f'{category} category has low TSG coverage ({coverage:.1f}%)',
                    'count': len(cat_incidents),
                    'coverage_pct': coverage
                })
        
        return sorted(priorities, key=lambda x: (
            {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x['priority']], 
            -x['count']
        ))
    
    def save_results(self, output_path: str):
        """Save analysis results to JSON"""
        results = {
            'analysis': self.analyze_gaps(),
            'incident_count': len(self.incidents),
            'incidents': [asdict(i) for i in self.incidents]
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {output_path}")
        return results
    
    def generate_report(self) -> str:
        """Generate human-readable TSG gap report"""
        analysis = self.analyze_gaps()
        
        report = []
        report.append("=" * 80)
        report.append("TSG GAP ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        summary = analysis['summary']
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append(f"Total Incidents Analyzed: {summary['total_incidents']}")
        report.append(f"TSG Coverage: {summary['tsg_coverage_pct']:.1f}% ({summary['incidents_with_tsg']}/{summary['total_incidents']})")
        report.append(f"Incidents WITHOUT TSG: {summary['incidents_without_tsg']}")
        report.append(f"TSGs Marked Effective: {summary['effective_tsgs']}")
        report.append(f"TSGs Marked Ineffective: {summary['ineffective_tsgs']}")
        report.append("")
        
        # Severity breakdown
        if analysis['severity_breakdown_no_tsg']:
            report.append("INCIDENTS WITHOUT TSG - BY SEVERITY")
            report.append("-" * 80)
            for sev, count in sorted(analysis['severity_breakdown_no_tsg'].items()):
                report.append(f"  Severity {sev}: {count} incidents")
            report.append("")
        
        # Category coverage
        report.append("TSG COVERAGE BY CATEGORY")
        report.append("-" * 80)
        for category, stats in sorted(analysis['category_coverage'].items(), 
                                      key=lambda x: x[1]['coverage_pct']):
            report.append(f"{category}:")
            report.append(f"  Total: {stats['total']} | With TSG: {stats['with_tsg']} | "
                         f"Coverage: {stats['coverage_pct']:.1f}%")
        report.append("")
        
        # Gap priorities
        report.append("TOP PRIORITY TSG GAPS")
        report.append("-" * 80)
        for i, gap in enumerate(analysis['gap_priorities'], 1):
            report.append(f"{i}. [{gap['priority']}] {gap['reason']}")
            if 'sample_incidents' in gap:
                report.append(f"   Sample Incidents: {', '.join(map(str, gap['sample_incidents']))}")
        report.append("")
        
        # Most used TSGs
        if analysis['most_used_tsgs']:
            report.append("MOST FREQUENTLY USED TSGs")
            report.append("-" * 80)
            for tsg_link, count in analysis['most_used_tsgs'][:5]:
                report.append(f"  [{count}x] {tsg_link}")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    analyzer = TSGGapAnalyzer()
    
    # Example: Load incidents from saved JSON
    # with open('incident_data.json', 'r') as f:
    #     incidents = json.load(f)
    #     for incident in incidents:
    #         tsg_data = analyzer.extract_tsg_data(incident)
    #         analyzer.add_incident(tsg_data)
    
    # results = analyzer.save_results('tsg_gap_analysis.json')
    # print(analyzer.generate_report())
    
    print("TSG Gap Analyzer ready for use")
