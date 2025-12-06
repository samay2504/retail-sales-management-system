"""Tests for API routes."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.index import app
from src.models import get_db


@pytest.mark.asyncio
async def test_health_endpoint(db_session: AsyncSession):
    """Test health check endpoint."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/health")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_root_endpoint(db_session: AsyncSession):
    """Test root endpoint."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TruEstate API"
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_transactions_endpoint_empty(db_session: AsyncSession):
    """Test transactions endpoint with empty database."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/transactions")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "meta" in data
    assert len(data["items"]) == 0
    assert data["meta"]["total"] == 0


@pytest.mark.asyncio
async def test_transactions_endpoint_with_data(db_session: AsyncSession, sample_transactions):
    """Test transactions endpoint with sample data."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/transactions")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["meta"]["total"] == 3
    assert data["meta"]["page"] == 1
    assert data["meta"]["limit"] == 10


@pytest.mark.asyncio
async def test_filter_metadata_endpoint(db_session: AsyncSession, sample_transactions):
    """Test filter metadata endpoint."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/meta/filters")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "customer_regions" in data
    assert "genders" in data
    assert "product_categories" in data
    assert len(data["customer_regions"]) > 0
