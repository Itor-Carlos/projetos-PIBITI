from flask import Flask, jsonify
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

app = Flask(__name__)
load_dotenv()

# Token do Hugging Face (do seu .env)
HF_TOKEN = os.getenv("HF_TOKEN")

# Carregar tokenizer e modelo com autenticação
tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-270m", token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-270m", token=HF_TOKEN)

# Se GPU disponível, mover o modelo
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

@app.route('/base')
def base_route():
    prompt_text = "How much is 1 + 1?"
    print(device)
    
    inputs = tokenizer(prompt_text, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=50)

    resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(resposta)

    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)
