Real-Time Analytics Backend API
 Overview

This project implements a robust backend API for a simulated real-time analytics system.
It demonstrates production-grade backend concepts such as:

⚡ Redis caching for performance
🚫 Rate limiting to prevent abuse
🔌 Circuit breaker for fault tolerance
🐳 Docker containerization
🏗️ Tech Stack
Python (FastAPI)
Redis
Docker & Docker Compose
⚙️ Setup Instructions
1️⃣ Clone Repository
git clone <your-repo-link>
cd analytics-api
2️⃣ Run with Docker
docker-compose up --build
3️⃣ Access API
http://localhost:8000/docs
📡 API Endpoints
🔹 POST /api/metrics

Add a metric

{
  "timestamp": "2026-01-01T10:00:00",
  "value": 50,
  "type": "cpu"
}
🔹 GET /api/metrics/summary

Get aggregated metrics

/api/metrics/summary?type=cpu

Response:

{
  "type": "cpu",
  "average": 50,
  "count": 1
}
🔹 GET /api/external

Simulated external API (with circuit breaker)

⚡ Caching (Redis)
Uses read-through caching
First request → CACHE MISS
Next requests → CACHE HIT
TTL used for automatic expiration
🚫 Rate Limiting
Limit: 5 requests per minute per IP
Uses Redis INCR + EXPIRE
Exceeded → 429 Too Many Requests
🔌 Circuit Breaker

States:

Closed → normal operation
Open → fallback response
Half-Open → test recovery

Prevents cascading failures from external services.

🐳 Docker Setup
Backend service
Redis service
Health checks included

Run:

docker-compose up --build