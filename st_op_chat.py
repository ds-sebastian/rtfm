import os
import shutil
import subprocess

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_community.vectorstores.pgvecto_rs import PGVecto_rs
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()  # temp

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
MODELS = os.getenv("MODELS").split(",")


embeddings = OpenAIEmbeddings(base_url=API_URL, api_key=API_KEY)


def initialize_state():
    """Initializes the Streamlit session state with default values."""
    state_defaults = {
        "references": [],
        "chat_history": [],
        "openai_model": MODELS[0],
        "chunk_size": 4000,
        "chunk_overlap": 0,
        "distance_metric": "cos",
        "fetch_k": 100,
        "k": 4,
        "readthedocs_url": "https://docs.comma.ai/",
    }
    for state_key, default_value in state_defaults.items():
        if state_key not in st.session_state:
            st.session_state[state_key] = default_value


def download_readthedocs(url, directory="rtdocs"):
    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.makedirs(directory)
    command = [
        "wget",
        "-r",  # Recursive download
        "-nd",  # no directories (save all files to one directory)
        "-np",  # no parent (don't ascend to the parent directory)
        "-P",
        directory,  # save files to rtdocs directory
        "-A.html",  # Accept only .html files
        url,  # The URL to download from
    ]

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f"Files were successfully downloaded to {directory}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def load_readthedocs(directory):
    loader = ReadTheDocsLoader(directory)
    return loader.load()


def split_documents(docs, chunk_size=4000, chunk_overlap=0):
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(docs)


def setup_retriever(texts):
    """Sets up the document retriever."""
    db = PGVecto_rs.from_documents(
        embedding=embeddings,
        documents=texts,
        collection_name="comma_chat_embed",
        db_url=CONNECTION_STRING,
    )
    retriever = db.as_retriever()
    # Config retriever with session state
    retriever.search_kwargs.update(
        {
            "distance_metric": st.session_state["distance_metric"],
            "fetch_k": st.session_state["fetch_k"],
            "k": st.session_state["k"],
        }
    )
    return retriever


def setup_qa_chain(_retriever, model_name=MODELS[0]):
    model = ChatOpenAI(model=model_name, base_url=API_URL, api_key=API_KEY)
    qa = ConversationalRetrievalChain.from_llm(
        model, retriever=_retriever, return_source_documents=True
    )
    return qa


def reset_session_data():
    """Resets the chat history and references in session state."""
    st.session_state.chat_history = []
    st.session_state.references = []


def preprocess_data():
    with st.status("Preprocessing Data..."):
        # Reset Session
        reset_session_data()

        st.write("Downloading documents from ReadTheDocs...")
        readthedocs_url = st.session_state["readthedocs_url"]
        download_readthedocs(readthedocs_url)

        st.write("Loading documents from ReadTheDocs...")
        readthedocs_dir = "rtdocs"
        readthedocs_docs = load_readthedocs(readthedocs_dir)

        st.write("Splitting documents...")
        chunk_size = st.session_state["chunk_size"]
        chunk_overlap = st.session_state["chunk_overlap"]
        texts = split_documents(readthedocs_docs, chunk_size, chunk_overlap)

        st.write("Setting up retriever...")
        retriever = setup_retriever(texts)

        st.write("Setting up QA chain...")
        qa = setup_qa_chain(retriever, st.session_state["openai_model"])

    st.sidebar.success("Preprocessing completed successfully!")
    st.rerun()  # Refresh the page to update the UI
    return qa


def main():
    st.set_page_config(page_title="RTFM Q&A", page_icon=":robot:")
    st.title("RTFM Q&A")

    initialize_state()

    # Sidebar - ReadTheDocs input
    st.sidebar.header("ReadTheDocs")
    st.session_state["readthedocs_url"] = st.sidebar.text_input(
        "ReadTheDocs URL", st.session_state["readthedocs_url"]
    )
    if st.sidebar.button("Refresh"):
        preprocess_data()
        st.rerun()  # Refresh the page to update the UI

    # Sidebar - Settings
    st.sidebar.header("Settings")
    selected_model = st.sidebar.selectbox("Select Model", MODELS)
    st.session_state["openai_model"] = selected_model
    with st.sidebar.expander("Preprocessing Settings"):
        chunk_size = st.number_input(
            "Chunk Size", value=st.session_state["chunk_size"], min_value=1
        )
        chunk_overlap = st.number_input(
            "Chunk Overlap", value=st.session_state["chunk_overlap"], min_value=0
        )
        st.session_state["chunk_size"] = chunk_size
        st.session_state["chunk_overlap"] = chunk_overlap
    with st.sidebar.expander("Retriever Settings"):
        distance_metric = st.selectbox(
            "Distance Metric",
            ["cos", "l2"],
            index=["cos", "l2"].index(st.session_state["distance_metric"]),
        )
        fetch_k = st.number_input(
            "Fetch K", value=st.session_state["fetch_k"], min_value=1
        )
        k = st.number_input("K", value=st.session_state["k"], min_value=1)
        st.session_state["distance_metric"] = distance_metric
        st.session_state["fetch_k"] = fetch_k
        st.session_state["k"] = k

    if not os.path.exists("rtdocs"):
        st.warning("Required data not found. Downloading and preprocessing data...")
        qa = preprocess_data()
    else:
        try:
            # Connect to existing vectorstore in database if exists
            connection_string = CONNECTION_STRING
            collection_name = "comma_chat_embed"
            db = PGVecto_rs.from_collection_name(
                embedding=embeddings,
                db_url=connection_string,
                collection_name=collection_name,
            )
            retriever = db.as_retriever()
            retriever.search_kwargs["distance_metric"] = st.session_state[
                "distance_metric"
            ]
            retriever.search_kwargs["fetch_k"] = st.session_state["fetch_k"]
            retriever.search_kwargs["k"] = st.session_state["k"]
            qa = setup_qa_chain(retriever, st.session_state["openai_model"])
        except Exception:
            st.warning("Vector database not found. Running preprocessing steps...")
            qa = preprocess_data()

    # Display chat messages from history
    for message in st.session_state.chat_history:
        with st.chat_message(message[0]):
            st.markdown(message[1])

    # Accept user input
    question = st.chat_input("Ask a question about the Docs:")
    if question:
        # Add user message to chat history
        st.session_state.chat_history.append(("user", question))

        # Display user message in chat container
        with st.chat_message("user"):
            st.markdown(question)

        # Display assistant response in chat container
        with st.chat_message("assistant"):
            # Generate response from OpenAI
            result = qa.invoke(
                {"question": question, "chat_history": st.session_state["chat_history"]}
            )
            response = result["answer"]
            references = result["source_documents"]
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state["chat_history"].append(("assistant", response))

        # Update references
        st.session_state["references"] = references

        st.rerun()  # Refresh the page to update the UI

    # Display the retrieved references in an expander
    with st.sidebar.popover("References"):
        for reference in st.session_state["references"]:
            source = reference.metadata["source"]
            page_content = reference.page_content

            st.caption(f"**{source}**")
            st.code(page_content)


if __name__ == "__main__":
    main()
