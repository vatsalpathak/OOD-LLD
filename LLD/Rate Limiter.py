# Design and implement a Rate Limiter system that enforces limits on how frequently a user can make a request.

# Support different rate-limiting algorithms, such as:
# Fixed Window: Reset counter at fixed intervals.
# Sliding Window: Track exact timestamps and remove expired ones.
# Implement the design in a way that:
# Allows easy extension for future rate-limiting strategies.
# Enforces that there is only one instance of the RateLimiter (Singleton).
# Uses Factory Pattern to instantiate specific rate limiter strategies.

from abc import ABC, abstractmethod
from datetime import datetime,timedelta
from collections import deque, defaultdict

class RateLimiter(ABC):
    def __init__(self,rate_limit,time_window) -> None:
        self.rate_limit = rate_limit
        self.time_window = time_window

    @abstractmethod
    def is_too_frequent(self,user_id):
        pass

    def now_time(self):
        return datetime.now()

class SlidingWindowRateLimiter(RateLimiter):
    def __init__(self, rate_limit, time_window):
        super().__init__(rate_limit, time_window)
        self.user_requests = defaultdict(deque)

    def is_too_frequent(self, user_id):
        current_time = self.now_time()
        dq = self.user_requests[user_id]

        # Remove old timestamps outside the window
        while dq and (current_time - dq[0]).total_seconds() > self.time_window:
            dq.popleft()

        dq.append(current_time)  # Add current request

        # If number of requests in window > allowed, deny
        return len(dq) > self.rate_limit

class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, rate_limit, time_window):
        super().__init__(rate_limit, time_window)
        self.user_windows = defaultdict(lambda: {"window_start": None, "count": 0})

    def is_too_frequent(self, user_id):
        current_time = self.now_time()
        user_data = self.user_windows[user_id]

        # Compute the start of the current time window
        window_start = current_time - timedelta(seconds=current_time.second % self.time_window,
                                                microseconds=current_time.microsecond)

        # New window → reset counter
        if user_data["window_start"] != window_start:
            user_data["window_start"] = window_start
            user_data["count"] = 1
        else:
            user_data["count"] += 1

        return user_data["count"] > self.rate_limit



class RateLimiterFactory:
    def create_limiter(self,limiter_type, rate_limit, time_window) -> None:

        if limiter_type == "fixed":
            return FixedWindowRateLimiter(rate_limit,time_window)
        elif limiter_type == "sliding":
            return SlidingWindowRateLimiter(rate_limit,time_window)
        else:
            raise ValueError("Unknown limiter type")
        
class RateLimiterManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, limiter_type=None, rate_limit=None, time_window=None):
        if not hasattr(self, '_initialized'):
            factory = RateLimiterFactory()
            self._rate_limiter = factory.create_limiter(limiter_type, rate_limit, time_window)
            self._initialized = True  # Prevent re-initialization

    def is_too_frequent(self, user_id):
        return self._rate_limiter.is_too_frequent(user_id)
    

if __name__ == "__main__":
    import time

    manager = RateLimiterManager("sliding", rate_limit=5, time_window=10)
    user_id = "user123"

    for i in range(7):
        time.sleep(1)
        print(f"Request {i+1}: Too Frequent? {manager.is_too_frequent(user_id)}")

