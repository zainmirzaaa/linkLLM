from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# placeholder: later load from SO dataset
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

def search(query: str):
    return index.query(query)

_index = None  # lazy-loaded
_data_dir = Path("data")

def _ensure_index():
    global _index
    if _index is not None:
        return _index
    try:
        from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
        docs = SimpleDirectoryReader(str(_data_dir)).load_data()
        _index = VectorStoreIndex.from_documents(docs)
    except Exception:
        _index = None
    return _index

def search(query: str) -> List[Dict]:
    idx = _ensure_index()
    if not idx:
        # fallback if index not available
        return [{"title": "Index not ready", "link": "https://stackoverflow.com", "snippet": query}]
    res = idx.query(query)
    # normalize
    return [{"title": str(r), "link": "https://stackoverflow.com", "snippet": str(r)} for r in res]

def rank(results: List[Dict]) -> List[Dict]:
    return sorted(results, key=lambda r: len(r.get("snippet", "")), reverse=True)[:10]

_cache = {}

def search(query: str):
    if query in _cache:
        return _cache[query]

    # placeholder response
    results = [{"title": "Cached Example", "link": "https://so.com", "snippet": query}]
    _cache[query] = results
    return results

from fastapi import Request, HTTPException

requests_per_ip = {}

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    ip = request.client.host
    count = requests_per_ip.get(ip, 0) + 1
    requests_per_ip[ip] = count
    if count > 50:  # limit for demo
        raise HTTPException(status_code=429, detail="Too many requests")
    return await call_next(request)
