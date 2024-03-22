import streamlit as st

from data_loaders.factory import get_data_loader
from qa_models.factory import get_qa_model
from ui.chat import (
    display_assistant_response,
    display_chat_history,
    display_question_input,
    display_references,
)
from ui.sidebar import display_sidebar
from utils.config import API_KEY, API_URL, CONNECTION_STRING
from utils.settings import settings
from vector_stores.factory import get_vector_store


def preprocess_data():
    with st.status("Preprocessing Data..."):
        data_loader = get_data_loader()
        directory = data_loader.load_data()

        from langchain_community.document_loaders import ReadTheDocsLoader

        loader = ReadTheDocsLoader(directory)
        docs = loader.load()

        from langchain.text_splitter import CharacterTextSplitter

        text_splitter = CharacterTextSplitter(
            chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
        )
        texts = text_splitter.split_documents(docs)

        from langchain_openai import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings(base_url=API_URL, api_key=API_KEY)

        vector_store = get_vector_store()
        db = vector_store.from_documents(
            embedding=embeddings,
            documents=texts,
            collection_name="comma_chat_embed",
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

        qa_model = get_qa_model()
        qa = qa_model.setup_qa_chain(retriever, settings.openai_model)

    st.sidebar.success("Preprocessing completed successfully!")
    st.rerun()  # Refresh the page to update the UI
    return qa


def main():
    st.set_page_config(page_title="RTFM Q&A", page_icon=":robot:")
    st.title("RTFM Q&A")

    display_sidebar()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "references" not in st.session_state:
        st.session_state.references = []

    if not st.session_state.get("qa"):
        st.warning("Required data not found. Downloading and preprocessing data...")
        st.session_state.qa = preprocess_data()

    display_chat_history(st.session_state.chat_history)

    question = display_question_input()
    if question:
        st.session_state.chat_history.append(("user", question))

        result = st.session_state.qa.invoke(
            {"question": question, "chat_history": st.session_state.chat_history}
        )
        response = result["answer"]
        references = result["source_documents"]
        st.session_state.chat_history.append(("assistant", response))
        st.session_state.references = references

        display_assistant_response(response)
        display_references(references)

        st.rerun()  # Refresh the page to update the UI


if __name__ == "__main__":
    main()
