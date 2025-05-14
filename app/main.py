import os
import streamlit as st

from search_docs import buscar_documentos_relevantes
from generate_response import generar_respuesta_con_llm
from generate_embeddings import create_vectorstore, load_documents

st.set_page_config(page_title="🧠 LLM Categorizer Demo", layout="centered")

st.title("🧱 LLM Categorizer Demo")
st.write("Esta demo utiliza Gemini para generar respuestas a partir de documentos cargados.")

VECTOR_DIR = "vectorstore"

# Si no existe el índice FAISS, lo genera automáticamente
if not os.path.exists(VECTOR_DIR):
    st.warning("⚠️ No se encontró el índice FAISS. Generándolo automáticamente...")
    docs = load_documents()
    if docs:
        create_vectorstore(docs)
        st.success("✅ Índice generado con éxito.")
    else:
        st.error("❌ No se encontraron documentos en /data/documentos_raw/.")

# Input del usuario
pregunta = st.text_input("🔍 Ingresá tu consulta:")

if pregunta:
    with st.spinner("🔎 Buscando documentos relevantes..."):
        fragmentos = buscar_documentos_relevantes(pregunta)

    st.subheader("📄 Fragmentos relevantes encontrados:")
    for i, doc in enumerate(fragmentos, 1):
        st.markdown(f"**Fragmento #{i}:**")
        st.info(doc.page_content)

    with st.spinner("✍️ Generando respuesta..."):
        respuesta = generar_respuesta_con_llm(pregunta, fragmentos, modelo="gemini")

    st.subheader("📌 Respuesta generada:")
    st.success(respuesta)
