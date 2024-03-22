from utils.settings import settings

from .readthedocs import ReadTheDocsLoader


def get_data_loader():
    if settings.data_loader == "readthedocs":
        return ReadTheDocsLoader(settings.readthedocs_url)
    else:
        raise ValueError(f"Unsupported data loader: {settings.data_loader}")
