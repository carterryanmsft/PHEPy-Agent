"""
Weekly Regional LQE Report Automation

Fetches fresh data from Kusto and generates regional LQE reports for:
- Americas
- EMEA  
- APAC

Author: Carter Ryan
Created: February 13, 2026
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from fetch_real_lqe_data import fetch_lqe_data
from generate_regional_lqe_reports import RegionalLQEReportGenerator


class WeeklyRegionalLQEAutomation:
    """Automates weekly regional LQE report generation."""
    
    def __init__(self, skip_data_fetch: bool = False):
        """
        Initialize automation.
        
        Args:
            skip_data_fetch: If True, use most recent data file instead of fetching
        """
        self.skip_data_fetch = skip_data_fetch
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.reports_dir = os.path.join(os.path.dirname(__file__), 'reports', 'regional_reports')
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def get_latest_data_file(self) -> Optional[str]:
        """Find the most recent LQE data file."""
        data_files = [
            f for f in os.listdir(self.data_dir) 
            if f.startswith('regional_lqe_') and f.endswith('.json')
        ]
        
        if not data_files:
            return None
        
        # Sort by timestamp in filename
        data_files.sort(reverse=True)
        return os.path.join(self.data_dir, data_files[0])
    
    def fetch_fresh_data(self) -> Optional[str]:
        """
        Fetch fresh LQE data from Kusto.
        
        Returns:
            Path to data file or None if fetch failed
        """
        print("=" * 80)
        print("FETCHING FRESH LQE DATA FROM KUSTO")
        print("=" * 80)
        print()
        
        try:
            data_file = fetch_lqe_data()
            
            if data_file and os.path.exists(data_file):
                print(f"✓ Fresh data saved to: {data_file}")
                return data_file
            else:
                print("✗ Failed to fetch data from Kusto")
                return None
                
        except Exception as e:
            print(f"✗ Error fetching data: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_data(self, data_file: str) -> List[Dict]:
        """Load LQE data from JSON file."""
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Handle both list and dict formats
        if isinstance(data, dict):
            return data.get('data', [])
        return data
    
    def generate_regional_reports(self, data_file: str) -> Dict[str, str]:
        """
        Generate reports for all regions.
        
        Args:
            data_file: Path to LQE data file
            
        Returns:
            Dictionary mapping region to HTML report path
        """
        print()
        print("=" * 80)
        print("GENERATING REGIONAL LQE REPORTS")
        print("=" * 80)
        print()
        
        # Load data
        print(f"Loading data from: {data_file}")
        escalations = self.load_data(data_file)
        print(f"✓ Loaded {len(escalations)} total escalations")
        print()
        
        # Initialize generator
        generator = RegionalLQEReportGenerator()
        
        # Generate reports for each region
        regions = ['Americas', 'EMEA', 'APAC']
        report_paths = {}
        
        for region in regions:
            print(f"Generating {region} report...")
            
            # Filter data for this region
            if region == 'APAC':
                # APAC includes Unknown
                regional_data = [
                    e for e in escalations 
                    if e.get('OriginRegion') in ['APAC', 'Unknown']
                ]
            else:
                regional_data = [
                    e for e in escalations 
                    if e.get('OriginRegion') == region
                ]
            
            print(f"  - Found {len(regional_data)} escalations for {region}")
            
            if len(regional_data) == 0:
                print(f"  ⚠ No escalations found for {region}, skipping...")
                continue
            
            # Generate report
            try:
                report_metadata = generator.generate_regional_report(
                    region=region,
                    escalations=regional_data,
                    output_dir=self.reports_dir
                )
                
                # The HTML report path
                html_file = report_metadata.get('html_path')
                if html_file:
                    report_paths[region] = html_file
                    print(f"  ✓ {region} report generated:")
                    print(f"    HTML: {html_file}")
                    
            except Exception as e:
                print(f"  ✗ Error generating {region} report: {e}")
                import traceback
                traceback.print_exc()
        
        return report_paths
    
    def print_summary(self, data_file: str, report_paths: Dict[str, str]):
        """Print execution summary."""
        print()
        print("=" * 80)
        print("WEEKLY REGIONAL LQE REPORT - EXECUTION SUMMARY")
        print("=" * 80)
        print()
        print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Data Source: {data_file}")
        print()
        print("📁 Reports Generated:")
        for region, path in report_paths.items():
            print(f"   ✓ {region:10s} → {os.path.basename(path)}")
        print()
        print("📂 Report Location:")
        print(f"   {self.reports_dir}")
        print()
        print("=" * 80)
    
    def run(self) -> bool:
        """
        Execute complete weekly workflow.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Step 1: Get data file
            if self.skip_data_fetch:
                print("Using existing data file...")
                data_file = self.get_latest_data_file()
                
                if not data_file:
                    print("✗ No existing data files found. Run with --fetch to get fresh data.")
                    return False
                
                print(f"✓ Using: {data_file}")
                print()
            else:
                data_file = self.fetch_fresh_data()
                
                if not data_file:
                    print("✗ Failed to fetch fresh data")
                    
                    # Try to use existing data as fallback
                    print()
                    print("Attempting to use latest existing data file...")
                    data_file = self.get_latest_data_file()
                    
                    if not data_file:
                        print("✗ No fallback data available")
                        return False
                    
                    print(f"✓ Using fallback: {data_file}")
            
            # Step 2: Generate regional reports
            report_paths = self.generate_regional_reports(data_file)
            
            if not report_paths:
                print("✗ No reports generated")
                return False
            
            # Step 3: Print summary
            self.print_summary(data_file, report_paths)
            
            return True
            
        except Exception as e:
            print()
            print("=" * 80)
            print("✗ EXECUTION FAILED")
            print("=" * 80)
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate weekly regional LQE reports with fresh data'
    )
    parser.add_argument(
        '--skip-fetch',
        action='store_true',
        help='Skip data fetch and use most recent data file'
    )
    parser.add_argument(
        '--use-data',
        type=str,
        metavar='FILE',
        help='Use specific data file (skips fetch)'
    )
    
    args = parser.parse_args()
    
    print()
    print("=" * 80)
    print("WEEKLY REGIONAL LQE REPORT AUTOMATION")
    print("=" * 80)
    print()
    
    # Run automation
    automation = WeeklyRegionalLQEAutomation(skip_data_fetch=args.skip_fetch)
    
    # Override with specific file if provided
    if args.use_data:
        if not os.path.exists(args.use_data):
            print(f"✗ Data file not found: {args.use_data}")
            sys.exit(1)
        
        print(f"Using specified data file: {args.use_data}")
        report_paths = automation.generate_regional_reports(args.use_data)
        
        if report_paths:
            automation.print_summary(args.use_data, report_paths)
            sys.exit(0)
        else:
            print("✗ Failed to generate reports")
            sys.exit(1)
    
    # Run full workflow
    success = automation.run()
    
    if success:
        print()
        print("✓✓✓ Weekly regional LQE reports generated successfully!")
        print()
        sys.exit(0)
    else:
        print()
        print("✗✗✗ Failed to generate weekly reports")
        print()
        sys.exit(1)


if __name__ == '__main__':
    main()
