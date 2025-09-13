import json
import os
from typing import List, Dict, Any
import numpy as np
from sklearn.neighbors import NearestNeighbors

from .ingest import EMB_PATH, CHUNKS_PATH
from .ingest import get_embed_fn


class SimpleRetriever:
    def __init__(self):
        if not (os.path.exists(EMB_PATH) and os.path.exists(CHUNKS_PATH)):
            raise RuntimeError("No existe el índice. Corré:  python -m app.ingest")

        self.embs = np.load(EMB_PATH).astype(np.float32)
        self.chunks: List[Dict[str, Any]] = []
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            for line in f:
                self.chunks.append(json.loads(line))

        # normalizamos para usar coseno ~ dot
        self._norm = np.linalg.norm(self.embs, axis=1, keepdims=True) + 1e-8
        self.embs = self.embs / self._norm

        self.nn = NearestNeighbors(n_neighbors=10, metric="cosine")
        self.nn.fit(self.embs)

        self.embed_fn, _ = get_embed_fn()

    def search(self, query: str, k: int = 6) -> List[Dict[str, Any]]:
        qv = np.array(self.embed_fn([query])[0], dtype=np.float32)
        qv = qv / (np.linalg.norm(qv) + 1e-8)
        dists, idxs = self.nn.kneighbors(qv.reshape(1, -1), n_neighbors=min(k, len(self.chunks)))
        results: List[Dict[str, Any]] = []
        for d, i in zip(dists[0], idxs[0]):
            ch = self.chunks[int(i)]
            results.append(
                {
                    "id": ch["id"],
                    "text": ch["text"],
                    "source": ch["source"],
                    "score": float(1.0 - d),  # similitud aproximada
                }
            )
        return results
