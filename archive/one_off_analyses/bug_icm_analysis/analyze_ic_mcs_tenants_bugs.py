"""
Analyze tenants associated with IC and MCS programs and identify open bugs related to those customers
"""
import pandas as pd
import json
from collections import defaultdict

def load_and_analyze():
    print("=" * 80)
    print("IC and MCS Tenant & Bug Analysis")
    print("=" * 80)
    
    # Load production cases
    cases_df = pd.read_csv('data/production_full_cases.csv')
    
    # Load ICM bugs
    bugs_df = pd.read_csv('data/icm_bugs.csv')
    
    # Filter for IC and MCS programs
    ic_cases = cases_df[cases_df['Program'] == 'IC'].copy()
    mcs_cases = cases_df[cases_df['Program'] == 'MCS'].copy()
    
    print(f"\n[SUMMARY]")
    print(f"  Total IC Cases: {len(ic_cases)}")
    print(f"  Total MCS Cases: {len(mcs_cases)}")
    print(f"  Total Open Bugs: {len(bugs_df)}")
    
    # Get unique tenants for IC
    ic_tenants = ic_cases.groupby(['TopParentName', 'TenantId']).agg({
        'ServiceRequestNumber': 'count',
        'HasICM': lambda x: (x == 'Yes').sum(),
        'RiskScore': 'max',
        'RiskLevel': lambda x: x.value_counts().index[0] if len(x) > 0 else 'Unknown'
    }).reset_index()
    ic_tenants.columns = ['Customer', 'TenantId', 'OpenCases', 'CasesWithICM', 'MaxRiskScore', 'PrimaryRiskLevel']
    ic_tenants = ic_tenants.sort_values('OpenCases', ascending=False)
    
    # Get unique tenants for MCS
    mcs_tenants = mcs_cases.groupby(['TopParentName', 'TenantId']).agg({
        'ServiceRequestNumber': 'count',
        'HasICM': lambda x: (x == 'Yes').sum(),
        'RiskScore': 'max',
        'RiskLevel': lambda x: x.value_counts().index[0] if len(x) > 0 else 'Unknown'
    }).reset_index()
    mcs_tenants.columns = ['Customer', 'TenantId', 'OpenCases', 'CasesWithICM', 'MaxRiskScore', 'PrimaryRiskLevel']
    mcs_tenants = mcs_tenants.sort_values('OpenCases', ascending=False)
    
    print("\n" + "=" * 80)
    print("IC (INCIDENT COMMANDER) TENANTS")
    print("=" * 80)
    print(f"\nTotal Unique IC Customers: {len(ic_tenants)}\n")
    print(ic_tenants.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("MCS (MICROSOFT CONSULTING SERVICES) TENANTS")
    print("=" * 80)
    print(f"\nTotal Unique MCS Customers: {len(mcs_tenants)}\n")
    print(mcs_tenants.to_string(index=False))
    
    # Analyze open bugs
    print("\n" + "=" * 80)
    print("OPEN BUGS ANALYSIS")
    print("=" * 80)
    
    open_bugs = bugs_df[bugs_df['Status'].isin(['Active', 'New'])].copy()
    print(f"\n[OPEN BUGS] Total: {len(open_bugs)}")
    print(f"   - Active: {len(open_bugs[open_bugs['Status'] == 'Active'])}")
    print(f"   - New: {len(open_bugs[open_bugs['Status'] == 'New'])}")
    
    print("\n" + "-" * 80)
    print("All Open Bugs:")
    print("-" * 80)
    for idx, bug in open_bugs.iterrows():
        print(f"\n[BUG] ID: {bug['BugId']} | ICM: {bug['IncidentId']} | Status: {bug['Status']}")
        print(f"   Owner: {bug['Owner']}")
        print(f"   Description: {bug['Description']}")
        print(f"   Link: {bug['AdoLink']}")
    
    # Map bugs to customers via ICM incidents
    print("\n" + "=" * 80)
    print("BUGS MAPPED TO IC CUSTOMERS")
    print("=" * 80)
    
    ic_bug_mapping = defaultdict(list)
    for idx, case in ic_cases.iterrows():
        if pd.notna(case['RelatedICM_Id']) and case['RelatedICM_Id']:
            icm_ids = str(case['RelatedICM_Id']).split(',')
            for icm_id in icm_ids:
                icm_id = icm_id.strip()
                # Find bugs for this ICM
                related_bugs = bugs_df[bugs_df['IncidentId'].astype(str) == icm_id]
                for _, bug in related_bugs.iterrows():
                    ic_bug_mapping[case['TopParentName']].append({
                        'case': case['ServiceRequestNumber'],
                        'icm': icm_id,
                        'bug_id': bug['BugId'],
                        'bug_status': bug['Status'],
                        'bug_desc': bug['Description'],
                        'bug_owner': bug['Owner'],
                        'bug_link': bug['AdoLink']
                    })
    
    if ic_bug_mapping:
        for customer, bugs in sorted(ic_bug_mapping.items()):
            print(f"\n[CUSTOMER] {customer}")
            print(f"   Total bugs found: {len(bugs)}")
            for bug in bugs:
                status_mark = "[CLOSED]" if bug['bug_status'] in ['Resolved', 'Closed', 'Done'] else "[OPEN]"
                print(f"\n   {status_mark} Bug {bug['bug_id']} ({bug['bug_status']})")
                print(f"      Case: {bug['case']}")
                print(f"      ICM: {bug['icm']}")
                print(f"      Description: {bug['bug_desc']}")
                print(f"      Owner: {bug['bug_owner']}")
                print(f"      Link: {bug['bug_link']}")
    else:
        print("\n   No bugs directly linked to IC customer ICMs")
    
    # Map bugs to MCS customers via ICM incidents
    print("\n" + "=" * 80)
    print("BUGS MAPPED TO MCS CUSTOMERS")
    print("=" * 80)
    
    mcs_bug_mapping = defaultdict(list)
    for idx, case in mcs_cases.iterrows():
        if pd.notna(case['RelatedICM_Id']) and case['RelatedICM_Id']:
            icm_ids = str(case['RelatedICM_Id']).split(',')
            for icm_id in icm_ids:
                icm_id = icm_id.strip()
                # Find bugs for this ICM
                related_bugs = bugs_df[bugs_df['IncidentId'].astype(str) == icm_id]
                for _, bug in related_bugs.iterrows():
                    mcs_bug_mapping[case['TopParentName']].append({
                        'case': case['ServiceRequestNumber'],
                        'icm': icm_id,
                        'bug_id': bug['BugId'],
                        'bug_status': bug['Status'],
                        'bug_desc': bug['Description'],
                        'bug_owner': bug['Owner'],
                        'bug_link': bug['AdoLink']
                    })
    
    if mcs_bug_mapping:
        for customer, bugs in sorted(mcs_bug_mapping.items()):
            print(f"\n[CUSTOMER] {customer}")
            print(f"   Total bugs found: {len(bugs)}")
            for bug in bugs:
                status_mark = "[CLOSED]" if bug['bug_status'] in ['Resolved', 'Closed', 'Done'] else "[OPEN]"
                print(f"\n   {status_mark} Bug {bug['bug_id']} ({bug['bug_status']})")
                print(f"      Case: {bug['case']}")
                print(f"      ICM: {bug['icm']}")
                print(f"      Description: {bug['bug_desc']}")
                print(f"      Owner: {bug['bug_owner']}")
                print(f"      Link: {bug['bug_link']}")
    else:
        print("\n   No bugs directly linked to MCS customer ICMs")
    
    # Count of open bugs per customer
    print("\n" + "=" * 80)
    print("OPEN BUGS BY CUSTOMER (IC)")
    print("=" * 80)
    
    ic_open_bug_counts = {}
    for customer, bugs in ic_bug_mapping.items():
        open_count = sum(1 for b in bugs if b['bug_status'] in ['Active', 'New'])
        if open_count > 0:
            ic_open_bug_counts[customer] = open_count
    
    if ic_open_bug_counts:
        for customer, count in sorted(ic_open_bug_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {customer}: {count} open bug(s)")
    else:
        print("   No open bugs found for IC customers")
    
    print("\n" + "=" * 80)
    print("OPEN BUGS BY CUSTOMER (MCS)")
    print("=" * 80)
    
    mcs_open_bug_counts = {}
    for customer, bugs in mcs_bug_mapping.items():
        open_count = sum(1 for b in bugs if b['bug_status'] in ['Active', 'New'])
        if open_count > 0:
            mcs_open_bug_counts[customer] = open_count
    
    if mcs_open_bug_counts:
        for customer, count in sorted(mcs_open_bug_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {customer}: {count} open bug(s)")
    else:
        print("   No open bugs found for MCS customers")
    
    # Export results
    output = {
        'ic_tenants': ic_tenants.to_dict('records'),
        'mcs_tenants': mcs_tenants.to_dict('records'),
        'open_bugs': open_bugs.to_dict('records'),
        'ic_bug_mapping': dict(ic_bug_mapping),
        'mcs_bug_mapping': dict(mcs_bug_mapping)
    }
    
    with open('data/ic_mcs_tenant_bug_analysis.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print("\n" + "=" * 80)
    print("[SUCCESS] Analysis complete! Results saved to: data/ic_mcs_tenant_bug_analysis.json")
    print("=" * 80)

if __name__ == "__main__":
    load_and_analyze()
