import json
import os
from typing import Callable, List, Dict, Any, Tuple
import numpy as np
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from .settings import settings


# Helpers de red y parsing HTML
def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # limpieza básica
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)


def chunk_text(text: str, max_chars: int = 800, overlap: int = 200) -> List[str]:
    """
    Chunking simple por párrafo con ventana deslizante.
    """
    paras = [p.strip() for p in text.split("\n") if p.strip()]
    chunks: List[str] = []
    buf = ""
    for p in paras:
        if not buf:
            buf = p
        elif len(buf) + 1 + len(p) <= max_chars:
            buf = f"{buf}\n{p}"
        else:
            chunks.append(buf)
            # overlap aproximado
            if overlap > 0 and len(buf) > overlap:
                buf = buf[-overlap:] + "\n" + p
            else:
                buf = p
    if buf:
        chunks.append(buf)
    return chunks

# Embeddings (fastembed, OpenAI, Gemini)

def _embed_fastembed(model_name: str) -> Callable[[List[str]], List[List[float]]]:
    # Carga perezosa para evitar dependencias innecesarias
    from fastembed import TextEmbedding

    te = TextEmbedding(model_name=model_name)
    # TextEmbedding devuelve un generador de np.array; lo convertimos a list[list[float]]
    def _fn(texts: List[str]) -> List[List[float]]:
        # fastembed soporta batch grande sin problemas; lo dejamos así
        vecs = te.embed(texts)
        return [v.tolist() for v in vecs]

    return _fn

def _embed_openai(model: str) -> Callable[[List[str]], List[List[float]]]:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)

    def _fn(texts: List[str]) -> List[List[float]]:
        resp = client.embeddings.create(model=model, input=texts)
        return [d.embedding for d in resp.data]

    return _fn


def _embed_gemini(model: str) -> Callable[[List[str]], List[List[float]]]:
    import google.generativeai as genai
    
    genai.configure(api_key=settings.gemini_api_key)

    def _fn(texts: List[str]) -> List[List[float]]:
        
        all_embeddings = []
        for i in range(0, len(texts), 99):
            batch = texts[i : i + 99]
            resp = genai.embed_content(model=model, content=batch)
            all_embeddings.extend(resp["embedding"])
        return all_embeddings

    return _fn


def get_embed_fn() -> Tuple[Callable[[List[str]], List[List[float]]], str]:
    """
    Retorna (función_de_embedding, nombre_modelo) según settings.
    Soporta: fastembed (recomendado), openai, gemini.
    """
    provider = "gemini"

    if provider == "fastembed":
        model_name = "intfloat/multilingual-e-5-small"
        return _embed_fastembed(model_name), f"fastembed:{model_name}"

    if provider == "openai":
        model_name = "text-embedding-3-small"
        return _embed_openai(model_name), f"openai:{model_name}"

    if provider == "gemini":
        model_name = "models/text-embedding-004"
        return _embed_gemini(model_name), f"gemini:{model_name}"

    raise ValueError(f"Proveedor de embeddings no soportado: {provider}")


# Persistencia de índice simple
DATA_DIR = os.path.join(".", "data")
EMB_PATH = os.path.join(DATA_DIR, "embeddings.npy")
CHUNKS_PATH = os.path.join(DATA_DIR, "chunks.jsonl")


def save_index(embeddings: np.ndarray, chunks: List[Dict[str, Any]]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    np.save(EMB_PATH, embeddings.astype(np.float32))
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        for ch in chunks:
            f.write(json.dumps(ch, ensure_ascii=False) + "\n")


# Ingesta principal
def ingest_sources() -> Dict[str, Any]:
    sources = settings.sources  # lista de URLs
    max_chars = settings.max_context_chars or 8000  # usado solo de referencia
    chunk_chars = 500
    overlap = 100

    embed_fn, embed_model_name = get_embed_fn()

    all_chunks: List[Dict[str, Any]] = []
    texts: List[str] = []

    for url in tqdm(sources, desc="Procesando URLs", ncols=100):
        try:
            html = fetch_html(url)
            text = html_to_text(html)
            chunks = chunk_text(text, max_chars=chunk_chars, overlap=overlap)

            for i, c in enumerate(chunks):
                all_chunks.append(
                    {
                        "id": f"{hash(url)}_{i}",
                        "source": url,
                        "text": c,
                    }
                )
                texts.append(c)
        except Exception as e:
            print(f"Error procesando {url}: {e}")


    # Embeddings
    vecs = []
    batch = 64
    for i in tqdm(range(0, len(texts), batch), desc="Generando Embeddings", ncols=100):
        vecs.extend(embed_fn(texts[i : i + batch]))

    embs = np.array(vecs, dtype=np.float32)
    save_index(embs, all_chunks)

    return {
        "indexed": len(all_chunks),
        "embedding_model": embed_model_name,
        "sources": sources,
    }


if __name__ == "__main__":
    print(ingest_sources())