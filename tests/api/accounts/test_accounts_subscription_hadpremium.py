import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_subscription_hadpremium.api_accounts_subscription_hadpremium import (
    AccountsSubscriptionHadPremiumAPI,
)


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /accounts/subscription/hadpremium
    """
)
class TestAccountsSubscriptionHadPremium:
    @allure.title("GET /accounts/subscription/hadpremium returns boolean flag")
    @pytest.mark.smoke
    def test_accounts_subscription_hadpremium_200(self):
        model = AccountsSubscriptionHadPremiumAPI().get_accounts_subscription_hadpremium()

        assert isinstance(model.hasHadPremium, bool)

    @allure.title("GET /accounts/subscription/hadpremium without auth")
    @pytest.mark.ng
    def test_accounts_subscription_hadpremium_401_without_auth(self):
        response = AccountsSubscriptionHadPremiumAPI().get_accounts_subscription_hadpremium_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
