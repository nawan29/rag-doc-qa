import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split(file_path: str, file_type: str):
    file_type = file_type.lower()
    if file_type == "pdf":
        loader = PyPDFLoader(file_path)
    elif file_type == "docx":
        loader = Docx2txtLoader(file_path)
    elif file_type == "txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"不支持的文件类型: {file_type}")

    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", "。", " ", ""]
    )
    return splitter.split_documents(docs)