from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.cards_hide.endpoints import Endpoints
from services.cards.cards_hide.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardsHideAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/hide")
    def hide_cards(self, *items: dict):
        payload = Payloads.build_cards_hide_payload(*items)
        response = self._call(
            "PUT",
            url=self.endpoints.hide_cards_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response
