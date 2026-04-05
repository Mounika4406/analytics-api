import time

class RateLimiter:
    def __init__(self, redis_client, limit=5, window=60):
        self.redis = redis_client
        self.limit = limit
        self.window = window

    def allow(self, key):
        current = self.redis.incr(key)

        if current == 1:
            self.redis.expire(key, self.window)

        return current <= self.limit

    def retry_after(self, key):
        return self.redis.ttl(key)