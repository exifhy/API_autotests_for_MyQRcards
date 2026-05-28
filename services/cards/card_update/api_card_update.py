from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_update.endpoints import Endpoints
from services.cards.card_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/{card_id}")
    def update_card(self, card_id: int, *, company_id: int):
        payload = Payloads.build_card_update_payload(company_id=company_id)
        response = self._call(
            "PUT",
            url=self.endpoints.update_card_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, payload

