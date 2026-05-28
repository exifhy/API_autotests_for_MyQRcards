from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cards.card_link_attribute_counter.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLinkAttributeCounterAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /cards/{token}/cardLink/attributes/click")
    def add_attribute_click(self, token: str, payload: dict) -> requests.Response:
        response = self._call(
            "PUT",
            url=self.endpoints.card_link_attribute_counter_endpoint.format(token=token),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ), f"Expected 200/202/204, got {response.status_code}: {response.text}"
        return response
