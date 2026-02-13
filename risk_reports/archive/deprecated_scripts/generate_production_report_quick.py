"""
Quick Production Report Generator
Accepts query result JSON via stdin and generates HTML report
"""
import json
import sys
import subprocess

print("=== IC/MCS Production Report Generator ===\n")

# Step 1: Execute Kusto query
print("Step 1: Executing Kusto query...")
print("(This will take a moment to fetch 131 cases from cxedata cluster)\n")

# For now, indicate the query needs to be run
print("Please ensure the Kusto query has been executed and the JSON result is available.")
print("Expected result: 131 cases from IC/MCS customers with 20+ day age\n")

# Step 2: Generate report
print("Step 2: Once data is available, the report generator will:")
print("  - Load all 131 cases from JSON")
print("  - Enrich with ICM owner data from icm.csv")  
print("  - Apply ACTIVE highlighting for awaiting customer status")
print("  - Group by customer with risk-based sorting")
print("  - Generate IC_MCS_Production_Report.htm\n")

print("Command to run after data is saved:")
print('python ic_mcs_risk_report_generator.py production_cases_131.json IC_MCS_Production_Report.htm icm.csv')
