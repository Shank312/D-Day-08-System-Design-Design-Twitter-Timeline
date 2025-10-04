

from fastapi import FastAPI
app = FastAPI(title="Graph")
@app.get("/health")
def health(): return {"status": "ok", "service": "graph"}
