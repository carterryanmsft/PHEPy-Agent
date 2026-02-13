"""
Expanded By-Design Analysis - 180 Days
Includes ALL By-Design ICMs for MIP/DLP/Encryption teams, not just public documentation

Author: Carter Ryan
Created: February 11, 2026
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add the icm_agent directory to path
sys.path.insert(0, r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\icm_agent')
from icm_agent import ICMAgent


def main():
    print("="*80)
    print("EXPANDED BY-DESIGN ANALYSIS - MIP/DLP/ENCRYPTION")
    print("="*80)
    print(f"\nAnalysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Scope: Last 180 days")
    print("Resolution: By Design (ALL prevention types)")
    print()
    
    # All MIP/DLP/Encryption teams
    teams = [
        # Labeling & Classification
        "PURVIEW\\SensitivityLabels",
        "PURVIEW\\Classification",
        
        # DLP Teams
        "PURVIEW\\DLP",
        "PURVIEW\\DLP (Generic)",
        "PURVIEW\\DLP Alerts",
        "PURVIEW\\DLP Endpoint",
        "PURVIEW\\DLP Exchange",
        "PURVIEW\\DLP SharePoint OneDrive",
        "PURVIEW\\DLP Teams",
        
        # Information Protection & Encryption
        "PURVIEW\\InformationProtection",
        "PURVIEW\\Encryption",
        "PURVIEW\\RMS",
        "PURVIEW\\AIP",
        
        # Auto Labeling
        "PURVIEW\\Server Side Auto Labeling",
        "PURVIEW\\ServerSideAutoLabeling",
    ]
    
    # Initialize agent
    agent = ICMAgent()
    
    print("\n📋 Generating ICM Queries for MIP/DLP/Encryption Teams")
    print("-"*80)
    
    # Query directory
    query_dir = Path(__file__).parent / "queries" / "expanded_by_design_180days"
    query_dir.mkdir(parents=True, exist_ok=True)
    
    all_queries = {}
    
    for team in teams:
        # Generate By Design query (180 days, all prevention types)
        query = agent.get_by_design_query(team_name=team, days_back=180)
        
        team_short = team.split("\\")[-1].replace(" ", "_")
        all_queries[team_short] = query
        
        # Save query to file
        query_file = query_dir / f"{team_short}_by_design_180days.kql"
        with open(query_file, 'w') as f:
            f.write(query)
        
        print(f"✓ Generated query for {team}")
        print(f"  File: {query_file.name}")
    
    print("\n" + "="*80)
    print("📊 QUERY EXECUTION INSTRUCTIONS")
    print("="*80)
    
    print("""
The queries have been generated for ALL By-Design ICMs (not just public documentation).

OPTION 1: Execute via GitHub Copilot using ICM MCP
---------------------------------------------------
Ask Copilot:
"Please execute all KQL queries in the folder:
 sub_agents/icm_agent/queries/expanded_by_design_180days/
 
 Use the ICM MCP server with:
 - Cluster: https://icmcluster.kusto.windows.net
 - Database: IcMDataWarehouse
 
 Save the combined results to:
 sub_agents/icm_agent/data/expanded_by_design_180days_results.json"

OPTION 2: Manual Execution via Kusto Explorer
----------------------------------------------
1. Open Kusto Explorer
2. Connect to: https://icmcluster.kusto.windows.net
3. Select Database: IcMDataWarehouse
4. Execute each query file in: queries/expanded_by_design_180days/
5. Export all results as JSON
6. Save combined results to: data/expanded_by_design_180days_results.json

OPTION 3: Use ICM MCP Directly
-------------------------------
Request the following ICM data:
- Teams: Classification, DLP (all variants), Sensitivity Labels, 
         Server Side Auto Labeling, Encryption, RMS, AIP, Information Protection
- Resolution: By Design (HowFixed = "By Design")
- Date Range: Last 180 days
- Include ALL prevention types (not just "Public Documentation")

NEXT STEPS:
-----------
After query execution, run:
  python analyze_expanded_by_design.py

This will:
1. Load the ICM data
2. Identify themes and patterns
3. Categorize by prevention type
4. Generate comprehensive documentation gap analysis
5. Create executive summary report
""")
    
    print("\n" + "="*80)
    print(f"✅ {len(teams)} queries generated")
    print(f"📁 Query directory: {query_dir}")
    print("="*80)
    
    # Create instructions file
    instruction_file = query_dir / "README_EXECUTION.md"
    with open(instruction_file, 'w', encoding='utf-8') as f:
        f.write(f"""# ICM Query Execution Instructions

## Expanded By-Design Analysis - 180 Days

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Scope:** Last 180 days  
**Resolution Type:** By Design (ALL prevention types)  
**Teams:** {len(teams)} MIP/DLP/Encryption teams

## Teams Included

### Labeling & Classification
- Sensitivity Labels
- Classification

### DLP (All Workloads)
- DLP (Generic)
- DLP Alerts
- DLP Endpoint
- DLP Exchange
- DLP SharePoint OneDrive
- DLP Teams

### Information Protection & Encryption
- Information Protection
- Encryption
- RMS (Rights Management Service)
- AIP (Azure Information Protection)

### Auto Labeling
- Server Side Auto Labeling

## Query Files

All query files are in this directory. Each file is named:
`[TeamName]_by_design_180days.kql`

## Execution Options

### Option 1: GitHub Copilot with ICM MCP (Recommended)

Ask Copilot:
```
Please execute all KQL queries in:
sub_agents/icm_agent/queries/expanded_by_design_180days/

Use ICM MCP with:
- Cluster: https://icmcluster.kusto.windows.net
- Database: IcMDataWarehouse

Save combined results to:
sub_agents/icm_agent/data/expanded_by_design_180days_results.json
```

### Option 2: Kusto Explorer

1. Open Kusto Explorer
2. Connect: https://icmcluster.kusto.windows.net
3. Database: IcMDataWarehouse
4. Execute each .kql file
5. Export as JSON and combine

### Option 3: ICM Portal Advanced Search

Use these filters:
- owning_team_id IN (teams listed above)
- how_fixed = "By Design"
- created_date >= now() - 180d
- Export results

## Expected Data

Each ICM should include:
- ID
- Title
- Description/Summary
- Severity
- Status
- Owning Team
- Created Date
- Modified Date
- How Fixed (should be "By Design")
- Prevention Type (if available)
- Customer Name
- Source

## Next Steps

After gathering data, run:
```bash
python analyze_expanded_by_design.py
```

This will generate:
1. Comprehensive documentation gap analysis
2. Prevention type breakdown
3. Theme identification across all By-Design types
4. Executive summary report (using approved format)
""")
    
    print(f"\n📄 Execution instructions saved to:")
    print(f"   {instruction_file}")
    print()


if __name__ == "__main__":
    main()
