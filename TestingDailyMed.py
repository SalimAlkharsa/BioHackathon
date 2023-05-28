# Trying to load data from DailyMed
# Documentation to follow: https://dailymed.nlm.nih.gov/dailymed/webservices-help/v2/spls_setid_api.cfm
import requests
import json

# This basically behaves like a search function, giving you a list of drug names that match the search criteria


def request_drug_names(drug_name=None, name_type='both', manufacturer=None, return_format='json'):
    base_url = 'https://dailymed.nlm.nih.gov/dailymed/services/v2/drugnames'
    endpoint = f'{base_url}.{return_format}'

    params = {
        'drug_name': drug_name,
        'name_type': name_type,
        'manufacturer': manufacturer,
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json() if return_format == 'json' else response.text
    else:
        print(f'Request failed with status code {response.status_code}.')
        return None

# This basically behaves like a search function, giving you a list of SPL IDs that match the search criteria


def request_spls(drug_name=None, name_type='both', return_format='json'):
    base_url = 'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls'
    endpoint = f'{base_url}.{return_format}'

    params = {
        'drug_name': drug_name,
        'name_type': name_type,
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json() if return_format == 'json' else response.text
    else:
        print(f'Request failed with status code {response.status_code}.')
        return None


def request_spl_xml(set_id):
    endpoint = f'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{set_id}.xml'

    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.text
    else:
        print(f'Request failed with status code {response.status_code}.')
        return None
###### Testing the function outputs######


# Request drug names in JSON format
drug_names_json = request_drug_names(drug_name='aspirin', return_format='json')
if drug_names_json:
    # Print the formatted JSON response
    formatted_json = json.dumps(drug_names_json, indent=4)
    print(formatted_json)

# Request SPL IDs in JSON format
print('\n\n')
spls_json = request_spls(
    drug_name='ASPIRIN EXTRA STRENGTH', return_format='json')
if spls_json:
    # Process the JSON response and retrieve the Set IDs
    set_ids = [s['setid'] for s in spls_json['data']]
    # print(set_ids) # ex setid -> f837c31f-24e5-a8df-e053-6394a90a0b36

# Request SPL XML
print('\n\n')
# -> f837c31f-24e5-a8df-e053-6394a90a0b36
spl_xml = request_spl_xml(set_ids[0])
if spl_xml:
    # Print the XML document
    print(spl_xml)
