"""
Finalize TSG Gap Analysis - Process available incident data and generate report
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tsg_gap_analyzer import TSGGapAnalyzer
from batch_icm_retriever import BatchICMRetriever

# Sample incidents we know about
SAMPLE_INCIDENTS = [
    {
        "id": 51000000879746,
        "title": "[Issue] Encryption label not working in OWA and New outlook",
        "severity": 3,
        "state": "ACTIVE",
        "createdDate": "2026-02-02T13:51:48.8244781Z",
        "customFields": [
            {"name": "Link to TSG", "value": "https://dev.azure.com/ASIM-Security/Compliance/_wiki/wikis/Information%20Protection/9036/How-to-Verify-and-set-the-Information-Rights-Management-(IRM)-Configuration-for-Purview-Message-Encryption"},
            {"name": "TSG Effectiveness", "value": "true"},
            {"name": "Escalation Quality", "value": "All Data Provided"}
        ],
        "tags": []
    },
    {
        "id": 51000000879655,
        "title": "Sensitivity label migration RFC",
        "severity": 3,
        "state": "ACTIVE",
        "createdDate": "2026-02-01T00:00:00Z",
        "customFields": [
            {"name": "TSG Effectiveness", "value": "false"}
        ],
        "tags": []
    },
    {
        "id": 51000000879362,
        "title": "DCR for file scanning limits",
        "severity": 3,
        "state": "ACTIVE",
        "createdDate": "2026-01-31T00:00:00Z",
        "customFields": [],
        "tags": []
    },
    {
        "id": 741203392,
        "title": "Office legacy file format labeling issues",
        "severity": 3,
        "state": "ACTIVE",
        "createdDate": "2026-01-30T00:00:00Z",
        "customFields": [],
        "tags": []
    },
    {
        "id": 51000000878019,
        "title": "General Password SIT detection issues",
        "severity": 3,
        "state": "RESOLVED",
        "createdDate": "2026-01-29T00:00:00Z",
        "customFields": [
            {"name": "Link to TSG", "value": "https://example.com/tsg"},
            {"name": "TSG Effectiveness", "value": "true"}
        ],
        "tags": []
    },
    {
        "id": 51000000877201,
        "title": "Missing CapexApproved Orders for Planning ID",
        "severity": 4,
        "state": "RESOLVED",
        "createdDate": "2026-01-30T02:22:55Z",
        "customFields": [],
        "tags": []
    }
]

def main():
    print("=" * 80)
    print("FINALIZING TSG GAP ANALYSIS")
    print("=" * 80)
    print()
    
    # Initialize analyzer
    analyzer = TSGGapAnalyzer()
    
    # Process sample incidents
    print(f"Processing {len(SAMPLE_INCIDENTS)} sample incidents...")
    for incident in SAMPLE_INCIDENTS:
        tsg_data = analyzer.extract_tsg_data(incident)
        analyzer.add_incident(tsg_data)
    
    print(f"✓ Processed {len(analyzer.incidents)} incidents")
    print()
    
    # Generate report
    print("Generating TSG gap analysis report...")
    report = analyzer.generate_report()
    
    # Save results
    output_dir = Path("../reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = output_dir / "tsg_gap_analysis_sample.json"
    report_file = output_dir / "tsg_gap_report_sample.md"
    
    # Save JSON results
    results = analyzer.analyze_gaps()
    results['metadata'] = {
        'analysis_date': '2026-02-04',
        'incident_count': len(SAMPLE_INCIDENTS),
        'note': 'Sample analysis based on 6 incidents for demonstration'
    }
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✓ Results saved to {results_file}")
    
    # Save markdown report
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✓ Report saved to {report_file}")
    print()
    
    # Display report
    print(report)
    
    return results

if __name__ == "__main__":
    main()
