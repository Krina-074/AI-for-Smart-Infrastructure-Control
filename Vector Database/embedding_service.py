from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "mxbai-embed-large"


class EmbedRequest(BaseModel):
    text: str


@app.post("/embed")
def embed(payload: EmbedRequest):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": payload.text
        },
        timeout=30
    )

    response.raise_for_status()
    vector = response.json()["embedding"]

    return {
        "vector": vector,
        "dim": len(vector),
        "model": MODEL
    }
