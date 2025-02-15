from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# placeholder: later load from SO dataset
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

def search(query: str):
    return index.query(query)
