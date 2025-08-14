
from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.requests import Request
from starlette.responses import Response
import random, time

app = FastAPI(title="Enterprise Migration App", version="1.0.0")

REQS = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
LAT = Histogram("request_latency_ms", "Request latency (ms)", buckets=(10,25,50,100,200,300,500,1000))

class PredictIn(BaseModel):
    symbol: str = Field(..., description="Ticker symbol (e.g. AMZN)")
    window: int = Field(5, ge=1, le=50, description="Lookback window")

def record(method, endpoint, status, t0):
    REQS.labels(method=method, endpoint=endpoint, status=str(status)).inc()
    LAT.observe(max(0, (time.time()*1000 - t0)))

@app.middleware("http")
async def metrics(request: Request, call_next):
    t0 = time.time()*1000
    try:
        resp = await call_next(request)
        status = resp.status_code
    except Exception:
        status = 500
        record(request.method, request.url.path, status, t0)
        raise
    record(request.method, request.url.path, status, t0)
    return resp

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: PredictIn):
    base = random.uniform(-1,1)
    score = round(sum(random.uniform(-0.5,0.5) for _ in range(payload.window))/payload.window + base, 4)
    return {"symbol": payload.symbol.upper(), "window": payload.window, "score": score}

@app.get("/metrics")
def prom():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
