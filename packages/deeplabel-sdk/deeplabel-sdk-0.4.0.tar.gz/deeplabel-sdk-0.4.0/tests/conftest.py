import pytest
from  deeplabel.client import DeeplabelClient


@pytest.fixture(scope="session")
def client():
    token = "Dt7xLMNH-87MRYsUv-pXZJKJsF-y80klrmO"
    client = DeeplabelClient(token=token, restriction=False)
    return client

@pytest.fixture(scope="session")
def project_id():
    project_id = "635a32f66a9ded001ea0b912"
    return project_id

