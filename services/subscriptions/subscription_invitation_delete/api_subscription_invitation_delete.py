from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_invitation_delete.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionInvitationDeleteAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Subscriptions/{sub_id}/invitation/{invite_id}")
    def delete_subscription_invitation(self, sub_id: int, invite_id: int) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_subscription_invitation_endpoint.format(
                sub_id=int(sub_id),
                invite_id=int(invite_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
            HTTPStatus.NOT_FOUND,
        ), f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT/HTTPStatus.NOT_FOUND, got {response.status_code}: {response.text}"
        return response
