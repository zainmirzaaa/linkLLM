from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .search import search as vector_search, rank as rank_results
from .llm import rephrase_query
from .llm import safe_query
import logging
import time
from fastapi import Request
from .config import settings
from fastapi import Request
from fastapi.responses import JSONResponse
import datetime
from fastapi import BackgroundTasks
from .search import _ensure_index
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND
import uuid
from fastapi import Request
from .logjson import log_json
from .auth import require_api_key
from fastapi import FastAPI
app = FastAPI(title="LinkLLM API", version="0.1.0", openapi_tags=[
    {"name": "health", "description": "Service health & readiness"},
    {"name": "search", "description": "Query, rank and fetch results"},
    {"name": "llm", "description": "LLM-backed endpoints"},
])
from pydantic import BaseModel, Field, constr

SafeQuery = constr(strip_whitespace=True, min_length=2, max_length=200,
                   regex=r"^[\w\s\-\+\.\?\#:/\(\)\[\]]+$")

class SearchRequest(BaseModel):
    q: SafeQuery = Field(..., description="Search string 2-200 chars")
    minScore: int = Field(0, ge=0, le=100)
    limit: int = Field(10, ge=1, le=50)


@app.get("/health", tags=["health"], summary="Basic health check")
async def health():
    """Returns liveness of the service."""
    return {"ok": True}


@app.get("/secure", dependencies=[Depends(require_api_key)])
async def secure_echo():
    return {"ok": True}


@app.get("/ping")
async def ping():
    log_json("ping", ok=True)
    return {"ok": True}


@app.middleware("http")
async def request_id_mw(request: Request, call_next):
    rid = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = rid
    response = await call_next(request)
    response.headers["x-request-id"] = rid
    print(f"[RID {rid}] {request.method} {request.url.path}")
    return response


@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content={"error": "not_found", "path": request.url.path},
    )


def warm_index():
    idx = _ensure_index()
    print("index warm:", bool(idx))

@app.on_event("startup")
async def app_start():
    # kick off warming without blocking startup
    import threading
    threading.Thread(target=warm_index, daemon=True).start()


def log_line(msg: str):
    with open("server.log", "a", encoding="utf-8") as f:
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        f.write(f"[{ts}] {msg}\n")

@app.get("/ping")
async def ping():
    log_line("ping called")
    return {"ok": True}


@app.exception_handler(Exception)
async def on_exception(request: Request, exc: Exception):
    print(f"[ERR] {request.method} {request.url.path} -> {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "message": str(exc)[:200]},
    )


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    print(f"{request.method} {request.url.path} took {duration}ms")
    return response

logging.basicConfig(level=logging.INFO)

@app.post("/ask")
async def ask(query: Query):
    logging.info(f"Received query: {query.question}")
    return {"message": f"You asked: {query.question}"}


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


@app.post("/search/v1", response_model=List[SearchResult])
async def search_api_v1(payload: SearchRequest):
    q = payload.q.strip()
    if not q:
        return []
    better_q = await rephrase_query(q)
    raw = vector_search(better_q or q)
    ranked = rank_results(raw)
    return [SearchResult(**r) for r in ranked]


class AskRequest(BaseModel):
  question: str

class AskResponse(BaseModel):
  answer: str

@app.post("/ask/v1", response_model=AskResponse)
async def ask_v1(req: AskRequest):
    answer = await safe_query(req.question)
    return AskResponse(answer=answer)

@app.get("/config-check")
async def config_check():
    return {"debug": settings.debug, "openai_key_set": bool(settings.openai_key)}

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

analytics = {"queries": 0, "asks": 0}

@app.post("/ask")
async def ask(query: Query):
    analytics["asks"] += 1
    return {"message": f"You asked: {query.question}"}

@app.post("/search")
async def search_api(payload: SearchRequest):
    analytics["queries"] += 1
    return [{"title": "Result", "link": "https://so.com", "snippet": payload.q}]

@app.get("/analytics")
async def get_analytics():
    return analytics

from typing import List
from pydantic import BaseModel

class SearchItem(BaseModel):
    title: str
    link: str
    snippet: str
    score: int = 0

@app.post("/search/typed", response_model=List[SearchItem])
async def search_typed(payload: SearchRequest):
    rows = [{"title":"Result","link":"https://so.com","snippet":payload.q,"score":75}]
    return [SearchItem(**r) for r in rows]

import datetime

def log_line(msg: str):
    with open("server.log", "a", encoding="utf-8") as f:
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        f.write(f"[{ts}] {msg}\n")

@app.get("/ping")
async def ping():
    log_line("ping called")
    return {"ok": True}



class SearchPageRequest(BaseModel):
    q: str
    offset: int = 0
    limit: int = 10

@app.post("/search/page", response_model=List[SearchItem])
async def search_page(req: SearchPageRequest):
    data = [
        {"title": f"Hit {i}", "link": "https://so.com", "snippet": req.q, "score": 50+i}
        for i in range(100)
    ]
    sl = data[req.offset : req.offset + req.limit]
    return [SearchItem(**r) for r in sl]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
