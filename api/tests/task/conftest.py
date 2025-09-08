from fastapi.testclient import TestClient
from pytest import fixture

from .steps import Steps


@fixture
def steps(client: TestClient) -> Steps:
    return Steps(client)
