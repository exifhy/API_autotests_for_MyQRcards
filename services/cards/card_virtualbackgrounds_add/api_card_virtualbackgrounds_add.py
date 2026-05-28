from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_virtualbackgrounds_add.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardVirtualBackgroundsAddAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Cards/{card_id}/virtualbackground")
    def add_card_virtualbackgrounds(self, card_id: int, background_ids: list[int]):
        response = self._call(
            "POST",
            url=self.endpoints.card_virtualbackgrounds_add_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=background_ids,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )
        return response
