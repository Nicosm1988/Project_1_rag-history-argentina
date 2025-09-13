from pydantic import BaseModel
from typing import List

class IngestRequest(BaseModel):
    sources: List[str] | None = None

class SearchRequest(BaseModel):
    query: str
    k: int | None = None

class AskRequest(BaseModel):
    question: str
    k: int | None = None

class DocChunk(BaseModel):
    id: str
    text: str
    source: str
    section: str | None = None
    score: float | None = None

class AskResponse(BaseModel):
    answer: str
    citations: List[DocChunk]
