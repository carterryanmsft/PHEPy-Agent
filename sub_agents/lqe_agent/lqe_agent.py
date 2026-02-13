"""
Low Quality Escalation Insight Agent

This agent analyzes escalations marked as low quality, organizes them by owner,
and prepares weekly reports for reviewers to follow up on escalation quality issues.

Author: Carter Ryan
Created: February 4, 2026
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
import pandas as pd


class LowQualityEscalationAgent:
    """Agent for analyzing and reporting on low quality escalations."""
    
    def __init__(self, kusto_client=None, config_path: str = None):
        """
        Initialize the Low Quality Escalation Agent.
        
        Args:
            kusto_client: Kusto client instance for running queries
            config_path: Path to reviewer configuration file
        """
        self.kusto_client = kusto_client
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 'lq_escalation_config.json'
        )
        self.reviewer_mapping = self._load_reviewer_config()
        self.escalations_data = None
        self.organized_data = None
        
    def _load_reviewer_config(self) -> Dict:
        """Load reviewer configuration from JSON file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                # Return default configuration structure
                return {
                    "reviewers": [],
                    "default_reviewer": "unassigned@example.com",
                    "escalation_owners": {}
                }
        except Exception as e:
            print(f"Error loading reviewer config: {e}")
            return {"reviewers": [], "default_reviewer": None, "escalation_owners": {}}
    
    def get_detailed_escalation_query(self, days_back: int = 30) -> str:
        """
        Generate Kusto query to get detailed low quality escalation information.
        
        Args:
            days_back: Number of days to look back for escalations
            
        Returns:
            Kusto query string
        """
        return f"""
let escalationInformation = IncidentsDedupView
| where OwningTenantName == "Purview"
| where ResolveDate > ago({days_back}d)
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
| extend IsTrueLowQuality = (QualityReviewFalsePositive != "Yes" or isempty(QualityReviewFalsePositive))
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
"""
    
    def get_weekly_unassigned_query(self, days_back: int = 7) -> str:
        """
        Generate Kusto query for weekly Friday run - unassigned low quality escalations
        with region and feature area information.
        
        This query focuses on cases with blank/no reviewer and includes geographic and
        product area dimensions for report chunking.
        
        Args:
            days_back: Number of days to look back (default 7 for weekly)
            
        Returns:
            Kusto query string with region and feature area
        """
        return f"""
let escalationInformation = IncidentsDedupView
| where OwningTenantName == "Purview"
| where ResolveDate > ago({days_back}d)
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
    
    def get_team_metrics_query(self, days_back: int = 30) -> str:
        """
        Generate Kusto query for team-level metrics (the original query).
        
        Args:
            days_back: Number of days to look back for escalations
            
        Returns:
            Kusto query string
        """
        return f"""
let escalationInformation = IncidentsDedupView
| where OwningTenantName == "Purview"
| where ResolveDate > ago({days_back}d)
| where IncidentType == "CustomerReported"
| extend FiscalWeek = 24 - toint((fw24EndDate - ResolveDate) / 7d)
| project ResolveDate, FiscalWeek, IncidentId, SourceCreatedBy, OwningTeamName;
let qualityInformation =
IncidentCustomFieldEntriesDedupView
| where Name == "Escalation Quality"
| project IncidentId, EscalationQuality = Value;
let supportReviews = IncidentCustomFieldEntriesDedupView
| where Name == "Escalation quality standards"
| project IncidentId, QualityReviewFalsePositive = Value;
let teamMetrics = escalationInformation
| join kind=inner (qualityInformation) on IncidentId
| join kind=leftouter (supportReviews) on IncidentId
| summarize
    AllEsc = count(),
    LQMarked = countif(EscalationQuality != "All Data Provided"),
    FP = countif(EscalationQuality != "All Data Provided" and QualityReviewFalsePositive == "Yes"),
    TrueLQ = countif(EscalationQuality != "All Data Provided" and QualityReviewFalsePositive != "Yes")
    by OwningTeam = OwningTeamName
| extend 
    LQMarkedPct = strcat(round(todouble(LQMarked) / todouble(AllEsc) * 100, 1), "%"),
    TrueLQPct = strcat(round(todouble(TrueLQ) / todouble(AllEsc) * 100, 1), "%"),
    FPPct = strcat(round(todouble(FP) / todouble(LQMarked) * 100, 1), "%");
let allUpRow = teamMetrics
| summarize
    AllEsc = sum(AllEsc),
    LQMarked = sum(LQMarked),
    FP = sum(FP),
    TrueLQ = sum(TrueLQ)
| extend OwningTeam = "All Up"
| extend 
    LQMarkedPct = strcat(round(todouble(LQMarked) / todouble(AllEsc) * 100, 1), "%"),
    TrueLQPct = strcat(round(todouble(TrueLQ) / todouble(AllEsc) * 100, 1), "%"),
    FPPct = strcat(round(todouble(FP) / todouble(LQMarked) * 100, 1), "%");
union teamMetrics, allUpRow
| order by OwningTeam asc
"""
    
    def execute_query_mcp(self, query: str, cluster_url: str = "https://icmcluster.kusto.windows.net", 
                          database: str = "IcMDataWarehouse", max_rows: int = 10000) -> pd.DataFrame:
        """
        Execute Kusto query using MCP Kusto tool and return results as DataFrame.
        
        This method calls the MCP Kusto execute_query tool which handles authentication.
        
        Args:
            query: Kusto query string
            cluster_url: Kusto cluster URL
            database: Kusto database name
            max_rows: Maximum number of rows to return
            
        Returns:
            DataFrame with query results
        """
        print(f"\nExecuting query via MCP Kusto on {cluster_url}/{database}...")
        print(f"Max rows: {max_rows}")
        
        # Note: This is a placeholder - actual MCP call would be made by GitHub Copilot
        # For now, we'll raise an error directing to use the MCP tool directly
        raise NotImplementedError(
            "Please use the mcp_kusto-mcp-ser_execute_query tool directly from GitHub Copilot.\n"
            f"Query to execute:\n{query}\n\n"
            f"Cluster: {cluster_url}\n"
            f"Database: {database}\n"
            f"Max Rows: {max_rows}"
        )
    
    def load_escalations(self, days_back: int = 30, from_file: str = None) -> pd.DataFrame:
        """
        Load low quality escalation data either from Kusto or from a file.
        
        Args:
            days_back: Number of days to look back
            from_file: Optional path to JSON file with cached data
            
        Returns:
            DataFrame with escalation data
        """
        if from_file and os.path.exists(from_file):
            print(f"Loading escalations from file: {from_file}")
            with open(from_file, 'r') as f:
                data = json.load(f)
            self.escalations_data = pd.DataFrame(data)
        else:
            print(f"Executing Kusto query for last {days_back} days...")
            query = self.get_detailed_escalation_query(days_back)
            self.escalations_data = self.execute_query_mcp(query)
            
            # Save to cache file if requested
            if from_file:
                self._save_to_file(self.escalations_data, from_file)
        
        print(f"Loaded {len(self.escalations_data)} low quality escalations")
        return self.escalations_data
    
    def _save_to_file(self, df: pd.DataFrame, filepath: str):
        """Save DataFrame to JSON file."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            df.to_json(filepath, orient='records', indent=2)
            print(f"Saved data to: {filepath}")
        except Exception as e:
            print(f"Error saving to file: {e}")
    
    def organize_by_owner(self) -> Dict[str, List[Dict]]:
        """
        Organize escalations by creator/owner.
        
        Returns:
            Dictionary mapping owner email to list of their escalations
        """
        if self.escalations_data is None:
            raise ValueError("No escalation data loaded. Call load_escalations() first.")
        
        organized = defaultdict(list)
        
        for _, row in self.escalations_data.iterrows():
            owner = row.get('CreatedBy', 'Unknown')
            escalation = {
                'IncidentId': row.get('IncidentId'),
                'IcMId': row.get('IcMId'),
                'RoutingId': row.get('RoutingId'),
                'Title': row.get('Title'),
                'Severity': row.get('Severity'),
                'OwningTeam': row.get('OwningTeam'),
                'ResolveDate': str(row.get('ResolveDate')),
                'FiscalWeek': row.get('FiscalWeek'),
                'EscalationQuality': row.get('EscalationQuality'),
                'LowQualityReason': row.get('LowQualityReason'),
                'CustomerSegment': row.get('CustomerSegment')
            }
            organized[owner].append(escalation)
        
        self.organized_data = dict(organized)
        return self.organized_data
    
    def organize_by_region_and_feature(self) -> Dict[str, Dict[str, List[Dict]]]:
        """
        Organize escalations by region and feature area for weekly Friday reports.
        
        Returns:
            Dictionary structured as {region: {feature_area: [escalations]}}
        """
        if self.escalations_data is None:
            raise ValueError("No escalation data loaded. Call load_escalations() first.")
        
        organized = defaultdict(lambda: defaultdict(list))
        
        for _, row in self.escalations_data.iterrows():
            region = row.get('OriginRegion', 'Unknown')
            feature_area = row.get('FeatureArea', 'Unknown')
            
            escalation = {
                'IncidentId': row.get('IncidentId'),
                'IcMId': row.get('IcMId'),
                'RoutingId': row.get('RoutingId'),
                'Title': row.get('Title'),
                'Severity': row.get('Severity'),
                'CreatedBy': row.get('CreatedBy'),
                'OwningTeam': row.get('OwningTeam'),
                'ResolveDate': str(row.get('ResolveDate')),
                'FiscalWeek': row.get('FiscalWeek'),
                'EscalationQuality': row.get('EscalationQuality'),
                'LowQualityReason': row.get('LowQualityReason'),
                'CustomerSegment': row.get('CustomerSegment'),
                'SourceOrigin': row.get('SourceOrigin')
            }
            organized[region][feature_area].append(escalation)
        
        # Convert defaultdicts to regular dicts
        return {region: dict(features) for region, features in organized.items()}
    
    def assign_to_reviewers(self) -> Dict[str, Dict[str, List[Dict]]]:
        """
        Assign organized escalations to reviewers based on configuration.
        
        Returns:
            Dictionary mapping reviewer email to their assigned escalations by owner
        """
        if self.organized_data is None:
            self.organize_by_owner()
        
        reviewer_assignments = defaultdict(lambda: defaultdict(list))
        escalation_owners = self.reviewer_mapping.get('escalation_owners', {})
        default_reviewer = self.reviewer_mapping.get('default_reviewer')
        
        for owner, escalations in self.organized_data.items():
            # Find assigned reviewer for this owner
            reviewer = escalation_owners.get(owner, default_reviewer)
            
            if reviewer:
                reviewer_assignments[reviewer][owner] = escalations
            else:
                print(f"Warning: No reviewer assigned for owner: {owner}")
        
        return dict(reviewer_assignments)
    
    def generate_summary_stats(self) -> Dict[str, Any]:
        """
        Generate summary statistics for the loaded escalations.
        
        Returns:
            Dictionary with summary statistics
        """
        if self.escalations_data is None:
            return {}
        
        df = self.escalations_data
        
        stats = {
            'total_escalations': len(df),
            'unique_owners': df['CreatedBy'].nunique() if 'CreatedBy' in df.columns else 0,
            'teams_affected': df['OwningTeam'].nunique() if 'OwningTeam' in df.columns else 0,
            'by_severity': df['Severity'].value_counts().to_dict() if 'Severity' in df.columns else {},
            'by_team': df['OwningTeam'].value_counts().to_dict() if 'OwningTeam' in df.columns else {},
            'by_quality_reason': df['LowQualityReason'].value_counts().to_dict() if 'LowQualityReason' in df.columns else {},
            'date_range': {
                'start': str(df['ResolveDate'].min()) if 'ResolveDate' in df.columns else None,
                'end': str(df['ResolveDate'].max()) if 'ResolveDate' in df.columns else None
            }
        }
        
        return stats
    
    def export_for_review(self, output_dir: str = None) -> Dict[str, str]:
        """
        Export escalations organized by reviewer to separate files.
        
        Args:
            output_dir: Directory to save output files
            
        Returns:
            Dictionary mapping reviewer to their output file path
        """
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'lq_escalation_reports')
        
        os.makedirs(output_dir, exist_ok=True)
        
        reviewer_assignments = self.assign_to_reviewers()
        output_files = {}
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for reviewer, owners_data in reviewer_assignments.items():
            # Create filename
            reviewer_name = reviewer.split('@')[0].replace('.', '_')
            filename = f"lq_escalations_{reviewer_name}_{timestamp}.json"
            filepath = os.path.join(output_dir, filename)
            
            # Prepare data for export
            export_data = {
                'reviewer': reviewer,
                'generated_date': datetime.now().isoformat(),
                'total_escalations': sum(len(escs) for escs in owners_data.values()),
                'owners_count': len(owners_data),
                'escalations_by_owner': owners_data
            }
            
            # Write to file
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            output_files[reviewer] = filepath
            print(f"Exported {export_data['total_escalations']} escalations for {reviewer} to {filepath}")
        
        return output_files
    
    def generate_csv_report(self, output_path: str = None) -> str:
        """
        Generate a CSV report of all low quality escalations.
        
        Args:
            output_path: Path for output CSV file
            
        Returns:
            Path to generated CSV file
        """
        if self.escalations_data is None:
            raise ValueError("No escalation data loaded.")
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(
                os.path.dirname(__file__),
                f'lq_escalations_{timestamp}.csv'
            )
        
        # Add reviewer assignment to data
        df = self.escalations_data.copy()
        escalation_owners = self.reviewer_mapping.get('escalation_owners', {})
        default_reviewer = self.reviewer_mapping.get('default_reviewer', 'Unassigned')
        
        df['AssignedReviewer'] = df['CreatedBy'].map(
            lambda x: escalation_owners.get(x, default_reviewer)
        )
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        print(f"CSV report saved to: {output_path}")
        
        return output_path
    
    def generate_weekly_report(self, output_path: str = None) -> str:
        """
        Generate weekly Friday report for unassigned low quality escalations,
        organized by region and feature area.
        
        Args:
            output_path: Path for output JSON file
            
        Returns:
            Path to generated report file
        """
        if self.escalations_data is None:
            raise ValueError("No escalation data loaded.")
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(
                os.path.dirname(__file__),
                f'weekly_lq_report_{timestamp}.json'
            )
        
        # Organize by region and feature area
        organized = self.organize_by_region_and_feature()
        
        # Calculate summary statistics
        total_escalations = len(self.escalations_data)
        regions_summary = {}
        
        for region, features in organized.items():
            region_total = sum(len(escs) for escs in features.values())
            feature_breakdown = {feature: len(escs) for feature, escs in features.items()}
            regions_summary[region] = {
                'total': region_total,
                'by_feature': feature_breakdown
            }
        
        # Build report structure
        report = {
            'report_type': 'Weekly Unassigned Low Quality Escalations',
            'generated_date': datetime.now().isoformat(),
            'period_days': 7,
            'total_escalations': total_escalations,
            'summary': {
                'regions_affected': len(organized),
                'by_region': regions_summary
            },
            'escalations': organized,
            'metadata': {
                'note': 'All escalations in this report have blank reviewer assignment',
                'filter': 'EscalationQuality != AllDataProvided AND ReviewerName is empty',
                'review_instructions': 'Please review and assign appropriate reviewers for follow-up'
            }
        }
        
        # Write to file
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nWeekly report saved to: {output_path}")
        print(f"Total escalations: {total_escalations}")
        print(f"Regions: {', '.join(organized.keys())}")
        
        return output_path
    
    def run_analysis(self, days_back: int = 30, export_reports: bool = True) -> Dict[str, Any]:
        """
        Run complete analysis workflow.
        
        Args:
            days_back: Number of days to analyze
            export_reports: Whether to export individual reviewer reports
            
        Returns:
            Dictionary with analysis results and file paths
        """
        print(f"\n{'='*60}")
        print("Low Quality Escalation Analysis")
        print(f"{'='*60}\n")
        
        # Load data
        self.load_escalations(days_back=days_back)
        
        # Organize by owner
        self.organize_by_owner()
        
        # Generate summary stats
        stats = self.generate_summary_stats()
        print(f"\nSummary Statistics:")
        print(f"  Total Low Quality Escalations: {stats['total_escalations']}")
        print(f"  Unique Escalation Owners: {stats['unique_owners']}")
        print(f"  Teams Affected: {stats['teams_affected']}")
        
        # Export reports
        output_files = {}
        csv_path = None
        
        if export_reports:
            print("\nExporting reports...")
            output_files = self.export_for_review()
            csv_path = self.generate_csv_report()
        
        results = {
            'summary_stats': stats,
            'organized_data': self.organized_data,
            'reviewer_assignments': self.assign_to_reviewers(),
            'output_files': output_files,
            'csv_report': csv_path
        }
        
        print(f"\n{'='*60}")
        print("Analysis Complete")
        print(f"{'='*60}\n")
        
        return results
    
    def run_weekly_friday_analysis(self, export_report: bool = True) -> Dict[str, Any]:
        """
        Run Friday-specific weekly analysis for unassigned low quality escalations.
        Focus on cases resolved in last 7 days with no reviewer assigned.
        
        Args:
            export_report: Whether to generate weekly report file
            
        Returns:
            Dictionary with analysis results and file paths
        """
        print(f"\n{'='*60}")
        print("Weekly Friday LQ Analysis - Unassigned Cases")
        print(f"Period: Last 7 days (closed {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')})")
        print(f"{'='*60}\n")
        
        # Load data using weekly unassigned query
        print("Loading unassigned low quality escalations from last 7 days...")
        query = self.get_weekly_unassigned_query(days_back=7)
        
        # For now, indicate MCP usage needed
        print("\nQuery ready for execution via MCP Kusto tool:")
        print(f"Cluster: https://icmcluster.kusto.windows.net")
        print(f"Database: IcMDataWarehouse")
        print(f"\nQuery:\n{query}")
        
        # Note: Actual execution would happen via MCP tool
        # self.escalations_data = execute via MCP
        
        results = {
            'report_type': 'weekly_friday_unassigned',
            'query': query,
            'instructions': {
                'step_1': 'Execute query via mcp_kusto-mcp-ser_execute_query',
                'step_2': 'Save results to data/weekly_lq_YYYYMMDD.json',
                'step_3': 'Load data with: load_escalations(from_file=...)',
                'step_4': 'Generate report with: generate_weekly_report()'
            }
        }
        
        # If data is already loaded, generate report
        if self.escalations_data is not None and len(self.escalations_data) > 0:
            organized = self.organize_by_region_and_feature()
            
            print(f"\nAnalysis Summary:")
            print(f"  Total Unassigned LQ Escalations: {len(self.escalations_data)}")
            print(f"  Regions: {len(organized)}")
            
            for region, features in organized.items():
                region_total = sum(len(escs) for escs in features.values())
                print(f"    {region}: {region_total} cases")
                for feature, escs in features.items():
                    print(f"      - {feature}: {len(escs)}")
            
            if export_report:
                report_path = self.generate_weekly_report()
                results['report_path'] = report_path
        
        print(f"\n{'='*60}")
        print("Friday Analysis Complete")
        print(f"{'='*60}\n")
        
        return results


def main():
    """Main execution function for testing."""
    # Initialize agent
    agent = LowQualityEscalationAgent()
    
    # For testing without Kusto client, you can load from a file:
    # agent.load_escalations(from_file='test_data.json')
    
    # Run analysis
    try:
        results = agent.run_analysis(days_back=30, export_reports=True)
        
        print("\nGenerated Files:")
        for reviewer, filepath in results['output_files'].items():
            print(f"  {reviewer}: {filepath}")
        
        if results['csv_report']:
            print(f"\nCSV Report: {results['csv_report']}")
            
    except Exception as e:
        print(f"Error running analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
