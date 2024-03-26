import logging

import streamlit as st
from langchain.text_splitter import CharacterTextSplitter

from data_loaders.factory import get_data_loader
from qa_models.factory import get_qa_model
from utils.config import CONNECTION_STRING
from utils.settings import settings
from vector_stores.factory import get_vector_store

logger = logging.getLogger(__name__)


def preprocess_data():
    with st.spinner("Preprocessing data..."):
        logger.info("Starting data preprocessing...")

        # Load data using the configured data loader
        data_loader = get_data_loader()
        documents = data_loader.load_data()

        # Chunk/split the documents into overlapping segments
        text_splitter = CharacterTextSplitter(
            chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
        )
        texts = text_splitter.split_documents(documents)

        # Get the embeddings from the selected QA model
        qa_model = get_qa_model()
        embeddings = qa_model.get_embeddings()

        # Store the embeddings in the configured vector store
        vector_store = get_vector_store()
        db = vector_store.store_embeddings(
            embedding=embeddings,
            documents=texts,
            collection_name="comma_chat_embed",
            db_url=CONNECTION_STRING,
        )

        # Set up the retriever and configure it
        retriever = db.as_retriever()
        retriever.search_kwargs.update(
            {
                "distance_metric": settings.distance_metric,
                "fetch_k": settings.fetch_k,
                "k": settings.k,
            }
        )

        # Combine the retriever and the specified QA model to create the QA chain
        qa = qa_model.setup_qa_chain(
            retriever=retriever, model_name=settings.model_name
        )

        logger.info("Data preprocessing completed.")
        st.success("Data preprocessing completed successfully!")

        return qa
