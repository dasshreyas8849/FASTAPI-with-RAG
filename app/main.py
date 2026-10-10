from fastapi import FastAPI
from routes.query import router as query_router

app=FastAPI(
    title="Rag API"
)

app.include_router(query_router)