"""
Agent Session Bootstrap Script

Quick commands to initialize and seed the agent memory system for new users.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from db import init_db
from preferences import add_preference, add_insight


def bootstrap_phepy_agent():
    """Initialize and seed agent memory with PHEPy context"""
    
    print("🚀 Bootstrapping PHEPy Agent Memory...")
    
    # Initialize database
    print("\n1️⃣ Initializing database...")
    init_db()
    print("   ✅ Database created at memory.db")
    
    # Add default preferences
    print("\n2️⃣ Adding default preferences...")
    
    # Work preferences
    add_preference("work", "workspace", "PHEPy - Purview Product Health & Escalation")
    add_preference("work", "workspace_path", r"C:\Users\carterryan\OneDrive - Microsoft\PHEPy")
    add_preference("work", "role", "PM/Engineer for Purview Escalations")
    
    # Tech preferences
    add_preference("tech", "primary_language", "Python")
    add_preference("tech", "query_engine", "Kusto (KQL)")
    add_preference("tech", "shell", "PowerShell")
    add_preference("tech", "ide", "VS Code")
    
    # Workflow preferences
    add_preference("workflow", "communication_style", "direct and data-driven")
    add_preference("workflow", "report_format", "HTML with embedded metrics and visualizations")
    add_preference("workflow", "tone", "professional but efficient")
    
    # Domain preferences
    add_preference("domain", "primary_focus", "ICM incident management and analysis")
    add_preference("domain", "key_databases", "IcMDataWarehouse, CXEDataPlatform")
    add_preference("domain", "main_team", "PURVIEW\\SensitivityLabels")
    
    print("   ✅ Default preferences added")
    
    # Add default insights
    print("\n3️⃣ Adding default insights...")
    
    # Context insights
    add_insight(
        "context",
        "PHEPy workspace has 8 sub-agents for specialized tasks: ICM Agent, LQ Escalation Agent, Support Case Manager, Tenant Health Monitor, Work Item Manager, Program Onboarding Manager, Contacts & Escalation Finder, Kusto Expert",
        ["workspace", "architecture"]
    )
    
    add_insight(
        "context",
        "5 MCP servers configured: o365exchange (ADO), ASIM-Security (ADO), ICM MCP ENG, enterprise-mcp (DFM), kusto-mcp",
        ["mcp", "configuration"]
    )
    
    add_insight(
        "context",
        "Common workflow: Generate Kusto query → Execute via MCP → Cache results → Process locally → Generate HTML report",
        ["workflow", "pattern"]
    )
    
    add_insight(
        "context",
        "IcMDataWarehouse for ICM data, CXEDataPlatform for customer experience metrics",
        ["databases", "kusto"]
    )
    
    # Pattern insights
    add_insight(
        "pattern",
        "Cache expensive Kusto query results in data/ folders to avoid re-execution",
        ["performance", "caching"]
    )
    
    add_insight(
        "pattern",
        "Link ICMs to ADO bugs using artifact links for traceability",
        ["icm", "ado", "tracking"]
    )
    
    print("   ✅ Default insights added")
    
    # Summary
    print("\n✅ Bootstrap complete!")
    print("\n📊 Status:")
    print("   Database: memory.db")
    print("   Preferences: 14 defaults added")
    print("   Insights: 6 defaults added")
    
    print("\n💡 Next steps:")
    print("   1. Run: python cli.py status")
    print("   2. Add your personal preferences:")
    print("      python cli.py pref add -c work -k name -v \"<your name>\"")
    print("   3. Add your goals:")
    print("      python cli.py insight add -t goal --content \"<your goal>\"")
    print("   4. Update custom instructions:")
    print("      Edit: C:\\Users\\carterryan\\.copilot\\copilot-instructions.md")


if __name__ == "__main__":
    bootstrap_phepy_agent()
