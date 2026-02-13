"""
Fetch real LQE data from Kusto for last 14 days
"""
import json
import os
from datetime import datetime
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.identity import DefaultAzureCredential


def load_engineer_region_mapping():
    """Load support engineer to region mapping."""
    mapping_file = os.path.join(os.path.dirname(__file__), 'support_engineer_regions.json')
    if os.path.exists(mapping_file):
        with open(mapping_file, 'r') as f:
            config = json.load(f)
            # Filter out comment keys
            return {k: v for k, v in config['mappings'].items() if not k.startswith('_comment')}
    return {}

def fetch_lqe_data():
    """Fetch LQE data from Kusto."""
    
    cluster = "https://icmcluster.kusto.windows.net"
    database = "IcMDataWarehouse"
    
    # Use Interactive authentication (will open browser)
    kcsb = KustoConnectionStringBuilder.with_interactive_login(cluster)
    client = KustoClient(kcsb)
    
    query = """
    let incidents = IncidentsDedupView
    | where OwningTenantName == "Purview"
    | where ResolveDate > ago(7d)
    | where IncidentType == "CustomerReported"
    | project IncidentId, RoutingId, Title, Severity, 
        CreatedBy = SourceCreatedBy, OwningTeam = OwningTeamName, 
        ResolveDate, SourceOrigin;
    let quality = IncidentCustomFieldEntriesDedupView
    | where Name == "Escalation Quality"
    | project IncidentId, EscalationQuality = Value;
    let reviewer = IncidentCustomFieldEntriesDedupView
    | where Name == "Escalation Reviewer"
    | project IncidentId, ReviewerName = Value;
    let region = IncidentCustomFieldEntriesDedupView
    | where Name == "Time Zone"
    | project IncidentId, TimeZone = Value;
    let qualityReason = IncidentCustomFieldEntriesDedupView
    | where Name == "Low Quality Reason"
    | project IncidentId, LowQualityReason = Value;
    let falsePositive = IncidentCustomFieldEntriesDedupView
    | where Name == "Escalation quality standards"
    | project IncidentId, QualityReviewFalsePositive = Value;
    incidents
    | join kind=inner quality on IncidentId
    | join kind=leftouter reviewer on IncidentId
    | join kind=leftouter region on IncidentId
    | join kind=leftouter qualityReason on IncidentId
    | join kind=leftouter falsePositive on IncidentId
    | where EscalationQuality != "All Data Provided"
    | where isempty(ReviewerName) or ReviewerName == ""
    | where QualityReviewFalsePositive != "Yes" or isempty(QualityReviewFalsePositive)
    | extend OriginRegion = "Unknown"
    | extend FeatureAreaCategory = case(
        OwningTeam contains "DLP" or OwningTeam contains "MIP" or OwningTeam contains "InformationProtection" or OwningTeam contains "RMS" or OwningTeam contains "SensitivityLabels" or OwningTeam contains "Classification" or OwningTeam contains "ExactDataMatch" or OwningTeam contains "EDM" or OwningTeam contains "ServerSideAutoLabeling" or OwningTeam contains "InformationBarriers" or OwningTeam contains "TrainableClassifiers", "MIP/DLP",
        OwningTeam contains "DLM" or OwningTeam contains "Lifecycle" or OwningTeam contains "Retention" or OwningTeam contains "Records", "DLM",
        OwningTeam contains "eDiscovery" or OwningTeam contains "eDisc" or OwningTeam contains "Discovery" or OwningTeam contains "Compliance", "eDiscovery",
        "Other"
    )
    | extend FeatureAreaDetail = case(
        FeatureAreaCategory == "Other" and OwningTeam contains @"\", extract(@"Purview\\(.*)", 1, OwningTeam),
        FeatureAreaCategory == "Other", OwningTeam,
        ""
    )
    | project 
        IncidentId,
        IcMId = IncidentId,
        RoutingId,
        Title,
        Severity,
        CreatedBy,
        OwningTeam,
        ResolveDate,
        EscalationQuality,
        LowQualityReason,
        QualityReviewFalsePositive,
        CustomerSegment = "Unknown",
        IsTrueLowQuality = true,
        ReviewerName,
        OriginRegion,
        FeatureArea = FeatureAreaCategory,
        FeatureAreaDetail,
        SourceOrigin,
        TimeZone
    | order by OriginRegion asc, FeatureArea asc, ResolveDate desc
    """
    
    print("Executing Kusto query...")
    print(f"Cluster: {cluster}")
    print(f"Database: {database}")
    print()
    
    try:
        response = client.execute(database, query)
        
        # Load engineer region mapping
        engineer_mapping = load_engineer_region_mapping()
        
        # Convert to list of dictionaries
        results = []
        columns = [col.column_name for col in response.primary_results[0].columns]
        
        for row in response.primary_results[0]:
            record = {}
            for i, col in enumerate(columns):
                value = row[i]
                # Convert datetime to ISO format string
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                record[col] = value
            
            results.append(record)
        
        # Apply engineer region mapping to all escalations
        mapped_count = 0
        for record in results:
            created_by = record.get('CreatedBy', '')
            if created_by in engineer_mapping:
                record['OriginRegion'] = engineer_mapping[created_by]
                mapped_count += 1
        
        print(f"✓ Query successful! Retrieved {len(results)} escalations")
        print(f"✓ Applied support engineer region mapping: {mapped_count}/{len(results)} escalations mapped")
        print(f"✓ Engineer mapping database contains {len(engineer_mapping)} known engineers")
        
        # Save to file
        output_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, f'regional_lqe_14day_real_{timestamp}.json')
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"✓ Data saved to: {output_file}")
        print()
        
        # Print summary
        from collections import defaultdict
        by_region = defaultdict(lambda: defaultdict(int))
        
        for esc in results:
            region = esc.get('OriginRegion', 'Unknown')
            feature = esc.get('FeatureArea', 'Unknown')
            by_region[region][feature] += 1
        
        print("Summary:")
        for region in sorted(by_region.keys()):
            print(f"\n{region}:")
            for feature, count in sorted(by_region[region].items()):
                print(f"  - {feature}: {count} cases")
        
        print()
        print("Now run:")
        print(f'python generate_regional_lqe_reports.py "{output_file}"')
        
        return output_file
        
    except Exception as e:
        print(f"Error executing query: {e}")
        print()
        print("Make sure you're authenticated with Azure CLI:")
        print("  az login")
        return None


if __name__ == '__main__':
    fetch_lqe_data()
