from flask import Flask, request, jsonify
from GPT3_CDS import generate_prompt, make_GPT_request


app = Flask(__name__)
@app.route('/cds', methods=['POST'])
def get_cds_output():
    patient_id = request.json['patient_id']
    prompt = generate_prompt(patient_id)
    response = make_GPT_request(prompt)
    cds_output = response.choices[0].text.strip()
    return jsonify({'cds_output': cds_output})

if __name__ == '__main__':
    app.run(debug=True)
