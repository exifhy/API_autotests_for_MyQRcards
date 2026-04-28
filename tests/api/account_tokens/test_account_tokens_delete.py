import allure
import pytest
from http import HTTPStatus

from services.account_tokens.account_tokens_add.api_account_tokens_add import AccountTokensAddAPI
from services.account_tokens.account_tokens_delete.api_account_tokens_delete import AccountTokensDeleteAPI


@allure.epic("API")
@allure.feature("AccountTokens")
@pytest.mark.api
@allure.description(
    """
    POST /accounttokens/ -> DELETE /accounttokens/{token}
    """
)
class TestAccountTokensDelete:
    @allure.title("POST /accounttokens/ -> DELETE /accounttokens/{token}")
    @pytest.mark.smoke
    def test_account_tokens_delete_200(self):
        with allure.step("POST /accounttokens/ — create token"):
            _, created = AccountTokensAddAPI().add_account_token()
            assert created.token, "No token in POST response"
            token = created.token

        with allure.step(f"DELETE /accounttokens/{token}"):
            response = AccountTokensDeleteAPI().delete_account_token(token)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

    @pytest.mark.ng
    @allure.title("DELETE /accounttokens/{token} without auth -> 401/403")
    def test_account_tokens_delete_401_without_auth(self):
        response = AccountTokensDeleteAPI().delete_account_token_without_auth("faketoken")
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
