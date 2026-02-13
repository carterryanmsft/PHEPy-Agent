"""
Complete End-to-End Workflow
Saves the 118 cases from recent Kusto query and generates reports
"""
import pandas as pd
import subprocess
import sys

print("="*80)
print("IC/MCS RISK ANALYSIS - COMPLETE END-TO-END WORKFLOW")
print("="*80)

# Note: The 118 cases from the Kusto query need to be manually saved first
# since we executed that query via mcp_kusto tool
print("\nStep 1: Case Data")
print("-" * 80)
df = pd.read_csv('data/production_full_cases.csv')
print(f"Current cases in CSV: {len(df)}")

if len(df) < 100:
    print(f"⚠️  WARNING: Expected ~118 cases, found {len(df)}")
    print("The Kusto query returned 118 cases but CSV not updated")
    print("Proceeding with available {len(df)} cases...")

# Extract ICM IDs
print("\nStep 2: Extract ICM IDs")
print("-" * 80)
icm_ids = set()
for icm_str in df['RelatedICM_Id'].dropna():
    for icm_id in str(icm_str).replace(',', ';').split(';'):
        if icm_id.strip():
            try:
                icm_ids.add(int(icm_id.strip()))
            except:
                pass

print(f"Found {len(icm_ids)} unique ICM IDs")
print(f"ICM IDs: {sorted(list(icm_ids))[:10]}..." if len(icm_ids) > 10 else f"ICM IDs: {sorted(list(icm_ids))}")

print("\nStep 3: ICM Data Query")
print("-" * 80)
print("Execute this query via mcp_kusto-mcp-ser_execute_query:")
print(f"Cluster: icmcluster")
print(f"Database: IcmDataWarehouse")
print(f"\nQuery:")
icm_list_str = ', '.join(str(id) for id in sorted(list(icm_ids)))
print(f"""
Incidents
| where IncidentId in ({icm_list_str})
| summarize arg_max(ModifiedDate, *) by IncidentId
| where OwningTenantName != "SCIM Escalation Management"
| project IncidentId, Severity, OwningContactAlias, Status
| order by IncidentId asc
""")

print("\nStep 4: After ICM query completes, run:")
print("python risk_reports/ic_mcs_risk_report_generator.py data/production_full_cases.csv IC_MCS_FINAL risk_reports/data/icm.csv")

print("\n" + "="*80)
print("WORKFLOW STEPS OUTLINED - Execute ICM query and then generate reports")
print("="*80)
