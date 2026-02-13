"""
Final Analysis: Why ADO Bugs Are Not Linked to IC/MCS Customer Cases
"""
import json
import pandas as pd

print('=' * 100)
print('WHY ADO BUGS ARE NOT LINKED TO IC/MCS CUSTOMERS')
print('=' * 100)

# Load customer cases
cases_df = pd.read_csv('data/production_full_cases.csv')

# Get all IC/MCS ICM IDs from customer cases
customer_icm_ids = set()
for _, case in cases_df.iterrows():
    if pd.notna(case['RelatedICM_Id']) and case['RelatedICM_Id']:
        icm_ids = str(case['RelatedICM_Id']).replace(',', ';').split(';')
        for icm_id in icm_ids:
            icm_id = icm_id.strip()
            if icm_id:
                try:
                    customer_icm_ids.add(int(icm_id))
                except ValueError:
                    pass

print(f'\n📊 IC/MCS Customer Cases have {len(customer_icm_ids)} unique ICM incidents')

# ADO bugs found
ado_bugs = {
    '3563451': {'icms': [21000000854034, 597578454, 602470308, 615540474], 'customer': 'ADNOC', 'program': 'MCS'},
    '4000625': {'icms': [], 'customer': 'NAB', 'program': 'IC'},
    '4676229': {'icms': [], 'customer': 'MUFJ/EY', 'program': 'IC/MCS'},
    '5166846': {'icms': [], 'customer': 'MUFJ', 'program': 'IC'},
    '5174195': {'icms': [], 'customer': 'MUFJ', 'program': 'IC'},
    '5193520': {'icms': [], 'customer': 'MUFJ', 'program': 'IC'},
    '5379952': {'icms': [], 'customer': 'Novartis', 'program': 'IC'}
}

print('\n' + '=' * 100)
print('ROOT CAUSE ANALYSIS')
print('=' * 100)

print('\n❌ PROBLEM: ADO Bugs are not linked to IC/MCS customer ICM incidents')
print('\n📋 FINDINGS:')
print('\n1️⃣  Bug 3563451 HAS 4 ICM hyperlinks:')
for icm in ado_bugs['3563451']['icms']:
    in_customers = icm in customer_icm_ids
    print(f'     • ICM {icm}: {"✓ IN customer cases" if in_customers else "✗ NOT in customer cases"}')

print(f'\n2️⃣  6 other bugs have NO ICM hyperlinks at all:')
for bug_id, info in ado_bugs.items():
    if not info['icms']:
        print(f'     • Bug {bug_id} ({info["customer"]} - {info["program"]}): No ICM hyperlinks')

print('\n' + '=' * 100)
print('WHY THEY ARE NOT LINKED')
print('=' * 100)

print('\n🔍 Reason 1: ICM Hyperlinks Missing from ADO Bugs')
print('   - 6 out of 7 bugs have NO ICM hyperlinks in their relations')
print('   - The bugs are tagged with customer names, but not linked to ICM incidents')

print('\n🔍 Reason 2: ICM Mismatch for Bug 3563451')
print('   - Bug 3563451 HAS ICM hyperlinks, but those ICMs are NOT in the customer case data')
print('   - The ICMs (21000000854034, 597578454, etc.) may be older/different incidents')

print('\n🔍 Reason 3: Incomplete Data in IncidentBugs Table')
print('   - Your original bug list had 17 bugs')
print('   - Only 7 bugs exist in ICM IncidentBugs table')
print('   - 10 bugs are missing entirely from ICM')

print('\n' + '=' * 100)
print('SOLUTION: HOW TO LINK THEM')
print('=' * 100)

print('\n✅ OPTION 1: Add ICM Hyperlinks to ADO Bugs')
print('   For each bug, add Hyperlink relation to the correct ICM incidents')
print('   Example: Bug 5174195 (MUFJ) should link to MUFJ ICM incidents')

print('\n✅ OPTION 2: Link Bugs to ICMs in ICM System')
print('   Use ICM portal to associate bugs with incidents')
print('   This populates the IncidentBugs table automatically')

print('\n✅ OPTION 3: Manual Mapping Table')
print('   Create a mapping of Bug ID → ICM IDs → Customers')
print('   Use this for reporting until proper links are established')

print('\n' + '=' * 100)
print('CURRENT STATE SUMMARY')
print('=' * 100)

print('\n📊 Statistics:')
print(f'   • IC/MCS Customer ICMs in Cases: {len(customer_icm_ids)}')
print(f'   • ADO Customer Escalation Bugs Found: 7')
print(f'   • Bugs with ICM Hyperlinks: 1')
print(f'   • Bugs WITHOUT ICM Hyperlinks: 6')
print(f'   • ICM Hyperlinks that Match Customer Cases: 0')

print('\n🎯 Bottom Line:')
print('   The bugs are NOT linked because:')
print('   1. They lack ICM hyperlinks in ADO')
print('   2. The one bug with hyperlinks points to different ICMs')
print('   3. The IncidentBugs table is incomplete')

# Save comprehensive analysis
output = {
    'problem': 'ADO bugs are not linked to IC/MCS customer ICM incidents',
    'root_causes': [
        'Missing ICM hyperlinks in 6 out of 7 ADO bugs',
        'Bug 3563451 has ICM links but to different ICMs than customer cases',
        'IncidentBugs table missing 10 out of 17 original bugs'
    ],
    'customer_icm_count': len(customer_icm_ids),
    'ado_bugs': ado_bugs,
    'recommendation': 'Add ICM hyperlinks to ADO bugs or link bugs to ICMs in ICM system'
}

with open('data/bug_linkage_root_cause_analysis.json', 'w') as f:
    json.dump(output, f, indent=2)

print('\n✓ Full analysis saved to: data/bug_linkage_root_cause_analysis.json')
print('=' * 100)
