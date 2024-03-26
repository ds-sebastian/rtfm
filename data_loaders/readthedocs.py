# data_loaders/readthedocs.py
import os
import shutil
import subprocess

from langchain_community.document_loaders import ReadTheDocsLoader

from .base import BaseLoader


class RTD_Loader(BaseLoader):
    def __init__(self, url):
        self.url = url

    def load_data(self, directory="data"):
        # if os.path.exists(directory):
        #     shutil.rmtree(directory)

        # os.makedirs(directory)
        # command = [
        #     "wget",
        #     "-r",  # Recursive download
        #     "-nd",  # No directories (save all files to one directory)
        #     "-np",  # No parent (don't ascend to the parent directory)
        #     "-P",
        #     directory,  # Save files to the specified directory
        #     "-A.html",  # Accept only .html files
        #     self.url,  # The URL to download from
        # ]

        # try:
        #     subprocess.run(command, check=True)
        #     print(f"Files were successfully downloaded to {directory}.")
        # except subprocess.CalledProcessError as e:
        #     print(f"Error occurred while downloading files: {e}")
        #     print(f"Command: {' '.join(command)}")
        #     print(f"Error code: {e.returncode}")
        #     print(f"Error output: {e.output}")
        #     pass
        # except Exception as e:
        #     print(f"An unexpected error occurred: {e}")
        #     pass

        # Load the downloaded HTML files and create a list of documents
        loader = ReadTheDocsLoader(directory)
        documents = loader.load()

        return documents
