import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_authorize.api_accounts_authorize import AccountsAuthorizeAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    POST /accounts/authorize
    """
)
class TestAccountsAuthorize:
    @allure.title("POST /accounts/authorize returns current account by token")
    def test_accounts_authorize_200(self):
        response, model = AccountsAuthorizeAPI().authorize_account()

        assert response.status_code == HTTPStatus.OK
        assert model.accountID is not None

    @allure.title("POST /accounts/authorize without auth")
    @pytest.mark.ng
    def test_accounts_authorize_401_without_auth(self):
        response = AccountsAuthorizeAPI().authorize_account_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
