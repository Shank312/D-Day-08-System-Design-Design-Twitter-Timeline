

from __future__ import annotations

import os
from typing import List, Optional

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette import status

# ---------- Settings ----------
TWEET_WRITE_URL = os.getenv("TWEET_WRITE_URL", "http://tweet-write:8000")
TIMELINE_READ_URL = os.getenv("TIMELINE_READ_URL", "http://timeline-read:8000")
SOCIAL_GRAPH_URL = os.getenv("SOCIAL_GRAPH_URL", "http://social-graph:8000")
ENGAGEMENT_URL = os.getenv("ENGAGEMENT_URL", "http://engagement:8000")

app = FastAPI(title="Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# One shared async client for the process
client: httpx.AsyncClient | None = None


@app.on_event("startup")
async def _startup() -> None:
    global client
    client = httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=3.0))


@app.on_event("shutdown")
async def _shutdown() -> None:
    global client
    if client:
        await client.aclose()
        client = None


# ---------- Schemas ----------
class TweetCreate(BaseModel):
    user_id: str = Field(..., description="Author user id")
    text: str = Field(..., max_length=280)
    media: Optional[List[str]] = None


class TimelineItem(BaseModel):
    id: str
    author_id: str
    text: str
    created_at: str


class TimelineResponse(BaseModel):
    user_id: str
    items: List[TimelineItem] = []


# ---------- Routes ----------
@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "gateway"}


# Create tweet -> forward to tweet-write service
@app.post("/tweets", status_code=status.HTTP_201_CREATED)
async def post_tweet(payload: TweetCreate):
    assert client is not None
    try:
        r = await client.post(f"{TWEET_WRITE_URL}/tweets", json=payload.model_dump())
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return JSONResponse(status_code=r.status_code, content=r.json())
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"tweet-write unreachable: {e!s}") from e


# Home timeline
@app.get("/timeline/home", response_model=TimelineResponse)
async def home_timeline(user_id: str, limit: int = Query(30, ge=1, le=200)):
    assert client is not None
    try:
        r = await client.get(
            f"{TIMELINE_READ_URL}/timeline/home",
            params={"user_id": user_id, "limit": limit},
        )
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"timeline-read unreachable: {e!s}") from e


# User profile timeline
@app.get("/users/{id}/timeline", response_model=TimelineResponse)
async def user_timeline(id: str, limit: int = Query(30, ge=1, le=200)):
    assert client is not None
    try:
        r = await client.get(
            f"{TIMELINE_READ_URL}/users/{id}/timeline",
            params={"limit": limit},
        )
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"timeline-read unreachable: {e!s}") from e


# Follow / Unfollow
@app.post("/follow/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def follow(id: str):
    assert client is not None
    try:
        r = await client.post(f"{SOCIAL_GRAPH_URL}/follow/{id}")
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"social-graph unreachable: {e!s}") from e


@app.delete("/follow/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow(id: str):
    assert client is not None
    try:
        r = await client.delete(f"{SOCIAL_GRAPH_URL}/follow/{id}")
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"social-graph unreachable: {e!s}") from e


# Like / Unlike
@app.post("/tweets/{id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def like(id: str):
    assert client is not None
    try:
        r = await client.post(f"{ENGAGEMENT_URL}/tweets/{id}/like")
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"engagement unreachable: {e!s}") from e


@app.delete("/tweets/{id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike(id: str):
    assert client is not None
    try:
        r = await client.delete(f"{ENGAGEMENT_URL}/tweets/{id}/like")
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"engagement unreachable: {e!s}") from e

