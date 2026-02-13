"""Direct execution script for weekly LQE report."""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from friday_lq_html_generator import FridayLQEHTMLGenerator

# Hard-coded data file path
DATA_FILE = r'lq_escalation_reports\lqe_full_data_20260205.json'

def load_data(json_file):
    """Load data from JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
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
        'regions': {},
        'stats': {
            'total': len(data),
            'by_quality': {},
            'by_product': {},
            'by_region': {}
        }
    }
    
    # Build region structure
    for region, features in organized.items():
        report_data['regions'][region] = {}
        report_data['stats']['by_region'][region] = 0
        
        for feature, escalations in features.items():
            report_data['regions'][region][feature] = escalations
            report_data['stats']['by_region'][region] += len(escalations)
            
            # Track by product
            if feature not in report_data['stats']['by_product']:
                report_data['stats']['by_product'][feature] = 0
            report_data['stats']['by_product'][feature] += len(escalations)
            
            # Track by quality
            for esc in escalations:
                quality = esc.get('EscalationQuality', 'Unknown')
                if quality not in report_data['stats']['by_quality']:
                    report_data['stats']['by_quality'][quality] = 0
                report_data['stats']['by_quality'][quality] += 1
    
    # Generate HTML
    generator = FridayLQEHTMLGenerator()
    html = generator.generate_report(report_data)
    
    # Save report
    output_file = Path(output_dir) / f'weekly_lqe_report_{timestamp}.htm'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✓ Weekly LQE Report Generated")
    print(f"  File: {output_file}")
    print(f"  Total Escalations: {report_data['stats']['total']}")
    print(f"\n  By Region:")
    for region, count in report_data['stats']['by_region'].items():
        print(f"    {region}: {count}")
    print(f"\n  By Product:")
    for product, count in report_data['stats']['by_product'].items():
        print(f"    {product}: {count}")
    print(f"\n  By Quality Issue:")
    for quality, count in report_data['stats']['by_quality'].items():
        print(f"    {quality}: {count}")
    
    return output_file

if __name__ == '__main__':
    try:
        print(f"Loading data from: {DATA_FILE}")
        data = load_data(DATA_FILE)
        print(f"Loaded {len(data)} escalations")
        
        output_file = generate_report(data)
        print(f"\n✓ Report ready: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
