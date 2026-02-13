"""
Analyze FTE vs Vendor distribution in LQE data
"""
import json
from collections import defaultdict

# Load the data
with open('data/regional_lqe_14day_real_20260213_094834.json') as f:
    data = json.load(f)

# Load engineer region mapping
with open('support_engineer_regions.json') as f:
    config = json.load(f)
    engineer_regions = {k: v for k, v in config['mappings'].items() if not k.startswith('_')}

# Apply mapping
for record in data:
    if record.get('OriginRegion') == 'Unknown':
        created_by = record.get('CreatedBy', '')
        if created_by in engineer_regions:
            record['OriginRegion'] = engineer_regions[created_by]

# Categorize engineers
def classify_engineer(alias):
    if alias.startswith('v-'):
        return 'Vendor'
    elif any(alias.startswith(p) for p in ['inf_', 'wcl_', 'cnx_']):
        return 'Delivery Center'
    else:
        return 'FTE'

# Count by region and type
region_stats = defaultdict(lambda: {'FTE': 0, 'Vendor': 0, 'Delivery Center': 0, 'cases': 0})

for record in data:
    region = record.get('OriginRegion', 'Unknown')
    engineer = record.get('CreatedBy', '')
    eng_type = classify_engineer(engineer)
    region_stats[region][eng_type] += 1
    region_stats[region]['cases'] += 1

print('=' * 80)
print('REGIONAL BREAKDOWN: FTE vs VENDORS')
print('=' * 80)

for region in ['Americas', 'EMEA', 'APAC', 'Unknown']:
    if region in region_stats:
        stats = region_stats[region]
        total = stats['cases']
        print(f'\n{region}:')
        print(f'  Total Cases: {total}')
        print(f'    - FTE: {stats["FTE"]} cases ({stats["FTE"]/total*100:.1f}%)')
        print(f'    - Vendors: {stats["Vendor"]} cases ({stats["Vendor"]/total*100:.1f}%)')
        if stats['Delivery Center'] > 0:
            print(f'    - Delivery Centers: {stats["Delivery Center"]} cases ({stats["Delivery Center"]/total*100:.1f}%)')

print()
print('=' * 80)
print('OVERALL SUMMARY')
print('=' * 80)

total_fte = sum(s['FTE'] for s in region_stats.values())
total_vendor = sum(s['Vendor'] for s in region_stats.values())
total_dc = sum(s['Delivery Center'] for s in region_stats.values())
total_cases = total_fte + total_vendor + total_dc

print(f'Total Cases: {total_cases}')
print(f'  - FTE: {total_fte} cases ({total_fte/total_cases*100:.1f}%)')
print(f'  - Vendors: {total_vendor} cases ({total_vendor/total_cases*100:.1f}%)')
print(f'  - Delivery Centers: {total_dc} cases ({total_dc/total_cases*100:.1f}%)')
print()

# Show percentage analysis
print('=' * 80)
print('KEY INSIGHTS')
print('=' * 80)
print(f'• {total_vendor/total_cases*100:.1f}% of LQ escalations come from vendor engineers')
print(f'• {total_fte/total_cases*100:.1f}% of LQ escalations come from FTE engineers')
if total_dc > 0:
    print(f'• {total_dc/total_cases*100:.1f}% of LQ escalations come from delivery center accounts')
print()
