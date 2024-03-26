import logging
import sys

import streamlit as st

from ui.chat import (
    display_assistant_response,
    display_chat_history,
    display_question_input,
)
from ui.sidebar import display_sidebar
from utils.qa_chain import preprocess_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main():
    st.set_page_config(page_title="RTFM Q&A", page_icon=":robot:")
    st.title("RTFM Q&A")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    display_sidebar()

    if st.sidebar.button("Load Data"):
        st.session_state.qa = preprocess_data()
        st.session_state.data_loaded = True

    display_chat_history(st.session_state.chat_history)

    question = display_question_input()
    if question:
        if "qa" not in st.session_state:
            st.warning("Please load the data first before attempting to chat.")
        else:
            st.session_state.chat_history.append(("user", question))

            logger.info(f"User question: {question}")
            result = st.session_state.qa.invoke(
                {"question": question, "chat_history": st.session_state.chat_history}
            )

            response = result["answer"]
            st.session_state.chat_history.append(("assistant", response))

            if not st.session_state.get("data_loaded"):
                st.warning(
                    "No context data has been set. Please load data to enable context-aware chatting."
                )
            else:
                references = result.get("source_documents", [])
                st.session_state.references = references

            logger.info(f"Assistant response: {response}")
            display_assistant_response(response)


if __name__ == "__main__":
    main()
