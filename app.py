# app.py

import logging
import sys

import streamlit as st

from ui.ui import UI
from utils.qa_chain import QAChain

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Initialize QAChain and UI
qa_chain = QAChain()
ui = UI()


def load_data():
    try:
        qa_chain.load_data()
        st.session_state.data_loaded = True
        st.session_state.qa_chain = qa_chain.qa  # Store qa_chain.qa in session state
        st.success("Data loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        st.error(
            "An error occurred while loading the data. Please check the logs for more information."
        )


def process_question(question):
    try:
        qa = st.session_state.qa_chain  # Retrieve qa_chain from session state
        if qa is None:
            st.warning(
                "Data not loaded. Please click 'Load Data' before asking a question."
            )
            return None, ""
        else:
            result = qa(
                {"question": question, "chat_history": st.session_state.chat_history}
            )
            answer = result["answer"]
            references = result["source_documents"]

            return references, answer

    except Exception as e:
        logger.error(f"Error processing question: {e}")
        st.error("An error occurred while processing the question. Please try again.")
        return None, ""


def main():
    st.set_page_config(page_title="RTFM Q&A", page_icon=":robot:")
    st.title("RTFM Q&A")

    # Display sidebar
    ui.display_sidebar()

    # Load data when button is clicked
    if st.sidebar.button("Load Data"):
        load_data()

    # Display chat interface
    ui.display_chat_interface()

    question = st.chat_input("Ask a question about the Docs:", key="question_input")

    if question:
        st.session_state.chat_history.append(("user", question))
        ui.display_user_message(question)

        references, answer = process_question(question)

        if references is not None:
            st.session_state.chat_history.append(("assistant", answer))
            st.session_state.references = references
            ui.display_assistant_response(answer)
            st.rerun()  # Trigger a rerun of the app


if __name__ == "__main__":
    main()
