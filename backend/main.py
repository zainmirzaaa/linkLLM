from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend.example"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

class SearchRequest(BaseModel):
    q: str

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/ask")
async def ask(query: Query):
    return {"message": f"You asked: {query.question}"}

@app.post("/search", response_model=List[SearchResult])
async def search_api(payload: SearchRequest):
    q = payload.q.strip()
    if not q:
        return []
    # placeholder; real search comes from search.py later
    return [
        SearchResult(
            title="Sample Result",
            link="https://stackoverflow.com/questions/123",
            snippet=f"Matched query: {q}"
        )
    ]
