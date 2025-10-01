import requests
from google import genai
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from fastmcp import Client
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/ask")
async def ask_gemini(question: str):
    mcp_client = Client("movies.py")
    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session]
            ),
        )
        return {"answer": response.text}
