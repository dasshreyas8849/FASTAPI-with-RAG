from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
load_dotenv()

pdf_path=Path(__file__).parent/ "data" / "sample.pdf"
loader=PyPDFLoader(str(pdf_path))
docs=loader.load()


text_Splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks=text_Splitter.split_documents(documents=docs)


embeddings=OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_Store=QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name='Sample collections',
    url="http://localhost:6333"
)

print("Vector store created and documents embedded successfully")