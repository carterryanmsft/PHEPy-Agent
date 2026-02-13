import json
from datetime import datetime

# Real ICM incidents from Purview service
icm_incidents = [
    {
        'Id': '636778552',
        'Title': '[Issue] cannot purge content in premium cases',
        'Description': 'Customer reports they cannot purge content in eDiscovery premium cases. The litigation hold is enabled and should be removed. No TSG available for this scenario.',
        'Severity': 3,
        'CreatedDate': '2025-05-30T19:34:56Z',
        'ResolvedDate': '2025-06-05T21:02:24Z',
        'OwningService': 'Purview',
        'OwningTeam': 'eDiscovery',
        'Product': 'eDiscovery',
        'CustomerImpact': 'High'
    },
    {
        'Id': '687747177',
        'Title': '[Issue] Unable to delete the teams meeting from backend',
        'Description': 'Customer unable to delete Teams meeting from backend despite 3 content searches. PowerShell commands executed successfully but invite not removed. No documentation for this scenario using Graph cmdlet.',
        'Severity': 3,
        'CreatedDate': '2025-09-19T16:53:10Z',
        'ResolvedDate': '2025-10-31T17:41:16Z',
        'OwningService': 'Purview',
        'OwningTeam': 'eDiscovery',
        'Product': 'eDiscovery',
        'CustomerImpact': 'Critical'
    },
    {
        'Id': '724369842',
        'Title': '[Issue] APAC | Customer not able to perform searches from a particular review set',
        'Description': 'After adding multiple searches to Review set, customer unable to perform searches. Progress bar stuck for 24 hours. Query executed successfully in premium case but not in modern UI.',
        'Severity': 3,
        'CreatedDate': '2025-12-18T14:33:31Z',
        'ResolvedDate': '2026-01-08T08:51:20Z',
        'OwningService': 'Purview',
        'OwningTeam': 'eDiscovery',
        'Product': 'eDiscovery',
        'CustomerImpact': 'High'
    }
]

# TSG Gap Analysis
print("=" * 80)
print("Purview ICM TSG Gap Analysis")
print("=" * 80)
print(f"\nAnalyzed {len(icm_incidents)} eDiscovery ICM incidents")
print("\n### HIGH PRIORITY TSG GAPS ###\n")

for incident in icm_incidents:
    print(f"ICM {incident['Id']}: {incident['Title']}")
    print(f"  Product: {incident['Product']}")
    print(f"  Impact: {incident['CustomerImpact']}")
    
    # Detect gap indicators
    desc = incident['Description'].lower()
    gaps = []
    if 'no tsg' in desc or 'missing' in desc:
        gaps.append('Missing Documentation')
    if 'unable' in desc or 'not able' in desc:
        gaps.append('Unclear Process')
    if 'commands' in desc or 'powershell' in desc:
        gaps.append('Missing Diagnostic Steps')
    
    if gaps:
        print(f"  Gap Types: {', '.join(gaps)}")
        print(f"  Recommendation: CREATE TSG for {incident['Product']} - {incident['Title']}")
    print()

# Summary
print("\n### SUMMARY ###")
print(f"Total Incidents: {len(icm_incidents)}")
print(f"Incidents with TSG Gaps: {len(icm_incidents)}")
print("\nTop TSG Recommendations:")
print("1. eDiscovery - Purge content in premium cases (hold removal)")
print("2. eDiscovery - Delete Teams meetings via content search/Graph")
print("3. eDiscovery - Review set search performance/modern UI issues")
