"""
Bulk ICM Retrieval and TSG Gap Analysis
Retrieves full details for 620 Sensitivity Labels ICMs from last 90 days
Author: PHEPy Agent
Date: 2026-02-04
"""

import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime
from collections import defaultdict

# ICM MCP HTTP endpoint
ICM_API_URL = "https://icm-mcp-prod.azure-api.net/v1/"

# TSG Gap Detection Keywords (from previous analyzer)
TSG_GAP_INDICATORS = {
    "performance": [
        "timeout", "slow", "delay", "latency", "performance", "waiting",
        "takes too long", "not responding", "freezing", "hanging"
    ],
    "missing_documentation": [
        "no documentation", "not documented", "unclear", "need guidance",
        "no tsg", "no troubleshooting", "how to", "need steps"
    ],
    "configuration": [
        "misconfigured", "configuration error", "setup issue", "not configured",
        "settings", "parameters", "incorrect config"
    ],
    "diagnostics": [
        "no logs", "cannot debug", "need diagnostics", "troubleshooting",
        "diagnostic", "investigation", "root cause", "unable to identify"
    ],
    "functionality": [
        "not working", "broken", "failing", "error", "issue", "problem",
        "unexpected behavior", "regression", "bug"
    ]
}

# Purview Product Areas
PURVIEW_PRODUCTS = [
    "Sensitivity Labels", "Classification", "Auto-labeling", "Encryption",
    "Trainable Classifiers", "EDM", "Information Protection", "DLP",
    "Message Encryption", "AIP", "Scanner", "Revocation", "Tracking"
]


class ICMBulkRetriever:
    """Bulk retrieve and analyze ICM incidents"""
    
    def __init__(self, icm_ids: List[int]):
        self.icm_ids = icm_ids
        self.retrieved_icms = []
        self.failed_icms = []
        self.tsg_gaps = defaultdict(list)
        
    def retrieve_icm_details(self, icm_id: int) -> Dict:
        """Retrieve full details for a single ICM"""
        # Note: This would call the ICM MCP endpoint
        # For now, we'll return a placeholder structure
        # In production, this would make the actual API call
        return {
            "id": icm_id,
            "retrieved": False,
            "error": "Placeholder - needs actual MCP call"
        }
    
    def analyze_for_tsg_gaps(self, icm: Dict) -> List[str]:
        """Analyze ICM for TSG gap indicators"""
        gaps_found = []
        
        title = icm.get("title", "").lower()
        summary = icm.get("summary", "").lower()
        combined_text = f"{title} {summary}"
        
        # Check each gap category
        for category, keywords in TSG_GAP_INDICATORS.items():
            for keyword in keywords:
                if keyword in combined_text:
                    gaps_found.append(category)
                    break  # Only count category once
        
        return gaps_found
    
    def process_batch(self, batch_size: int = 50):
        """Process ICMs in batches"""
        total = len(self.icm_ids)
        
        for i in range(0, total, batch_size):
            batch = self.icm_ids[i:i+batch_size]
            print(f"Processing batch {i//batch_size + 1} ({i+1}-{min(i+batch_size, total)} of {total})")
            
            for icm_id in batch:
                try:
                    details = self.retrieve_icm_details(icm_id)
                    if details.get("retrieved"):
                        self.retrieved_icms.append(details)
                        
                        # Analyze for TSG gaps
                        gaps = self.analyze_for_tsg_gaps(details)
                        if gaps:
                            self.tsg_gaps[icm_id] = gaps
                    else:
                        self.failed_icms.append(icm_id)
                except Exception as e:
                    print(f"  Error retrieving ICM {icm_id}: {e}")
                    self.failed_icms.append(icm_id)
                
                # Rate limiting - pause between requests
                time.sleep(0.1)
            
            print(f"  Batch complete. Retrieved: {len(self.retrieved_icms)}, Failed: {len(self.failed_icms)}")
    
    def generate_gap_report(self) -> str:
        """Generate TSG gap analysis report"""
        report = []
        report.append("# Purview Sensitivity Labels - TSG Gap Analysis Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\nTotal ICMs Analyzed: {len(self.retrieved_icms)}")
        report.append(f"Failed Retrievals: {len(self.failed_icms)}")
        report.append(f"\n## TSG Gap Summary\n")
        
        # Count gaps by category
        gap_counts = defaultdict(int)
        for icm_id, gaps in self.tsg_gaps.items():
            for gap in gaps:
                gap_counts[gap] += 1
        
        report.append("| Gap Category | ICM Count | % of Total |")
        report.append("|--------------|-----------|------------|")
        for category, count in sorted(gap_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(self.retrieved_icms) * 100) if self.retrieved_icms else 0
            report.append(f"| {category.title()} | {count} | {pct:.1f}% |")
        
        report.append(f"\n## Detailed ICM Breakdown\n")
        
        # Group ICMs by team
        icms_by_team = defaultdict(list)
        for icm in self.retrieved_icms:
            team = icm.get("owningTeamName", "Unknown")
            icms_by_team[team].append(icm)
        
        for team, icms in sorted(icms_by_team.items()):
            report.append(f"\n### {team} ({len(icms)} ICMs)\n")
            for icm in icms[:10]:  # Top 10 per team
                gaps = self.tsg_gaps.get(icm["id"], [])
                gap_str = ", ".join(gaps) if gaps else "None detected"
                report.append(f"- **{icm['id']}**: {icm.get('title', 'N/A')}")
                report.append(f"  - Gaps: {gap_str}")
                report.append(f"  - Severity: {icm.get('severity', 'N/A')}")
                report.append("")
        
        return "\n".join(report)
    
    def save_results(self, output_dir: Path):
        """Save results to files"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save raw ICM data
        with open(output_dir / "retrieved_icms.json", "w") as f:
            json.dump(self.retrieved_icms, f, indent=2)
        
        # Save gap analysis
        with open(output_dir / "tsg_gaps.json", "w") as f:
            json.dump(dict(self.tsg_gaps), f, indent=2)
        
        # Save gap report
        report = self.generate_gap_report()
        with open(output_dir / "tsg_gap_analysis_report.md", "w") as f:
            f.write(report)
        
        print(f"\nResults saved to {output_dir}")


def main():
    """Main execution"""
    print("="*80)
    print("Purview Sensitivity Labels - ICM Bulk Retrieval & TSG Gap Analysis")
    print("="*80)
    
    # This will be populated from Kusto query results
    # For now, using placeholder - will be updated with actual ICM IDs
    icm_ids = [
        21000000887894, 21000000887192, 21000000887231, 51000000886131,
        21000000886974, 51000000885589, 21000000884499, 21000000884661,
        51000000883429, 51000000883110
        # ... remaining 610 ICMs from Kusto query
    ]
    
    print(f"\nTotal ICMs to retrieve: {len(icm_ids)}")
    print(f"Starting bulk retrieval...\n")
    
    # Initialize retriever
    retriever = ICMBulkRetriever(icm_ids)
    
    # Process in batches
    retriever.process_batch(batch_size=50)
    
    # Generate and save report
    output_dir = Path(__file__).parent.parent / "reports"
    retriever.save_results(output_dir)
    
    print("\n" + "="*80)
    print("Retrieval Complete!")
    print("="*80)
    print(f"Successfully retrieved: {len(retriever.retrieved_icms)} ICMs")
    print(f"Failed retrievals: {len(retriever.failed_icms)}")
    print(f"TSG gaps identified in: {len(retriever.tsg_gaps)} ICMs")
    
    # Print gap summary
    gap_counts = defaultdict(int)
    for gaps in retriever.tsg_gaps.values():
        for gap in gaps:
            gap_counts[gap] += 1
    
    print("\nTop TSG Gap Categories:")
    for category, count in sorted(gap_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {category.title()}: {count} ICMs")


if __name__ == "__main__":
    main()
