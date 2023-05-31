import jwt
import requests
import json
import time
import uuid

# This is setting up the project as a an EPIC backend service.
# The docs https://fhir.epic.com/Documentation?docId=oauth2&section=BackendOAuth2Guide

# Define the JWT headers
headers = {
    "alg": "RS384",
    "typ": "JWT",
    "kid": ""  # IDK what this is
}

# Define the JWT payload
# Construct JWT claims
now = time.time()
claims = {
    "iss": "34039589-fc11-4319-bba9-4ba65bdc684a",
    "sub": "34039589-fc11-4319-bba9-4ba65bdc684a",
    "aud": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
    "jti": str(uuid.uuid4()),  # fill with reference id
    "exp": int(now + 1 * 60)  # cannot be more than 5 minutes!
}

# Generate signed token using private key with RS384 algorithm
# Replace with the path to your private key file
signing_key = open("privatekey.pem").read()
signed_token = jwt.encode(claims, signing_key, algorithm="RS384")


# Prepare API call payload
payload = {
    "grant_type": "client_credentials",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": signed_token.encode("utf-8"),
}

# Make API call
oauth2TokenUrl = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
# Dispatch the API call
response = requests.post(oauth2TokenUrl, data=payload)

# Check for errors
response.raise_for_status()

# Print response details
print("  => response body:", response.text)

# Now interacting w the API
access_token = json.loads(response.text).get("access_token")
auth = "Bearer " + access_token
# Testing Allergy Intolerance
base_url = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/DSTU2/"
spec = "Patient"
patient_ID = "egqBHVfQlt4Bw3XGXoxVxHg3"
# patient_ID = "T297OoGZ77MTaMTLPOjxyEwB"


url = base_url + spec + "/" + patient_ID

# Temp Auth (docs version)
# auth = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1cm46b2lkOmZoaXIiLCJjbGllbnRfaWQiOiJkOWYwN2JlNi0yOGNkLTQ2OWEtYjJjMS1jNjU5NWNjODE5MDEiLCJlcGljLmVjaSI6InVybjplcGljOk9wZW4uRXBpYy1jdXJyZW50IiwiZXBpYy5tZXRhZGF0YSI6IkI4UWgxWHRjb19tMFM4QmpXNS1QbWVQZ2piSzJFb3F0QXFCZHpHQlN5WG4talUwVm5ObnZMeWlyTGYydlpPbzlWU2ZmbjktZmhNQmk1UnlpZTk5cnBMaW1aNk40NzVDRmFhRFF5SkU1a3ZVckxYTVVfb3UtVGJCSWZwaFZXVmtGIiwiZXBpYy50b2tlbnR5cGUiOiJhY2Nlc3MiLCJleHAiOjE2ODU0NzQxNzIsImlhdCI6MTY4NTQ3MDU3MiwiaXNzIjoidXJuOm9pZDpmaGlyIiwianRpIjoiYzlkN2Q5MWMtNGE5Zi00NzY1LWEwODktMDNhMmMxNjdkMDhhIiwibmJmIjoxNjg1NDcwNTcyLCJzdWIiOiJldk5wLUtoWXdPT3FBWm4xcFoyZW51QTMifQ.SrQxvbfrbSRvVfG_WTlndwHstZReJynsNyDOEkXJYJ_lud3xgLqP7bLkXdnROIpa1FMRiBXiFEzYv4WfpIg_F3c_5boYSpSvYiEnZPvi4TKMRkI0TkNslgXKM6tFRtiqSV9ddxF2FeVpqLdhdmZX87NankB76wjDChTDXCC078jzK-a9Pun23fABxS-2y6YX_1kVIFHcPsxqMAykPl1xK_cmEMWyZTLjcm7GNa4IcL88nOnHZCE36KyuTs1O-gdLc3LLx0N__cBiSznPeAa8hnYrOPWdudOSzvxDxKUoXOWGo7ZrYT36nFha3hIkyoWNg_m87zV_C4X2nmGNl_LpKg"


headers = {
    "Authorization": auth
}

response = requests.get(url, headers=headers)
# print(response.text)
