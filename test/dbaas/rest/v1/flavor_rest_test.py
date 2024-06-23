from fastapi.testclient import TestClient
from starlette import status

from dbaas.api import app
from dbaas.rest.v1.flavor_rest import BASE_URL

client = TestClient(app)


class TestFlavorRest:
    def test_should_get_flavors(self):

        response = client.get(BASE_URL)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 3
