"""
PHEPy Agent Router - Windows-Compatible Test Script
"""

from agent_router import AgentRouter

def test_routing():
    """Test routing with common queries"""
    router = AgentRouter()
    
    test_queries = [
        "Get ICM details for 21000000887894",
        "Generate IC production risk report",
        "Run by design analysis for last 6 months",
        "Create bug for sensitivity label issue",
        "Query Kusto for errors in the last 48 hours",
        "What are at-risk cases this week",
        "How does auto-labeling work in SharePoint",
        "Who is on call for DLP team",
        "New P0 ICM response workflow",
        "Weekly health review",
        "Friday operations routine"
    ]
    
    print("=" * 80)
    print("PHEPy Agent Router - Test Results")
    print("=" * 80)
    print()
    
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. Query: {query}")
        result = router.route(query)
        print(f"   Route Type: {result.get('routing_type').upper()}")
        print(f"   Agent: {result.get('agent', 'N/A')}")
        print(f"   Confidence: {result.get('confidence', 0):.0%}")
        
        if result.get('workflow'):
            print(f"   Workflow: {result['workflow']}")
            print(f"   Steps: {len(result.get('steps', []))} actions")
        elif result.get('script'):
            print(f"   Script: {result['script']}")
        elif result.get('domain'):
            print(f"   Domain: {result['domain']}")
            
        mcp_tools = result.get('mcp_tools', [])
        if mcp_tools:
            print(f"   MCP Tools: {', '.join(mcp_tools)}")
        print()
    
    print("=" * 80)
    print("Routing test complete! All queries processed successfully.")
    print("=" * 80)

if __name__ == "__main__":
    test_routing()
