# app/main.py

import streamlit as st
from app.search_documents import buscar_documentos_relevantes
from app.generate_response import generar_respuesta_con_llm

st.set_page_config(page_title="🧠 LLM Categorizer Demo", layout="centered")

st.title("🧱 LLM Categorizer Demo")
st.write("Esta demo utiliza el modelo Gemini Pro para generar respuestas basadas en documentos.")

pregunta = st.text_input("🔍 Ingresá tu consulta:")

if pregunta:
    with st.spinner("🔎 Buscando documentos relevantes..."):
        fragmentos = buscar_documentos_relevantes(pregunta)

    st.subheader("📄 Fragmentos relevantes encontrados:")
    for i, doc in enumerate(fragmentos, 1):
        st.markdown(f"**Fragmento #{i}:**")
        st.info(doc.page_content)

    with st.spinner("✍️ Generando respuesta con Gemini..."):
        respuesta = generar_respuesta_con_llm(pregunta, fragmentos, modelo="gemini")

    st.subheader("📌 Respuesta generada:")
    st.success(respuesta)