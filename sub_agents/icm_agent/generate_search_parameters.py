"""
Fetch Expanded By-Design ICMs using ICM MCP
Searches for last 180 days across all MIP/DLP/Encryption teams

Author: Carter Ryan  
Created: February 11, 2026
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

def generate_search_parameters():
    """Generate search parameters for ICM queries"""
    
    # Teams to search
    teams = {
        "Labeling": [
            "PURVIEW\\SensitivityLabels",
            "PURVIEW\\Classification",
            "PURVIEW\\ClientSideLabeling"
        ],
        "DLP": [
            "PURVIEW\\DLP",
            "PURVIEW\\DLP\\Alerts",
            "PURVIEW\\DLP\\Endpoint",
            "PURVIEW\\DLP\\Exchange",
            "PURVIEW\\DLP\\SharePointOneDrive",
            "PURVIEW\\DLP\\Teams"
        ],
        "Encryption": [
            "PURVIEW\\InformationProtection",
            "PURVIEW\\Encryption",
            "PURVIEW\\RMS",
            "PURVIEW\\AIP",
            "PURVIEW\\ProtectionSDK"
        ],
        "Auto-labeling": [
            "PURVIEW\\ServerSideAutoLabeling"
        ]
    }
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    search_params = {
        "date_range": {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
            "days": 180
        },
        "filters": {
            "resolution": "By Design",
            "prevention_types": "ALL"  # Not filtering by prevention type
        },
        "teams": teams
    }
    
    return search_params


def main():
    print("="*80)
    print("ICM SEARCH PARAMETERS FOR EXPANDED BY-DESIGN ANALYSIS")
    print("="*80)
    print()
    
    params = generate_search_parameters()
    
    print(f"📅 DATE RANGE:")
    print(f"   Start: {params['date_range']['start']}")
    print(f"   End: {params['date_range']['end']}")
    print(f"   Duration: {params['date_range']['days']} days")
    print()
    
    print(f"🔍 FILTERS:")
    print(f"   Resolution: {params['filters']['resolution']}")
    print(f"   Prevention Types: {params['filters']['prevention_types']}")
    print()
    
    print(f"👥 TEAMS TO SEARCH:")
    total_teams = 0
    for category, team_list in params['teams'].items():
        print(f"\n   {category} ({len(team_list)} teams):")
        for team in team_list:
            team_short = team.split("\\")[-1]
            print(f"      • {team_short}")
            total_teams += 1
    
    print()
    print(f"   TOTAL: {total_teams} teams")
    print()
    
    # Save parameters
    output_file = Path(__file__).parent / "data" / "search_parameters.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(params, f, indent=2)
    
    print(f"💾 Search parameters saved to: {output_file}")
    print()
    
    # Generate ICM portal search URLs
    print("="*80)
    print("🔗 ICM PORTAL SEARCH LINKS")
    print("="*80)
    print()
    print("Use these links to search in ICM portal:")
    print()
    
    base_url = "https://portal.microsofticm.com/imp/v3/incidents/search"
    
    for category, team_list in params['teams'].items():
        print(f"\n{category}:")
        for team in team_list:
            team_short = team.split("\\")[-1]
            # ICM search format (simplified - actual URL encoding needed)
            search_url = f"{base_url}?q=OwningTeam:{team}+HowFixed:ByDesign+CreatedDate:>{params['date_range']['start']}"
            print(f"   {team_short}:")
            print(f"      {search_url}")
    
    print()
    print("="*80)
    print("📋 NEXT STEPS")
    print("="*80)
    print()
    print("OPTION 1: Export from ICM Portal")
    print("-" * 40)
    print("1. Use the search links above in ICM portal")
    print("2. Export incident IDs to CSV/JSON")
    print("3. Save to: data/expanded_by_design_icm_ids.txt (one ID per line)")
    print()
    print("OPTION 2: Use Kusto Direct")
    print("-" * 40)
    print("1. Run the queries in: queries/expanded_by_design_180days/")
    print("2. Combine results and extract incident IDs")
    print("3. Save to: data/expanded_by_design_icm_ids.txt")
    print()
    print("OPTION 3: Provide Known ICM IDs")
    print("-" * 40)
    print("If you have ICM IDs from another source:")
    print("   python fetch_and_analyze.py <id1> <id2> <id3> ...")
    print()
    print("="*80)
    

if __name__ == "__main__":
    main()
