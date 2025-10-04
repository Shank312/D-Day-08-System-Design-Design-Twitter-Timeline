

from fastapi import FastAPI
app = FastAPI(title="Counters")
@app.get("/health")
def health(): return {"status": "ok", "service": "counters"}
