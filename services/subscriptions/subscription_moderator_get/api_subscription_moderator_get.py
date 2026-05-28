from http import HTTPStatus

import allure

from config.headers import Headers
from services.subscriptions.subscription_moderator_get.endpoints import Endpoints
from services.subscriptions.subscription_moderator_get.models.subscription_moderator_get_model import (
    SubscriptionModeratorGetModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionModeratorGetAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /subscriptions/{sub_id}/moderators/{account_id}")
    def get_subscription_moderator(self, sub_id: int, account_id: int) -> SubscriptionModeratorGetModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_moderator_endpoint.format(
                sub_id=int(sub_id),
                account_id=int(account_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        resp_account_id = data.get("accountID", data.get("AccountID"))
        assert resp_account_id is not None, f"No accountID field in response: {data}"
        assert int(resp_account_id) == int(account_id), (
            f"Expected accountID={account_id}, got {resp_account_id}"
        )
        return SubscriptionModeratorGetModel(
            accountID=resp_account_id,
            cardID=data.get("cardID", data.get("CardID")),
            email=data.get("email", data.get("Email")),
        )
