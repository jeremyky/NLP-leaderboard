"""
Rate limiting middleware for API endpoints

Protects against abuse and ensures fair usage of the leaderboard API.
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


# Rate limit configurations for different endpoint types
RATE_LIMITS = {
    "default": "100/minute",           # General API calls
    "submission": "10/minute",         # Model submissions
    "admin": "5/minute",               # Admin operations (seeding, imports)
    "leaderboard": "200/minute",       # Leaderboard queries (higher limit)
}


def setup_rate_limiting(app):
    """
    Configure rate limiting for the FastAPI app
    
    Usage in main.py:
        from rate_limiter import setup_rate_limiting
        setup_rate_limiting(app)
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    return limiter

