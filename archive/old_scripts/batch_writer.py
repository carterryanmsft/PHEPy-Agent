"""
Batch processor for MCP Kusto query results
Handles large datasets by processing in smaller chunks
"""

import pandas as pd
from pathlib import Path

def process_batch(batch_data, output_file, mode='w'):
    """
    Process a batch of cases and append to CSV
    
    Args:
        batch_data: List of case dictionaries
        output_file: Path to output CSV
        mode: 'w' for write (first batch), 'a' for append
    """
    df = pd.DataFrame(batch_data)
    
    # Write or append
    header = (mode == 'w')
    df.to_csv(output_file, mode=mode, index=False, header=header, encoding='utf-8')
    
    return len(df)

def main():
    output_file = Path('data/production_full_cases.csv')
    output_file.parent.mkdir(exist_ok=True)
    
    print("Batch CSV Writer - Processing 131 cases in batches")
    print("=" * 60)
    
    # Since we have the MCP query result with all 131 cases,
    # we need to split it into batches of ~20 cases each
    # This will create 7 batches (6 x 20 + 1 x 11)
    
    # Ask user for approach
    print("\nOptions:")
    print("1. Run 7 MCP queries (20 cases each) with pagination")
    print("2. Manually provide batches of case data")
    print("\nRecommendation: Let's modify the query to use 'skip' and 'take'")
    print("We can run the same query 7 times with different offsets:")
    print("  - Batch 1: | skip 0 | take 20")
    print("  - Batch 2: | skip 20 | take 20")
    print("  - ... etc")
    
    total_cases = 0
    
    print(f"\nReady to process batches into: {output_file}")
    print("Would you like me to:")
    print("A) Run the query 7 times with pagination")
    print("B) Process data you provide directly")

if __name__ == "__main__":
    main()
