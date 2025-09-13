import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .rag_pipeline import answer_question

# ===== FastAPI =====
app = FastAPI(title="Mini RAG – Historia Argentina", version="0.2.0")

# (CORS no sería necesario si servimos todo en el mismo origen,
#  pero lo dejamos por si abrís el HTML desde file://)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # podés restringir a ["http://127.0.0.1:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Frontend estático =====
# Servimos la raíz del repo como estático para poder devolver index.html
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
app.mount("/static", StaticFiles(directory=ROOT_DIR), name="static")

@app.get("/", include_in_schema=False)
def root():
    if os.path.exists(INDEX_PATH):
        return FileResponse(INDEX_PATH, media_type="text/html; charset=utf-8")
    return PlainTextResponse("index.html no encontrado en la raíz del proyecto.", status_code=404)

# ===== API =====
class AskRequest(BaseModel):
    question: str

@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    return answer_question(req.question)

# ===== Runner (python -m app.api) =====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
