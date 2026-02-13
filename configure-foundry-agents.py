"""
Configure PHEPy Sub-Agents in Azure AI Foundry
Uploads agent definitions and configures routing
"""

import json
import os
from pathlib import Path

# Optional Azure SDK imports
try:
    from azure.identity import DefaultAzureCredential
    from azure.ai.ml import MLClient
    AZURE_SDK_AVAILABLE = True
except ImportError:
    AZURE_SDK_AVAILABLE = False

# Foundry project configuration
SUBSCRIPTION_ID = "82b24542-e1a0-441c-845a-f5677d342450"  # Visual Studio Enterprise
RESOURCE_GROUP = "rg-PHEPy"
WORKSPACE_NAME = "phepy"
PROJECT_ENDPOINT = "https://phepy-resource.services.ai.azure.com"

def get_ml_client():
    """Connect to Azure AI Foundry workspace"""
    if not AZURE_SDK_AVAILABLE:
        print("ℹ️  Azure ML SDK not installed (optional)")
        print("   Install with: pip install azure-ai-ml azure-identity")
        return None
    
    print("🔐 Authenticating...")
    
    try:
        credential = DefaultAzureCredential()
        ml_client = MLClient(
            credential=credential,
            subscription_id=SUBSCRIPTION_ID,
            resource_group_name=RESOURCE_GROUP,
            workspace_name=WORKSPACE_NAME
        )
        print(f"✅ Connected to workspace: {WORKSPACE_NAME}")
        return ml_client
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 Try: az login")
        return None

def load_agent_definitions():
    """Load agent routing map and sub-agent structure"""
    with open("agent_routing_map.json", 'r') as f:
        routing_map = json.load(f)
    
    agents = []
    routing_patterns = routing_map.get("routing_patterns", {})
    
    for category, config in routing_patterns.items():
        agent_info = {
            "id": category,
            "name": config.get("agent", category),
            "path": config.get("sub_agent_path", f"sub_agents/{category}/"),
            "mcp_tools": config.get("mcp_tools", []),
            "patterns": config.get("patterns", []),
            "quick_actions": config.get("quick_actions", {})
        }
        agents.append(agent_info)
    
    return agents

def create_agent_config_file():
    """Generate agent configuration for Foundry"""
    print("\n📋 Generating agent configuration...")
    
    agents = load_agent_definitions()
    
    config = {
        "orchestrator": {
            "name": "PHEPy Orchestrator",
            "version": "1.0.0",
            "description": "Microsoft Purview Health & Escalation Python-based orchestrator",
            "endpoint": PROJECT_ENDPOINT,
            "model_deployment": "phepy-chat"
        },
        "sub_agents": []
    }
    
    for agent in agents:
        agent_def = {
            "id": agent["id"],
            "name": agent["name"],
            "path": agent["path"],
            "tools": agent["mcp_tools"],
            "capabilities": {
                "patterns": agent["patterns"][:10],  # Sample patterns
                "quick_actions": list(agent["quick_actions"].keys())
            }
        }
        config["sub_agents"].append(agent_def)
    
    # Save configuration
    output_file = "foundry_agent_config.json"
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created: {output_file}")
    print(f"📊 Configured {len(agents)} sub-agents")
    return config

def generate_agent_system_prompt():
    """Generate comprehensive system prompt with agent routing"""
    print("\n📝 Generating system prompt with agent routing...")
    
    agents = load_agent_definitions()
    
    prompt = """# PHEPy Orchestrator - System Instructions

You are the PHEPy Orchestrator, a specialized support engineering assistant for Microsoft Purview products.

## Core Identity
You coordinate a team of specialized sub-agents to help Microsoft support engineers analyze product health, track escalations, and resolve customer issues.

## Available Sub-Agents

"""
    
    for agent in agents[:10]:  # Top 10 agents
        prompt += f"""### {agent['name']}
**Domain:** {agent['id'].replace('_', ' ').title()}
**Tools:** {', '.join(agent['mcp_tools'])}
**Capabilities:** {', '.join(agent['patterns'][:5])}

"""
    
    prompt += """## Routing Logic

When a user asks a question:
1. **Identify intent** from the query
2. **Route to appropriate sub-agent** based on patterns
3. **Execute using designated MCP tools**
4. **Return actionable insights** with relevant IDs/links

## Key Products
- Data Loss Prevention (DLP)
- Microsoft Information Protection (MIP)  
- eDiscovery
- Insider Risk Management (IRM)
- Communication Compliance
- Purview Auditing

## Response Guidelines
- Always include work item IDs (ICM, ADO, DFM cases)
- Use Kusto for aggregations and trends
- Format responses with clear bullet points
- Provide next steps and actionable recommendations
- Check severity: Sev 0/1 = critical, P0 bugs = customer-blocking

## Safety
Never expose customer PII. Redact confidential information. Follow Microsoft data handling policies.
"""
    
    # Save prompt
    output_file = "foundry_system_prompt.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"✅ Created: {output_file}")
    return prompt

def create_agent_data_index():
    """Generate list of files to upload as knowledge base"""
    print("\n📚 Identifying agent knowledge base files...")
    
    knowledge_files = []
    
    # Core documentation
    core_docs = [
        "GETTING_STARTED.md",
        "CAPABILITY_MATRIX.md",
        "ADVANCED_CAPABILITIES.md",
        "QUICK_REFERENCE.md",
        "agent_routing_map.json",
        "sub_agents/README.md"
    ]
    
    for doc in core_docs:
        if Path(doc).exists():
            knowledge_files.append(doc)
    
    # Sub-agent documentation
    sub_agent_path = Path("sub_agents")
    if sub_agent_path.exists():
        for agent_dir in sub_agent_path.iterdir():
            if agent_dir.is_dir():
                # Look for agent instructions and capabilities
                for doc_file in ["AGENT_INSTRUCTIONS.md", "CAPABILITIES.md", "QUERY_PATTERNS.md"]:
                    doc_path = agent_dir / doc_file
                    if doc_path.exists():
                        knowledge_files.append(str(doc_path))
    
    # Save file list
    output_file = "foundry_knowledge_files.txt"
    with open(output_file, 'w') as f:
        f.write('\n'.join(knowledge_files))
    
    print(f"✅ Created: {output_file}")
    print(f"📄 Found {len(knowledge_files)} knowledge files")
    return knowledge_files

def print_portal_instructions(config):
    """Print instructions for completing setup in portal"""
    print("\n" + "="*60)
    print("🎯 NEXT STEPS: Complete Setup in Azure AI Foundry Portal")
    print("="*60)
    
    print(f"""
1. **Open your project:**
   → https://ai.azure.com
   → Navigate to project: {WORKSPACE_NAME}

2. **Upload System Prompt:**
   → Go to "Playground" or "Agent builder"
   → Copy content from: foundry_system_prompt.txt
   → Paste into "System message" box

3. **Upload Knowledge Base:**
   → Go to "Data" or "Files" section
   → Upload files listed in: foundry_knowledge_files.txt
   → Key files:
     - agent_routing_map.json
     - CAPABILITY_MATRIX.md
     - ADVANCED_CAPABILITIES.md
     - sub_agents/*/AGENT_INSTRUCTIONS.md

4. **Configure MCP Servers (if supported):**
   → Settings → Integrations or Tools
   → Configure from mcp.json:
     • ICM MCP ENG: https://icm-mcp-prod.azure-api.net/v1/
     • ADO o365exchange (stdio)
     • Kusto MCP (stdio)
     • One Agentic Platform: https://oap.microsoft.com/api/v1/

5. **Test Your Orchestrator:**
   → Go to Playground
   → Try: "List all critical ICMs from last week"
   → Verify routing and agent responses

📋 Generated Files:
   • foundry_agent_config.json - Agent configuration
   • foundry_system_prompt.txt - System prompt (copy to portal)
   • foundry_knowledge_files.txt - Files to upload

🔧 Sub-agents configured: {len(config.get('sub_agents', []))}
""")

def main():
    """Main configuration workflow"""
    print("=" * 60)
    print("🚀 PHEPy Foundry Agent Configuration")
    print("=" * 60)
    
    # Check we're in the right directory
    if not Path("agent_routing_map.json").exists():
        print("❌ Error: Must run from PHEPy root directory")
        print("Expected file: agent_routing_map.json")
        return
    
    # Generate configuration files
    config = create_agent_config_file()
    generate_agent_system_prompt()
    create_agent_data_index()
    
    # Print portal instructions
    print_portal_instructions(config)
    
    print("\n✅ Configuration files generated!")
    print("📖 Follow the instructions above to complete setup in the portal")
    
    # Optional: Try to connect to workspace
    print("\n" + "="*60)
    print("🔍 Checking Azure connection...")
    print("="*60)
    
    ml_client = get_ml_client()
    if ml_client:
        try:
            workspace = ml_client.workspaces.get(WORKSPACE_NAME)
            print(f"✅ Workspace verified: {workspace.name}")
            print(f"   Location: {workspace.location}")
            print(f"   Resource Group: {RESOURCE_GROUP}")
        except Exception as e:
            print(f"⚠️  Could not fetch workspace details: {e}")

if __name__ == "__main__":
    main()
