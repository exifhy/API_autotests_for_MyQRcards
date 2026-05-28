from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_moderators_delete.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionModeratorsDeleteAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /subscriptions/{sub_id}/moderators")
    def delete_subscription_moderator(self, sub_id: int, account_id: int) -> requests.Response:
        variants = [
            [int(account_id)],
            {"accountID": [int(account_id)]},
            {"accountID": int(account_id)},
        ]
        last = None
        for body in variants:
            response = self._call(
                "DELETE",
                url=self.endpoints.delete_subscription_moderators_endpoint.format(sub_id=int(sub_id)),
                headers=Headers.auth_header(bearer_token=get_token()),
                json=body,
            )
            last = response
            if response.status_code in (
                HTTPStatus.OK,
                HTTPStatus.ACCEPTED,
                HTTPStatus.NO_CONTENT,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.CONFLICT,
            ):
                return response
        assert last is not None, "DELETE moderator did not perform any request"
        raise AssertionError(f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT/HTTPStatus.NOT_FOUND/HTTPStatus.CONFLICT, got {last.status_code}: {last.text}")
