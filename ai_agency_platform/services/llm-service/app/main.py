from fastapi import FastAPI
from app.services.llm_client import LLMClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/generate")
def generate(prompt: str):
    client = LLMClient()
    return {"response": client.generate(prompt)} 