import os
from dotenv import load_dotenv
from Epic_data import Patient
import openai


def generate_prompt(patient_id):
    patient = Patient(patient_id)
    prompt = "This is a CDS system in alpha testing with the job of flagging potential issues in medicationOrders given a json of patient data.\n\n"
    prompt += f"Patient Data:\n{patient.build_json()}\n\n"
    prompt += "Q: Does the medicationOrder have any potential issues, given the patient profile? Answer in a simple yes or no, and provide reasoning.\n\nA:"
    return prompt

def make_api_request(prompt):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=24, ### 24 testing, usw 200 otherwise
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response

def print_response(response):
    print("Response:", response.choices[0].text.strip())

'''
# Example usage
id = 'eIXesllypH3M9tAA5WdJftQ3'
prompt = generate_prompt(id)
response = make_api_request(prompt)
print_response(response)
'''