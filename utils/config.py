# utils/config.py
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
MODELS = (
    os.getenv("MODELS").split(",") if os.getenv("MODELS") else []
)  # Modify this line
