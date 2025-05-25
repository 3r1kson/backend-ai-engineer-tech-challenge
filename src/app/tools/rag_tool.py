# python
from pathlib import Path
from typing import List, Optional, Dict
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

_vector_store = None

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def create_vector_store() -> FAISS:
    global _vector_store
    if _vector_store is not None:
        return _vector_store

    kb_path = Path(__file__).parent / "../data/knowledge_base.txt"
    kb_path = kb_path.resolve()

    print(f"- Loading knowledge base from absolute path: {kb_path}")

    loader = TextLoader(str(kb_path))
    try:
        documents = loader.load()
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load knowledge base: {e}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    _vector_store = FAISS.from_documents(docs, embeddings)
    return _vector_store

def query_knowledge_base(query: str, filters: Optional[Dict] = None) -> List[str]:
    store = create_vector_store()
    results = store.similarity_search(query, k=3)
    return [doc.page_content for doc in results]
