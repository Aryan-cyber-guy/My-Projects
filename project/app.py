from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

app = Flask(__name__)
CORS(app)  # 👈 Enables CORS for all routes

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": user_message}
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    else:
        return jsonify({"error": "API Error", "details": response.text}), 500

if __name__ == "__main__":
    app.run(debug=True)
