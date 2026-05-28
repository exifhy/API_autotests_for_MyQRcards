from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cardlinks.cardlink_statistic_view.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLinkStatisticViewAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /cardlinks/{card_link}/statisticview")
    def add_statistic_view(self, card_link: str) -> requests.Response:
        response = self._call(
            "PUT",
            url=self.endpoints.cardlink_statistic_view_endpoint.format(card_link=card_link),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )
        return response
