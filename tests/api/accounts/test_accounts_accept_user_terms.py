import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_accept_user_terms.api_accounts_accept_user_terms import (
    AccountsAcceptUserTermsAPI,
)


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /accounts/this/acceptUserTerms
    """
)
class TestAccountsAcceptUserTerms:
    @allure.title("PUT /accounts/this/acceptUserTerms accepts terms")
    @pytest.mark.smoke
    def test_accounts_accept_user_terms_202(self):
        response, payload = AccountsAcceptUserTermsAPI().accept_user_terms()

        assert response.status_code == HTTPStatus.ACCEPTED
        assert payload["Timestamp"] == "9999-12-31T23:59:59"

    @allure.title("PUT /accounts/this/acceptUserTerms without auth")
    @pytest.mark.ng
    def test_accounts_accept_user_terms_401_without_auth(self):
        response, _ = AccountsAcceptUserTermsAPI().accept_user_terms_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
