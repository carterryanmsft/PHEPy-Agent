"""
Full End-to-End By-Design ICM Analysis
Expanded scope: 180 days, all By-Design ICMs, all MIP/DLP/Encryption teams

Author: Carter Ryan
Created: February 11, 2026
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add icm_agent to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("="*80)
    print("FULL END-TO-END BY-DESIGN ICM ANALYSIS")
    print("="*80)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📋 SCOPE:")
    print("  • Timeline: Last 180 days")
    print("  • Resolution: By Design (ALL prevention types)")
    print("  • Teams: 15 MIP/DLP/Encryption teams")
    print()
    
    # Teams covered
    teams = [
        "Sensitivity Labels", "Classification", "DLP (Generic)", "DLP Alerts",
        "DLP Endpoint", "DLP Exchange", "DLP SharePoint OneDrive", "DLP Teams",
        "Information Protection", "Encryption", "RMS", "AIP",
        "Server Side Auto Labeling", "Client Side Labeling", "Protection SDK"
    ]
    
    print(f"📊 TEAMS COVERED ({len(teams)}):")
    for i, team in enumerate(teams, 1):
        print(f"  {i:2d}. {team}")
    print()
    
    # Check for query files
    query_dir = Path(__file__).parent / "queries" / "expanded_by_design_180days"
    
    if not query_dir.exists():
        print("⚠️  Query directory not found. Creating queries...")
        from icm_agent import ICMAgent
        agent = ICMAgent()
        query_dir.mkdir(parents=True, exist_ok=True)
        
        team_paths = [
            "PURVIEW\\SensitivityLabels",
            "PURVIEW\\Classification",
            "PURVIEW\\DLP",
            "PURVIEW\\DLP\\Alerts",
            "PURVIEW\\DLP\\Endpoint",
            "PURVIEW\\DLP\\Exchange",
            "PURVIEW\\DLP\\SharePointOneDrive",
            "PURVIEW\\DLP\\Teams",
            "PURVIEW\\InformationProtection",
            "PURVIEW\\Encryption",
            "PURVIEW\\RMS",
            "PURVIEW\\AIP",
            "PURVIEW\\ServerSideAutoLabeling",
            "PURVIEW\\ClientSideLabeling",
            "PURVIEW\\ProtectionSDK"
        ]
        
        for team_path in team_paths:
            team_short = team_path.split("\\")[-1]
            query = agent.get_by_design_query(team_name=team_path, days_back=180)
            query_file = query_dir / f"{team_short}_by_design_180days.kql"
            with open(query_file, 'w') as f:
                f.write(query)
            print(f"  ✓ {team_short}")
        print()
    
    query_files = list(query_dir.glob("*.kql"))
    print(f"✓ Found {len(query_files)} query files")
    print()
    
    print("="*80)
    print("⚠️  MANUAL STEP REQUIRED - EXECUTE KUSTO QUERIES")
    print("="*80)
    print()
    print("To continue, you need to execute the KQL queries to get ICM IDs:")
    print()
    print("OPTION 1: Use Kusto MCP Tool")
    print("-" * 40)
    print("Execute queries in: queries/expanded_by_design_180days/")
    print("Against: https://icmcluster.kusto.windows.net")
    print("Database: IcMDataWarehouse")
    print()
    print("OPTION 2: Provide ICM IDs Directly")
    print("-" * 40)
    print("If you have ICM IDs from another source, save them to:")
    print("  data/expanded_by_design_icm_ids.txt")
    print("  (One ICM ID per line)")
    print()
    print("="*80)
    print()
    
    # Check if we have ICM IDs
    icm_ids_file = Path(__file__).parent / "data" / "expanded_by_design_icm_ids.txt"
    
    if icm_ids_file.exists():
        print("✓ Found ICM IDs file!")
        with open(icm_ids_file, 'r') as f:
            icm_ids = [line.strip() for line in f if line.strip().isdigit()]
        
        print(f"  Total ICMs to analyze: {len(icm_ids)}")
        print()
        
        # TODO: Fetch ICM details using MCP
        # TODO: Run analysis
        # TODO: Generate reports
        
        print("🚀 Ready to fetch ICM details and generate reports...")
        print()
        print("Next step: Run fetch and analysis...")
        
    else:
        print("⏸️  Waiting for ICM IDs...")
        print()
        print("Once you have ICM IDs, either:")
        print("  1. Save them to: data/expanded_by_design_icm_ids.txt")
        print("  2. Or run: python fetch_expanded_icms.py <icm_id1> <icm_id2> ...")
        print()
    
    print("="*80)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)


if __name__ == "__main__":
    main()
