# RTFM - RAG This For Me

RTFM is a modular web application that uses Retrieval Augmented Generation (RAG) to enable interactive question-answering based on a given data source. The app alleows users to provide a link to a data source (such as a ReadTheDocs website or a GitHub repository), which is then loaded into a vector database for efficient similarity search. Users can ask questions related to the loaded data, and the app retrieves relevant references from the vector database and sends them to a configured language model (LLM) to generate informative answers.



<img width="1425" alt="image" src="https://github.com/ds-sebastian/rtfm/assets/69488704/45142619-aaf9-47e7-83e5-8240c7ecd19d">



## Features

- Modular architecture allowing easy integration of different databases, models, and data loaders through plugin-style `.py` files
- Supports various data sources, including ReadTheDocs websites and GitHub repositories
- Utilizes vector databases for efficient similarity search and retrieval of relevant references
- Integrates with powerful language models to generate informative answers based on retrieved references
- User-friendly web interface built with Streamlit for easy interaction and configuration

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/rtfm-qa-app.git
cd rtfm-qa-app
```

2. Create a new conda environment using the provided `environment.yml` file:

```
conda env create -f environment.yml
```

3. Activate the conda environment:

```
conda activate rtfm-qa-app
```

4. Set the required environment variables:

```
export API_KEY=your_api_key
export API_URL=your_api_url
export CONNECTION_STRING=your_database_connection_string
export MODELS=model1,model2,model3
```

5. Run the app:

```
streamlit run app.py
```

## Usage

1. Open the app in your web browser (usually at `http://localhost:8501`).

2. In the sidebar, enter the URL of the data source you want to load (e.g., a ReadTheDocs website or a GitHub repository).

3. Click the "Load Data" button to fetch and process the data from the specified source. The data will be loaded into the vector database.

4. Once the data is loaded, you can start asking questions related to the loaded data in the chat interface.

5. The app will retrieve relevant references from the vector database based on your question and send them to the configured LLM to generate an informative answer.

6. The answer, along with the retrieved references, will be displayed in the chat interface.

## Configuration

The app's behavior can be configured through the settings in the sidebar:

- **Select Model**: Choose the language model to use for generating answers.
- **Preprocessing Settings**: Adjust the chunk size and overlap for splitting the loaded data into smaller segments.
- **Retriever Settings**: Configure the distance metric, fetch count, and number of references to retrieve from the vector database.

## Customization

To extend or customize the app, you can add new data loaders, vector databases, or language models by creating the appropriate `.py` files in the corresponding directories:

- **Data Loaders**: Add new data loaders in the `data_loaders` directory.
- **Vector Databases**: Add new vector databases in the `vector_stores` directory.
- **Language Models**: Add new language models in the `qa_models` directory.

Make sure to follow the existing structure and inherit from the respective base classes to ensure compatibility with the app's modular architecture.
