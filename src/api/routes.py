from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

from src.config.redis_client import redis_client
from src.services.cache_service import CacheService
from fastapi import Request
from src.services.rate_limiter import RateLimiter
from src.services.circuit_breaker import CircuitBreaker
from src.services.external_service import external_call

router = APIRouter()


# Cache setup
cache = CacheService(redis_client)
limiter = RateLimiter(redis_client)
cb = CircuitBreaker()

# In-memory DB
metrics_db = []

# Model
class Metric(BaseModel):
    timestamp: datetime
    value: float
    type: str

# POST API
@router.post("/api/metrics", status_code=201)
def create_metric(metric: Metric, request: Request):

    ip = request.client.host
    key = f"rate:{ip}"

    if not limiter.allow(key):
        retry = limiter.retry_after(key)

        raise HTTPException(
            status_code=429,
            detail="Too many requests",
            headers={"Retry-After": str(retry)}   # ✅ ADD HERE
        )

    metrics_db.append(metric)
    return {"message": "Metric stored"}

# GET API with caching
@router.get("/api/metrics/summary")
def get_summary(type: str, period: str = "daily"):

    def compute():
        filtered = [m.value for m in metrics_db if m.type == type]

        if not filtered:
            raise HTTPException(status_code=404, detail="No data")

        return {
            "type": type,
            "period": period,   # ✅ ADD THIS
            "average": sum(filtered)/len(filtered),
            "count": len(filtered)
        }

    return cache.get_or_set(f"summary:{type}:{period}", compute)

    return cache.get_or_set(f"summary:{type}", compute)
@router.get("/api/external")
def call_external():
    return cb.call(external_call)