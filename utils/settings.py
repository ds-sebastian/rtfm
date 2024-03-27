# utils/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    data_loader: str = "readthedocs"
    vector_store: str = "pgvecto_rs"  # Add this line
    url_input: str = "https://docs.comma.ai/"
    chunk_size: int = 4000
    chunk_overlap: int = 0
    distance_metric: str = "cos"
    fetch_k: int = 100
    k: int = 4
    model_name: str = "gpt-3.5-turbo"
    qa_model: str = "openai"


settings = Settings()
