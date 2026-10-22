import redis.asyncio as redis


client = redis.from_url("redis://default:YourSecurePasswordHere@redis-cache:6373/0", decode_responses=True)


async def add_token(token:str):
    response = await client.sadd("blacklist:tokens",token)

        # blacklist.add(token)
    print("Token added", response)

async def is_blacklisted(token:str):
    is_blacklisted = await client.sismember("blacklist:tokens", token)
    print(is_blacklisted, "this is from is blacklisted")
    return bool(is_blacklisted)



