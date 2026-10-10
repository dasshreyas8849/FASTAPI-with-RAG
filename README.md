# FastAPI RAG API


A Retrieval-Augmented Generation (RAG) API built with FastAPI, LangChain, Qdrant, and OpenAI.

The application processes a PDF document, splits it into smaller chunks, generates vector embeddings, stores those embeddings in Qdrant, and uses semantic similarity search to retrieve relevant information when answering user questions.

## Architecture

PDF File
    |
    v
PDF Loader
    |
    v
Text Splitter
    |
    v
OpenAI Embeddings
    |
    v
Qdrant Vector Database
    |
    | Similarity Search
    v
FastAPI Query Endpoint
    |
    v
GPT-5
    |
    v
Generated Answer

## Features

- PDF document loading and processing
- Recursive text chunking
- OpenAI vector embeddings
- Qdrant vector database
- Semantic similarity search
- Context-aware LLM responses
- FastAPI REST API
- Docker Compose setup for Qdrant
- Environment-variable based API key configuration

## Tech Stack

- Python
- FastAPI
- LangChain
- OpenAI
- Qdrant
- Docker
- PyPDF

## Project Structure

FASTAPI-with-RAG/
|
├── app/
│   ├── data/
│   │   └── sample.pdf
│   │
│   ├── routes/
│   │   └── query.py
│   │
│   ├── index.py
│   └── main.py
│
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md

## Main Files

### app/index.py

Responsible for creating the vector database.

The process is:

1. Load sample.pdf.
2. Split the document into smaller chunks.
3. Generate OpenAI embeddings for the chunks.
4. Store the embeddings in Qdrant.

The project uses:

- Chunk size: 1000 characters
- Chunk overlap: 400 characters
- Embedding model: text-embedding-3-large

### app/routes/query.py

Contains the `/query/` API endpoint.

The endpoint:

1. Receives a user question.
2. Performs a similarity search against Qdrant.
3. Retrieves relevant document chunks.
4. Combines the retrieved chunks into context.
5. Sends the context and question to GPT-5.
6. Returns the generated answer.

### app/main.py

Creates the FastAPI application and registers the query router.

### docker-compose.yml

Used to run Qdrant locally through Docker Compose.

Qdrant is exposed on port 6333.

## Setup

### 1. Clone the repository

git clone <your-repository-url>
cd FASTAPI-with-RAG

### 2. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\Activate.ps1

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure the OpenAI API key

Create a `.env` file in the project root:

OPENAI_API_KEY=your_openai_api_key

Do not commit the `.env` file to Git.

The repository's `.gitignore` is configured to ignore environment files.

### 5. Start Qdrant

Make sure Docker Desktop is running, then execute:

docker compose up -d

Check that Qdrant is running:

docker ps

Qdrant should be available at:

http://localhost:6333

### 6. Create the vector store

Run:

python app/index.py

This loads the PDF, creates document chunks, generates embeddings, and stores them in Qdrant.

### 7. Start the FastAPI server

Run:

fastapi dev app/main.py

The API will be available at:

http://127.0.0.1:8000

Interactive Swagger documentation:

http://127.0.0.1:8000/docs

## API Usage

### Query Endpoint

POST /query/

The endpoint accepts a question and searches the Qdrant vector database for relevant document chunks.

Example:

POST http://127.0.0.1:8000/query/?question=What%20is%20this%20document%20about?

Example response:

{
    "question": "What is this document about?",
    "answer": "The document discusses..."
}

You can also test the endpoint through the Swagger UI:

http://127.0.0.1:8000/docs

## How the RAG Pipeline Works

### 1. Document Ingestion

The PDF is loaded and converted into documents.

### 2. Text Chunking

The document is divided into smaller overlapping chunks.

The current configuration uses a chunk size of 1000 characters and an overlap of 400 characters.

The overlap helps preserve context between neighboring chunks.

### 3. Embedding Generation

Each chunk is converted into a vector representation using OpenAI's:

text-embedding-3-large

### 4. Vector Storage

The generated vectors are stored in Qdrant.

PDF -> Chunks -> Embeddings -> Qdrant

### 5. Retrieval

When a user asks a question, the system performs a similarity search against the stored vectors and retrieves the most relevant document chunks.

Question -> Similarity Search -> Relevant Chunks

### 6. Generation

The retrieved chunks are passed to GPT-5 as context together with the user's question.

Question + Retrieved Context -> GPT-5 -> Answer

This is the core Retrieval-Augmented Generation workflow.

## Running the Project

A typical development session requires Qdrant and the FastAPI application to be running.

Terminal 1:

docker compose up -d

Terminal 2:

python app/index.py

Terminal 3:

fastapi dev app/main.py

Then open:

http://127.0.0.1:8000/docs

## Environment Variables

Create a `.env` file:

OPENAI_API_KEY=your_openai_api_key

Never commit this file to GitHub.

If an API key is accidentally exposed, revoke the exposed key and generate a new one.

## Future Improvements

Possible improvements include:

- Support for multiple PDF documents
- File upload endpoint
- Conversation history
- Streaming LLM responses
- Improved prompt templates
- Configurable chunk size
- Configurable number of retrieved documents
- Metadata filtering in Qdrant
- Persistent Qdrant storage
- Authentication and authorization
- Dockerizing the FastAPI application
- Production deployment
- Frontend chat interface
- Chat history and session management

## Security

API keys and other secrets should always be stored in environment variables.

Never hardcode an OpenAI API key in the source code.

Never commit `.env` files or other files containing secrets.

If a secret is accidentally pushed to a public or protected Git repository, revoke it immediately and replace it with a new key.

## License

This project is intended for educational and development purposes.
