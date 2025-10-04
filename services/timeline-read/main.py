

from fastapi import FastAPI
app = FastAPI(title="Timeline Read")

@app.get("/health")
def health():
    return {"status": "ok", "service": "timeline-read"}

@app.get("/timeline/home")
def home(user_id: str, limit: int = 30):
    # TODO: fetch from HTL store (Redis/Cassandra), call ranker
    return {"user_id": user_id, "items": []}
