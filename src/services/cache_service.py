import json

class CacheService:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_or_set(self, key, func, ttl=60):
        cached = self.redis.get(key)

        if cached:
            print("CACHE HIT")
            return json.loads(cached)

        print("CACHE MISS")
        data = func()

        self.redis.setex(key, ttl, json.dumps(data))
        return data