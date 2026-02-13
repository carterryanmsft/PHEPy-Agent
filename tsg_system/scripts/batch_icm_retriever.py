"""
Batch ICM Retriever - Efficiently retrieve ICM incidents for TSG analysis
Handles rate limiting, error recovery, and progress tracking
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class BatchICMRetriever:
    """Retrieve ICM incidents in batches with progress tracking"""
    
    def __init__(self, output_dir: str = "tsg_system/data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.progress_file = self.output_dir / "retrieval_progress.json"
        self.data_file = self.output_dir / "retrieved_incidents.jsonl"
        
        self.progress = self._load_progress()
    
    def _load_progress(self) -> Dict:
        """Load retrieval progress from file"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'total_incidents': 0,
            'retrieved': 0,
            'failed': [],
            'last_updated': None,
            'incident_ids': []
        }
    
    def _save_progress(self):
        """Save retrieval progress"""
        self.progress['last_updated'] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def set_incident_ids(self, incident_ids: List[int]):
        """Set the list of incident IDs to retrieve"""
        self.progress['incident_ids'] = incident_ids
        self.progress['total_incidents'] = len(incident_ids)
        self._save_progress()
        print(f"Set {len(incident_ids)} incident IDs for retrieval")
    
    def save_incident(self, incident_data: Dict):
        """Append incident data to JSONL file"""
        with open(self.data_file, 'a') as f:
            f.write(json.dumps(incident_data) + '\n')
        
        self.progress['retrieved'] += 1
        self._save_progress()
    
    def mark_failed(self, incident_id: int, error: str):
        """Mark an incident as failed to retrieve"""
        self.progress['failed'].append({
            'incident_id': incident_id,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
        self._save_progress()
    
    def get_next_batch(self, batch_size: int = 10) -> List[int]:
        """Get next batch of incident IDs to retrieve"""
        retrieved_ids = self._get_retrieved_ids()
        failed_ids = {f['incident_id'] for f in self.progress['failed']}
        
        remaining = [
            iid for iid in self.progress['incident_ids']
            if iid not in retrieved_ids and iid not in failed_ids
        ]
        
        return remaining[:batch_size]
    
    def _get_retrieved_ids(self) -> set:
        """Get set of already retrieved incident IDs"""
        if not self.data_file.exists():
            return set()
        
        retrieved = set()
        with open(self.data_file, 'r') as f:
            for line in f:
                if line.strip():
                    incident = json.loads(line)
                    retrieved.add(incident.get('id'))
        
        return retrieved
    
    def get_status(self) -> Dict:
        """Get current retrieval status"""
        retrieved_ids = self._get_retrieved_ids()
        
        return {
            'total': self.progress['total_incidents'],
            'retrieved': len(retrieved_ids),
            'failed': len(self.progress['failed']),
            'remaining': self.progress['total_incidents'] - len(retrieved_ids) - len(self.progress['failed']),
            'progress_pct': (len(retrieved_ids) / self.progress['total_incidents'] * 100) 
                           if self.progress['total_incidents'] > 0 else 0
        }
    
    def print_status(self):
        """Print current status"""
        status = self.get_status()
        print("\n" + "=" * 60)
        print("ICM RETRIEVAL STATUS")
        print("=" * 60)
        print(f"Total Incidents: {status['total']}")
        print(f"Retrieved: {status['retrieved']} ({status['progress_pct']:.1f}%)")
        print(f"Failed: {status['failed']}")
        print(f"Remaining: {status['remaining']}")
        print("=" * 60 + "\n")
    
    def load_all_incidents(self) -> List[Dict]:
        """Load all retrieved incidents from JSONL file"""
        if not self.data_file.exists():
            return []
        
        incidents = []
        with open(self.data_file, 'r') as f:
            for line in f:
                if line.strip():
                    incidents.append(json.loads(line))
        
        return incidents
    
    def export_to_json(self, output_file: str):
        """Export all retrieved incidents to a single JSON file"""
        incidents = self.load_all_incidents()
        
        with open(output_file, 'w') as f:
            json.dump(incidents, f, indent=2)
        
        print(f"Exported {len(incidents)} incidents to {output_file}")


# Example usage with MCP tool calls
def retrieve_batch_with_mcp(retriever: BatchICMRetriever, batch_size: int = 5):
    """
    Example function showing how to use with MCP tools
    In actual use, this would be called from the Copilot agent
    """
    batch = retriever.get_next_batch(batch_size)
    
    if not batch:
        print("No more incidents to retrieve!")
        retriever.print_status()
        return None
    
    print(f"Next batch: {batch}")
    print(f"Use mcp_icm_mcp_eng_get_incident_details_by_id for each ID")
    print(f"Then call retriever.save_incident(incident_data) for each result")
    
    return batch


if __name__ == "__main__":
    # Initialize retriever
    retriever = BatchICMRetriever()
    
    # Example: Load incident IDs from Kusto query results
    # retriever.set_incident_ids([51000000879655, 51000000879746, ...])
    
    # Print status
    retriever.print_status()
    
    # Get next batch to retrieve
    # next_batch = retrieve_batch_with_mcp(retriever, batch_size=5)
    
    print("Batch ICM Retriever ready for use")
