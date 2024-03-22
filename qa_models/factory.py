from utils.settings import settings

from .openai import OpenAIModel


def get_qa_model():
    if settings.qa_model == "openai":
        return OpenAIModel()
    else:
        raise ValueError(f"Unsupported QA model: {settings.qa_model}")
