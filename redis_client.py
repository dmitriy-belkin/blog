import aioredis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis = None


async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.create_redis_pool(REDIS_URL)
    return redis


async def close_redis():
    global redis
    if redis:
        redis.close()
        await redis.wait_closed()
