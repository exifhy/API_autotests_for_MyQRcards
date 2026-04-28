from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cardlinks.cardlink_unassign.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLinkUnassignAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /cardlinks/{card_link}/unassign")
    def unassign_cardlink(self, card_link: str) -> requests.Response:
        response = self._call(
            "PUT",
            url=self.endpoints.unassign_cardlink_endpoint.format(card_link=card_link),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
            HTTPStatus.CONFLICT,
            HTTPStatus.FORBIDDEN,
        ), f"Expected 200/202/204/409/403, got {response.status_code}: {response.text}"
        return response
