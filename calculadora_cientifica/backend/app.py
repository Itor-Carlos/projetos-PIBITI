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
    try:
        resp = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_req.prompt
        )
        return {"response": resp.text}
    except Exception as e:
        return {"error": str(e)}