import jwt
import requests
import json
import time
import uuid
import xml.etree.ElementTree as ET

# Set up a patient object


class Patient:
    def __init__(self, patient_ID):
        # Helper Getter variables
        self.token = "Bearer " + self.get_access_token()
        self.base_url = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/DSTU2/"
        # Define patient data
        self.patient_ID = patient_ID

        # Get patient data
        self.patientData = self.get_patientData()
        self.allergyIntolerance = self.get_allergyIntolerance()
        self.condition = self.get_condition()
        self.diagnostics = self.get_Diagnostics()
        self.goal = self.get_Goal()
        self.medication = self.get_Medication()
        self.medicationOrder = self.get_MedicationOrder()
        self.medicationStatement = self.get_MedicationStatement()
        self.observation = self.get_Observation()

    # Basic Getters

    def get_patientData(self):
        headers = {
            "Authorization": self.token
        }
        return requests.get(self.base_url + "Patient/" + self.patient_ID, headers=headers)

    def get_resourceID(self, resource_name):
        headers = {
            "Authorization": self.token
        }
        if resource_name == "Observation":
            url = self.base_url + resource_name + "?patient=" + self.patient_ID + "&category=social-history&issued={issued}"
        else:
            url = self.base_url + resource_name + "?patient=" + self.patient_ID
        response = requests.get(url, headers=headers)
        root = ET.fromstring(response.text)

        # Define the namespace
        namespace = {'fhir': 'http://hl7.org/fhir'}

        # Extract the ID values
        id_values = []
        entries = root.findall(".//fhir:entry", namespace)
        for entry in entries:
            resource = entry.find(".//fhir:resource", namespace)
            if resource is not None:
                id_element = resource.find(".//fhir:id", namespace)
                if id_element is not None:
                    id_value = id_element.attrib['value']
                    id_values.append(id_value)

        return id_values

    # Data Getters

    def get_allergyIntolerance(self):
        headers = {
            "Authorization": self.token
        }
        rescIDs = self.get_resourceID("AllergyIntolerance")
        info = []
        for rescID in rescIDs:
            info.append(requests.get(self.base_url +
                        "AllergyIntolerance/" + rescID, headers=headers).text)
        return info

    def get_condition(self):
        headers = {
            "Authorization": self.token
        }
        rescIDs = self.get_resourceID("Condition")
        info = []
        for rescID in rescIDs:
            info.append(requests.get(self.base_url +
                        "Condition/" + rescID, headers=headers).text)
        return info

    def get_Diagnostics(self):
        headers = {
            "Authorization": self.token
        }
        rescIDs = self.get_resourceID("DiagnosticReport")
        info = []
        for rescID in rescIDs:
            info.append(requests.get(self.base_url +
                        "DiagnosticReport/" + rescID, headers=headers).text)
        return info

    def get_Goal(self):
        headers = {
            "Authorization": self.token
        }
        rescIDs = self.get_resourceID("Goal")
        info = []
        for rescID in rescIDs:
            info.append(requests.get(self.base_url +
                        "Goal/" + rescID, headers=headers).text)
        return info

    def get_Medication(self):
        headers = {
            "Authorization": self.token
        }
        rescIDs = self.get_resourceID("Medication")
        info = []
        for rescID in rescIDs:
            info.append(requests.get(self.base_url +
                        "Medication/" + rescID, headers=headers).text)
        return info

    def get_MedicationOrder(self):
        headers = {
            "Authorization": self.token
        }
        rescIDs = self.get_resourceID("MedicationOrder")
        info = []
        for rescID in rescIDs:
            info.append(requests.get(self.base_url +
                        "MedicationOrder/" + rescID, headers=headers).text)
        return info

    def get_MedicationStatement(self):
        headers = {
            "Authorization": self.token
        }
        rescIDs = self.get_resourceID("MedicationStatement")
        info = []
        for rescID in rescIDs:
            info.append(requests.get(self.base_url +
                        "MedicationStatement/" + rescID, headers=headers).text)
        return info

    def get_Observation(self):
        headers = {
            "Authorization": self.token
        }
        rescIDs = self.get_resourceID("Observation")
        info = []
        for rescID in rescIDs:
            info.append(requests.get(self.base_url +
                        "Observation/" + rescID, headers=headers).text)
        return info

    # Get the data in a JSON format
    def to_text(self):
        patient_text = f"Patient ID: {self.patient_ID}\n"
        patient_text += f"Patient Data:\n{self.patientData.text}\n"
        patient_text += f"Allergy Intolerance:\n{self.allergyIntolerance}\n"
        patient_text += f"Condition:\n{self.condition}\n"
        patient_text += f"Diagnostics:\n{self.diagnostics}\n"
        patient_text += f"Goal:\n{self.goal}\n"
        patient_text += f"Medication:\n{self.medication}\n"
        patient_text += f"Medication Order:\n{self.medicationOrder}\n"
        patient_text += f"Medication Statement:\n{self.medicationStatement}\n"
        patient_text += f"Observation:\n{self.observation}\n"
        return patient_text

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
patID = "erXuFYUfucBZaryVksYEcMg3"
patient = Patient(patID)
# '''
x = patient.to_text()
with open('x.txt', 'w') as file:
    file.write(x)
# '''
