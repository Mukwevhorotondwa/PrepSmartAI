from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Hugging Face API configuration
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def query_hugging_face(payload):
    try:
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            return {"error": "Model is loading, please try again in a few seconds"}
        else:
            return {"error": f"API request failed with status {response.status_code}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

@app.route('/api/prepsmart', methods=['POST'])
def prepsmart_api():
    try:
        data = request.get_json()
        if not data or 'question' not in data or 'context' not in data:
            return jsonify({"error": "Missing question or context in request"}), 400

        question = data['question']
        context = data['context']

        # Prepare payload for Hugging Face question-answering
        payload = {
            "inputs": {
                "question": question,
                "context": context
            }
        }

        # Query Hugging Face API
        result = query_hugging_face(payload)

        if "error" in result:
            return jsonify(result), 500

        # Format response
        response = {
            "question": question,
            "answer": result.get("answer", "No answer found"),
            "score": result.get("score", 0.0)
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)