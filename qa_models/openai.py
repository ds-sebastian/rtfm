from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from sentence_transformers import SentenceTransformer, util

from utils.config import API_KEY, API_URL

from .base import BaseQAModel


class OpenAIModel(BaseQAModel):
    def __init__(self):
        self.embed_model = "sentence-transformers/all-mpnet-base-v2"
        self.embed_encode_kwargs = {"normalize_embeddings": False}
        self.cache_folder = "cache"

    def setup_qa_chain(self, retriever, model_name):
        print("MODEL NAME: ", model_name)
        model = ChatOpenAI(model=model_name, api_key=API_KEY, base_url=API_URL)
        return ConversationalRetrievalChain.from_llm(
            model, retriever=retriever, return_source_documents=True
        )

    def get_embeddings(self):
        return HuggingFaceEmbeddings(
            model_name=self.embed_model,
            encode_kwargs=self.embed_encode_kwargs,
            cache_folder=self.cache_folder,
        )
