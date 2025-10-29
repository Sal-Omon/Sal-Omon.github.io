from redis import Redis
import os
import logging
import json

logger = logging.getLogger(__name__)
_redis_client: Redis | None = None


def get_redis_client() -> Redis:
    global _redis_client
    try:
        if _redis_client is None:
            url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            _redis_client = Redis.from_url(
                url, 
                decode_responses=True,
                socket_timeout=5,  # seconds
                retry_on_timeout=True
            )
            _redis_client.ping()  # Test connection
        return _redis_client
    except Exception as e:
        logger.error(f"Redis connection error: {e}")
        raise
            
         
def cache_get(key: str):
    client = get_redis_client()
    data = client.get(key)
    return json.loads(data) if data else None
 
def cache_set(key: str, value, timeout: int = 100):
    client = get_redis_client()
    client.set(key, json.dumps(value), ex=timeout)
            
            
    return _redis_client
