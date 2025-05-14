# app/search_documents.py

import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from app.config import OPENAI_API_KEY

VECTOR_DIR = "vectorstore"

def load_vectorstore():
    if not os.path.exists(VECTOR_DIR):
        raise FileNotFoundError("[!] No se encontró el vectorstore. Ejecutá generate_embeddings.py primero.")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return FAISS.load_local(VECTOR_DIR, embeddings)

def buscar_documentos_relevantes(pregunta, k=3):
    vectorstore = load_vectorstore()
    resultados = vectorstore.similarity_search(pregunta, k=k)
    return resultados
