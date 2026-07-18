import json
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# -----------------------------
# Config
# -----------------------------
JSON_FILE = "it_admin_tools.json"
COLLECTION_NAME = "it_admin_tools"

OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "mxbai-embed-large"

# -----------------------------
# Load JSON
# -----------------------------
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# -----------------------------
# Prepare embedding text
# -----------------------------
texts = []

for item in data:
    combined_text = " ".join([
        item.get("tool", ""),
        item.get("intent", ""),
        item.get("description", ""),
        " ".join(item.get("keywords", []))
    ])
    texts.append(combined_text)

print("Prepared texts:", texts)

# -----------------------------
# Create embeddings via Ollama
# -----------------------------
def get_embedding(text: str) -> list[float]:
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": text
        },
        timeout=60
    )
    r.raise_for_status()
    return r.json()["embedding"]


vectors = [get_embedding(text) for text in texts]

print(f"Vector dimension: {len(vectors[0])}")  # ✅ 1024

# -----------------------------
# Connect to Qdrant
# -----------------------------
client = QdrantClient(host="localhost", port=6333)

# -----------------------------
# Create collection safely
# -----------------------------
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,                     # 🔥 MUST match mxbai-embed-large
            distance=Distance.COSINE
        )
    )

# -----------------------------
# Build points (FIXED IDs)
# -----------------------------
points = []

for idx, item in enumerate(data):
    point_id = int(item["id"])  # "028" → 28 (correct)

    points.append(
        PointStruct(
            id=point_id,
            vector=vectors[idx],
            payload=item
        )
    )

# -----------------------------
# Upsert data
# -----------------------------
client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print("✅ Data uploaded successfully to Qdrant with Ollama embeddings")
