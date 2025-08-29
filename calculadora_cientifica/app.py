from flask import Flask
from dotenv import load_dotenv
from openai import OpenAI
import os

app = Flask(__name__)

load_dotenv()

cliente = OpenAI(api_key = os.getenv("OPENAPI_KEY"))

@app.route('/base')
def base_route():
    prompt = cliente.chat.completions.create(
        model = "gpt-4",
        messages = [
            {
                "role": "user",
                "content": "Qual é a raiz quadrada de 16?"
            }
        ]
    )
    print(prompt)
    return "<button onclick='console.log(\"teste\")'>Click me</button>"