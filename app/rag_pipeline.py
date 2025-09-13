from typing import Dict, Any

from .retriever import SimpleRetriever
from .generator import generate_answer, model
from .settings import settings

# Se inicializa el retriever una sola vez cuando el módulo se carga.
retriever = SimpleRetriever()

def _clean_expanded_query(raw_query: str) -> str:
    """
    Limpia la respuesta del LLM para extraer solo la primera consulta sugerida.
    """
    # Busca la primera línea que contenga un asterisco '*'
    lines = raw_query.splitlines()
    first_option_line = next((line for line in lines if '*' in line), None)
    
    if first_option_line:
        # Extrae el texto después del asterisco y lo limpia
        return first_option_line.split('*', 1)[-1].strip().replace('"', '')
    else:
        # Si no encuentra un formato esperado, devuelve la respuesta original limpia
        return raw_query.strip().replace('"', '')


def answer_question(question: str) -> Dict[str, Any]:
    """
    Orquesta el proceso de RAG: expande la pregunta, busca documentos y genera una respuesta.
    """
    # --- PASO DE EXPANSIÓN DE LA CONSULTA ---
    expansion_prompt = f"""Reescribe la siguiente pregunta para una búsqueda semántica más efectiva en una base de datos de documentos sobre la historia de Argentina. Enfócate en nombres, eventos y conceptos clave. Devuelve solo una línea con la consulta mejorada. Pregunta original: '{question}'"""
    
    try:
        raw_expanded_query = model.generate_content(expansion_prompt).text
        # Limpiamos la respuesta del LLM para obtener solo la consulta útil
        expanded_query = _clean_expanded_query(raw_expanded_query)
        print(f"Pregunta original: '{question}' -> Pregunta expandida para búsqueda: '{expanded_query}'")
    except Exception as e:
        print(f"Error en la expansión de la consulta, usando la original. Error: {e}")
        expanded_query = question

    # 1. Usar la PREGUNTA EXPANDIDA Y LIMPIA para obtener los documentos relevantes.
    k = settings.top_k or 10
    retrieved_docs = retriever.search(expanded_query, k=k)

    # 2. Pasar la PREGUNTA ORIGINAL y los documentos al generador.
    return generate_answer(question, retrieved_docs)