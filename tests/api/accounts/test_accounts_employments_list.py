import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_employments_list.api_accounts_employments_list import (
    AccountsEmploymentsListAPI,
)


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    GET /accounts/{subscription_id}/employments
    """
)
class TestAccountsEmploymentsList:
    @allure.title("GET /accounts/{subscription_id}/employments returns employments dict as normalized list")
    def test_accounts_employments_list_200(self, cfg):
        subscription_id = cfg.get("subscription_id")
        assert subscription_id, "cfg['subscription_id'] is empty"

        response, model = AccountsEmploymentsListAPI().get_accounts_employments(int(subscription_id))

        assert response.status_code == HTTPStatus.OK
        assert isinstance(model.items, list)
        if model.items:
            first = model.items[0]
            assert first.accountID is not None
            assert first.cardID is not None
            assert first.defaultCardLinkUrl is None or first.defaultCardLinkUrl.startswith("http")
