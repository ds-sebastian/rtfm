import streamlit as st

from utils.config import MODELS
from utils.settings import settings


def display_sidebar():
    if "references" not in st.session_state:
        st.session_state.references = []

    st.sidebar.header("ReadTheDocs")
    settings.readthedocs_url = st.sidebar.text_input(
        "ReadTheDocs URL", settings.readthedocs_url
    )
    if st.sidebar.button("Refresh"):
        pass

    st.sidebar.header("Settings")
    settings.model_name = st.sidebar.selectbox("Select Model", MODELS)

    with st.sidebar.expander("Preprocessing Settings"):
        settings.chunk_size = st.number_input(
            "Chunk Size", value=settings.chunk_size, min_value=1, step=1
        )
        settings.chunk_overlap = st.number_input(
            "Chunk Overlap", value=settings.chunk_overlap, min_value=0, step=1
        )
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

    with st.sidebar.popover("References"):
        for reference in st.session_state["references"]:
            source = reference.metadata["source"]
            page_content = reference.page_content

            st.caption(f"**{source}**")
            st.code(page_content)
