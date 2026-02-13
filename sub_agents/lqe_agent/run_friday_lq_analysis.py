"""
Friday Weekly Low Quality Escalation Analysis Runner

Specialized script for Friday night runs to analyze unassigned low quality escalations
from the past 7 days, organized by region and feature area.

This script focuses on:
- Escalations closed in last 7 days
- Cases with blank/no reviewer assignment
- Organization by originating region (Americas, EMEA, APAC, LATAM)
- Organization by feature area (MIP/DLP, DLM, eDiscovery)

Author: Carter Ryan
Created: February 5, 2026
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from low_quality_escalation_agent import LowQualityEscalationAgent
from friday_lq_html_generator import FridayLQEHTMLGenerator


class FridayLQRunner:
    """Runner for Friday night unassigned low quality escalation analysis."""
    
    def __init__(self, config_path: str = None):
        """Initialize the Friday runner."""
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 'lq_escalation_config.json'
        )
        self.agent = LowQualityEscalationAgent(config_path=self.config_path)
        
    def get_kusto_query(self) -> str:
        """
        Get the Kusto query for Friday's unassigned low quality escalations.
        
        Returns:
            Kusto query string
        """
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
    
    def run_friday_analysis(self, data_file: str = None) -> Dict:
        """
        Run the Friday night analysis workflow.
        
        Args:
            data_file: Optional path to pre-loaded data file
            
        Returns:
            Dictionary with analysis results
        """
        print("\n" + "="*80)
        print("FRIDAY NIGHT LOW QUALITY ESCALATION ANALYSIS")
        print(f"Run Date: {datetime.now().strftime('%A, %B %d, %Y %I:%M %p')}")
        print("="*80 + "\n")
        
        results = {
            'run_date': datetime.now().isoformat(),
            'period_start': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'period_end': datetime.now().strftime('%Y-%m-%d'),
            'success': False
        }
        
        # If data file provided, load it
        if data_file and os.path.exists(data_file):
            print(f"Loading data from: {data_file}")
            self.agent.load_escalations(from_file=data_file)
        else:
            # Show query for manual execution
            print("Step 1: Execute Kusto Query")
            print("-" * 80)
            print("Cluster: https://icmcluster.kusto.windows.net")
            print("Database: IcMDataWarehouse")
            print("\nQuery:")
            print(self.get_kusto_query())
            print("-" * 80)
            print("\nTo execute:")
            print("1. Use GitHub Copilot MCP tool: mcp_kusto-mcp-ser_execute_query")
            print("2. Save results to: data/friday_lq_YYYYMMDD.json")
            print("3. Re-run with: python run_friday_lq_analysis.py --data-file data/friday_lq_YYYYMMDD.json")
            print("\n")
            results['query'] = self.get_kusto_query()
            results['instructions'] = {
                'step_1': 'Execute Kusto query via MCP tool',
                'step_2': 'Save to data/friday_lq_YYYYMMDD.json',
                'step_3': 'Re-run with --data-file parameter'
            }
            return results
        
        # Organize data by region and feature area
        print("\nStep 2: Organizing Escalations")
        print("-" * 80)
        organized = self.agent.organize_by_region_and_feature()
        
        # Display summary
        total = len(self.agent.escalations_data)
        print(f"\nTotal Unassigned Low Quality Escalations: {total}")
        print(f"Regions Affected: {len(organized)}\n")
        
        region_summary = {}
        for region, features in sorted(organized.items()):
            region_total = sum(len(escs) for escs in features.values())
            region_summary[region] = {'total': region_total, 'by_feature': {}}
            
            print(f"  {region}: {region_total} escalations")
            for feature, escs in sorted(features.items()):
                print(f"    - {feature}: {len(escs)} cases")
                region_summary[region]['by_feature'][feature] = len(escs)
        
        # Generate detailed report
        print("\nStep 3: Generating Report")
        print("-" * 80)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(
            os.path.dirname(__file__),
            'friday_reports',
            f'friday_lq_report_{timestamp}.json'
        )
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        # Build comprehensive report
        report = {
            'report_metadata': {
                'report_type': 'Friday Weekly Unassigned Low Quality Escalations',
                'generated_date': datetime.now().isoformat(),
                'period_days': 7,
                'period_start': results['period_start'],
                'period_end': results['period_end'],
                'filter_criteria': {
                    'escalation_quality': 'Not "All Data Provided"',
                    'reviewer_assignment': 'Blank/Empty',
                    'false_positive_review': 'Not marked as false positive'
                }
            },
            'executive_summary': {
                'total_escalations': total,
                'regions_affected': len(organized),
                'by_region': region_summary
            },
            'escalations_by_region': organized,
            'reviewer_instructions': {
                'purpose': 'Review unassigned low quality escalations and assign reviewers',
                'next_steps': [
                    'Review escalations by region and feature area',
                    'Assign appropriate reviewer for each case',
                    'Follow up with escalation owners on quality issues',
                    'Update escalation tracking systems'
                ],
                'reviewer_list': self._get_reviewer_list()
            }
        }
        
        # Save report
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved: {report_path}")
        
        # Also generate CSV for easy viewing
        csv_path = report_path.replace('.json', '.csv')
        self.agent.generate_csv_report(output_path=csv_path)
        print(f"CSV saved: {csv_path}")
        
        # Generate HTML report
        html_path = report_path.replace('.json', '.htm')
        print(f"\nGenerating HTML report...")
        html_generator = FridayLQEHTMLGenerator()
        html_generator.generate_report(report, html_path)
        print(f"HTML saved: {html_path}")
        
        results['success'] = True
        results['summary'] = region_summary
        results['report_path'] = report_path
        results['csv_path'] = csv_path
        results['html_path'] = html_path
        
        print("\n" + "="*80)
        print("FRIDAY ANALYSIS COMPLETE")
        print("="*80 + "\n")
        
        return results
    
    def _get_reviewer_list(self) -> List[Dict]:
        """Get list of available reviewers from config."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            return config.get('reviewers', [])
        except Exception:
            return []


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Friday night low quality escalation analysis'
    )
    parser.add_argument(
        '--data-file',
        type=str,
        help='Path to pre-loaded Kusto query results JSON file'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    runner = FridayLQRunner(config_path=args.config)
    
    try:
        results = runner.run_friday_analysis(data_file=args.data_file)
        
        if results['success']:
            print("\nGenerated files:")
            print(f"  Report: {results['report_path']}")
            print(f"  CSV: {results['csv_path']}")
            print(f"  HTML: {results['html_path']}")
            
            print("\nNext steps:")
            print("  1. Review the report file for detailed breakdown")
            print("  2. Distribute to reviewer team for assignment")
            print("  3. Follow up on quality issues with escalation owners")
        else:
            print("\nTo complete analysis:")
            print("  1. Execute the Kusto query shown above")
            print("  2. Save results to data/friday_lq_YYYYMMDD.json")
            print("  3. Re-run this script with --data-file parameter")
            
    except Exception as e:
        print(f"\nError during analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
