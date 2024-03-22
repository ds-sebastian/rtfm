import streamlit as st


def display_chat_history(chat_history):
    for message in chat_history:
        with st.chat_message(message[0]):
            st.markdown(message[1])


def display_question_input():
    question = st.chat_input("Ask a question about the Docs:")
    return question


def display_assistant_response(response):
    with st.chat_message("assistant"):
        st.markdown(response)


def display_references(references):
    with st.sidebar.popover("References"):
        for reference in references:
            source = reference.metadata["source"]
            page_content = reference.page_content

            st.caption(f"**{source}**")
            st.code(page_content)
