from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_moderators_list.endpoints import Endpoints
from services.subscriptions.subscription_moderators_list.models.subscription_moderators_list_model import (
    SubscriptionModeratorItemModel,
    SubscriptionModeratorsListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionModeratorsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /subscriptions/{sub_id}/moderators")
    def get_subscription_moderators(self, sub_id: int) -> tuple[requests.Response, SubscriptionModeratorsListModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_moderators_endpoint.format(sub_id=int(sub_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, SubscriptionModeratorsListModel(items=[])

        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)} / {data}"
        items = [
            SubscriptionModeratorItemModel(
                accountID=item.get("accountID", item.get("AccountID")),
                cardID=item.get("cardID", item.get("CardID")),
                email=item.get("email", item.get("Email")),
            )
            for item in data
            if isinstance(item, dict)
        ]
        return response, SubscriptionModeratorsListModel(items=items)
