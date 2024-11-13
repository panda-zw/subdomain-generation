# test_main.py
import pytest
from httpx import AsyncClient
from main import app
from database import db

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_organization(async_client):
    # Clean up before test
    await db.organizations.delete_many({"subdomain": "awesome-inc"})

    # Test creating a new organization
    response = await async_client.post("/create-organization", json={"name": "Awesome Inc"})
    assert response.status_code == 200
    data = response.json()
    assert data["subdomain"] == "awesome-inc"

    # Test creating a duplicate organization
    response = await async_client.post("/create-organization", json={"name": "Awesome Inc"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Subdomain is already in use."

    # Clean up after test
    await db.organizations.delete_many({"subdomain": "awesome-inc"})
