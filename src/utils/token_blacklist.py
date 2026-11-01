import os
import time

import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://default:YourSecurePasswordHere@redis-cache:6379/0")

client = redis.from_url(REDIS_URL, decode_responses=True)

PREFIX = "blacklist:token:"


async def add_token(token: str, exp: int | None = None):
    # keep the entry only until the token would have expired anyway
    ttl = max(int(exp - time.time()), 1) if exp else 60 * 60
    await client.set(PREFIX + token, "1", ex=ttl)


async def is_blacklisted(token: str) -> bool:
    return bool(await client.exists(PREFIX + token))
