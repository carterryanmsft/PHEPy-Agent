import pandas as pd

icm = pd.read_csv('data/icm.csv')
test_icms = [693849812, 693543577, 694142803, 694208210, 694253124, 693952482, 694041459]

print('Checking ICMs in dict:')
for icm_id in test_icms:
    in_dict = icm_id in icm['IncidentId'].values
    print(f'  {icm_id}: {in_dict}')
    if in_dict:
        owner = icm[icm['IncidentId'] == icm_id]['IcmOwner'].values[0]
        status = icm[icm['IncidentId'] == icm_id]['IcmStatus'].values[0]
        print(f'    Owner: {owner}, Status: {status}')
