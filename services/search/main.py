

from fastapi import FastAPI
app = FastAPI(title="Search")
@app.get("/health")
def health(): return {"status": "ok", "service": "search"}
