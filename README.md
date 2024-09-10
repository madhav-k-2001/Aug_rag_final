Misinformation Detector with RAG-based Approach
This project is a Misinformation Detection Bot built using a Retrieval-Augmented Generation (RAG) approach. The system is designed to retrieve and rank contextually relevant information from a PostgreSQL database, embedding vectors, and large language models (LLMs). It uses Streamlit as a user interface, HuggingFace, Cohere, and Groq LLM APIs for embeddings and LLM responses.

Features
RAG-based Approach: Combines retrieval of factual information with a generative model to detect and respond to potential misinformation.
Embeddings: Uses sentence embeddings to represent queries and documents in vector space.
Retrieval: Uses PostgreSQL's pgvector extension for efficient similarity search.
LLM-based Answers: Integrates Groq LLM to generate intelligent responses based on retrieved information.
History-aware Retrieval: Incorporates past interactions for contextually aware conversations.
Customizable Prompts: Utilizes custom system and human prompts to guide the bot’s behavior.
Scalable: Supports PostgreSQL for storing large datasets and optimized embeddings for fast retrieval.

Technologies Used
LangChain: Modular framework for LLM applications.
Sentence Transformers: For embedding and similarity search.
PostgreSQL + pgvector: Vectorized database storage for embedding-based retrieval.
Groq: For LLM-based conversational AI.
Streamlit: Provides the frontend interface for interacting with the bot.
HuggingFace: Provides embeddings and cross-encoder rerankers.
Cohere: Optionally supports embeddings and reranking.
Project Structure

.
├── config_pg.py          # Contains PostgreSQL configuration details
├── main.py               # Main application script
├── .env                  # Stores environment variables like DB connection string
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies

Setup Instructions

Prerequisites
Python 3.8+
PostgreSQL with pgvector extension enabled
API keys for Groq, HuggingFace, Cohere, and other external services
Installation
Clone the repository:

git clone repo

cd misinfo-detector

Create and activate a Python virtual environment:

python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt


Set up the .env file for storing environment variables. This file should include:

makefile
Copy code
PG_CONN_PARAMS={"dbname": "your_db", "user": "postgres", "password": "password", "host": "localhost", "port": "5432"}
CONNECTION_STRING=postgresql://user:password@host:port/dbname
GROQ_API_KEY=your_groq_api_key
Ensure that PostgreSQL has the pgvector extension installed:

CREATE EXTENSION IF NOT EXISTS vector;
Running the Application
Run the bot using Streamlit:

streamlit run main.py
Environment Variables
The following environment variables must be set in the .env file:

PG_CONN_PARAMS: JSON string with PostgreSQL connection parameters.
CONNECTION_STRING: Connection string for PostgreSQL.
GROQ_API_KEY: API key for the Groq model.

Configuration
Prompts: You can define custom system and human prompts in config_pg.py to guide the bot’s behavior.
Retrieval: Set similarity search parameters and embeddings through config_pg.py and main.py.
Usage
Once the app is running, you can query the misinformation detector through the Streamlit interface. The bot will use embeddings to retrieve relevant information and the LLM to generate a final response.

Key Components
EduBotCreator Class
The main class in the project responsible for:

Creating chat prompts (create_chat_prompt_1, create_chat_prompt_2).
Embedding model setup (create_embedding_model_instance).
Retriever function to query PostgreSQL for relevant documents (own_retriever).
Chat history formatting (format_chat_history).
Integration with LLMs such as Groq and retrieval models like HuggingFace and Cohere.
Functions
create_chat_prompt_1 & create_chat_prompt_2: Defines the templates for the prompts.
get_embedding: Encodes user input into an embedding vector.
own_retriever: Queries the database for relevant content based on embeddings.
create_bot: Creates the full RAG chain that combines retrieval and generation.
load_llm: Loads the chosen LLM model (e.g., Groq).
load_vectorstore: Initializes the vector store using pgvector.
Data Storage

PostgreSQL: Stores embeddings and documents for efficient retrieval.
pgvector: Extension for storing and querying vectorized embeddings.

Customization
You can modify the following to suit your use case:

Models: Swap out HuggingFace or Groq models for others.
Prompts: Customize how the system and human prompts are structured.
Retrieval Parameters: Adjust similarity thresholds and embedding models.


License
This project is licensed under the MIT License.

