import requests

# Set the API endpoint URL
url = 'https://prescraib.herokuapp.com'

# Example patient ID
patient_id = 'eIXesllypH3M9tAA5WdJftQ3'

# Create the request payload
payload = {'patient_id': patient_id}

# Send the POST request to the API endpoint
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    cds_output = data['cds_output']
    print('CDS Output:', cds_output)
else:
    print('Error:', response.status_code)
