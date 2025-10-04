

from fastapi import FastAPI
app = FastAPI(title="Ranker")
@app.get("/health")
def health(): return {"status": "ok", "service": "ranker"}
