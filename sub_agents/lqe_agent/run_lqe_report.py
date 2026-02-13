"""
Quick script to fetch LQE data and generate Friday reports
"""
import json
import subprocess
from datetime import datetime

# Read the query
with open('lq_escalation_reports/lqequery.kql', 'r') as f:
    query = f.read()

print("Fetching LQE data from Kusto...")

# Note: Since MCP tool has issues with complex queries, 
# this script expects manual query execution
# For now, we'll check if data file exists or use test data

import os
from pathlib import Path

# Check for existing data file
data_dir = Path('lq_escalation_reports')
data_files = list(data_dir.glob('lqe_data_*.json'))

if data_files:
    # Use most recent file
    latest_file = max(data_files, key=os.path.getctime)
    print(f"Using existing data file: {latest_file}")
    data_file = str(latest_file)
else:
    print("\nNo data file found. Please:")
    print("1. Run the query in Kusto Explorer:")
    print("   File: lq_escalation_reports/lqequery.kql")
    print("2. Export results to JSON")
    print("3. Save as: lq_escalation_reports/lqe_data_YYYYMMDD.json")
    print("\nOR use test data for demonstration...")
    
    # Ask if they want to use test data
    use_test = input("\nGenerate report with test data? (y/n): ").lower()
    if use_test == 'y':
        data_file = 'test_data'
    else:
        exit(1)

# Generate reports
if data_file == 'test_data':
    print("\nGenerating reports with TEST data...")
    cmd = ['python', 'test_friday_analysis.py']
else:
    print(f"\nGenerating reports from: {data_file}")
    cmd = ['python', 'generate_friday_reports.py', data_file]

result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)
