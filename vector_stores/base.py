from abc import ABC, abstractmethod


class BaseVectorStore(ABC):
    @abstractmethod
    def from_documents(self, embedding, documents, **kwargs):
        pass

    @abstractmethod
    def from_collection_name(self, embedding, collection_name, **kwargs):
        pass

    @abstractmethod
    def as_retriever(self):
        pass
