import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=10):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = "CLOSED"
        self.last_failure_time = None

    def call(self, func):
        if self.state == "OPEN":
            if time.time() > self.last_failure_time + self.reset_timeout:
                self.state = "HALF_OPEN"
            else:
                return {"message": "Fallback response (circuit open)"}

        try:
            result = func()
            self.failure_count = 0
            self.state = "CLOSED"
            return result

        except Exception:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            return {"message": "Fallback response (failure)"}