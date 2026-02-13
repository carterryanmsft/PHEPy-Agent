"""
PHEPy Agent Router - Windows-Compatible Test Script
"""

from agent_router import AgentRouter

def test_routing():
    """Test routing with common queries"""
    router = AgentRouter()
    
    test_queries = [
        # Original tests
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
        "Friday operations routine",
        
        # New enhanced tests - Regional
        "Generate APAC LQE report",
        "Run EMEA regional report",
        "Americas LQE analysis",
        
        # Time-based queries
        "Show me ICMs from last 7 days",
        "Sev2 incidents this week",
        "High priority bugs assigned to me",
        
        # Combined operations
        "Generate IC report and send email",
        "Refresh data then run report",
        
        # TSG operations
        "Analyze TSG gaps",
        "Find missing TSGs",
        
        # Team-specific
        "Team performance for my team",
        "DLP team ICMs this month",
        
        # Customer operations
        "Customer deep dive for Fabrikam",
        "Tenant health check for CIBC"
    ]
    
    print("=" * 80)
    print("PHEPy Agent Router - Enhanced Test Results")
    print("=" * 80)
    print()
    
    success_count = 0
    high_confidence_count = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. Query: {query}")
        result = router.route(query)
        confidence = result.get('confidence', 0)
        
        print(f"   Route Type: {result.get('routing_type').upper()}")
        print(f"   Agent: {result.get('agent', 'N/A')}")
        print(f"   Confidence: {confidence:.0%}", end="")
        
        if confidence >= 0.80:
            print(" [HIGH]")
            high_confidence_count += 1
        elif confidence >= 0.60:
            print(" [MEDIUM]")
        else:
            print(" [LOW]")
        
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
        
        if confidence >= 0.50:
            success_count += 1
        
        print()
    
    print("=" * 80)
    print(f"RESULTS: {success_count}/{len(test_queries)} queries routed successfully")
    print(f"High Confidence (80%+): {high_confidence_count}/{len(test_queries)}")
    print(f"Success Rate: {success_count/len(test_queries)*100:.1f}%")
    print("=" * 80)

if __name__ == "__main__":
    test_routing()
