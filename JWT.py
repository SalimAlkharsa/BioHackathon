import jwt
import requests
from datetime import datetime, timedelta

# This is setting up the project as a an EPIC backend service.
# The docs https://fhir.epic.com/Documentation?docId=oauth2&section=BackendOAuth2Guide

# Define the private key
with open("privatekey.pem", "r") as file:
    private_key = file.read()

# Define the JWT headers
headers = {
    "alg": "RS384",
    "typ": "JWT"
}

# Define the JWT payload
payload = {
    # client_id -> just a test client_id not real
    "iss": "34039589-fc11-4319-bba9-4ba65bdc684a",
    "sub": "d45049c3-3441-40ef-ab4d-b9cd86a17225",  # ?? maybe client_id
    "aud": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
    "jti": "f9eaafba-2e49-11ea-8880-5ce0c5aee679",  # This should not be hardcoded
    # Max is 5 minutes
    "exp": int((datetime.utcnow() + timedelta(minutes=5)).timestamp()),
}

# Generate the JWT
jwt_token = jwt.encode(payload, private_key,
                       algorithm="RS384", headers=headers)

# Print the JWT
print(jwt_token.encode())


# Define the token endpoint URL
token_endpoint = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"

# Define the form-urlencoded parameters
payload = {
    "grant_type": "client_credentials",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": jwt_token.encode()
}

# Send the POST request
# There is a prior error bc this does not return what is expected
response = requests.post(token_endpoint, data=payload)

# Check the response status code and content
if response.status_code == 200:
    access_token = response.json().get("access_token")
    print("Access Token:", access_token)
else:
    print("Error:", response.text)
