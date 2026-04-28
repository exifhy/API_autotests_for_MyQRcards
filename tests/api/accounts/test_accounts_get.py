import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_get.api_accounts_get import AccountsGetAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /accounts/{id}
    """
)
class TestAccountsGet:
    @allure.title("GET /accounts/{id} returns account data")
    @pytest.mark.smoke
    def test_get_account_200(self, cfg):
        account_id = cfg.get("lk_account_id")
        assert account_id, "cfg['lk_account_id'] is empty"

        model = AccountsGetAPI().get_account(int(account_id))

        assert model.id == int(account_id)
        assert model.email is None or "@" in model.email

    @allure.title("GET /accounts/{id} without auth")
    @pytest.mark.ng
    def test_get_account_401_without_auth(self, cfg):
        account_id = cfg.get("lk_account_id")
        assert account_id, "cfg['lk_account_id'] is empty"

        response = AccountsGetAPI().get_account_without_auth(int(account_id))
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
