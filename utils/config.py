# config.py
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("API_KEY environment variable is missing")

API_URL = os.getenv("API_URL")
if API_URL is None:
    raise ValueError("API_URL environment variable is missing")

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
if CONNECTION_STRING is None:
    raise ValueError("CONNECTION_STRING environment variable is missing")

MODELS = os.getenv("MODELS")
if MODELS is None:
    raise ValueError("MODELS environment variable is missing")
else:
    MODELS = MODELS.split(",")
