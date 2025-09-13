from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    """
    Configuraciones centralizadas para la aplicación RAG.
    Carga las variables desde un archivo .env.
    """
    
    # --- Configuración de Gemini ---
    # La clave de API se carga automáticamente desde la variable GEMINI_API_KEY en el archivo .env
    gemini_api_key: Optional[str] = None
    
    # Modelos específicos de Gemini que estamos utilizando
    gemini_generation_model: str = "gemini-1.5-flash"
    gemini_embedding_model: str = "models/text-embedding-004"

    # --- Configuración del RAG ---
    # Fuentes de datos para la ingesta
    sources: List[str] = [
        "https://es.wikipedia.org/wiki/Argentina",
        "https://es.wikipedia.org/wiki/Historia_de_la_Argentina",
    ]
    
    # Parámetros de la recuperación de documentos
    top_k: int = 10  # Aumentamos a 10 como habíamos acordado
    max_context_chars: int = 8000

    # Configuración de Pydantic para que lea el archivo .env
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


# Se crea una instancia única de la configuración para ser usada en toda la aplicación
settings = Settings()