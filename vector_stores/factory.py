from utils.settings import settings

from .pgvecto_rs import PGVectorStore


def get_vector_store():
    if settings.vector_store == "pgvecto_rs":
        return PGVectorStore()
    else:
        raise ValueError(f"Unsupported vector store: {settings.vector_store}")
