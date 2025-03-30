from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import time
from functools import lru_cache

@lru_cache(maxsize=1024)
def normalize_query(q: str) -> str:
    return " ".join(q.lower().split())

def search(query: str):
    qn = normalize_query(query)
    return [{"title": "Normalized", "link": "https://so.com", "snippet": qn}]


_cache = {}  # key -> (expiry_ts, value)
_TTL_SEC = 120

def search(query: str):
    now = time.time()
    hit = _cache.get(query)
    if hit and hit[0] > now:
        return hit[1]
    results = [{"title":"TTL Example","link":"https://so.com","snippet":query}]
    _cache[query] = (now + _TTL_SEC, results)
    return results


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

