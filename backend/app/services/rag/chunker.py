import re


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []
    # Split into sentences/paragraphs first
    parts = re.split(r"\n+", text)
    chunks = []
    current = ""
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if len(current) + len(part) + 1 <= chunk_size:
            current = (current + " " + part).strip() if current else part
        else:
            if current:
                chunks.append(current)
            current = part
    if current:
        chunks.append(current)
    # Further split oversized chunks
    result = []
    for c in chunks:
        if len(c) <= chunk_size:
            result.append(c)
        else:
            for i in range(0, len(c), chunk_size - overlap):
                result.append(c[i : i + chunk_size])
    # dedup adjacent duplicates
    out = []
    for c in result:
        if not out or c != out[-1]:
            out.append(c)
    return out
