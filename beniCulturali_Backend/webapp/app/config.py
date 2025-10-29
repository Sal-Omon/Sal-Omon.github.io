# app/config.py
import os

# Database connection: fallback to local Postgres if DATABASE_URL not set
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/beniculturali_db")
SQLALCHEMY_DATABASE_URI = DATABASE_URL

# Disable modification tracking (saves memory)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Caching config (Redis)
# Depending on the version of flask-caching you use, the backend string may vary:
# - "RedisCache" for modern versions, or "redis" for older adapters.
CACHE_TYPE = os.getenv("CACHE_TYPE", "RedisCache")
CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/0")
CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "60"))
