from dotenv import load_dotenv
import os
from redis.asyncio import Redis


load_dotenv()  # Load environment variables from a .env.local file

# Get the Redis URL from environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
# Initialize the Redis connection pool
redis = Redis.from_url(REDIS_URL, decode_responses=True)


async def get_redis() -> Redis:
    return redis


async def is_subdomain_valid(subdomain: str) -> bool:
    # Check if the subdomain exists in the Redis Set
    return await redis.sismember("valid_subdomains", subdomain)

async def add_subdomain(subdomain: str):
    # Add subdomain to the Redis Set
    await redis.sadd("valid_subdomains", subdomain)

