"""Caching utilities with pluggable backends."""

import hashlib
import json
from abc import ABC, abstractmethod
from typing import Any, Optional
from cachetools import TTLCache  # type: ignore[import-untyped]

from src.config import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


class CacheBackend(ABC):
    """Abstract base class for cache backends."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cache entries."""
        pass


class MemoryCache(CacheBackend):
    """In-memory LRU cache with TTL."""

    def __init__(self, max_size: int = 1000, ttl: int = 30):
        self.cache = TTLCache(maxsize=max_size, ttl=ttl)
        self.hits = 0
        self.misses = 0

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.cache[key]
            self.hits += 1
            logger.debug(f"Cache hit for key: {key}")
            return value
        except KeyError:
            self.misses += 1
            logger.debug(f"Cache miss for key: {key}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        self.cache[key] = value
        logger.debug(f"Cache set for key: {key}")

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        try:
            del self.cache[key]
            logger.debug(f"Cache delete for key: {key}")
        except KeyError:
            pass

    async def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        logger.info("Cache cleared")

    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2f}%",
            "size": len(self.cache),
        }


class RedisCache(CacheBackend):
    """Redis cache backend."""

    def __init__(self, redis_url: str, ttl: int = 30):
        self.redis_url = redis_url
        self.default_ttl = ttl
        self.redis = None

    async def connect(self) -> None:
        """Connect to Redis."""
        try:
            import redis.asyncio as aioredis

            self.redis = await aioredis.from_url(
                self.redis_url, encoding="utf-8", decode_responses=True
            )
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()
            logger.info("Disconnected from Redis")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.redis:
            return None

        try:
            value = await self.redis.get(key)
            if value:
                logger.debug(f"Redis cache hit for key: {key}")
                return json.loads(value)
            logger.debug(f"Redis cache miss for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL."""
        if not self.redis:
            return

        try:
            serialized = json.dumps(value, default=str)
            await self.redis.setex(key, ttl or self.default_ttl, serialized)
            logger.debug(f"Redis cache set for key: {key}")
        except Exception as e:
            logger.error(f"Redis set error: {e}")

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        if not self.redis:
            return

        try:
            await self.redis.delete(key)
            logger.debug(f"Redis cache delete for key: {key}")
        except Exception as e:
            logger.error(f"Redis delete error: {e}")

    async def clear(self) -> None:
        """Clear all cache entries."""
        if not self.redis:
            return

        try:
            await self.redis.flushdb()
            logger.info("Redis cache cleared")
        except Exception as e:
            logger.error(f"Redis clear error: {e}")


class CacheManager:
    """Cache manager with pluggable backends."""

    def __init__(self):
        self.backend: Optional[CacheBackend] = None

    async def initialize(self) -> None:
        """Initialize cache backend based on settings."""
        if settings.cache_backend == "redis":
            self.backend = RedisCache(settings.redis_url, settings.cache_ttl)
            await self.backend.connect()  # type: ignore
        else:
            self.backend = MemoryCache(settings.cache_max_size, settings.cache_ttl)

        logger.info(f"Cache backend initialized: {settings.cache_backend}")

    async def shutdown(self) -> None:
        """Shutdown cache backend."""
        if isinstance(self.backend, RedisCache):
            await self.backend.disconnect()

    def generate_cache_key(self, prefix: str, **kwargs: Any) -> str:
        """Generate a cache key from parameters."""
        # Sort kwargs for consistent key generation
        sorted_params = json.dumps(kwargs, sort_keys=True, default=str)
        hash_value = hashlib.md5(sorted_params.encode()).hexdigest()
        return f"{prefix}:{hash_value}"

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.backend:
            return None
        return await self.backend.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        if not self.backend:
            return
        await self.backend.set(key, value, ttl)

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        if not self.backend:
            return
        await self.backend.delete(key)

    async def clear(self) -> None:
        """Clear all cache entries."""
        if not self.backend:
            return
        await self.backend.clear()


# Global cache manager instance
cache_manager = CacheManager()
