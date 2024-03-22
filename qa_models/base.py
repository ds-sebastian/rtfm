from abc import ABC, abstractmethod


class BaseQAModel(ABC):
    @abstractmethod
    def setup_qa_chain(self, retriever):
        pass
