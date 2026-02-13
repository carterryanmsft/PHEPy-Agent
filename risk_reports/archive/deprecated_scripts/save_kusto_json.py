#!/usr/bin/env python3
# Paste the Kusto JSON result and save to file
import json

kusto_result = input("Paste Kusto JSON: ")
data = json.loads(kusto_result)

with open('data/production_cases_131.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(data.get('data', []))} cases to production_cases_131.json")
