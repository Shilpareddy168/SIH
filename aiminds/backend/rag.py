"""RAG: extract text -> chunk -> embed into a vector DB (ChromaDB) -> retrieve relevant chunks."""
import io
import chromadb
from pypdf import PdfReader

col = chromadb.PersistentClient(path="./chroma").get_or_create_collection("materials")

def extract_text(data: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
    return data.decode("utf-8", errors="ignore")

def chunk(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    step = size - overlap
    return [text[i:i + size] for i in range(0, len(text), step) if text[i:i + size].strip()]

def index(user: str, doc: str, text: str) -> int:
    chunks = chunk(text)
    if chunks:
        col.add(ids=[f"{user}:{doc}:{i}" for i in range(len(chunks))], documents=chunks,
                metadatas=[{"user": user, "doc": doc}] * len(chunks))
    return len(chunks)

def retrieve(user: str, query: str, k: int = 6) -> list[str]:
    res = col.query(query_texts=[query], n_results=k, where={"user": user})
    return res["documents"][0] if res["documents"] else []
