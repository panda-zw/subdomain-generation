from dotenv import load_dotenv
import os
from upstash_redis import Redis

load_dotenv()  # Load environment variables from a .env.local file

# Get the Redis URL from environment variables
UPSTASH_REDIS_URL = os.getenv("UPSTASH_REDIS_URL")
UPSTASH_REDIS_TOKEN = os.getenv("UPSTASH_REDIS_TOKEN")

# Initialize the Redis connection pool
redis = Redis(url=UPSTASH_REDIS_URL, token=UPSTASH_REDIS_TOKEN)


async def get_redis() -> Redis:
    return redis


async def is_subdomain_valid(subdomain: str) -> bool:
    # Check if the subdomain exists in the Redis Set
    return redis.sismember("valid_subdomains", subdomain)

async def add_subdomain(subdomain: str):
    # Add subdomain to the Redis Set
    redis.sadd("valid_subdomains", subdomain)

