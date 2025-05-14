# app/generate_response.py

import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key="AIzaSyDN-qxuXqr6wt1Ca5P2h7PjCw__KK2E9os")

def construir_prompt(pregunta, fragmentos):
    contexto = "\n\n".join([f"- {doc.page_content}" for doc in fragmentos])
    prompt = f"""Basado en los siguientes documentos:

{contexto}

Respondé con precisión a la siguiente pregunta:
{pregunta}
"""
    return prompt

def generar_respuesta_con_gemini(pregunta, fragmentos):
    prompt = construir_prompt(pregunta, fragmentos)
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt)
    return response.text.strip()







