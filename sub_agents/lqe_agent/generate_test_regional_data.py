"""
Generate test data for 14-day regional LQE analysis
"""
import json
from datetime import datetime, timedelta

def generate_14day_test_data():
    """Generate test escalations for last 7 days across all regions."""
    
    base_date = datetime.now()
    escalations = []
    
    # Americas - MIP/DLP cases
    for i in range(8):
        escalations.append({
            "IncidentId": f"INC{20001+i}",
            "IcMId": f"28820{1+i:03d}",
            "RoutingId": f"RT20{1+i:03d}",
            "Title": f"MIP policy not applying correctly - Americas Case {i+1}",
            "Severity": 3,
            "CreatedBy": f"support.americas{i%3+1}@microsoft.com",
            "OwningTeam": "Purview-MIP",
            "ResolveDate": (base_date - timedelta(days=i+1)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Diagnostics" if i % 2 == 0 else "Insufficient Investigation",
            "LowQualityReason": "No diagnostic logs attached" if i % 2 == 0 else "Incomplete troubleshooting",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "Americas",
            "FeatureArea": "MIP/DLP",
            "SourceOrigin": "Americas-US"
        })
    
    # Americas - DLM cases
    for i in range(5):
        escalations.append({
            "IncidentId": f"INC{21001+i}",
            "IcMId": f"28821{1+i:03d}",
            "RoutingId": f"RT21{1+i:03d}",
            "Title": f"Retention policy issue - Americas Case {i+1}",
            "Severity": 3 if i < 3 else 4,
            "CreatedBy": f"support.americas{i%3+1}@microsoft.com",
            "OwningTeam": "Purview-DLM",
            "ResolveDate": (base_date - timedelta(days=i+2)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Customer Context",
            "LowQualityReason": "Customer impact not clearly documented",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Enterprise",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "Americas",
            "FeatureArea": "DLM",
            "SourceOrigin": "Americas-US"
        })
    
    # Americas - eDiscovery cases
    for i in range(4):
        escalations.append({
            "IncidentId": f"INC{22001+i}",
            "IcMId": f"28822{1+i:03d}",
            "RoutingId": f"RT22{1+i:03d}",
            "Title": f"eDiscovery search performance - Americas Case {i+1}",
            "Severity": 2 if i == 0 else 3,
            "CreatedBy": f"support.americas{i%2+1}@microsoft.com",
            "OwningTeam": "Purview-eDiscovery",
            "ResolveDate": (base_date - timedelta(days=i+3)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Insufficient Investigation",
            "LowQualityReason": "Basic troubleshooting steps not documented",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "GBB",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "Americas",
            "FeatureArea": "eDiscovery",
            "SourceOrigin": "Americas-US"
        })
    
    # EMEA - MIP/DLP cases
    for i in range(7):
        escalations.append({
            "IncidentId": f"INC{30001+i}",
            "IcMId": f"28830{1+i:03d}",
            "RoutingId": f"RT30{1+i:03d}",
            "Title": f"Sensitivity labels not syncing - EMEA Case {i+1}",
            "Severity": 3,
            "CreatedBy": f"support.emea{i%3+1}@microsoft.com",
            "OwningTeam": "Purview-MIP",
            "ResolveDate": (base_date - timedelta(days=i+2)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Diagnostics",
            "LowQualityReason": "No logs or screenshots provided",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "EMEA",
            "FeatureArea": "MIP/DLP",
            "SourceOrigin": "EMEA-Europe"
        })
    
    # EMEA - DLM cases
    for i in range(6):
        escalations.append({
            "IncidentId": f"INC{31001+i}",
            "IcMId": f"28831{1+i:03d}",
            "RoutingId": f"RT31{1+i:03d}",
            "Title": f"Records management configuration - EMEA Case {i+1}",
            "Severity": 3 if i < 4 else 4,
            "CreatedBy": f"support.emea{i%2+1}@microsoft.com",
            "OwningTeam": "Purview-DLM",
            "ResolveDate": (base_date - timedelta(days=i+1)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Insufficient Investigation",
            "LowQualityReason": "Did not verify configuration settings",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Enterprise",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "EMEA",
            "FeatureArea": "DLM",
            "SourceOrigin": "EMEA-Europe"
        })
    
    # EMEA - eDiscovery cases
    for i in range(5):
        escalations.append({
            "IncidentId": f"INC{32001+i}",
            "IcMId": f"28832{1+i:03d}",
            "RoutingId": f"RT32{1+i:03d}",
            "Title": f"Hold policy not working - EMEA Case {i+1}",
            "Severity": 2 if i == 0 else 3,
            "CreatedBy": f"support.emea{i%3+1}@microsoft.com",
            "OwningTeam": "Purview-eDiscovery",
            "ResolveDate": (base_date - timedelta(days=i+4)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Customer Context",
            "LowQualityReason": "Business impact not documented",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "EMEA",
            "FeatureArea": "eDiscovery",
            "SourceOrigin": "EMEA-Europe"
        })
    
    # APAC - MIP/DLP cases
    for i in range(6):
        escalations.append({
            "IncidentId": f"INC{40001+i}",
            "IcMId": f"28840{1+i:03d}",
            "RoutingId": f"RT40{1+i:03d}",
            "Title": f"DLP policy blocking legitimate content - APAC Case {i+1}",
            "Severity": 3,
            "CreatedBy": f"support.apac{i%2+1}@microsoft.com",
            "OwningTeam": "Purview-MIP",
            "ResolveDate": (base_date - timedelta(days=i+3)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Diagnostics",
            "LowQualityReason": "No policy logs collected",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Commercial",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "APAC",
            "FeatureArea": "MIP/DLP",
            "SourceOrigin": "APAC-Asia"
        })
    
    # APAC - DLM cases
    for i in range(4):
        escalations.append({
            "IncidentId": f"INC{41001+i}",
            "IcMId": f"28841{1+i:03d}",
            "RoutingId": f"RT41{1+i:03d}",
            "Title": f"Retention label deployment issue - APAC Case {i+1}",
            "Severity": 3 if i < 2 else 4,
            "CreatedBy": f"support.apac{i%2+1}@microsoft.com",
            "OwningTeam": "Purview-DLM",
            "ResolveDate": (base_date - timedelta(days=i+5)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Insufficient Investigation",
            "LowQualityReason": "Did not check tenant configuration",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "Enterprise",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "APAC",
            "FeatureArea": "DLM",
            "SourceOrigin": "APAC-Asia"
        })
    
    # APAC - eDiscovery cases
    for i in range(3):
        escalations.append({
            "IncidentId": f"INC{42001+i}",
            "IcMId": f"28842{1+i:03d}",
            "RoutingId": f"RT42{1+i:03d}",
            "Title": f"Content search timeout - APAC Case {i+1}",
            "Severity": 3,
            "CreatedBy": f"support.apac{i%2+1}@microsoft.com",
            "OwningTeam": "Purview-eDiscovery",
            "ResolveDate": (base_date - timedelta(days=i+6)).isoformat(),
            "FiscalWeek": 24,
            "EscalationQuality": "Missing Customer Context",
            "LowQualityReason": "Search scope not clearly defined",
            "QualityReviewFalsePositive": "",
            "CustomerSegment": "GBB",
            "IsTrueLowQuality": True,
            "ReviewerName": "",
            "OriginRegion": "APAC",
            "FeatureArea": "eDiscovery",
            "SourceOrigin": "APAC-Asia"
        })
    
    return escalations


if __name__ == '__main__':
    import os
    from pathlib import Path
    
    # Generate test data
    data = generate_14day_test_data()
    
    # Save to file
    output_dir = Path(__file__).parent / 'data'
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d')
    output_file = output_dir / f'regional_lqe_14day_test_{timestamp}.json'
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Generated {len(data)} test escalations")
    print(f"Saved to: {output_file}")
    print()
    print("Summary:")
    
    # Count by region and feature
    from collections import defaultdict
    by_region = defaultdict(lambda: defaultdict(int))
    
    for esc in data:
        region = esc['OriginRegion']
        feature = esc['FeatureArea']
        by_region[region][feature] += 1
    
    for region in sorted(by_region.keys()):
        print(f"\n{region}:")
        for feature, count in sorted(by_region[region].items()):
            print(f"  - {feature}: {count} cases")
