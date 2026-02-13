"""
Query ICM for Sensitivity Labels / Information Protection incidents
Uses ICM context search to find incidents matching criteria
"""

# Based on screenshot filters:
# - Owning Service: Microsoft Security/Purview
# - Owning Team: Classification, Purview Message Encryption, Sensitivity Labels, 
#                Server Side Auto Labeling, Trainable Classifiers
# - Resolve Time: Last 90 days
# - How Fixed: NOT "By Design" and NOT "Fixed with Hotfix"

# Known Purview team information:
PURVIEW_TEAMS = {
    'Classification': {'team_id': 126934, 'service_id': 36626},
    'Sensitivity_Labels': {'team_id': None, 'service_id': 36626},  # Part of IP service
    'Message_Encryption': {'team_id': None, 'service_id': 36626},
    'MIP_Solutions': {'team_id': 45424, 'service_id': 22035},  # EOP service
    'Server_Side_Auto_Labeling': {'team_id': None, 'service_id': 36626},
    'Trainable_Classifiers': {'team_id': None, 'service_id': 36626}
}

# ICM IDs we know about from manual search
KNOWN_SENSITIVITY_LABEL_ICMS = [
    730591118,  # EDM classification performance - Classification team
    710987654,  # MIP watermarks - MIP Solutions team
]

# Need to query systematically for more ICMs
# Since Kusto unavailable, use ICM context search with keywords

SEARCH_KEYWORDS = [
    # Sensitivity Labels specific
    'sensitivity label',
    'label not showing',
    'label encryption',
    'auto labeling',
    'trainable classifier',
    
    # Classification / EDM
    'classification timeout',
    'EDM',
    'custom SIT',
    'sensitive information type',
    'FIPS classification',
    
    # Message Encryption
    'message encryption',
    'OME',
    'purview message encryption',
    
    # Performance issues
    'watermark',
    'classification performance',
    'regex pattern',
]

# Additional ICM IDs to retrieve based on team routing patterns
# These are estimated based on typical ICM numbering patterns
ESTIMATED_ICM_RANGE = range(700000000, 731000000)  # Last ~4 months

print("ICM Search Plan for Sensitivity Labels Analysis")
print("=" * 80)
print("\nTarget Teams:")
for team_name, info in PURVIEW_TEAMS.items():
    print(f"  - {team_name}: Team {info['team_id']}, Service {info['service_id']}")

print(f"\nSearch Keywords: {len(SEARCH_KEYWORDS)} terms")
print(f"Known ICMs: {len(KNOWN_SENSITIVITY_LABEL_ICMS)}")
print("\nRecommended Approach:")
print("1. Use mcp_icm_mcp_eng_get_incident_context for known ICMs")
print("2. Extract 'similar incidents' or related ICM references")
print("3. Use ICM numbers from support case 'RelatedICM_Id' fields")
print("4. Iterate through team-routed incidents systematically")
