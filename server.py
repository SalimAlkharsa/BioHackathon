from flask import Flask, request, jsonify, render_template
from GPT3_CDS import generate_prompt, make_GPT_request


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/cds', methods=['POST'])
def get_cds_output():
    patient_id = request.json['patient_id']
    prompt = generate_prompt(patient_id)
    response = make_GPT_request(prompt)
    cds_output = response.choices[0].text.strip()
    return jsonify({'cds_output': cds_output})

@app.route('/demo', methods=['GET'])
def demo():
    # Pre-selected patient IDs
    patient_ids = ['erXuFYUfucBZaryVksYEcMg3', 'eq081-VQEgP8drUUqCWzHfw3', 'egqBHVfQlt4Bw3XGXoxVxHg3']
    return render_template('demo.html', patient_ids=patient_ids)

if __name__ == '__main__':
    app.run()
