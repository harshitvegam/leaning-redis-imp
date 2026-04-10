from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import os
from app.db import redis_client
from app.db.redis_client import connect_redis, disconnect_redis, get_redis
from dotenv import load_dotenv
from app.api import user
from app.services.redis_service import RedisService
from app.config.logging import logger
load_dotenv()  # Load environment variables from .env file


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize resources (e.g., database connections, Redis clients)
    logger.info("Starting up...")
    logger.info("Connecting to Redis...")
    logger.info(f"REDIS_URL: {os.getenv('REDIS_URL')}")
    await connect_redis(os.getenv("REDIS_URL"))
    yield  # This is where the application runs

    await disconnect_redis()
    # Clean up resources
    logger.info("Shutting down...")



app = FastAPI(lifespan=lifespan)




app.include_router(user.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/redis")
async def test_redis():
    # await redis redis call
    await redis_client.redis_client.set("test_key", "Hello Redis!")
    value = await redis_client.redis_client.get("test_key")
    return {"message": f"Hello from Redis! Value: {value}"}

@app.get("/test-json")
async def test_json():
    await RedisService.set_json("user:1", {
        "name": "Harshit",
        "email": "test@gmail.com"
    })

    await RedisService.update_json("user:1", {
        "name": "Updated"
    })

    data = await RedisService.get_json("user:1")

    return data