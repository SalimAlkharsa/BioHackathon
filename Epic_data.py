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
        self.goal = self.get_Goal()
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
            url = self.base_url + resource_name + "?patient=" + self.patient_ID + "&category=vital-signs&issued={issued}"
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


    # Data formatting
    def format_patientData(self):
        # Parse the XML data
        root = ET.fromstring(self.patientData.text)
        # Define the namespace
        namespace = {'fhir': 'http://hl7.org/fhir'}
        # Extract the values
        extension = root.find('.//{http://hl7.org/fhir}extension[@url="http://hl7.org/fhir/StructureDefinition/us-core-birth-sex"]')
        gender_value = extension.find('{http://hl7.org/fhir}valueCodeableConcept/{http://hl7.org/fhir}coding/{http://hl7.org/fhir}code').attrib['value']
        birth_date_value = root.find('.//fhir:birthDate', namespace).attrib['value']

        return [gender_value, birth_date_value]
    
    def format_allergyIntolerance(self):
        allergies = []
        for allergy in self.allergyIntolerance:
            # Parse the XML data
            root = ET.fromstring(allergy)
            # Define the namespace
            namespace = {'fhir': 'http://hl7.org/fhir'}
            # Extract the value
            allergy_value = root.find('.//fhir:substance/fhir:coding/fhir:display', namespace).attrib['value']
            allergies.append(allergy_value)
        return allergies
    
    def format_condition(self):
        conditions = []
        for condition in self.condition:
            # Parse the XML data
            root = ET.fromstring(condition)
            # Define the namespace
            namespace = {'fhir': 'http://hl7.org/fhir'}
            # Extract the value
            try:
                condition_value = root.find('.//fhir:code/fhir:coding/fhir:display', namespace).attrib['value']
                clinical_status = root.find('.//fhir:clinicalStatus', namespace).attrib['value']
            except AttributeError:
                condition_value = "No condition description"
                clinical_status = "No clinical status"
            conditions.append({condition_value: clinical_status})
        return conditions
    
    def format_goal(self):
        goals = []
        for goal in self.goal:
            # Parse the XML data
            root = ET.fromstring(goal)
            # Define the namespace
            namespace = {'fhir': 'http://hl7.org/fhir'}
            # Extract the value
            try:
                goal_value = root.find('.//fhir:description', namespace).attrib['value']
            except AttributeError:
                goal_value = "No goal description"
            goals.append(goal_value)
        return goals
    
    def format_medicationStatement(self):
        medications = []
        for medication in self.medicationStatement:
            # Parse the XML data
            root = ET.fromstring(medication)
            # Define the namespace
            namespace = {'fhir': 'http://hl7.org/fhir'}
            # Extract the value
            try:
                medication_value = root.find('.//fhir:medicationCodeableConcept/fhir:coding/fhir:display', namespace).attrib['value']
                instructions = root.find('.//fhir:dosage/fhir:text', namespace).attrib['value']
            except AttributeError:
                medication_value = "No medication description"
                instructions = "No instructions"
            medications.append({medication_value: {'instructions': instructions}})
        return medications
            
    def format_observation(self):
        # This function is logically tricky, so I'll implement it later,
        # for now I'll skip it but its data will probably be helpful.
        pass

    def format_medicationOrder(self):
        medications = []
        for medication in self.medicationOrder:
            # Parse the XML data
            root = ET.fromstring(medication)
            # Define the namespace
            namespace = {'fhir': 'http://hl7.org/fhir'}
            # Extract the value
            try:
                medication = root.find('.//fhir:medicationReference/fhir:display', namespace).attrib['value']
                instruction = root.find('.//fhir:dosageInstruction/fhir:text', namespace).attrib['value']
                duration = root.find('.//fhir:dispenseRequest/fhir:expectedSupplyDuration/fhir:value', namespace).attrib['value']
            except AttributeError:
                medication = "No medication prescribed"
                instruction = "No instructions available"
                duration = "No duration available"
            medications.append({medication: [{'instruction': instruction}, {'duration': duration}]})
        return medications

    def build_json(self):
        patient_json = {
            "patientData": {
                "sex": self.format_patientData()[0],
                "birth_date": self.format_patientData()[1]
            },
            "allergyIntolerance": self.format_allergyIntolerance(),
            "condition": self.format_condition(),
            "goal": self.format_goal(),
            "medicationStatement": self.format_medicationStatement(),
            "medicationOrder": self.format_medicationOrder(),
        }
        return patient_json
    
    # Get the data in a text format for my own reference!
    def to_text(self): # Used just for debugging
        patient_text = f"Patient ID: {self.patient_ID}\n"

        #patient_text += f"Patient Data:\n{self.patientData.text}\n"
        #patient_text += f"Allergy Intolerance:\n{self.allergyIntolerance}\n"
        #patient_text += f"Condition:\n{self.condition}\n"
        #patient_text += f"Goal:\n{self.goal}\n"
        #patient_text += f"Medication Order:\n{self.medicationOrder}\n" ####FLAG
        #patient_text += f"Medication Statement:\n{self.medicationStatement}\n"
        
        #patient_text += f"Observation:\n{self.observation}\n"

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


'''
### TESTING###
patID = "eIXesllypH3M9tAA5WdJftQ3"
patient = Patient(patID)
x = patient.to_text()
with open('x.xml', 'w') as file:
    file.write(x)
print(patient.build_json())
'''