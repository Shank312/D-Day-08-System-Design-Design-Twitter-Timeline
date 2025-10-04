

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os

app = FastAPI(title="Gateway")

@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway"}

# Pass-through stubs; in real deployment, forward to internal services
@app.post("/tweets")
async def post_tweet(payload: dict):
    # TODO: forward to tweet-write service
    return JSONResponse(status_code=201, content={"id": "snowflake-123", **payload})

@app.get("/timeline/home")
async def home_timeline(user_id: str, limit: int = 30):
    # TODO: call timeline-read service
    return {"user_id": user_id, "items": []}

@app.get("/users/{id}/timeline")
async def user_timeline(id: str, limit: int = 30):
    return {"user_id": id, "items": []}

@app.post("/follow/{id}")
async def follow(id: str):
    return JSONResponse(status_code=204, content=None)

@app.delete("/follow/{id}")
async def unfollow(id: str):
    return JSONResponse(status_code=204, content=None)

@app.post("/tweets/{id}/like")
async def like(id: str):
    return JSONResponse(status_code=204, content=None)

@app.delete("/tweets/{id}/like")
async def unlike(id: str):
    return JSONResponse(status_code=204, content=None)
