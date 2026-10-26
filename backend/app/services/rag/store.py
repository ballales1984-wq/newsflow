import json
import os
from typing import List, Dict, Any


class VectorStore:
    def __init__(self, path: str):
        self.path = path
        self._data: List[Dict[str, Any]] = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = []

    def add(self, items: List[Dict[str, Any]]):
        # items: {id, text, embedding, metadata}
        existing = {i["id"] for i in self._data}
        for it in items:
            if it["id"] in existing:
                # update
                for idx, d in enumerate(self._data):
                    if d["id"] == it["id"]:
                        self._data[idx] = it
                        break
            else:
                self._data.append(it)
        self._save()

    def remove(self, ids: List[str]):
        s = set(ids)
        self._data = [d for d in self._data if d["id"] not in s]
        self._save()

    def search(self, query_vec, top_k: int = 5) -> List[Dict[str, Any]]:
        scored = []
        for d in self._data:
            score = sum(a * b for a, b in zip(d["embedding"], query_vec))
            scored.append((score, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:top_k]]

    def count(self) -> int:
        return len(self._data)

    def _save(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f)
