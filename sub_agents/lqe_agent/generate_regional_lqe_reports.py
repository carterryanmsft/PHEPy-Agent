"""
Generate Regional LQE Reports

Creates separate reports for Americas, EMEA, and APAC regions with 
region-specific reviewer assignments for last 7 days of unassigned LQEs.

Author: Carter Ryan
Created: February 11, 2026
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Not importing LowQualityEscalationAgent - self-contained generator


class RegionalLQEReportGenerator:
    """Generate region-specific LQE reports."""
    
    def __init__(self, config_path: str = None):
        """Initialize the regional report generator."""
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 'config', 'regional_reviewers_config.json'
        )
        self.regional_config = self._load_regional_config()
        
    def _load_regional_config(self) -> Dict:
        """Load regional reviewer configuration."""
        if not os.path.exists(self.config_path):
            # Return default config if file doesn't exist
            return {
                'regions': {
                    'Americas': {},
                    'EMEA': {},
                    'APAC': {}
                }
            }
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def get_14day_kusto_query(self) -> str:
        """
        Get the Kusto query for last 7 days of unassigned low quality escalations.
        
        Returns:
            Kusto query string
        """
        return """
let escalationInformation = IncidentsDedupView
| where OwningTenantName == "Purview"
| where ResolveDate > ago(14d)
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
    isempty(FeatureArea), "Other",
    "Other"
)
| extend FeatureAreaDetail = case(
   FeatureAreaCategory == "Other" and OwningTeamName contains @"\", extract(@"Purview\\(.*)", 1, OwningTeamName),
    FeatureAreaCategory == "Other", OwningTeamName,
    ""
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
    FeatureAreaDetail,
    SourceOrigin
| order by OriginRegion asc, FeatureArea asc, ResolveDate desc
"""
    
    def filter_data_by_region(self, data: List[Dict], region: str) -> List[Dict]:
        """Filter escalations by region."""
        if region == "APAC":
            # APAC includes both APAC and Unknown (often Asia-Pacific cases)
            return [esc for esc in data if esc.get('OriginRegion') in ['APAC', 'Unknown']]
        else:
            return [esc for esc in data if esc.get('OriginRegion') == region]
    
    def generate_regional_report(self, region: str, escalations: List[Dict], output_dir: str) -> Dict:
        """
        Generate a regional report.
        
        Args:
            region: Region name (Americas, EMEA, APAC)
            escalations: List of escalation dictionaries
            output_dir: Output directory path
            
        Returns:
            Report metadata
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Get reviewers for this region
        region_reviewers = self.regional_config['regions'].get(region, {})
        
        # Organize by feature area
        by_feature = {}
        for esc in escalations:
            feature = esc.get('FeatureArea', 'Other')
            if feature not in by_feature:
                by_feature[feature] = []
            by_feature[feature].append(esc)
        
        # Calculate quality issue summary
        quality_summary = {}
        for esc in escalations:
            quality = esc.get('EscalationQuality', 'Unknown')
            quality_summary[quality] = quality_summary.get(quality, 0) + 1
        
        # Build report structure
        report = {
            'metadata': {
                'report_type': 'Regional LQE Analysis',
                'region': region,
                'generated': datetime.now().isoformat(),
                'date_range': 'Last 7 days',
                'total_escalations': len(escalations)
            },
            'summary': {
                'total_count': len(escalations),
                'by_feature_area': {feature: len(cases) for feature, cases in by_feature.items()},
                'by_quality_issue': quality_summary
            },
            'reviewers': region_reviewers,
            'escalations_by_feature': {}
        }
        
        # Add escalations organized by feature area
        for feature, cases in by_feature.items():
            report['escalations_by_feature'][feature] = {
                'count': len(cases),
                'reviewers': region_reviewers.get(feature, []),
                'escalations': cases
            }
        
        # Save JSON report
        json_filename = f'{region.lower()}_lqe_report_{timestamp}.json'
        json_path = os.path.join(output_dir, json_filename)
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Save CSV
        csv_filename = f'{region.lower()}_lqe_report_{timestamp}.csv'
        csv_path = os.path.join(output_dir, csv_filename)
        df = pd.DataFrame(escalations)
        
        # Add reviewer column
        def get_reviewers(row):
            feature = row.get('FeatureArea', 'Other')
            reviewers = region_reviewers.get(feature, [])
            return ', '.join([r['name'] for r in reviewers])
        
        if not df.empty:
            df['AssignedReviewers'] = df.apply(get_reviewers, axis=1)
            df.to_csv(csv_path, index=False)
        
        # Generate HTML report
        html_filename = f'{region.lower()}_lqe_report_{timestamp}.htm'
        html_path = os.path.join(output_dir, html_filename)
        self._generate_html_report(region, report, html_path)
        
        return {
            'region': region,
            'total': len(escalations),
            'json_path': json_path,
            'csv_path': csv_path,
            'html_path': html_path,
            'by_feature': {feature: len(cases) for feature, cases in by_feature.items()}
        }
    
    def _generate_html_report(self, region: str, report: Dict, output_path: str):
        """Generate HTML report for a region."""
        
        # Build email-optimized HTML with inline styles
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{region} LQE Report - Last 7 Days</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 800px; margin: 0 auto; background-color: #ffffff;">
        <!-- Header -->
        <tr>
            <td style="background-color: #0078d4; color: #ffffff; padding: 20px;">
                <h1 style="margin: 0; font-size: 24px; font-weight: bold;">{region} Region - Low Quality Escalation Report</h1>
                <p style="margin: 10px 0 0 0; font-size: 14px;">Generated: {report['metadata']['generated'][:10]} | Date Range: Last 7 Days</p>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Total Unassigned LQEs: <strong>{report['summary']['total_count']}</strong></p>
            </td>
        </tr>
        
        <!-- Summary by Feature Area -->
        <tr>
            <td style="padding: 20px;">
                <h2 style="margin: 0 0 15px 0; font-size: 18px; color: #333;">Summary by Feature Area</h2>
                <ul style="margin: 0; padding-left: 20px;">
"""
        
        # Add summary
        for feature, count in report['summary']['by_feature_area'].items():
            html_content += f"                    <li style=\"margin-bottom: 8px;\"><strong>{feature}</strong>: {count} cases</li>\n"
        
        html_content += """                </ul>
            </td>
        </tr>
        
        <!-- Quality Issues Summary -->
        <tr>
            <td style="padding: 20px; background-color: #f9f9f9;">
                <h2 style="margin: 0 0 15px 0; font-size: 18px; color: #333;">Quality Issues Summary</h2>
                <ul style="margin: 0; padding-left: 20px;">
"""
        
        # Add quality issue summary
        for quality, count in sorted(report['summary']['by_quality_issue'].items(), key=lambda x: x[1], reverse=True):
            html_content += f"                    <li style=\"margin-bottom: 8px;\"><strong>{quality}</strong>: {count} cases</li>\n"
        
        html_content += """                </ul>
            </td>
        </tr>
"""
        
        # Add feature sections
        for feature, data in report['escalations_by_feature'].items():
            reviewers = data['reviewers']
            
            html_content += f"""        
        <!-- {feature} Section -->
        <tr>
            <td style="padding: 20px; border-top: 3px solid #0078d4;">
                <div style="background-color: #f0f0f0; padding: 10px; font-weight: bold; font-size: 16px; border-left: 4px solid #0078d4; margin-bottom: 15px;">
                    {feature} ({data['count']} cases)
                </div>
                
                <table width="100%" cellpadding="8" cellspacing="0" style="border-collapse: collapse; margin-top: 10px;">
                    <thead>
                        <tr>
                            <th style="background-color: #0078d4; color: #ffffff; padding: 10px; text-align: left; border: 1px solid #ddd;">ICM ID</th>
                            <th style="background-color: #0078d4; color: #ffffff; padding: 10px; text-align: left; border: 1px solid #ddd;">Title</th>"""
            
            # Add Team column header for "Other" feature areas
            if feature == "Other":
                html_content += """
                            <th style="background-color: #0078d4; color: #ffffff; padding: 10px; text-align: left; border: 1px solid #ddd;">Team</th>"""
            
            html_content += """
                            <th style="background-color: #0078d4; color: #ffffff; padding: 10px; text-align: left; border: 1px solid #ddd;">Quality Issue</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            
            for esc in data['escalations']:
                icm_id = esc.get('IcMId', 'N/A')
                icm_link = f"https://portal.microsofticm.com/imp/v3/incidents/details/{icm_id}/home"
                title = esc.get('Title', 'N/A')[:80]
                quality = esc.get('EscalationQuality', 'N/A')
                feature_detail = esc.get('FeatureAreaDetail', '')
                
                html_content += f"""                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><a href="{icm_link}" style="color: #0078d4; text-decoration: none;">{icm_id}</a></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{title}</td>"""
                
                # Add Team column for "Other" feature areas
                if feature == "Other":
                    team_display = feature_detail if feature_detail else esc.get('OwningTeam', 'N/A')
                    html_content += f"""
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{team_display}</td>"""
                
                html_content += f"""
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{quality}</td>
                        </tr>
"""
            
            html_content += """                    </tbody>
                </table>
            </td>
        </tr>
"""
        
        html_content += """        
        <!-- Footer -->
        <tr>
            <td style="padding: 20px; background-color: #f9f9f9;">
                <p style="margin: 0 0 10px 0; font-weight: bold;">Action Required:</p>
                <p style="margin: 0; font-size: 14px; color: #666;">Please review these escalations and assign appropriate reviewers in ICM. This report includes escalations closed in the last 7 days that have no reviewer assigned and are not marked as "All Data Provided".</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def run_regional_analysis(self, data_file: str = None) -> Dict:
        """
        Run the full regional analysis.
        
        Args:
            data_file: Optional path to data file (if not provided, shows query)
            
        Returns:
            Analysis results
        """
        print("=" * 80)
        print("REGIONAL LQE REPORT GENERATION")
        print("=" * 80)
        print()
        
        # Load data
        if data_file and os.path.exists(data_file):
            print(f"Loading data from: {data_file}")
            with open(data_file, 'r') as f:
                all_data = json.load(f)
            print(f"Loaded {len(all_data)} escalations")
        else:
            print("No data file provided. Here's the 14-day Kusto query:")
            print()
            print(self.get_14day_kusto_query())
            print()
            print("To run analysis:")
            print("1. Execute the query above in Kusto")
            print("2. Save results to JSON")
            print("3. Run: python generate_regional_lqe_reports.py <data_file.json>")
            return None
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), 'regional_reports')
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate reports for each region
        results = {}
        regions = ['Americas', 'EMEA', 'APAC']
        
        print()
        print("Generating regional reports...")
        print("-" * 80)
        
        for region in regions:
            print(f"\n📍 Processing {region}...")
            
            # Filter data for this region
            regional_data = self.filter_data_by_region(all_data, region)
            
            if regional_data:
                result = self.generate_regional_report(region, regional_data, output_dir)
                results[region] = result
                
                print(f"   ✓ {result['total']} escalations")
                for feature, count in result['by_feature'].items():
                    print(f"     - {feature}: {count}")
                print(f"   📄 Reports saved to: regional_reports/")
            else:
                print(f"   ⚠ No escalations found for {region}")
        
        print()
        print("=" * 80)
        print("✅ REGIONAL REPORTS COMPLETE")
        print("=" * 80)
        print()
        
        # Print summary
        for region, result in results.items():
            print(f"{region}:")
            print(f"  Total: {result['total']} escalations")
            print(f"  JSON: {result['json_path']}")
            print(f"  CSV: {result['csv_path']}")
            print(f"  HTML: {result['html_path']}")
            print()
        
        return results


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate regional LQE reports')
    parser.add_argument('data_file', nargs='?', help='Path to JSON data file')
    args = parser.parse_args()
    
    generator = RegionalLQEReportGenerator()
    generator.run_regional_analysis(data_file=args.data_file)


if __name__ == '__main__':
    main()
