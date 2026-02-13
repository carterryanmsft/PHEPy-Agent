"""
Generate Weekly Low Quality Escalation Report from Kusto Data

Usage:
    python generate_weekly_lqe_report.py <json_file>
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Import the HTML generator
from friday_lq_html_generator import FridayLQEHTMLGenerator


def load_data(json_file):
    """Load data from JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle Kusto JSON format
    if isinstance(data, dict) and 'data' in data:
        return data['data']
    return data


def organize_by_region_and_feature(escalations):
    """Organize escalations by region and feature area."""
    organized = defaultdict(lambda: defaultdict(list))
    
    for escalation in escalations:
        region = escalation.get('CreatorRegion', 'Unknown')
        feature = escalation.get('ProductArea', 'Unknown')
        organized[region][feature].append(escalation)
    
    return dict(organized)


def generate_report(data, output_dir='friday_reports'):
    """Generate HTML report from data."""
    Path(output_dir).mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Organize data
    organized = organize_by_region_and_feature(data)
    
    # Prepare report data
    report_data = {
        'timestamp': datetime.now(),
        'total_escalations': len(data),
        'regions': {}
    }
    
    for region, features in organized.items():
        region_data = {
            'name': region,
            'total': sum(len(cases) for cases in features.values()),
            'feature_areas': {}
        }
        
        for feature, cases in features.items():
            region_data['feature_areas'][feature] = {
                'name': feature,
                'count': len(cases),
                'escalations': cases
            }
        
        report_data['regions'][region] = region_data
    
    # Generate HTML
    generator = FridayLQEHTMLGenerator()
    html = generator.generate_report(report_data, region_filter=None)
    
    # Save report
    output_file = Path(output_dir) / f'weekly_lqe_report_{timestamp}.htm'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n{'='*80}")
    print("WEEKLY LOW QUALITY ESCALATION REPORT GENERATED")
    print(f"{'='*80}\n")
    print(f"Report: {output_file}")
    print(f"Total Escalations: {len(data)}")
    print(f"\nBreakdown by Region:")
    
    for region, region_data in report_data['regions'].items():
        print(f"  {region}: {region_data['total']} cases")
        for feature, feature_data in region_data['feature_areas'].items():
            print(f"    - {feature}: {feature_data['count']}")
    
    print()
    
    return str(output_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_weekly_lqe_report.py <json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if not Path(json_file).exists():
        print(f"Error: File not found: {json_file}")
        sys.exit(1)
    
    print(f"Loading data from: {json_file}")
    data = load_data(json_file)
    print(f"Loaded {len(data)} escalations")
    
    output_file = generate_report(data)
    
    # Open in browser
    import subprocess
    subprocess.run(['start', output_file], shell=True)
