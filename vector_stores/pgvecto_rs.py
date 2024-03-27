from langchain_community.vectorstores.pgvecto_rs import PGVecto_rs

from .base import BaseVectorStore


class PGVectorStore(BaseVectorStore):
    def store_embeddings(
        self, embedding, documents, pre_delete_collection=True, **kwargs
    ):
        return PGVecto_rs.from_documents(
            embedding=embedding,
            documents=documents,
            pre_delete_collection=pre_delete_collection,
            **kwargs,
        )

    def from_collection_name(self, embedding, collection_name, **kwargs):
        return PGVecto_rs.from_collection_name(
            embedding=embedding, collection_name=collection_name, **kwargs
        )

    def as_retriever(self):
        return self.as_retriever()
