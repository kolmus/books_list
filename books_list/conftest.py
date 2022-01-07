from manager_app.tests.utils import create_fake_book
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def set_up():
    for i in range(15):
        create_fake_book()


@pytest.fixture
def set_up2():
    client = APIClient()

    import_data = {
        "title": "ogniem",
        "author": "sienkiewicz",
    }
    response = client.post("/books/import/", import_data)

    return response
