from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.cards_show.endpoints import Endpoints
from services.cards.cards_show.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardsShowAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/show")
    def show_cards(self, *items: dict):
        payload = Payloads.build_cards_show_payload(*items)
        response = self._call(
            "PUT",
            url=self.endpoints.show_cards_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response
