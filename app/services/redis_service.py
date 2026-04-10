from app.db.redis_client import get_redis
import json
from typing import Any, Optional, Dict, List



class RedisService:
    
    # ---------------------------
    # 🔹 BASIC KEY-VALUE
    # ---------------------------
    @staticmethod
    async def set(key: str, value: str, ex: Optional[int] = None):
        _client = get_redis()
        await _client.set(key, value, ex=ex)

    @staticmethod
    async def get(key: str) -> Optional[str]:
        _client = get_redis()
        return await _client.get(key)

    @staticmethod
    async def delete(key: str):
        _client = get_redis()
        await _client.delete(key)

    # ---------------------------
    # 🔹 REDIS JSON (REAL)
    # ---------------------------
    @staticmethod
    async def set_json(key: str, value: Dict, ex: Optional[int] = None):
        """
        Store JSON document
        """
        _client = get_redis()
        await _client.json().set(key, "$", value)

        if ex:
            await _client.expire(key, ex)

    @staticmethod
    async def get_json(key: str) -> Optional[Dict]:
        """
        Get full JSON document
        """
        _client = get_redis()
        return await _client.json().get(key)

    @staticmethod
    async def update_json(key: str, updates: Dict):
        """
        Partial update (top-level fields)
        """
        _client = get_redis()
        for field, value in updates.items():
            await _client.json().set(key, f"$.{field}", value)

        return await _client.json().get(key)

    @staticmethod
    async def delete_json(key: str):
        """
        Delete JSON document
        """
        _client = get_redis()
        await _client.delete(key)
    # ---------------------------
    # 🔹 LIST OPERATIONS
    # ---------------------------
    @staticmethod
    async def push_to_list(key: str, value: str):
        _client = get_redis()
        await _client.lpush(key, value)

    @staticmethod
    async def get_list(key: str) -> List[str]:
        _client = get_redis()
        return await _client.lrange(key, 0, -1)

    # ---------------------------
    # 🔹 CACHE HELPERS
    # ---------------------------
    @staticmethod
    async def cache_set(key: str, value: Dict, ttl: int =2000):
        cached_key = f"cache:user:{key}"
        await RedisService.set_json(cached_key, value, ex=ttl)

    @staticmethod
    async def cache_get(key: str) -> Optional[Dict]:
        cached_key = f"cache:user:{key}"
        return await RedisService.get_json(cached_key)
    @staticmethod
    async def delete_cache(key: str):
        cached_key = f"cache:user:{key}"
        await RedisService.delete(cached_key)   
    # ---------------------------
    # 🔹 METRICS
    # ---------------------------
    @staticmethod
    async def increment(key: str):
        _client = get_redis()
        id = await _client.incr(key)
        return id

    @staticmethod
    async def get_metric(key: str) -> int:
        _client = get_redis()
        value = await _client.get(key)
        return int(value) if value else 0

    # ---------------------------
    # 🔹 STREAMS
    # ---------------------------
    @staticmethod
    async def add_to_stream(stream: str, data: Dict):
        _client = get_redis()
        await _client.xadd(stream, data)

    @staticmethod
    async def read_stream(stream: str, last_id="0"):
        _client = get_redis()
        return await _client.xread({stream: last_id}, block=5000)