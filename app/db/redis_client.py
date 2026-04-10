import redis.asyncio as redis
import os
from dotenv import load_dotenv
from typing import Optional
from app.config.logging import logger

# Global client (singleton)

redis_client: Optional[redis.Redis] = None

def get_redis():
    if redis_client is None:
        raise RuntimeError("Redis not connected")
    return redis_client
async def connect_redis(url: str)-> None:
    global redis_client
    redis_client = redis.from_url(url,decode_responses=True ) # return str instead of bytes

    try:
        await redis_client.ping()
        logger.info("Connected to Redis successfully!")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise 


async def disconnect_redis() -> None:
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Disconnected from Redis successfully!")