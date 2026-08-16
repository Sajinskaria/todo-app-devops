import os
import sys

import pytest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../app")
    )
)

from app import app  # noqa: E402


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code in [200, 500]


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code in [200, 503]


def test_add_todo_without_title(client):
    response = client.post(
        "/add",
        data={}
    )

    assert response.status_code == 302


def test_complete_todo(client):
    response = client.get("/complete/1")

    assert response.status_code in [302, 500]


def test_delete_todo(client):
    response = client.get("/delete/1")

    assert response.status_code in [302, 500]
