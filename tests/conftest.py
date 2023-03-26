import pytest
from django.test import Client


@pytest.fixture(scope="module")
def client() -> Client:
    return Client()
