"""
Batch CSV Appender - Processes query results in batches
Run this after each MCP query batch to append results to CSV
"""

import pandas as pd
from pathlib import Path
import json
import sys

def append_batch(batch_json, output_file='data/production_full_cases.csv', batch_num=1):
    """
    Append a batch of cases to the CSV file
    
    Args:
        batch_json: JSON string or dict with batch data
        output_file: Path to CSV file
        batch_num: Batch number (for reporting)
    """
    # Parse JSON if needed
    if isinstance(batch_json, str):
        data = json.loads(batch_json)
    else:
        data = batch_json
    
    # Extract cases
    if 'data' in data:
        cases = data['data']
    elif isinstance(data, list):
        cases = data
    else:
        raise ValueError("Unexpected data structure")
    
    # Convert to DataFrame
    df = pd.DataFrame(cases)
    
    # Determine if file exists (first batch vs append)
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)
    
    if batch_num == 1 or not output_path.exists():
        # First batch - write with header
        df.to_csv(output_path, mode='w', index=False, header=True)
        print(f"✓ Batch {batch_num}: Created file with {len(df)} cases")
    else:
        # Subsequent batches - append without header
        df.to_csv(output_path, mode='a', index=False, header=False)
        print(f"✓ Batch {batch_num}: Appended {len(df)} cases")
    
    # Count total
    total_df = pd.read_csv(output_path)
    print(f"  Total cases in file: {len(total_df)}")
    
    return len(df)

if __name__ == "__main__":
    # This will be used interactively
    print("Batch Appender Ready")
    print("Usage: Call append_batch() with your batch data")
