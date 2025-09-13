# app/generator.py

from typing import List, Dict, Any
import google.generativeai as genai

from .settings import settings

# --- Configuración del cliente de Gemini ---
genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


# --- Funciones auxiliares para el generador ---

def _build_context(chunks: List[Dict[str, Any]], max_len: int = 8000) -> str:
    """
    Construye el string de contexto para el prompt a partir de los chunks recuperados.
    """
    context_str = ""
    for i, ch in enumerate(chunks):
        piece = f"[{i}] {ch['text'].strip()}"
        if len(context_str) + len(piece) + 2 < max_len:
            context_str += piece + "\n\n"
        else:
            break
    return context_str


def _format_citations(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Formatea las citas a partir de los chunks usados en el contexto.
    """
    citations = []
    for i, ch in enumerate(chunks):
        citation = {
            "id": ch.get("id") or f"doc-{i}",
            "source": ch.get("source"),
        }
        citations.append(citation)
    return citations


def _build_prompt(question: str, context: str) -> str:
    """
    Construye el prompt final para el modelo de lenguaje.
    """
    # --- PROMPT PROFESIONALIZADO ---
    return f"""Actúa como un Profesor de Historia de la Universidad de Buenos Aires con más de 30 años de experiencia en la cátedra. Tu tono debe ser académico, preciso y didáctico. Utiliza un español formal y característico de Argentina.

Tu misión es responder la pregunta del estudiante basándote EXCLUSIVAMENTE en el contexto documental que te proporciono a continuación. No debes usar ningún conocimiento externo.

**Instrucciones precisas:**
1.  **Analizá la pregunta:** Comprendé con exactitud qué es lo que el estudiante quiere saber.
2.  **Basate en la evidencia:** Leé cuidadosamente los fragmentos de texto del contexto y sintetizá la información para construir tu respuesta.
3.  **Cita tus fuentes:** Es fundamental que cites cada afirmación que hagas. Al final de una oración o párrafo que se base en un fragmento, añadí la cita correspondiente, por ejemplo: [0], [1], etc.
4.  **Si la respuesta no está en los textos:** Sé honesto y académico. Respondé con una frase como: "A partir de la documentación consultada, no es posible responder con precisión a su pregunta." o "Los textos proporcionados no contienen información específica sobre ese punto." No inventes ni deduzcas información.
5.  **Mantené la personalidad:** Redactá la respuesta con la cadencia y el vocabulario de un profesor experimentado. Podés empezar con frases como "Efectivamente, como usted consulta...", "Es una pregunta interesante. Según los documentos..." o "Analicemos lo que nos dicen las fuentes...".

**Contexto Documental:**
{context}

**Pregunta del Estudiante:** {question}

**Respuesta del Profesor:**
"""

# --- Función principal de generación ---

def generate_answer(question: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Genera una respuesta usando el LLM a partir de la pregunta y los chunks recuperados.
    """
    if not retrieved_chunks:
        return {"answer": "Tras revisar los archivos, no se encontró material pertinente para elaborar una respuesta.", "citations": []}

    if sum(len(x["text"]) for x in retrieved_chunks) < 200:
        return {"answer": "La información encontrada en los documentos es demasiado fragmentaria para construir una respuesta académica sólida.", "citations": []}

    context = _build_context(retrieved_chunks, 8000)
    prompt = _build_prompt(question, context)

    try:
        response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        print(f"Error al llamar a la API de Gemini: {e}")
        answer = "Hubo una dificultad técnica al consultar los archivos. Por favor, intente nuevamente."

    citations = _format_citations(retrieved_chunks)
    return {"answer": answer, "citations": citations}