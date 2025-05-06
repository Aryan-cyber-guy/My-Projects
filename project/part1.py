import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def chat_with_llm(user_message):
    data = {
        "model": "llama3-8b-8192",  # You can use mixtral-8x7b-32768 or gemma-7b-it too
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Simple console chatbot loop
print("Chat with the LLM (type 'exit' to quit):")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    reply = chat_with_llm(user_input)
    print("Bot:", reply)
