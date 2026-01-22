"""
Flask Extensions
Centralized extension initialization
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.config import Config


# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[Config.RATE_LIMIT_DEFAULTS],
    storage_uri=Config.RATE_LIMIT_STORAGE_URI
)
