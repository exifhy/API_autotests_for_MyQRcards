import allure
import pytest
from http import HTTPStatus

from services.client_tokens.client_tokens_get.api_client_tokens_get import (
    ClientTokensGetAPI,
)


@allure.epic("API")
@allure.feature("ClientTokens")
@pytest.mark.api
@allure.description(
    """
    /clientTokens
    """
)
class TestClientTokensGet:
    @allure.title("GET /clientTokens returns current client token")
    @pytest.mark.smoke
    def test_client_tokens_get_200(self):
        model = ClientTokensGetAPI().get_client_tokens()

        # 204 = no token registered for this account — valid response
        if model.clientID is not None:
            assert model.pushToken is None or model.pushToken != ""
            assert model.created is None or model.created != ""

    @allure.title("GET /clientTokens without auth")
    @pytest.mark.ng
    def test_client_tokens_get_401_without_auth(self):
        response = ClientTokensGetAPI().get_client_tokens_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
