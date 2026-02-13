import sys
import os

# Add the icm_agent directory to path
sys.path.insert(0, r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\icm_agent')

# Import and run the ICM agent
from icm_agent import ICMAgent

# Initialize agent
agent = ICMAgent()

# Load data from file
data_file = r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\icm_agent\data\dlp_by_design_results.json'
print(f"Loading data from: {data_file}")
agent.load_from_file(data_file)

# Run analysis
print("\nAnalyzing patterns...")
analysis = agent.analyze_by_design_patterns()

# Generate report
print("\nGenerating report...")
report_path = agent.generate_report()

# Export theme impact queries
print("\nExporting theme impact queries...")
query_files = agent.export_theme_impact_queries()

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print(f"\nReport: {report_path}")
print(f"Themes Identified: {analysis['summary']['total_themes_identified']}")
print(f"Total 'By Design' Incidents: {analysis['summary']['total_by_design_incidents']}")

# Open report in browser
import webbrowser
webbrowser.open(report_path)
print(f"\nOpening report in browser...")
