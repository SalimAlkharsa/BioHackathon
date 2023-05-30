import jwt
import requests
import time
import uuid

# This is setting up the project as a an EPIC backend service.
# The docs https://fhir.epic.com/Documentation?docId=oauth2&section=BackendOAuth2Guide

# Define the private key
with open("privatekey.pem", "r") as file:
    private_key = file.read()

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

# print("  => signed token:", signed_token)

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
print("  => response status:", response.status_code)
print("  => response header:", response.headers)
print("  => response body:", response.text)
