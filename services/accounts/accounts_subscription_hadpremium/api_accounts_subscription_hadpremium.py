from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_subscription_hadpremium.endpoints import Endpoints
from services.accounts.accounts_subscription_hadpremium.models.accounts_subscription_hadpremium_model import (
    AccountsSubscriptionHadPremiumModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsSubscriptionHadPremiumAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/subscription/hadpremium")
    def get_accounts_subscription_hadpremium(self) -> AccountsSubscriptionHadPremiumModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_subscription_hadpremium_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        assert "hasHadPremium" in data, f"'hasHadPremium' missing in response: {data}"
        return AccountsSubscriptionHadPremiumModel(**data)

    @allure.step("GET /accounts/subscription/hadpremium without auth")
    def get_accounts_subscription_hadpremium_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_subscription_hadpremium_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response

