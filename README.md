# README for RTFM Q&A Streamlit Application

## Overview
The RTFM Q&A Streamlit application is a conversational question-answering (QA) system designed to fetch, preprocess, and utilize documentation from ReadTheDocs websites for generating answers. It leverages the power of OpenAI's language models and document retrieval techniques to provide users with accurate and contextually relevant answers based on the provided documentation.

## Features
- **Dynamic Documentation Loading**: Allows users to specify the URL of a ReadTheDocs website from which the documentation is downloaded and processed.
- **Configurable Preprocessing**: Includes settings for chunk size and chunk overlap to customize how documents are split into manageable pieces.
- **Advanced Retrieval System**: Utilizes a Postgres-based vector search engine (PGVecto_rs) for efficient document retrieval based on query similarity.
- **Interactive Q&A Interface**: Offers a user-friendly chat interface for asking questions and receiving answers, complete with references to the source documentation.

## Installation

### Prerequisites
- Python 3.8+
- Pipenv or virtualenv (recommended for managing dependencies)
- Access to an OpenAI API key
- A PostgreSQL database for storing document vectors

### Steps
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Setup a virtual environment** (optional, but recommended):
   - With virtualenv:
     ```
     python -m venv venv
     source venv/bin/activate
     ```
   - With Pipenv:
     ```
     pipenv shell
     ```

3. **Install dependencies**:
   - With pip:
     ```
     pip install -r requirements.txt
     ```
   - With Pipenv:
     ```
     pipenv install
     ```

4. **Environment Variables**: Create a `.env` file in the root directory with the following variables:
   ```
   API_KEY=<Your OpenAI API Key>
   API_URL=<OpenAI API URL>
   CONNECTION_STRING=<PostgreSQL Connection String>
   MODELS=<Comma-separated list of model names>
   ```
   
5. **Initialize the Database**: Ensure your PostgreSQL database is running and accessible through the `CONNECTION_STRING` specified in the `.env` file.

## Usage

1. **Start the Streamlit application**:
   ```
   streamlit run script.py
   ```

2. **Interact with the Application**:
   - The sidebar allows you to enter the URL of a ReadTheDocs website, select the model, and adjust preprocessing and retriever settings.
   - Click the "Refresh" button in the sidebar after changing the ReadTheDocs URL or settings to reprocess the documentation.
   - Use the chat input box at the bottom to ask questions and receive answers based on the loaded documentation.

## Key Functions

- `download_readthedocs(url, directory)`: Downloads HTML files from a specified ReadTheDocs URL.
- `load_readthedocs(directory)`: Loads and parses the downloaded HTML files.
- `split_documents(docs, chunk_size, chunk_overlap)`: Splits documents into chunks based on the specified size and overlap.
- `setup_retriever(texts)`: Initializes the document retriever with the processed texts.
- `setup_qa_chain(_retriever, model_name)`: Sets up the QA chain with the given language model and retriever.
- `preprocess_data()`: Orchestrates the downloading, loading, splitting, and retrieval setup processes.

