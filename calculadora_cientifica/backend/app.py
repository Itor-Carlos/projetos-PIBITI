from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_TOKEN")
client = genai.Client(api_key=GEMINI_API_KEY)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

class PromptRequest(BaseModel):
    prompt: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(prompt_req: PromptRequest):

    prompt_message = prompt = f"""
        Você é um assistente matemático. Sua tarefa é ler uma equação ou problema matemático descrito em linguagem natural e transformá-lo em uma equação simbólica. 
        Em seguida, resolva passo a passo, explicando o raciocínio até chegar ao resultado final. Defina o passo a passo e use uma didática clara.

        Sempre siga esta estrutura na resposta:
        1. Interpretar o enunciado em linguagem natural.
        2. Escrever a equação matemática correspondente.
        3. Resolver a equação mostrando os passos.
        4. Apresentar o resultado final de forma clara e objetiva.

        Exemplo de entrada: 'Qual é o valor de x se cinco vezes x mais 3 é igual a 18?'
        Exemplo de saída:
        1. Interpretação: o problema pede para resolver uma equação linear.
        2. Equação: 5x + 3 = 18
        3. Resolução: 5x = 18 - 3 → 5x = 15 → x = 15/5 → x = 3
        4. Resposta final: x = 3

        Problema em linguagem natural:
        {prompt_req.prompt}
        """
    try:
        resp = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_message
        )
        return {"response": resp.text}
    except Exception as e:
        return {"error": str(e)}