import allure
import pytest
from http import HTTPStatus

from services.account_tokens.account_tokens_add.api_account_tokens_add import AccountTokensAddAPI
from services.account_tokens.account_tokens_get.api_account_tokens_get import AccountTokensGetAPI


@allure.epic("API")
@allure.feature("AccountTokens")
@pytest.mark.api
@allure.description(
    """
    POST /accounttokens/ -> GET /accounttokens/{token}
    """
)
class TestAccountTokensGet:
    @allure.title("POST /accounttokens/ -> GET /accounttokens/{token} -> 200")
    @pytest.mark.smoke
    def test_account_tokens_get_200(self):
        with allure.step("POST /accounttokens/ — create token"):
            _, created = AccountTokensAddAPI().add_account_token()
            assert created.token, "No token in POST response"
            token = created.token

        with allure.step(f"GET /accounttokens/{token}"):
            response, model = AccountTokensGetAPI().get_account_token(token)

        assert response.status_code == HTTPStatus.OK
        assert model.token == token

    @pytest.mark.ng
    @allure.title("GET /accounttokens/{token} without auth -> 401/403")
    def test_account_tokens_get_401_without_auth(self):
        response = AccountTokensGetAPI().get_account_token_without_auth("faketoken")
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
