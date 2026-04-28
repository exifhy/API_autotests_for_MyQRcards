from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_moderators_add.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionModeratorsAddAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /subscriptions/{sub_id}/moderators")
    def add_subscription_moderator(self, sub_id: int, account_id: int) -> requests.Response:
        response = self._call(
            "POST",
            url=self.endpoints.add_subscription_moderators_endpoint.format(sub_id=int(sub_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=[int(account_id)],
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
            HTTPStatus.CONFLICT,
        ), f"Expected HTTPStatus.OK/HTTPStatus.CREATED/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT/HTTPStatus.CONFLICT, got {response.status_code}: {response.text}"
        return response
