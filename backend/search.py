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
