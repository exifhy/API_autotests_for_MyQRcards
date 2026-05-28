from http import HTTPStatus

import allure

from config.headers import Headers
from services.subscriptions.subscription_get.endpoints import Endpoints
from services.subscriptions.subscription_get.models.subscription_get_model import SubscriptionGetModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionGetAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Subscriptions/{sub_id}/account/{account_id}")
    def get_subscription(self, sub_id: int, account_id: int) -> SubscriptionGetModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_endpoint.format(
                sub_id=int(sub_id),
                account_id=int(account_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        if response.status_code == HTTPStatus.NOT_FOUND or not response.text:
            return SubscriptionGetModel()

        data = response.json()
        resp_id = data.get("id", data.get("Id"))
        assert resp_id is not None, f"No id field in response: {data}"
        assert int(resp_id) == int(sub_id), f"Expected subscription id={sub_id}, got {resp_id}"

        normalized = {
            "id": int(resp_id),
            "accountID": data.get("accountID", data.get("AccountID")),
            "name": data.get("name", data.get("Name")),
        }
        return SubscriptionGetModel(**normalized)

    @allure.step("GET /Subscriptions/{sub_id}/account/{account_id} without auth")
    def get_subscription_without_auth(self, sub_id: int, account_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_endpoint.format(
                sub_id=int(sub_id),
                account_id=int(account_id),
            ),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN, HTTPStatus.NOT_FOUND), (
            f"Expected 401/403/404, got {response.status_code} {response.text}"
        )
        return response
