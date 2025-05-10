from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import logging

# Load environment variables
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Setup Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=["https://my-projects-git-main-xenos-projects-71c5e6e1.vercel.app"])
# Set up logging to capture detailed logs for troubleshooting
logging.basicConfig(level=logging.INFO)

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return '', 200  # Handle preflight check
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            raise ValueError("Missing 'message' in request data")

        user_message = data['message']
        app.logger.info(f"Received message: {user_message}")

        # Set up payload for the Groq API
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

        # Send the request to the Groq API
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            app.logger.info(f"API response: {reply}")
            return jsonify({"reply": reply})
        else:
            error_message = f"Groq API returned error: {response.text}"
            app.logger.error(error_message)
            return jsonify({"error": "API Error", "details": error_message}), 500

    except Exception as e:
        # Log the exception and return the error message
        app.logger.error(f"Error in chat route: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
