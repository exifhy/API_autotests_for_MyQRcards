import allure
import pytest
from http import HTTPStatus

from services.account_tokens.account_tokens_add.api_account_tokens_add import AccountTokensAddAPI


@allure.epic("API")
@allure.feature("AccountTokens")
@pytest.mark.api
@allure.description(
    """
    POST /accounttokens/
    """
)
class TestAccountTokensAdd:
    @allure.title("POST /accounttokens/ -> 201 Created")
    @pytest.mark.smoke
    def test_account_tokens_add_201(self):
        response, model = AccountTokensAddAPI().add_account_token()

        assert response.status_code == HTTPStatus.CREATED
        assert model.token is not None

    @pytest.mark.ng
    @allure.title("POST /accounttokens/ without auth -> 401/403")
    def test_account_tokens_add_401_without_auth(self):
        response = AccountTokensAddAPI().add_account_token_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
