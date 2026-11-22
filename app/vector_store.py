import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import settings

def _get_embeddings():
    return OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-v3"),
        api_key=os.getenv("EMBEDDING_API_KEY"),
        base_url=os.getenv("EMBEDDING_BASE_URL"),
        check_embedding_ctx_length=False,
        chunk_size=10, 
    )

def get_vectorstore(collection_name: str = "docs"):
    return Chroma(
        collection_name=collection_name,
        persist_directory=settings.CHROMA_PERSIST_DIR,
        embedding_function=_get_embeddings(),
    )

def add_documents(chunks, collection_name: str = "docs"):
    vs = get_vectorstore(collection_name)
    vs.add_documents(chunks)
    return len(chunks)
