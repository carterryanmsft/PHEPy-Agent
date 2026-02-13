"""
PHEPy Intelligent Agent Router
Fast, direct routing based on intent patterns instead of regex keyword matching
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re

class AgentRouter:
    """Efficient intent-based routing to PHEPy sub-agents"""
    
    def __init__(self, routing_map_path: str = "agent_routing_map.json"):
        self.routing_map_path = Path(routing_map_path)
        self.routing_config = self._load_routing_map()
        self.patterns = self.routing_config.get("routing_patterns", {})
        self.workflows = self.routing_config.get("workflow_shortcuts", {})
        self.direct_map = self.routing_config.get("common_asks_direct_map", {})
        
    def _load_routing_map(self) -> Dict:
        """Load the routing configuration"""
        with open(self.routing_map_path, 'r') as f:
            return json.load(f)
    
    def route(self, user_query: str) -> Dict:
        """
        Route a user query to the appropriate agent/workflow
        
        Returns:
            {
                "routing_type": "workflow|agent|direct",
                "agent": "agent_name",
                "path": "sub_agents/...",
                "action": "script.py or workflow steps",
                "mcp_tools": ["tool1", "tool2"],
                "confidence": 0.0-1.0
            }
        """
        query_lower = user_query.lower().strip()
        
        # Priority 1: Check workflow shortcuts (multi-step operations)
        workflow_match = self._match_workflow(query_lower)
        if workflow_match:
            return workflow_match
        
        # Priority 2: Check direct script mappings (specific reports/operations)
        direct_match = self._match_direct_script(query_lower)
        if direct_match:
            return direct_match
        
        # Priority 3: Match to agent patterns
        agent_match = self._match_agent_pattern(query_lower)
        if agent_match:
            return agent_match
        
        # Fallback: Return orchestrator recommendation
        return self._fallback_routing(query_lower)
    
    def _match_workflow(self, query: str) -> Optional[Dict]:
        """Check if query matches a predefined workflow"""
        for workflow_name, workflow_config in self.workflows.items():
            # Check if any trigger matches
            for trigger in workflow_config.get("triggers", []):
                if trigger in query:
                    return {
                        "routing_type": "workflow",
                        "workflow": workflow_name,
                        "description": workflow_config.get("description"),
                        "steps": workflow_config.get("steps"),
                        "confidence": 0.95
                    }
        return None
    
    def _match_direct_script(self, query: str) -> Optional[Dict]:
        """Check if query matches a direct script mapping"""
        # Check each category in direct_map
        for category, scripts in self.direct_map.items():
            for script_key, script_path in scripts.items():
                # Convert script_key to readable pattern (e.g. "ic_production_report" -> "ic production report")
                pattern = script_key.replace("_", " ")
                if pattern in query:
                    # Determine agent from script path
                    if "/" in script_path:
                        agent = script_path.split("/")[0]
                        agent_config = self._get_agent_config(agent)
                        return {
                            "routing_type": "direct",
                            "category": category,
                            "script": script_path,
                            "agent": agent,
                            "mcp_tools": agent_config.get("mcp_tools", []) if agent_config else [],
                            "confidence": 0.90
                        }
        return None
    
    def _match_agent_pattern(self, query: str) -> Optional[Dict]:
        """Match query to agent based on pattern matching"""
        best_match = None
        best_score = 0
        
        for domain, config in self.patterns.items():
            patterns = config.get("patterns", [])
            
            # Count how many patterns match
            matches = sum(1 for pattern in patterns if pattern in query)
            
            if matches > best_score:
                best_score = matches
                best_match = {
                    "routing_type": "agent",
                    "domain": domain,
                    "agent": config.get("agent"),
                    "path": config.get("sub_agent_path"),
                    "mcp_tools": config.get("mcp_tools", []),
                    "quick_actions": config.get("quick_actions", {}),
                    "confidence": min(0.85, 0.50 + (matches * 0.15))  # Scale confidence
                }
        
        return best_match if best_score > 0 else None
    
    def _get_agent_config(self, agent_keyword: str) -> Optional[Dict]:
        """Get agent configuration by matching keyword to domain"""
        for domain, config in self.patterns.items():
            if agent_keyword in config.get("sub_agent_path", ""):
                return config
        return None
    
    def _fallback_routing(self, query: str) -> Dict:
        """Fallback when no clear match is found"""
        return {
            "routing_type": "orchestrator",
            "agent": "orchestrator",
            "recommendation": "Use multi-agent orchestration",
            "suggestion": "Query may require multiple agents or clarification",
            "confidence": 0.30
        }
    
    def get_agent_capabilities(self, agent_name: str) -> Dict:
        """Get capabilities for a specific agent"""
        for domain, config in self.patterns.items():
            if config.get("agent") == agent_name:
                return {
                    "domain": domain,
                    "patterns": config.get("patterns"),
                    "mcp_tools": config.get("mcp_tools"),
                    "quick_actions": config.get("quick_actions")
                }
        return {}
    
    def suggest_query_improvements(self, query: str) -> List[str]:
        """Suggest more specific queries based on user input"""
        query_lower = query.lower()
        suggestions = []
        
        # Find partial matches
        for domain, config in self.patterns.items():
            patterns = config.get("patterns", [])
            matching_patterns = [p for p in patterns if any(word in p for word in query_lower.split())]
            
            if matching_patterns:
                agent = config.get("agent")
                suggestions.extend([
                    f"Be more specific: Try '{pattern}' (routes to {agent})"
                    for pattern in matching_patterns[:3]  # Top 3 suggestions
                ])
        
        return suggestions[:5]  # Return top 5 overall


# Example usage and testing
if __name__ == "__main__":
    router = AgentRouter()
    
    # Test queries
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
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        result = router.route(query)
        print(f"   ✅ Route: {result.get('routing_type').upper()}")
        print(f"   🎯 Agent: {result.get('agent', 'N/A')}")
        print(f"   📊 Confidence: {result.get('confidence', 0):.0%}")
        
        if result.get('workflow'):
            print(f"   🔄 Workflow: {result['workflow']}")
            print(f"   📋 Steps: {len(result.get('steps', []))} actions")
        elif result.get('script'):
            print(f"   ⚡ Direct Script: {result['script']}")
        elif result.get('domain'):
            print(f"   🏷️  Domain: {result['domain']}")
            quick_actions = result.get('quick_actions', {})
            if quick_actions:
                print(f"   🚀 Quick Actions: {', '.join(quick_actions.keys())}")
        
        mcp_tools = result.get('mcp_tools', [])
        if mcp_tools:
            print(f"   🔧 MCP Tools: {', '.join(mcp_tools)}")
    
    print("\n" + "=" * 80)
    print("✅ Routing test complete!")
    print("=" * 80)
