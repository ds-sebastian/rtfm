# ui/ui.py

import streamlit as st

from utils.config import MODELS
from utils.settings import settings


class UI:
    def __init__(self):
        self.initialize_session_state()

    def initialize_session_state(self):
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "data_loaded" not in st.session_state:
            st.session_state.data_loaded = False
        if "references" not in st.session_state:
            st.session_state.references = []

    def display_sidebar(self):
        self.display_url_input()
        self.display_model_settings()
        self.display_preprocessing_settings()
        self.display_retriever_settings()
        self.display_references()

    def display_url_input(self):
        st.sidebar.header("ReadTheDocs")
        settings.url_input = st.sidebar.text_input(
            "ReadTheDocs URL", settings.url_input
        )
        if st.sidebar.button("Refresh"):
            pass

    def display_model_settings(self):
        st.sidebar.header("Settings")
        settings.model_name = st.sidebar.selectbox("Select Model", MODELS)

    def display_preprocessing_settings(self):
        with st.sidebar.expander("Preprocessing Settings"):
            settings.chunk_size = st.number_input(
                "Chunk Size", value=settings.chunk_size, min_value=1, step=1
            )
            settings.chunk_overlap = st.number_input(
                "Chunk Overlap", value=settings.chunk_overlap, min_value=0, step=1
            )

    def display_retriever_settings(self):
        with st.sidebar.expander("Retriever Settings"):
            settings.distance_metric = st.selectbox(
                "Distance Metric",
                ["cos", "l2"],
                index=["cos", "l2"].index(settings.distance_metric),
            )
            settings.fetch_k = st.number_input(
                "Fetch K", value=settings.fetch_k, min_value=1, step=1
            )
            settings.k = st.number_input("K", value=settings.k, min_value=1, step=1)

    def display_chat_interface(self):
        self.display_chat_history()

        question = st.chat_input("Ask a question about the Docs:", key="question_input")

        if question:
            st.session_state.chat_history.append(("user", question))

            if not st.session_state.data_loaded:
                st.warning("Please load the data first before attempting to chat.")
            else:
                response, references = st.session_state.qa_chain.process_question(
                    question, st.session_state.chat_history, st.session_state.qa_chain
                )
                st.session_state.chat_history.append(("assistant", response))
                st.session_state.references = references

    def display_chat_history(self):
        for message in st.session_state.chat_history:
            with st.chat_message(message[0]):
                st.markdown(message[1])

    def display_assistant_response(self, response):
        with st.chat_message("assistant"):
            st.markdown(response)

    def display_references(self):
        if not st.session_state.data_loaded:
            st.warning(
                "No context data has been set. Please load data to enable context-aware chatting."
            )
        else:
            with st.sidebar.expander("References"):
                for reference in st.session_state.references:
                    source = reference.metadata["source"]
                    page_content = reference.page_content
                    st.caption(f"**{source}**")
                    st.code(page_content)
