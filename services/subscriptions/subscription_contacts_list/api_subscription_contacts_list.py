from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_contacts_list.endpoints import Endpoints
from services.subscriptions.subscription_contacts_list.models.subscription_contacts_list_model import (
    SubscriptionContactItemModel,
    SubscriptionContactsListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionContactsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Subscriptions/{sub_id}/contacts")
    def get_subscription_contacts(
        self,
        sub_id: int,
        *,
        account_id: int | None = None,
    ) -> tuple[requests.Response, SubscriptionContactsListModel]:
        params = {}
        if account_id is not None:
            params["accountID"] = account_id
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_contacts_endpoint.format(sub_id=int(sub_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            params=params,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, SubscriptionContactsListModel(items=[])

        data = response.json()
        if isinstance(data, list):
            items = [SubscriptionContactItemModel(**item) for item in data if isinstance(item, dict)]
        else:
            items = []
        return response, SubscriptionContactsListModel(items=items)

    @allure.step("GET /Subscriptions/{sub_id}/contacts without auth")
    def get_subscription_contacts_without_auth(self, sub_id: int, *, account_id: int | None = None) -> requests.Response:
        params = {}
        if account_id is not None:
            params["accountID"] = account_id
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_contacts_endpoint.format(sub_id=int(sub_id)),
            headers=Headers.without_authorization_field_header(),
            params=params,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
