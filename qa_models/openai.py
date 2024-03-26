from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from utils.config import API_KEY

from .base import BaseQAModel


class OpenAIModel(BaseQAModel):
    def setup_qa_chain(self, retriever, model_name):
        print("MODEL NAME: ", model_name)
        model = ChatOpenAI(model=model_name, api_key=API_KEY)  #! REMOVE model_name
        return ConversationalRetrievalChain.from_llm(
            model, retriever=retriever, return_source_documents=True
        )

    def get_embeddings(self):
        return OpenAIEmbeddings(api_key=API_KEY)
