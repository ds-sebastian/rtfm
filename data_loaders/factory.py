from utils.settings import settings

from .readthedocs import RTD_Loader


def get_data_loader():
    if settings.data_loader == "readthedocs":
        return RTD_Loader(settings.url_input)
    else:
        raise ValueError(f"Unsupported data loader: {settings.data_loader}")
