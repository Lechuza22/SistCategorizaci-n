# app/generate_embeddings.py

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.document_loaders import TextLoader, PyPDFLoader

DATA_DIR = "data/documentos_raw"
VECTOR_DIR = "vectorstore"

def load_documents():
    documents = []
    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(path)
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            print(f"[!] Formato no compatible: {filename}")
            continue
        docs = loader.load()
        documents.extend(docs)
    return documents

def create_vectorstore(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    try:
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", model_kwargs={"device": "cpu"})
    except ImportError as e:
        raise ImportError(
            "[!] No se pudo cargar HuggingFaceEmbeddings. Asegurate de tener 'sentence-transformers' instalado correctamente."
        ) from e

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DIR)
    print(f"[✓] Vectorstore guardado en '{VECTOR_DIR}'")

if __name__ == "__main__":
    docs = load_documents()
    if docs:
        create_vectorstore(docs)
    else:
        print("[!] No se encontraron documentos válidos.")
