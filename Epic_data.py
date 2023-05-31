import jwt
import requests
import json
import time
import uuid

# Set up a patient object


class Patient:
    def __init__(self, patient_ID):
        # Define the JWT headers
        '''self.headers = {"alg": "RS384",
                        "typ": "JWT",
                        "kid": ""  # IDK what this is
                        }'''
        # Helper Getter variables
        self.token = "Bearer " + self.get_access_token()
        self.base_url = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/DSTU2/"
        # Define patient data
        self.patient_ID = patient_ID

        # Get patient data
        self.patientData = self.get_patientData()
        self.allergyIntolerance = self.get_allergyIntolerance()

    # Getters
    def get_patientData(self):
        headers = {
            "Authorization": self.token
        }
        return requests.get(self.base_url + "Patient/" + self.patient_ID, headers=headers)

    def get_allergyIntolerance(self):
        headers = {
            "Authorization": self.token
        }
        return requests.get(self.base_url + "AllergyIntolerance/" + self.patient_ID, headers=headers)

    # Establish a connection to the API
    def generate_signed_token(self):
        now = time.time()
        claims = {
            "iss": "34039589-fc11-4319-bba9-4ba65bdc684a",
            "sub": "34039589-fc11-4319-bba9-4ba65bdc684a",
            "aud": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
            "jti": str(uuid.uuid4()),  # fill with reference id
            "exp": int(now + 4 * 60)  # cannot be more than 5 minutes!
        }
        signing_key = open("privatekey.pem").read()
        signed_token = jwt.encode(claims, signing_key, algorithm="RS384")
        return signed_token.encode("utf-8")

    def get_access_token(self):
        signed_token = self.generate_signed_token()
        payload = {
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": signed_token,
        }
        self.token_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
        response = requests.post(self.token_url, data=payload)
        access_token = json.loads(response.text).get("access_token")
        return access_token


### TESTING###
patID = "T81lum-5p6QvDR7l6hv7lfE52bAbA2ylWBnv9CZEzNb0B"
pat = Patient(patID)
# '''
print(pat.patientData.text)
print(pat.allergyIntolerance.text)
# '''
