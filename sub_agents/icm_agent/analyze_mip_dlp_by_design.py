"""
MIP/DLP By-Design Analysis with Documentation Gap Detection

This script:
1. Queries ICM for by-design incidents in MIP/DLP areas (last 90 days)
2. Uses ICM Agent to identify themes
3. Generates documentation gap analysis prompts for Purview Product Expert

Author: Carter Ryan
Created: February 11, 2026
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add the icm_agent directory to path
sys.path.insert(0, r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\sub_agents\icm_agent')
from icm_agent import ICMAgent


def main():
    print("="*70)
    print("MIP/DLP By-Design Analysis & Documentation Gap Detection")
    print("="*70)
    print(f"\nAnalysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Scope: Last 90 days")
    print("Teams: Encryption, Labeling, DLP")
    print()
    
    # MIP/DLP related teams
    teams = [
        "PURVIEW\\SensitivityLabels",  # Labeling
        "PURVIEW\\DLP",                # DLP  
        "PURVIEW\\InformationProtection" # Encryption/MIP
    ]
    
    # Initialize agent
    agent = ICMAgent()
    
    # Query generation for each team
    print("\n📋 Step 1: Generating ICM Queries for MIP/DLP Teams")
    print("-"*70)
    
    all_queries = {}
    for team in teams:
        query = agent.get_by_design_query(team_name=team, days_back=90)
        team_short = team.split("\\")[-1]
        all_queries[team_short] = query
        
        # Save query to file
        query_dir = Path(__file__).parent / "queries" / "mip_dlp_analysis"
        query_dir.mkdir(parents=True, exist_ok=True)
        
        query_file = query_dir / f"{team_short}_by_design_90days.kql"
        with open(query_file, 'w') as f:
            f.write(query)
        
        print(f"✓ Generated query for {team}")
        print(f"  Saved to: {query_file}")
    
    print("\n" + "="*70)
    print("🔍 NEXT STEPS - ICM MCP Query Execution Required")
    print("="*70)
    print("""
The queries have been generated. To complete the analysis:

STEP 2: Execute ICM Queries via Kusto
--------------------------------------
Execute each query file in Kusto Explorer against:
  Cluster: https://icmcluster.kusto.windows.net
  Database: IcMDataWarehouse

Query files are located in:
  sub_agents/icm_agent/queries/mip_dlp_analysis/

STEP 3: Save Query Results
---------------------------
Export results from Kusto as JSON and save to:
  sub_agents/icm_agent/data/mip_dlp_by_design_results.json

Format: JSON array of all results from all three teams

STEP 4: Run Theme Analysis
---------------------------
python sub_agents/icm_agent/analyze_mip_dlp_themes.py

STEP 5: Run Documentation Gap Analysis
---------------------------------------
python sub_agents/icm_agent/generate_doc_gap_analysis.py
""")
    
    # Create instruction file for ICM MCP query
    instruction_file = Path(__file__).parent / "data" / "ICM_QUERY_INSTRUCTIONS.md"
    with open(instruction_file, 'w', encoding='utf-8') as f:
        f.write(f"""# ICM MCP Query Instructions for MIP/DLP By-Design Analysis

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Query Details
- **Scope**: Last 90 days  
- **Teams**: Encryption, Labeling, DLP
- **Resolution Type**: By Design
- **Purpose**: Identify documentation gaps causing customer confusion

## Teams to Query

### 1. Sensitivity Labels (Labeling)
- Team: PURVIEW\\SensitivityLabels
- Query File: `queries/mip_dlp_analysis/SensitivityLabels_by_design_90days.kql`

### 2. DLP  
- Team: PURVIEW\\DLP
- Query File: `queries/mip_dlp_analysis/DLP_by_design_90days.kql`

### 3. Information Protection (Encryption/MIP)
- Team: PURVIEW\\InformationProtection
- Query File: `queries/mip_dlp_analysis/InformationProtection_by_design_90days.kql`

## Using ICM MCP

### Option A: Use Kusto MCP Tool
```
Execute the KQL queries using the kusto-mcp tool with:
- Cluster: https://icmcluster.kusto.windows.net
- Database: IcMDataWarehouse
```

### Option B: Request via GitHub Copilot
Ask Copilot to execute the queries:
```
Please execute the MIP/DLP by-design ICM queries in 
sub_agents/icm_agent/queries/mip_dlp_analysis/ 
using the ICM MCP server and save the combined results to
sub_agents/icm_agent/data/mip_dlp_by_design_results.json
```

## Expected Output Format

Save all results as a single JSON array combining all three teams:

```json
[
  {{
    "Title": "Sensitivity label not visible in File Explorer",
    "Count": 45,
    "FirstSeen": "2025-11-15T10:30:00Z",
    "LastSeen": "2026-02-03T14:22:00Z",
    "SampleIncidents": [728221759, 729445123, 730112456],
    "AffectedCustomers": 32,
    "SeverityBreakdown": {{"2": 5, "3": 30, "4": 10}},
    "DaysBetween": 80,
    "IsRecurring": "Yes"
  }},
  ...
]
```

## Next Steps After Query Execution

1. ✓ Save combined results to `data/mip_dlp_by_design_results.json`
2. Run: `python analyze_mip_dlp_themes.py`
3. Run: `python generate_doc_gap_analysis.py`
4. Review: Generated HTML report and documentation recommendations
""")
    
    print(f"\n📄 Detailed instructions saved to:")
    print(f"   {instruction_file}")
    print("\n" + "="*70)
    
    # Display queries for reference
    print("\n📊 Generated KQL Queries:")
    print("="*70)
    for team_short, query in all_queries.items():
        print(f"\n### {team_short} ###")
        print(query[:500] + "..." if len(query) > 500 else query)
        print()


if __name__ == "__main__":
    main()
