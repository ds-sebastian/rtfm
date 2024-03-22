from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

from utils.config import API_KEY, API_URL

from .base import BaseQAModel


class OpenAIModel(BaseQAModel):
    def setup_qa_chain(self, retriever, model_name):
        model = ChatOpenAI(model=model_name, base_url=API_URL, api_key=API_KEY)
        return ConversationalRetrievalChain.from_llm(
            model, retriever=retriever, return_source_documents=True
        )
