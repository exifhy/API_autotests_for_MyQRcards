from http import HTTPStatus

import allure

from config.headers import Headers
from services.subscriptions.subscription_prices.endpoints import Endpoints
from services.subscriptions.subscription_prices.models.subscription_prices_model import (
    SubscriptionPricesItemModel,
    SubscriptionPricesModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionPricesAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /SubscriptionPrices")
    def get_subscription_prices(self) -> SubscriptionPricesModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_prices_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}: {data}"
        return SubscriptionPricesModel(
            items=[SubscriptionPricesItemModel(**item) for item in data]
        )

    @allure.step("GET /SubscriptionPrices without auth")
    def get_subscription_prices_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_prices_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        return response
