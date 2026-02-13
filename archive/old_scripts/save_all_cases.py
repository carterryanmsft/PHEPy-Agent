"""
Direct script to save the 131 cases to CSV.
Since the JSON is too large for file operations, we'll embed the critical data directly.
"""
import pandas as pd
import json

# The MCP query returned 131 cases - we need to save them all
# For now, let me check what we currently have
current_csv = pd.read_csv('data/production_full_cases.csv')
print(f"Current CSV has {len(current_csv)} cases")
print(f"Customers: {current_csv['TopParentName'].nunique()}")

# The issue is that the create_file tool truncates large content
# We need to run the MCP query again and save the result properly
print("\n✗ The JSON file was truncated during creation")
print("✓ Solution: Re-run the MCP query and save results using a file handle")
