import requests
import re
import xml.etree.ElementTree as ET

# Documentation to follow: https://dailymed.nlm.nih.gov/dailymed/webservices-help/v2/spls_setid_api.cfm

# Set up the drug object
class Drug:
    def __init__(self, name):
        self.name = name
        self.spl = self.request_spls(name_type='both', return_format='json')
        self.spl_xml = self.request_spl_xml()

    # Helper
    def extract_text_in_parentheses(self, text):
        pattern = r'\((.*?)\)'  # Regular expression pattern to match text within parentheses
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None
    
    def request_spls(self, name_type='both', return_format='json'):
        base_url = 'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls'
        endpoint = f'{base_url}.{return_format}'

        params = {
            'drug_name': self.extract_text_in_parentheses(self.name),
            'name_type': name_type
        }

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            return response.json() if return_format == 'json' else response.text
        else:
            print(f'Request failed with status code {response.status_code}.')
            return None
        
    def request_spl_xml(self):
        if self.spl is None:
            return None
        
        set_id = self.spl['data'][0]['setid']

        endpoint = f'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{set_id}.xml'

        response = requests.get(endpoint)

        if response.status_code == 200:
            return response.text
        else:
            print(f'Request failed with status code {response.status_code}.')
            return None
    
    def traverse_xml(self):
        if self.spl_xml is None:
            return None
        root = ET.fromstring(self.request_spl_xml())
        namespaces = {'ns': 'urn:hl7-org:v3'}
        ingredients = root.findall('.//ns:ingredient', namespaces=namespaces)
        ingredient_data = []
        for ingredient in ingredients:
            ingredient_data.append({
                'name': ingredient.find('.//ns:quantity/ns:ingredientSubstance', namespaces=namespaces),
                #'strength': ingredient.find('.//ns:strength', namespaces=namespaces).text,
                #'code': ingredient.find('.//ns:code', namespaces=namespaces).attrib['code']
        })
        return ingredient_data

###### Testing the function outputs ######
# drug = Drug('drospirenone-ethinyl estradiol (YAZ) 3-0.02 MG per tablet')
# n = Drug.traverse_xml(drug)
# print(n)
