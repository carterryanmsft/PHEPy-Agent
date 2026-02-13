import pandas as pd

# Show which cases should have bug links
bugs_df = pd.read_csv(r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\data\icm_bugs.csv')
cases_df = pd.read_csv(r'c:\Users\carterryan\OneDrive - Microsoft\PHEPy\data\production_full_cases.csv')

print('=== CASES THAT SHOULD SHOW BUG LINKS ===\n')

bug_cases = []
for _, bug in bugs_df.iterrows():
    icm_id = str(bug['IncidentId'])
    matching_cases = cases_df[cases_df['RelatedICM_Id'].astype(str).str.contains(icm_id, na=False)]
    
    if len(matching_cases) > 0:
        for _, case in matching_cases.iterrows():
            customer = case["TopParentName"]
            case_num = case["ServiceRequestNumber"]
            program = case["Program"]
            bug_id = bug["BugId"]
            bug_status = bug["Status"]
            
            print(f'Customer: {customer}')
            print(f'Case: {case_num}')
            print(f'Program: {program}')
            print(f'ICM: {icm_id}')
            print(f'Bug Link: 🔧{bug_id} (Status: {bug_status})')
            print(f'Look in: ICM Owner column\n')
            
            bug_cases.append({
                'Customer': customer,
                'Program': program,
                'Case': case_num,
                'ICM': icm_id,
                'Bug': bug_id
            })

print(f'\nTotal cases with bugs: {len(bug_cases)}')
print(f'IC Program cases: {len([c for c in bug_cases if c["Program"] == "IC"])}')
print(f'MCS Program cases: {len([c for c in bug_cases if c["Program"] == "MCS"])}')
