"""
Execute Friday LQE Kusto Query and Generate Reports

This script executes the Friday LQE query via MCP Kusto tool and generates
4 HTML reports: 1 all-up report and 1 for each region (Americas, EMEA, APAC).

Usage:
    Ask GitHub Copilot to execute the Kusto query and save results to data/
    Then run: python generate_friday_reports.py

Author: Carter Ryan
Created: February 5, 2026
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from friday_lq_html_generator import FridayLQEHTMLGenerator


class FridayReportGenerator:
    """Generate multiple Friday LQE reports from Kusto data."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.html_generator = FridayLQEHTMLGenerator()
        self.data = None
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def get_kusto_query(self) -> str:
        """Get the Kusto query to execute."""
        return """
let escalationInformation = IncidentsDedupView
| where OwningTenantName == "Purview"
| where ResolveDate > ago(7d)
| where IncidentType == "CustomerReported"
| extend FiscalWeek = 24 - toint((fw24EndDate - ResolveDate) / 7d)
| project ResolveDate, FiscalWeek, IncidentId, SourceCreatedBy, OwningTeamName, 
    Title, Severity, RoutingId, IcMId, CustomerSegment, SourceOrigin, ImpactStartDate;
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
let reviewerAssignment = IncidentCustomFieldEntriesDedupView
| where Name == "Escalation Reviewer"
| project IncidentId, ReviewerName = Value;
let featureArea = IncidentCustomFieldEntriesDedupView
| where Name == "Feature Area"
| project IncidentId, FeatureArea = Value;
escalationInformation
| join kind=inner (qualityInformation) on IncidentId
| join kind=leftouter (supportReviews) on IncidentId
| join kind=leftouter (qualityReasons) on IncidentId
| join kind=leftouter (reviewerAssignment) on IncidentId
| join kind=leftouter (featureArea) on IncidentId
| where EscalationQuality != "All Data Provided"
| where QualityReviewFalsePositive != "Yes" or isempty(QualityReviewFalsePositive)
| where isempty(ReviewerName) or ReviewerName == ""
| extend OriginRegion = case(
    SourceOrigin contains "EMEA" or SourceOrigin contains "Europe", "EMEA",
    SourceOrigin contains "APAC" or SourceOrigin contains "Asia", "APAC",
    SourceOrigin contains "LATAM" or SourceOrigin contains "Latin", "LATAM",
    SourceOrigin contains "Americas" or SourceOrigin contains "US" or SourceOrigin contains "NA", "Americas",
    "Unknown"
)
| extend FeatureAreaCategory = case(
    FeatureArea contains "MIP" or FeatureArea contains "DLP" or FeatureArea contains "Information Protection", "MIP/DLP",
    FeatureArea contains "DLM" or FeatureArea contains "Lifecycle" or FeatureArea contains "Retention", "DLM",
    FeatureArea contains "eDiscovery" or FeatureArea contains "eDisc" or FeatureArea contains "Discovery", "eDiscovery",
    FeatureArea contains "Compliance" or FeatureArea contains "Records", "Compliance",
    isempty(FeatureArea), "Unknown",
    "Other"
)
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
    IsTrueLowQuality,
    ReviewerName,
    OriginRegion,
    FeatureArea = FeatureAreaCategory,
    SourceOrigin
| order by OriginRegion asc, FeatureArea asc, ResolveDate desc
"""
    
    def load_kusto_data(self, data_file: str) -> List[Dict]:
        """Load escalation data from Kusto query results."""
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'results' in data:
            return data['results']
        else:
            raise ValueError("Unexpected data format")
    
    def organize_by_region_and_feature(self, escalations: List[Dict]) -> Dict:
        """Organize escalations by region and feature area."""
        organized = defaultdict(lambda: defaultdict(list))
        
        for esc in escalations:
            region = esc.get('OriginRegion', 'Unknown')
            feature = esc.get('FeatureArea', 'Unknown')
            organized[region][feature].append(esc)
        
        return {region: dict(features) for region, features in organized.items()}
    
    def generate_report_data(self, escalations: List[Dict], region_filter: str = None) -> Dict:
        """Generate report data structure."""
        # Filter by region if specified
        if region_filter:
            escalations = [e for e in escalations if e.get('OriginRegion') == region_filter]
        
        # Organize data
        organized = self.organize_by_region_and_feature(escalations)
        
        # Calculate summary
        total = len(escalations)
        regions_summary = {}
        
        for region, features in organized.items():
            region_total = sum(len(escs) for escs in features.values())
            feature_breakdown = {feature: len(escs) for feature, escs in features.items()}
            regions_summary[region] = {
                'total': region_total,
                'by_feature': feature_breakdown
            }
        
        # Build report structure
        period_end = datetime.now()
        period_start = period_end.replace(day=period_end.day - 7) if period_end.day > 7 else period_end.replace(month=period_end.month-1, day=period_end.day+23)
        
        report_type = f"{region_filter} Region Low Quality Escalations" if region_filter else "All Regions - Unassigned Low Quality Escalations"
        
        return {
            'report_metadata': {
                'report_type': report_type,
                'generated_date': datetime.now().isoformat(),
                'period_days': 7,
                'period_start': period_start.strftime('%Y-%m-%d'),
                'period_end': period_end.strftime('%Y-%m-%d'),
                'region_filter': region_filter
            },
            'executive_summary': {
                'total_escalations': total,
                'regions_affected': len(organized),
                'by_region': regions_summary
            },
            'escalations_by_region': organized
        }
    
    def generate_all_reports(self, data_file: str, output_dir: str = None) -> Dict[str, str]:
        """
        Generate all 4 reports from Kusto data.
        
        Args:
            data_file: Path to Kusto query results JSON
            output_dir: Output directory for reports
            
        Returns:
            Dictionary mapping report type to file path
        """
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'friday_reports')
        
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n" + "="*80)
        print("FRIDAY LQE REPORT GENERATION - MULTI-REPORT")
        print("="*80 + "\n")
        
        # Load data
        print(f"Loading Kusto data from: {data_file}")
        escalations = self.load_kusto_data(data_file)
        print(f"Loaded {len(escalations)} escalations\n")
        
        reports = {}
        
        # 1. All-up report
        print("Generating All-Up Report...")
        allup_data = self.generate_report_data(escalations)
        allup_path = os.path.join(output_dir, f'friday_lq_allup_{self.timestamp}.htm')
        self.html_generator.generate_report(allup_data, allup_path)
        reports['All-Up'] = allup_path
        print(f"  ✓ {allup_data['executive_summary']['total_escalations']} total escalations\n")
        
        # 2-4. Regional reports
        regions = ['Americas', 'EMEA', 'APAC']
        for region in regions:
            print(f"Generating {region} Report...")
            region_data = self.generate_report_data(escalations, region_filter=region)
            region_count = region_data['executive_summary']['total_escalations']
            
            if region_count > 0:
                region_path = os.path.join(output_dir, f'friday_lq_{region.lower()}_{self.timestamp}.htm')
                self.html_generator.generate_report(region_data, region_path)
                reports[region] = region_path
                print(f"  ✓ {region_count} escalations\n")
            else:
                print(f"  ⊘ No escalations for {region}\n")
        
        print("="*80)
        print("REPORT GENERATION COMPLETE")
        print("="*80 + "\n")
        
        print("Generated Reports:")
        for report_type, path in reports.items():
            print(f"  {report_type}: {path}")
        
        return reports


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate Friday LQE reports from Kusto data'
    )
    parser.add_argument(
        'data_file',
        nargs='?',
        help='Path to Kusto query results JSON file'
    )
    parser.add_argument(
        '--execute-query',
        action='store_true',
        help='Show query to execute in Kusto'
    )
    
    args = parser.parse_args()
    
    generator = FridayReportGenerator()
    
    # Show query if requested
    if args.execute_query or not args.data_file:
        print("\n" + "="*80)
        print("KUSTO QUERY FOR FRIDAY LQE DATA")
        print("="*80 + "\n")
        print("Cluster: https://icmcluster.kusto.windows.net")
        print("Database: IcMDataWarehouse\n")
        print("Query:")
        print("-"*80)
        print(generator.get_kusto_query())
        print("-"*80 + "\n")
        print("INSTRUCTIONS:")
        print("1. Execute query via GitHub Copilot MCP tool: mcp_kusto-mcp-ser_execute_query")
        print("2. Save results to: data/friday_lq_kusto_YYYYMMDD.json")
        print("3. Run: python generate_friday_reports.py data/friday_lq_kusto_YYYYMMDD.json")
        print("\n")
        
        if not args.data_file:
            return 0
    
    # Generate reports
    try:
        reports = generator.generate_all_reports(args.data_file)
        
        print("\n✅ All reports generated successfully!\n")
        print("To view reports, open them in your browser:")
        for report_type, path in reports.items():
            print(f"  start \"{path}\"")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error generating reports: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
