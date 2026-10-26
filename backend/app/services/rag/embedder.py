import hashlib
import math
from typing import List

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


def _local_embed(text: str, dim: int = 256) -> List[float]:
    vec = [0.0] * dim
    for token in text.lower().split():
        h = int(hashlib.md5(token.encode()).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 1.0
    # normalize
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def embed_texts(texts: List[str], model: str = "", api_key: str = "") -> List[List[float]]:
    if api_key and OpenAI is not None and model:
        try:
            client = OpenAI(api_key=api_key)
            resp = client.embeddings.create(model=model, input=texts)
            return [d.embedding for d in resp.data]
        except Exception:
            pass
    return [_local_embed(t) for t in texts]


def cosine(a, b) -> float:
    return sum(x * y for x, y in zip(a, b))
