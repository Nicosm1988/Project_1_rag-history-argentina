from typing import Dict, Any

from .retriever import SimpleRetriever
from .generator import generate_answer, model  # <--- 1. Importamos el modelo de Gemini
from .settings import settings

# Se inicializa el retriever una sola vez cuando el módulo se carga.
retriever = SimpleRetriever()

def answer_question(question: str) -> Dict[str, Any]:
    """
    Orquesta el proceso de RAG: expande la pregunta, busca documentos y genera una respuesta.
    """
    # Creamos un prompt para que el LLM enriquezca la pregunta original.
    expansion_prompt = f"""Reescribe la siguiente pregunta de un usuario para que sea más efectiva en una búsqueda semántica dentro de una base de datos de documentos sobre la historia de Argentina. Enfócate en nombres, eventos y conceptos clave. Pregunta original: '{question}'"""
    
    # Usamos el modelo para generar la consulta expandida.
    try:
        expanded_query = model.generate_content(expansion_prompt).text.strip()
        print(f"Pregunta original: '{question}' -> Pregunta expandida: '{expanded_query}'") # Log para ver qué está pasando
    except Exception as e:
        print(f"Error en la expansión de la consulta, usando la original. Error: {e}")
        expanded_query = question

    # 1. Usar la PREGUNTA EXPANDIDA para obtener los documentos relevantes.
    k = settings.top_k or 10
    retrieved_docs = retriever.search(expanded_query, k=k)

    # 2. Pasar la PREGUNTA ORIGINAL y los documentos al generador.
    #    Es importante usar la pregunta original aquí para que la respuesta final sea directa.
    return generate_answer(question, retrieved_docs)