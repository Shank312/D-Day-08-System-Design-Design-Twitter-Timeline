

from fastapi import FastAPI
app = FastAPI(title="Fanout")
@app.get("/health")
def health(): return {"status": "ok", "service": "fanout"}
