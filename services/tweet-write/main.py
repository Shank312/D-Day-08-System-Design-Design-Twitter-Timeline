

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Tweet Write")

class TweetCreate(BaseModel):
    author_id: str
    text: str
    media_urls: list[str] = []

@app.get("/health")
def health():
    return {"status": "ok", "service": "tweet-write"}

@app.post("/tweets", status_code=201)
def create_tweet(t: TweetCreate):
    # TODO: persist to Cassandra, emit Kafka event
    return {
        "id": "snowflake-xyz",
        "author_id": t.author_id,
        "text": t.text,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "like_count": 0
    }
