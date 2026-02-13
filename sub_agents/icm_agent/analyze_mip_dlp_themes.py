"""
Analyze MIP/DLP By-Design Themes

Processes ICM query results to identify common themes and patterns
in by-design incidents for encryption, labeling, and DLP.

Author: Carter Ryan
Created: February 11, 2026
"""

import sys
import os
sys.path.insert(0, r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\icm_agent')

from icm_agent import ICMAgent
from pathlib import Path
import json
from datetime import datetime


def main():
    print("="*70)
    print("MIP/DLP By-Design Theme Analysis")
    print("="*70)
    print(f"\nAnalysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize agent
    agent = ICMAgent()
    
    # Load data from file
    data_file = Path(__file__).parent / "data" / "mip_dlp_by_design_results.json"
    
    if not data_file.exists():
        print(f"❌ ERROR: Data file not found")
        print(f"   Expected: {data_file}")
        print()
        print("Please run the ICM queries first using:")
        print("  python analyze_mip_dlp_by_design.py")
        print()
        print("Then execute the generated KQL queries and save results to:")
        print(f"  {data_file}")
        return
    
    print(f"📊 Loading data from: {data_file}")
    agent.load_from_file(str(data_file))
    incident_count = len(agent.incidents_data) if agent.incidents_data is not None else 0
    print(f"✓ Loaded {incident_count} incident patterns")
    
    # Run analysis
    print("\n🔍 Analyzing patterns and generating themes...")
    analysis = agent.analyze_by_design_patterns()
    
    print(f"\n✓ Analysis complete!")
    print(f"  Total 'By Design' Incidents: {analysis['summary']['total_by_design_incidents']}")
    print(f"  Unique Issue Types: {analysis['summary']['unique_issue_types']}")
    print(f"  Themes Identified: {analysis['summary']['total_themes_identified']}")
    print(f"  Customers Affected: {analysis['summary']['total_customers_affected']}")
    
    # Generate report
    print("\n📄 Generating HTML report...")
    report_path = agent.generate_report()
    print(f"✓ Report generated: {report_path}")
    
    # Export theme impact queries
    print("\n📝 Exporting theme impact queries...")
    query_files = agent.export_theme_impact_queries()
    print(f"✓ Generated {len(query_files)} theme impact queries")
    
    # Save themes for documentation gap analysis
    themes_file = Path(__file__).parent / "data" / "mip_dlp_themes.json"
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_to_json_serializable(obj):
        """Convert numpy types to native Python types."""
        import numpy as np
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_to_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_json_serializable(item) for item in obj]
        return obj
    
    serializable_data = {
        'analysis_date': datetime.now().isoformat(),
        'scope': 'MIP/DLP - Last 90 days',
        'teams': ['SensitivityLabels', 'DLP', 'InformationProtection'],
        'summary': convert_to_json_serializable(analysis['summary']),
        'themes': convert_to_json_serializable(analysis['themes'])
    }
    
    with open(themes_file, 'w') as f:
        json.dump(serializable_data, f, indent=2)
    
    print(f"\n✓ Themes saved for documentation analysis: {themes_file}")
    
    # Display top themes
    print("\n" + "="*70)
    print("🎯 Top Themes Identified")
    print("="*70)
    
    # Convert themes dict to list of theme data with names
    themes_list = []
    if isinstance(analysis['themes'], dict):
        for theme_name, theme_data in analysis['themes'].items():
            theme_info = {
                'theme_name': theme_name,
                'total_incidents': theme_data['total_incidents'],
                'total_customers': theme_data['total_customers_affected'],
                'issue_count': theme_data['unique_issue_types'],
                'related_issues': theme_data.get('incidents', [])
            }
            themes_list.append(theme_info)
        # Sort by total incidents descending
        themes_list.sort(key=lambda x: x['total_incidents'], reverse=True)
    
    for i, theme in enumerate(themes_list[:10], 1):
        print(f"\n{i}. {theme['theme_name']}")
        print(f"   📊 {theme['total_incidents']} incidents | "
              f"👥 {theme['total_customers']} customers | "
              f"📋 {theme['issue_count']} unique issues")
        print(f"   Related Issues:")
        for issue in theme['related_issues'][:3]:
            print(f"     • {issue['title'][:70]}...")
            print(f"       {issue['count']} incidents | {issue['customers']} customers")
    
    print("\n" + "="*70)
    print("✅ Theme analysis complete!")
    print("="*70)
    print(f"\nNext step: Run documentation gap analysis")
    print("  python generate_doc_gap_analysis.py")
    print()
    print(f"Or open the report in browser:")
    print(f"  {report_path}")
    
    # Optionally open report
    import webbrowser
    webbrowser.open(report_path)


if __name__ == "__main__":
    main()
