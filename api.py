from flask import Flask, request, jsonify
import torch
import json
from model import CognitiveClassifier

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

app = Flask(__name__)

model = CognitiveClassifier()
checkpoint = torch.load('bloom_classifier_pt.pt', map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)

@app.route('/')
def hello_world():
    return 'PlaforEDU Bloom Classifier'

@app.route('/predict', methods=['POST'])
def predict():
    description = request.json['description']
    prediction = model.classify(description)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)