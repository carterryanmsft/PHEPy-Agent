"""
Save LQ Escalation Data from Kusto Query Results

This script helps you save Kusto query results for use with the LQ Escalation agent.

Usage:
1. Run your Kusto query in Kusto Explorer or via MCP
2. Copy the results
3. Save them to a JSON file in the data/ directory
4. Run the agent with: python run_weekly_lq_analysis.py --from-file data/lq_escalations.json
"""

import json
from pathlib import Path

# Instructions for manual data collection
INSTRUCTIONS = """
=============================================================================
HOW TO COLLECT LOW QUALITY ESCALATION DATA FROM KUSTO
=============================================================================

Step 1: Run this query in Kusto Explorer or via GitHub Copilot MCP:

Cluster: https://icmcluster.kusto.windows.net
Database: IcMDataWarehouse

Query:
------
let escalationInformation = IncidentsDedupView
| where OwningTenantName == "Purview"
| where ResolveDate > ago(30d)
| where IncidentType == "CustomerReported"
| extend FiscalWeek = 24 - toint((fw24EndDate - ResolveDate) / 7d)
| project ResolveDate, FiscalWeek, IncidentId, SourceCreatedBy, OwningTeamName, 
    Title, Severity, RoutingId, IcMId, CustomerSegment;
let qualityInformation =
IncidentCustomFieldEntriesDedupView
| where Name == "Escalation Quality"
| project IncidentId, EscalationQuality = Value;
let supportReviews = IncidentCustomFieldEntriesDedupView
| where Name == "Escalation quality standards"
| project IncidentId, QualityReviewFalsePositive = Value;
let qualityReasons = IncidentCustomFieldEntriesDedupView
| where Name == "Low Quality Reason"
| project IncidentId, LowQualityReason = Value;
escalationInformation
| join kind=inner (qualityInformation) on IncidentId
| join kind=leftouter (supportReviews) on IncidentId
| join kind=leftouter (qualityReasons) on IncidentId
| where EscalationQuality != "All Data Provided"
| where QualityReviewFalsePositive != "Yes" or isempty(QualityReviewFalsePositive)
| extend IsTrueLowQuality = true
| project 
    IncidentId,
    IcMId,
    RoutingId,
    Title,
    Severity,
    CreatedBy = SourceCreatedBy,
    OwningTeam = OwningTeamName,
    ResolveDate,
    FiscalWeek,
    EscalationQuality,
    LowQualityReason,
    QualityReviewFalsePositive,
    CustomerSegment,
    IsTrueLowQuality
| order by ResolveDate desc, OwningTeam asc
------

Step 2: Export the results to JSON format

Step 3: Save the JSON to: data/lq_escalations_YYYYMMDD.json

Step 4: Run the agent:
    python run_weekly_lq_analysis.py --from-file data/lq_escalations_YYYYMMDD.json

=============================================================================

Alternatively, use the test data we already have:
    python test_lq_with_sample_data.py
    
Or schedule the weekly runner to use cached data files.

=============================================================================
"""

def main():
    print(INSTRUCTIONS)
    
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent / 'data'
    data_dir.mkdir(exist_ok=True)
    print(f"\nData directory created: {data_dir}")
    print(f"Save your Kusto query results there as JSON files.")


if __name__ == "__main__":
    main()
