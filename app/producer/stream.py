import json
from redis.asyncio import Redis

from app.db.redis_client import get_redis

# redis = Redis(host="localhost", port=6379, decode_responses=True)

STREAM_NAME = "user:stream"

async def publish_user_created(user: dict):
    _client = get_redis()
    print("Before Publishing to stream:", user)
    await _client.xadd(
        STREAM_NAME,
        {
            "event": "user_created",
            "data": json.dumps(user)
        }
    )
    print("After Publishing to stream:", user)