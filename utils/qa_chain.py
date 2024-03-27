# utils/qa_chain.py

import logging
import sys

from langchain.text_splitter import CharacterTextSplitter

from data_loaders.factory import get_data_loader
from qa_models.factory import get_qa_model
from utils.config import CONNECTION_STRING
from utils.settings import settings
from vector_stores.factory import get_vector_store

logger = logging.getLogger(__name__)


class QAChain:
    def __init__(self):
        self.qa = None

    def load_data(self):
        logger.info("Starting data loading...")

        try:
            documents = self._load_documents()
            texts = self._split_documents(documents)
            embeddings = self._get_embeddings()
            retriever = self._store_embeddings(embeddings, texts)

            logger.debug(f"Retriever: {retriever}")  # Add debug logging

            self.qa = self._setup_qa_chain(retriever)

            logger.debug(f"QA Chain: {self.qa}")  # Add debug logging

            logger.info("Data loading completed.")
        except Exception as e:
            logger.error(f"Error in load_data: {e}")
            raise

    def _load_documents(self):
        data_loader = get_data_loader()
        return data_loader.load_data()

    def _split_documents(self, documents):
        text_splitter = CharacterTextSplitter(
            chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
        )
        return text_splitter.split_documents(documents)

    def _get_embeddings(self):
        qa_model = get_qa_model()
        return qa_model.get_embeddings()

    def _store_embeddings(self, embeddings, texts):
        vector_store = get_vector_store()
        db = vector_store.store_embeddings(
            embedding=embeddings,
            documents=texts,
            pre_delete_collection=True,
            collection_name="rtfm_embeddings",
            db_url=CONNECTION_STRING,
        )
        retriever = db.as_retriever()
        retriever.search_kwargs.update(
            {
                "distance_metric": settings.distance_metric,
                "fetch_k": settings.fetch_k,
                "k": settings.k,
            }
        )
        return retriever

    def _setup_qa_chain(self, retriever):
        qa_model = get_qa_model()
        return qa_model.setup_qa_chain(
            retriever=retriever, model_name=settings.model_name
        )

    def process_question(self, question, chat_history, qa):
        logger.info(f"Processing question: {question}")

        try:
            result = qa.invoke({"question": question, "chat_history": chat_history})
            response = result["answer"]
            references = result["source_documents"]

            logger.info(f"Generated response: {response}")
            return response, references
        except Exception as e:
            logger.error(f"Error in process_question: {e}")
            raise
