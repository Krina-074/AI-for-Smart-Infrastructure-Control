from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="it_admin_tools",
    vectors_config={
        "text": VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    }
)

print("✅ Collection created with named vector: text")
