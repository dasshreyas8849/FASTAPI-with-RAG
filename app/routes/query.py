from fastapi import APIRouter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os
from openai import OpenAI

router= APIRouter(
    prefix="/query",
    tags=["Query"]
)

OpenAI_client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embeddings=OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db=QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name='Sample collections',
    url="http://localhost:6333"
)

@router.post("/")
async def query(question:str):
    search_results=vector_db.similarity_search(query=question)
    print(f"Search results for question '{question}':{search_results}")
    context=" ".join([result.page_content for result in search_results])
    SYSTEM_PROMPT=f"""
    You are a helpful assistant that answers questions based on the context provided. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    {context}
    """

    response = OpenAI_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":question}
        ]
    )
    return {"question":question,"answer":response.choices[0].message.content}