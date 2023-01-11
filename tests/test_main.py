from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
async def client() -> AsyncGenerator[TestClient, None]:
    from app.main import app

    yield TestClient(app)


def test_root(client: TestClient) -> None:
    response = client.get("/")
    response.status_code == 200
    response.json() == {"message": "Hello World"}
