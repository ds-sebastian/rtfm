# ui/sidebar.py
import streamlit as st

from utils.config import MODELS
from utils.settings import settings


def display_sidebar():
    st.sidebar.header("ReadTheDocs")
    settings.readthedocs_url = st.sidebar.text_input(
        "ReadTheDocs URL", settings.readthedocs_url
    )
    if st.sidebar.button("Refresh"):
        # Trigger data preprocessing and refresh the page
        pass

    st.sidebar.header("Settings")
    settings.openai_model = st.sidebar.selectbox(
        "Select Model", MODELS
    )  # Use MODELS from config
    with st.sidebar.expander("Preprocessing Settings"):
        settings.chunk_size = st.number_input(
            "Chunk Size", value=settings.chunk_size, min_value=1
        )
        settings.chunk_overlap = st.number_input(
            "Chunk Overlap", value=settings.chunk_overlap, min_value=0
        )
    with st.sidebar.expander("Retriever Settings"):
        settings.distance_metric = st.selectbox(
            "Distance Metric",
            ["cos", "l2"],
            index=["cos", "l2"].index(settings.distance_metric),
        )
        settings.fetch_k = st.number_input(
            "Fetch K", value=settings.fetch_k, min_value=1
        )
        settings.k = st.number_input("K", value=settings.k, min_value=1)
