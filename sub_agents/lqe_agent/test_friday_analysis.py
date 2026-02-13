"""
Test the Friday LQ Analysis with Sample Data

This script creates sample data and runs the Friday analysis to demonstrate the workflow.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

def create_sample_data():
    """Create sample Friday LQ escalation data."""
    
    # Generate sample escalations across regions and feature areas
    sample_escalations = []
    
    # Americas - MIP/DLP cases
    for i in range(5):
        sample_escalations.append({
            "IncidentId": f"INC{10001 + i}",
            "IcMId": f"288{10001 + i}",
            "RoutingId": f"RT{10001 + i}",
            "Title": f"MIP policy not applying correctly - Case {i+1}",
            "Severity": 3 if i < 3 else 4,
            "CreatedBy": f"supportengineer{i+1}@microsoft.com",
            "OwningTeam": "Purview-MIP",
            "ResolveDate": (datetime.now() - timedelta(days=i)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Diagnostics",
            "LowQualityReason": "No diagnostic logs attached",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "Americas",
            "FeatureArea": "MIP/DLP",
            "SourceOrigin": "Americas-US"
        })
    
    # Americas - DLM cases
    for i in range(3):
        sample_escalations.append({
            "IncidentId": f"INC{20001 + i}",
            "IcMId": f"288{20001 + i}",
            "RoutingId": f"RT{20001 + i}",
            "Title": f"Retention policy delay issue - Case {i+1}",
            "Severity": 3,
            "CreatedBy": f"supportdlm{i+1}@microsoft.com",
            "OwningTeam": "Purview-DLM",
            "ResolveDate": (datetime.now() - timedelta(days=i+1)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Insufficient Investigation",
            "LowQualityReason": "Did not follow TSG steps",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Enterprise",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "Americas",
            "FeatureArea": "DLM",
            "SourceOrigin": "Americas-US"
        })
    
    # EMEA - MIP/DLP cases
    for i in range(4):
        sample_escalations.append({
            "IncidentId": f"INC{30001 + i}",
            "IcMId": f"288{30001 + i}",
            "RoutingId": f"RT{30001 + i}",
            "Title": f"Sensitivity label issue - Case {i+1}",
            "Severity": 3,
            "CreatedBy": f"supportemea{i+1}@microsoft.com",
            "OwningTeam": "Purview-MIP",
            "ResolveDate": (datetime.now() - timedelta(days=i+2)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Customer Context",
            "LowQualityReason": "No business impact documented",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Strategic",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "EMEA",
            "FeatureArea": "MIP/DLP",
            "SourceOrigin": "EMEA-Europe"
        })
    
    # EMEA - eDiscovery cases
    for i in range(2):
        sample_escalations.append({
            "IncidentId": f"INC{40001 + i}",
            "IcMId": f"288{40001 + i}",
            "RoutingId": f"RT{40001 + i}",
            "Title": f"eDiscovery search failure - Case {i+1}",
            "Severity": 2,
            "CreatedBy": f"supportedisc{i+1}@microsoft.com",
            "OwningTeam": "Purview-eDiscovery",
            "ResolveDate": (datetime.now() - timedelta(days=i+1)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Diagnostics",
            "LowQualityReason": "No error messages captured",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "EMEA",
            "FeatureArea": "eDiscovery",
            "SourceOrigin": "EMEA-Europe"
        })
    
    # APAC - MIP/DLP cases
    for i in range(3):
        sample_escalations.append({
            "IncidentId": f"INC{50001 + i}",
            "IcMId": f"288{50001 + i}",
            "RoutingId": f"RT{50001 + i}",
            "Title": f"DLP policy blocking legitimate content - Case {i+1}",
            "Severity": 3,
            "CreatedBy": f"supportapac{i+1}@microsoft.com",
            "OwningTeam": "Purview-MIP",
            "ResolveDate": (datetime.now() - timedelta(days=i)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Insufficient Investigation",
            "LowQualityReason": "Did not check policy configuration",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "APAC",
            "FeatureArea": "MIP/DLP",
            "SourceOrigin": "APAC-Asia"
        })
    
    # APAC - DLM case
    sample_escalations.append({
        "IncidentId": "INC60001",
        "IcMId": "28860001",
        "RoutingId": "RT60001",
        "Title": "Retention label not available",
        "Severity": 4,
        "CreatedBy": "supportapacdlm@microsoft.com",
        "OwningTeam": "Purview-DLM",
        "ResolveDate": (datetime.now() - timedelta(days=3)).isoformat(),
        "FiscalWeek": 24,
        "EscalationQuality": "Missing Customer Context",
        "LowQualityReason": "No tenant configuration details",
        "QualityReviewFalsePositive": "",
        "CustomerSegment": "Enterprise",
        "IsTrueLowQuality": True,
        "ReviewerName": "",
        "OriginRegion": "APAC",
        "FeatureArea": "DLM",
        "SourceOrigin": "APAC-Asia"
    })
    
    return sample_escalations


def save_sample_data():
    """Save sample data to file."""
    data = create_sample_data()
    
    # Create data directory
    data_dir = Path(__file__).parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Save with today's date
    filename = f"friday_lq_test_{datetime.now().strftime('%Y%m%d')}.json"
    filepath = data_dir / filename
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Sample data created: {filepath}")
    print(f"Total escalations: {len(data)}")
    
    # Show breakdown
    from collections import defaultdict
    by_region = defaultdict(lambda: defaultdict(int))
    
    for esc in data:
        region = esc['OriginRegion']
        feature = esc['FeatureArea']
        by_region[region][feature] += 1
    
    print("\nBreakdown:")
    for region, features in sorted(by_region.items()):
        total = sum(features.values())
        print(f"  {region}: {total} cases")
        for feature, count in sorted(features.items()):
            print(f"    - {feature}: {count}")
    
    return str(filepath)


def run_test():
    """Run the Friday analysis with sample data."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    
    # Create sample data
    print("="*80)
    print("FRIDAY LQ ANALYSIS - TEST RUN WITH SAMPLE DATA")
    print("="*80 + "\n")
    
    data_file = save_sample_data()
    
    print("\n" + "="*80)
    print("Running Friday Analysis...")
    print("="*80 + "\n")
    
    # Import and run
    from run_friday_lq_analysis import FridayLQRunner
    
    runner = FridayLQRunner()
    results = runner.run_friday_analysis(data_file=data_file)
    
    if results['success']:
        print("\n" + "="*80)
        print("TEST SUCCESSFUL!")
        print("="*80)
        print(f"\nReport: {results['report_path']}")
        print(f"CSV: {results['csv_path']}")
        
        print("\nSummary:")
        for region, info in results['summary'].items():
            print(f"  {region}: {info['total']} cases")
            for feature, count in info['by_feature'].items():
                print(f"    - {feature}: {count}")
    else:
        print("\nTest failed - see output above")


if __name__ == "__main__":
    run_test()
