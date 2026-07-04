from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from agent import embed

def load_qdrant():
    return QdrantClient("http://vector_database:6333")

def create_collection(qdrant, collection_name):
    if not qdrant.collection_exists(collection_name):
        qdrant.create_collection(
            collection_name = collection_name,
            vectors_config = VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )
        return True
    return False

def add_data_to_the_collection(data: list[str], collection_name, qdrant):
    points = [
        PointStruct(id=i, vector = embed(data_piece), payload={'text': data_piece})
        for i, data_piece in enumerate(data)
    ]
    qdrant.upsert(
        collection_name = collection_name,
        points = points
    )

def get_data_from_the_collection(task: str, collection_name, qdrant):
    return qdrant.query_points(
        collection_name = collection_name,
        query = embed(task),
        limit = 10,
        with_payload = True
    )