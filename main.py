import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.document_loader import load_and_split
from app.vector_store import add_documents, get_vectorstore
from app.rag_chain import build_qa_chain

app = FastAPI(title="RAG Doc QA API")

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename.split(".")[-1].lower()
    if ext not in {"pdf", "docx", "txt"}:
        raise HTTPException(400, "仅支持 pdf/docx/txt")

    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    chunks = load_and_split(save_path, ext)
    count = add_documents(chunks)
    return {"filename": filename, "chunks_indexed": count}

@app.post("/ask")
async def ask(question: str):
    vs = get_vectorstore()
    qa = build_qa_chain(vs)
    result = qa.invoke({"query": question})
    sources = [
        {
            "content": doc.page_content[:200],
            "source": doc.metadata.get("source", ""),
            "page": doc.metadata.get("page", None),
        }
        for doc in result["source_documents"]
    ]
    return {"answer": result["result"], "sources": sources}