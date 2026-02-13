"""
Analyze ADO bugs and match them to IC/MCS customers
"""
import json
import pandas as pd

# Load IC/MCS customer cases
cases_df = pd.read_csv('data/production_full_cases.csv')

# Get unique IC/MCS customers
ic_mcs_customers = cases_df['TopParentName'].unique()
ic_mcs_customer_set = set([c.upper() for c in ic_mcs_customers])

# ADO bugs from search
bugs = [
    {"id": 3563451, "title": "Content Explorer GetTypePathAggregatesItems requests not working properly for very large scaled out shards", "state": "Resolved", "tags": "ADNOC; Customer Escalation; Incident Repair Item; MCSIC; P0ClassificationBug; Triage; Triage needed; US CUSTOMS"},
    {"id": 4000625, "title": "Unable to View Exchange Items under Trainable Classifier in Content Explorer", "state": "New", "tags": "Athena Health; beis.gov.uk; BugReviewCompleted; Carle Health; CostingRequired; CustomerEscalation; CY25H2-Candidate; DFA Milk; HighPriorityFeature; John Jordan; OCE; P0ClassificationBug; TransitionToPriva; Triage; Walgreens; WBA"},
    {"id": 4263833, "title": "View source feature is providing pre-auth token which can be used for data exfiltration", "state": "Active", "tags": "Customer Escalation; CY25H2-Candidate; P0ClassificationBug"},
    {"id": 4676229, "title": "[Globalization] Keyword dictionary SIT doesn't detect the same text with Chinese/Japanese characters and single byte characters", "state": "Active", "tags": "CustomerEscalation; DCRCandidate; DSI-TEC:Area-Globalization; DSI-TEC:CarryForward-CY25-11; DSI-TEC:Cx-MUFJ; DSI-TEC:CY25-H1-P0CommittedBugs; DSI-TEC:Sprint-CY25-09; DSI-TEC:SprintScheduled; high priority; LTIM; OCE; P0; P0ClassificationBug; Waiting for Spec"},
    {"id": 5007992, "title": "Credit card SIT is detecting values in excel sheet with cell value in a decimal number due to Line Feed (LF)", "state": "New", "tags": "Customer Escalation; DSI-TEC:CY25-H1-P0CommittedBugs; LTIM; OCE; P0ClassificationBug; ToBeTriaged"},
    {"id": 5017813, "title": "EU passport number SIT shows duplicated results for same confidence level", "state": "New", "tags": "Customer Escalation; CxE-CEM-Purview-; DSI-TEC:CY25-H1-P0CommittedBugs; LTIM; OCE; P0ClassificationBug; ToBeTriaged"},
    {"id": 5101127, "title": "Remove \"Matches and Accuracy\" table in Data explorer for M365 cloud", "state": "Resolved", "tags": "CustomerEscalation; OCE; P0ClassificationBug"},
    {"id": 5166846, "title": "MCE Classification timeout in Exchange when sent multiple mails", "state": "Resolved", "tags": "Customer Escalation; DSI-TEC:CY25-H1-P0CommittedBugs; LTIM; MUFJ; OCE; P0ClassificationBug; ToBeTriaged"},
    {"id": 5174195, "title": "[Cx Escalation] [MUFJ] Full and half width characters should be handled consistently", "state": "New", "tags": "CustomerEscalation; DSI-TEC:Area-CxEscalation; DSI-TEC:Area-Globalization; DSI-TEC:Cx-MUFJ; DSI-TEC:Sprint-CY26-02; DSI-TEC:SprintScheduled; LTIM; OCE; P0ClassificationBug"},
    {"id": 5193520, "title": "[EDM] EDMUploadAgent.exe displays error line number incorrectly", "state": "Resolved", "tags": "CSU_HighRiskItem; Customer Escalation; EDM bugs; LTIM; MUFJ; OCE; P0ClassificationBug"},
    {"id": 5379952, "title": "[Novartis] [S500] High latency for EDM classification resulting in no outlook policy tips", "state": "Resolved", "tags": "LTIM; P0ClassificationBug"}
]

print('=' * 100)
print('ADO BUGS MATCHED TO IC/MCS CUSTOMERS')
print('=' * 100)

ic_mcs_matched = []
unmatched = []

for bug in bugs:
    tags = bug['tags'].upper()
    title = bug['title'].upper()
    matched_customers = []
    
    # Check if any IC/MCS customer is mentioned in tags or title
    for customer in ic_mcs_customer_set:
        # Handle special cases
        customer_variations = [customer]
        if customer == 'MUFJ':
            customer_variations.append('MITSUBISHI')
        elif customer == 'FORD':
            customer_variations.extend(['FORD MOTOR'])
        
        for variation in customer_variations:
            if variation in tags or variation in title:
                # Get the original customer name from cases
                original_name = [c for c in ic_mcs_customers if c.upper() == customer][0]
                program = cases_df[cases_df['TopParentName'] == original_name]['Program'].iloc[0] if original_name in cases_df['TopParentName'].values else 'Unknown'
                matched_customers.append({'name': original_name, 'program': program})
                break
    
    if matched_customers:
        bug['matched_customers'] = matched_customers
        ic_mcs_matched.append(bug)
    else:
        unmatched.append(bug)

print(f'\n✅ Bugs Matched to IC/MCS Customers: {len(ic_mcs_matched)}')
print(f'❌ Bugs NOT Matched: {len(unmatched)}')

print('\n' + '=' * 100)
print('IC/MCS CUSTOMER BUGS')
print('=' * 100)

for bug in ic_mcs_matched:
    print(f'\n[Bug {bug["id"]}] {bug["state"]}')
    print(f'  Title: {bug["title"]}')
    print(f'  Customers:')
    for cust in bug['matched_customers']:
        print(f'    - {cust["name"]} ({cust["program"]})')
    print(f'  Link: https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug["id"]}')

print('\n' + '=' * 100)
print('BUGS NOT MATCHED TO IC/MCS CUSTOMERS')
print('=' * 100)

for bug in unmatched:
    print(f'\n[Bug {bug["id"]}] {bug["state"]}')
    print(f'  Title: {bug["title"][:80]}...')
    print(f'  Link: https://o365exchange.visualstudio.com/IP%20Engineering/_workitems/edit/{bug["id"]}')

# Save result
output = {
    'ic_mcs_matched_bugs': ic_mcs_matched,
    'unmatched_bugs': unmatched,
    'summary': {
        'total_bugs': len(bugs),
        'ic_mcs_matched': len(ic_mcs_matched),
        'unmatched': len(unmatched)
    }
}

with open('data/ado_bugs_ic_mcs_mapping.json', 'w') as f:
    json.dump(output, f, indent=2)

print('\n' + '=' * 100)
print(f'✓ Analysis saved to: data/ado_bugs_ic_mcs_mapping.json')
print('\n📋 SUMMARY:')
print(f'  Total Customer Escalation Bugs: {len(bugs)}')
print(f'  Matched to IC/MCS Customers: {len(ic_mcs_matched)}')
print(f'  Customers Found: MUFJ (IC), Novartis (IC)')
print('\n⚠️  NOTE: These bugs have hyperlinks to ICM incidents.')
print('  To get the exact ICM IDs from hyperlinks, fetch each bug individually with expand=relations')
print('=' * 100)
