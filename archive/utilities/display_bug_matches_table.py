"""
Display bug-to-customer matches in a numeric table format
"""
import json
import pandas as pd

# Load the results
with open('data/bug_customer_matches_final.json', 'r') as f:
    results = json.load(f)

# Prepare table data
table_data = []

# Process matched bugs
for bug in results['matched_bugs']:
    customers = ', '.join([f"{c['Customer']} ({c['Program']})" for c in bug['Customers']])
    table_data.append({
        'Bug ID': bug['BugId'],
        'Status': bug['Status'],
        'Customer(s)': customers,
        'Title': bug['Title'][:60] + '...' if len(bug['Title']) > 60 else bug['Title'],
        'Matched': '✓'
    })

# Process unmatched bugs
for bug in results['unmatched_bugs']:
    table_data.append({
        'Bug ID': bug['BugId'],
        'Status': bug['Status'],
        'Customer(s)': 'None Found',
        'Title': bug['Title'][:60] + '...' if len(bug['Title']) > 60 else bug['Title'],
        'Matched': '✗'
    })

# Create DataFrame and sort by Bug ID
df = pd.DataFrame(table_data)
df = df.sort_values('Bug ID')

# Display summary
print('=' * 130)
print('BUG TO CUSTOMER MAPPING - SORTED BY BUG ID')
print('=' * 130)
print(f'\nTotal Bugs: {len(df)}')
print(f'Matched: {results["summary"]["matched_count"]} | Unmatched: {results["summary"]["unmatched_count"]}')
print(f'IC Customers: {len(results["summary"]["ic_customers"])} | MCS Customers: {len(results["summary"]["mcs_customers"])}')
print('\n' + '=' * 130)

# Display full table
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 70)

print(df.to_string(index=False))
print('=' * 130)

# Display by customer grouping
print('\n' + '=' * 130)
print('GROUPED BY CUSTOMER')
print('=' * 130)

# IC Customers
if results['summary']['ic_customers']:
    print('\n🔵 IC CUSTOMERS:')
    for customer in sorted(results['summary']['ic_customers']):
        bugs = df[df['Customer(s)'].str.contains(customer, na=False)]['Bug ID'].tolist()
        print(f'  {customer}: {len(bugs)} bug(s) - {bugs}')

# MCS Customers
if results['summary']['mcs_customers']:
    print('\n🟢 MCS CUSTOMERS:')
    for customer in sorted(results['summary']['mcs_customers']):
        bugs = df[df['Customer(s)'].str.contains(customer, na=False)]['Bug ID'].tolist()
        print(f'  {customer}: {len(bugs)} bug(s) - {bugs}')

# Unmatched
unmatched_bugs = df[df['Matched'] == '✗']['Bug ID'].tolist()
if unmatched_bugs:
    print(f'\n⚪ NO CUSTOMER MATCH: {len(unmatched_bugs)} bug(s) - {unmatched_bugs}')

print('=' * 130)

# Export to CSV for easy viewing
csv_file = 'data/bug_customer_mapping_table.csv'
df.to_csv(csv_file, index=False)
print(f'\n✅ Table exported to: {csv_file}')
print('=' * 130)
