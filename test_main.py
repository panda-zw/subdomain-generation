# test_main.py
import pytest
from httpx import AsyncClient
from main import app
from redis.asyncio import Redis

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="module")
async def redis_client():
    # Initialize a Redis client (assuming REDIS_URL is your connection URL)
    redis = Redis.from_url("redis://localhost:6379/0", decode_responses=True)
    yield redis
    await redis.close()  # Close the connection after tests

@pytest.mark.asyncio
async def test_create_organization(async_client, redis_client):
    # Clean up before test by removing any existing subdomain in Redis
    await redis_client.srem("valid_subdomains", "awesome-inc")

    # Test creating a new organization
    response = await async_client.post("/create-organization", json={"name": "Awesome Inc"})
    assert response.status_code == 200
    data = response.json()
    assert data["subdomain"] == "awesome-inc"

    # Verify that the subdomain was added to Redis
    is_subdomain_in_redis = await redis_client.sismember("valid_subdomains", "awesome-inc")
    assert is_subdomain_in_redis

    # Test creating a duplicate organization
    response = await async_client.post("/create-organization", json={"name": "Awesome Inc"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Subdomain is already in use."

    # Clean up after test by removing the subdomain from Redis
    await redis_client.srem("valid_subdomains", "awesome-inc")
