"""
Test Weekly Regional LQE Reports with Sample Data

Validates the weekly workflow using test data without requiring Kusto access.

Author: Carter Ryan
Created: February 13, 2026
"""

import os
import json
from datetime import datetime, timedelta
import random


def generate_test_regional_data(num_escalations: int = 30) -> list:
    """Generate test LQE data with regional distribution."""
    
    regions = {
        'Americas': 0.4,  # 40% of escalations
        'EMEA': 0.35,     # 35% of escalations
        'APAC': 0.20,     # 20% of escalations
        'Unknown': 0.05   # 5% of escalations
    }
    
    feature_areas = ['MIP/DLP', 'DLM', 'eDiscovery', 'Other']
    
    quality_issues = [
        'Incomplete or Limited Information',
        'Not a Valid Escalation',
        'Duplicate',
        'Missing diagnostics'
    ]
    
    engineers = [
        'jsmith', 'mwilson', 'ataylor', 'dlee', 'rbrown',
        'kchen', 'sgarcia', 'jpatel', 'mnogueira', 'tkim'
    ]
    
    teams = [
        r'Purview\DLP Platform',
        r'Purview\MIP Core',
        r'Purview\DLM Retention',
        r'Purview\eDiscovery Search',
        r'Purview\Information Protection',
        r'Purview\Compliance'
    ]
    
    escalations = []
    base_date = datetime.now() - timedelta(days=6)
    
    for i in range(num_escalations):
        # Determine region based on weighted distribution
        rand = random.random()
        cumulative = 0
        region = 'Unknown'
        for r, weight in regions.items():
            cumulative += weight
            if rand <= cumulative:
                region = r
                break
        
        # Random dates in last 7 days
        days_ago = random.randint(0, 6)
        resolve_date = base_date + timedelta(days=days_ago)
        
        escalation = {
            'IncidentId': 500000 + i,
            'IcMId': 500000 + i,
            'RoutingId': f'R{100000 + i}',
            'Title': f'Sample escalation {i+1} - {random.choice(["Label visibility", "Policy not applying", "Retention issue", "Search failure"])}',
            'Severity': random.choice(['Sev2', 'Sev3', 'Sev3', 'Sev4']),
            'CreatedBy': random.choice(engineers),
            'OwningTeam': random.choice(teams),
            'ResolveDate': resolve_date.isoformat(),
            'EscalationQuality': random.choice(quality_issues),
            'LowQualityReason': f'TEST: {random.choice(quality_issues)}',
            'QualityReviewFalsePositive': None,
            'CustomerSegment': random.choice(['Enterprise', 'Commercial', 'SMB']),
            'IsTrueLowQuality': True,
            'ReviewerName': None,  # Unassigned
            'OriginRegion': region,
            'FeatureArea': random.choice(feature_areas),
            'FeatureAreaDetail': '',
            'SourceOrigin': region,
            'TimeZone': 'PST' if region == 'Americas' else ('GMT' if region == 'EMEA' else 'IST')
        }
        
        escalations.append(escalation)
    
    return escalations


def main():
    """Generate test data and validate workflow."""
    
    print("=" * 80)
    print("WEEKLY LQE REPORT - TEST DATA GENERATOR")
    print("=" * 80)
    print()
    
    # Generate test data
    print("Generating test data...")
    num_escalations = 30
    test_data = generate_test_regional_data(num_escalations)
    print(f"✓ Generated {len(test_data)} test escalations")
    print()
    
    # Show distribution
    by_region = {}
    by_feature = {}
    
    for esc in test_data:
        region = esc['OriginRegion']
        feature = esc['FeatureArea']
        
        by_region[region] = by_region.get(region, 0) + 1
        by_feature[feature] = by_feature.get(feature, 0) + 1
    
    print("Distribution by Region:")
    for region, count in sorted(by_region.items()):
        pct = (count / len(test_data)) * 100
        print(f"  {region:10s}: {count:2d} ({pct:5.1f}%)")
    
    print()
    print("Distribution by Feature Area:")
    for feature, count in sorted(by_feature.items()):
        pct = (count / len(test_data)) * 100
        print(f"  {feature:15s}: {count:2d} ({pct:5.1f}%)")
    
    # Save to data directory
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(data_dir, f'regional_lqe_test_{timestamp}.json')
    
    with open(output_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print()
    print(f"✓ Test data saved to: {output_file}")
    print()
    print("=" * 80)
    print("Next Step: Run Weekly Report Generation")
    print("=" * 80)
    print()
    print("PowerShell:")
    print(f'  .\\Run-WeeklyLQEReports.ps1 -DataFile "{output_file}"')
    print()
    print("Python:")
    print(f'  python run_weekly_regional_reports.py --use-data "{output_file}"')
    print()


if __name__ == '__main__':
    main()
