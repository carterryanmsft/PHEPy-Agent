"""Save fresh case data from Kusto query to CSV"""
import pandas as pd
import json

# The fresh case data from the Kusto query
cases_data = {
    "name": "PrimaryResult",
    "data": []  # Will be populated from query results
}

print(f"Ready to save fresh cases from Kusto query")
print(f"Please provide the case data JSON")
