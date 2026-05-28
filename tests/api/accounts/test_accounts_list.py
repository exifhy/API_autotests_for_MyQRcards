import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_list.api_accounts_list import AccountsListAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /accounts
    """
)
class TestAccountsList:
    @allure.title("GET /accounts returns list of accounts")
    @pytest.mark.smoke
    def test_accounts_list_200_or_206(self, cfg):
        response, model = AccountsListAPI().get_accounts(range_header="items=0-199")

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "Expected Content-Range header for 206 response"

        assert isinstance(model.items, list)
        if model.items:
            assert model.items[0].id is not None

        lk_account_id = cfg.get("lk_account_id")
        if lk_account_id:
            ids = {item.id for item in model.items}
            assert int(lk_account_id) in ids, (
                f"lk_account_id={lk_account_id} not found in returned list"
            )

    @allure.title("GET /accounts without auth")
    @pytest.mark.ng
    def test_accounts_list_401_without_auth(self):
        response = AccountsListAPI().get_accounts_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
