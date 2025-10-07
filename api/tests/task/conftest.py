from fastapi.testclient import TestClient
from pytest import fixture

from api.tests.auth.steps import Steps as AuthSteps

from .steps import Steps


@fixture
def steps(client: TestClient) -> Steps:
    auth_steps = AuthSteps(client)
    token = auth_steps.create_token()
    client.headers.update({"Authorization": f"Bearer {token}"})
    return Steps(client)
