

from fastapi import FastAPI
app = FastAPI(title="IDGen")
@app.get("/health")
def health(): return {"status": "ok", "service": "idgen"}
