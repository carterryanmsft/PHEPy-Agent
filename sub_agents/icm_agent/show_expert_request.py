"""
Demo: Show the Expert Request that gets sent to Purview Product Expert
"""

from icm_agent import ICMAgent
import json

# Load agent and data
agent = ICMAgent('icm_config.json')
agent.load_from_file('data/dlp_by_design_results.json')

# Run analysis
print("Running analysis...")
analysis = agent.analyze_by_design_patterns()

# Extract expert request
expert_request = analysis['expert_analysis']['expert_response']['expert_request']

print("\n" + "="*70)
print("EXPERT REQUEST - READY TO SEND TO PURVIEW PRODUCT EXPERT")
print("="*70 + "\n")

print(expert_request)

print("\n" + "="*70)
print("To invoke the expert, copy the above request and use:")
print("  runSubagent(agent='purview_product_expert', prompt=<request>)")
print("="*70)
