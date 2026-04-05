import json
import os

def get_or_set(self, key, func):
    ttl = int(os.getenv("CACHE_TTL", 60))   # ✅ ADD HERE

    cached = self.redis.get(key)
    if cached:
        print("CACHE HIT")
        return json.loads(cached)

    print("CACHE MISS")
    data = func()
    self.redis.setex(key, ttl, json.dumps(data))
    return data