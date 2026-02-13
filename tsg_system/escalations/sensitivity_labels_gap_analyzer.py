"""
Sensitivity Labels ICM Gap Analyzer
Retrieves and analyzes Sensitivity Labels / Information Protection ICMs from last 90 days
Focuses on issues NOT resolved as By Design or Linked to Work Item
"""

import json
from datetime import datetime, timedelta

# Sample ICMs retrieved so far
sensitivity_labels_icms = [
    {
        'Id': '730591118',
        'Title': '[MCSfMSC] | Some emails not hitting EDM',
        'Created': '2026-01-06',
        'Status': 'ACTIVE',
        'Severity': 3,
        'DaysOpen': 29,
        'Product': 'Classification / EDM',
        'Team': 'Classification',
        'HowFixed': 'Not yet resolved',
        'Customer': 'Barclays',
        'Issue': 'EDM SIT performance - classification timeouts with unlimited proximity patterns',
        'RootCause': 'Unlimited proximity (90 patterns), loose regex causing FIPS scan timeouts',
        'Resolution': 'TSG guidance - remove problematic SIT, optimize configs',
        'TSG_Link': 'https://o365exchange.visualstudio.com/IP%20Engineering/_wiki/wikis/IP%20Engineering.wiki/46387/MIP-Classification-for-SRE-or-OCE',
        'TSG_Effectiveness': 'Partial - covered general classification but not specific performance optimization',
        'Gap_Indicators': ['Performance degradation', 'Custom SIT optimization', 'Unlimited proximity impact', 'FIPS timeout diagnostics']
    },
    {
        'Id': '710987654',
        'Title': 'Watermarks for database JPNPR01DG563-db379 below threshold',
        'Created': '2025-11-14',
        'Status': 'ACTIVE',
        'Severity': 4,
        'DaysOpen': 82,
        'Product': 'MIP Solutions / Mailbox Assistants',
        'Team': 'Microsoft Information Protection (MIP) Solutions',
        'HowFixed': 'Not yet resolved',
        'Customer': 'Internal monitoring',
        'Issue': 'Mailbox Assistant watermarks behind threshold for 4+ hours',
        'RootCause': 'EventAssistantsWatermarksProbe failure - watermarks behind on db379',
        'Resolution': 'Not yet mitigated',
        'TSG_Link': 'None specified',
        'TSG_Effectiveness': 'Unknown - no TSG referenced',
        'Gap_Indicators': ['Watermark monitoring', 'EventAssistants performance', 'Database-level diagnostics']
    }
]

# TSG Gap patterns identified
gap_patterns = {
    'Performance_Optimization': {
        'count': 1,
        'icms': ['730591118'],
        'description': 'Custom SIT and classification performance optimization guidance',
        'recommended_tsg': 'Performance Best Practices for Custom SITs and EDM Patterns',
        'priority': 'HIGH'
    },
    'Watermark_Diagnostics': {
        'count': 1,
        'icms': ['710987654'],
        'description': 'Mailbox Assistant watermark monitoring and troubleshooting',
        'recommended_tsg': 'EventAssistants Watermark Troubleshooting Guide',
        'priority': 'MEDIUM'
    },
    'FIPS_Timeout': {
        'count': 1,
        'icms': ['730591118'],
        'description': 'FIPS classification scan timeout root cause analysis',
        'recommended_tsg': 'FIPS Classification Timeout Diagnostics',
        'priority': 'HIGH'
    },
    'Regex_Pattern_Optimization': {
        'count': 1,
        'icms': ['730591118'],
        'description': 'Regex pattern design for SITs to avoid performance issues',
        'recommended_tsg': 'Regex Pattern Optimization for Custom SITs',
        'priority': 'HIGH'
    }
}

# Existing TSG coverage from wiki baseline
existing_coverage = {
    'Total_Pages': 93,
    'TSG_Pages': 48,
    'Coverage_Percent': 52,
    'Categories': {
        'Sensitivity_Labels': {
            'pages': 27,
            'scenarios': ['Label not showing', 'Not working correctly', 'Content marking', 
                         'Encryption access', 'Configuration', 'Unexpectedly applied', 
                         'Missing in Purview', 'Stuck PendingDeletion', 'Unable to Delete']
        },
        'Message_Encryption': {
            'pages': 26,
            'scenarios': 8
        },
        'Auto_Labeling': {
            'pages': 21,
            'client_side': 10,
            'server_side': 11
        },
        'Activity_Explorer': {
            'pages': 13,
            'scenarios': 4
        },
        'Data_Explorer': {
            'pages': 11,
            'scenarios': 4
        }
    },
    'Known_Gaps': [
        'Container labels (Teams/Groups/Sites) troubleshooting',
        'Co-authoring label conflicts',
        'DKE (Double Key Encryption) troubleshooting',
        'Performance optimization for custom SITs',
        'Watermark monitoring and diagnostics',
        'FIPS classification timeout diagnostics'
    ]
}

def analyze_gaps():
    """Analyze TSG gaps from ICM incidents"""
    print("=" * 80)
    print("SENSITIVITY LABELS ICM GAP ANALYSIS")
    print("=" * 80)
    print(f"\nDate Range: Last 90 days (Nov 6, 2025 - Feb 4, 2026)")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}\n")
    
    print("### ICM INCIDENTS ANALYZED ###\n")
    for icm in sensitivity_labels_icms:
        print(f"ICM {icm['Id']}: {icm['Title']}")
        print(f"  Status: {icm['Status']} ({icm['DaysOpen']} days open)")
        print(f"  Severity: {icm['Severity']}")
        print(f"  Product: {icm['Product']}")
        print(f"  HowFixed: {icm['HowFixed']}")
        print(f"  TSG Effectiveness: {icm['TSG_Effectiveness']}")
        print(f"  Gap Indicators: {', '.join(icm['Gap_Indicators'])}")
        print()
    
    print("\n### TSG GAP PATTERNS IDENTIFIED ###\n")
    for gap_name, gap_data in gap_patterns.items():
        print(f"🔴 {gap_name.replace('_', ' ')} (Priority: {gap_data['priority']})")
        print(f"   Description: {gap_data['description']}")
        print(f"   Affected ICMs: {', '.join(gap_data['icms'])}")
        print(f"   Recommended TSG: \"{gap_data['recommended_tsg']}\"")
        print()
    
    print("\n### EXISTING TSG COVERAGE BASELINE ###\n")
    print(f"Total Information Protection Pages: {existing_coverage['Total_Pages']}")
    print(f"TSG Pages: {existing_coverage['TSG_Pages']}")
    print(f"Coverage: {existing_coverage['Coverage_Percent']}%")
    print(f"\nKnown Gaps:")
    for gap in existing_coverage['Known_Gaps']:
        print(f"  - {gap}")
    
    print("\n### SUMMARY ###\n")
    total_icms = len(sensitivity_labels_icms)
    active_icms = len([i for i in sensitivity_labels_icms if i['Status'] == 'ACTIVE'])
    high_priority_gaps = len([g for g in gap_patterns.values() if g['priority'] == 'HIGH'])
    
    print(f"Total ICMs Analyzed: {total_icms}")
    print(f"Active (Unresolved): {active_icms}")
    print(f"High Priority TSG Gaps: {high_priority_gaps}")
    print(f"Total Gap Patterns: {len(gap_patterns)}")
    
    print("\n### TOP 3 TSG RECOMMENDATIONS ###\n")
    print("1. 🔴 HIGH: Performance Best Practices for Custom SITs and EDM Patterns")
    print("   - Unlimited proximity impact analysis")
    print("   - Regex pattern optimization guide")
    print("   - Classification timeout troubleshooting")
    print()
    print("2. 🔴 HIGH: FIPS Classification Timeout Diagnostics")
    print("   - Root cause analysis workflow")
    print("   - DPA log interpretation")
    print("   - Mitigation strategies")
    print()
    print("3. 🟡 MEDIUM: EventAssistants Watermark Troubleshooting Guide")
    print("   - Watermark monitoring best practices")
    print("   - Database-level diagnostics")
    print("   - Recovery procedures")

if __name__ == '__main__':
    analyze_gaps()
