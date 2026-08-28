from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_indexing_update.endpoints import Endpoints
from services.cards.card_indexing_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardIndexingUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/{card_id}/indexing")
    def update_card_indexing(self, card_id: int, is_indexable: bool):
        payload = Payloads.build_card_indexing_payload(is_indexable)
        response = self._call(
            "PUT",
            url=self.endpoints.update_card_indexing_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response

    @allure.step("PUT /Cards/{card_id}/indexing (raw payload, no assert — for negative cases)")
    def update_card_indexing_raw(self, card_id, payload):
        return self._call(
            "PUT",
            url=self.endpoints.update_card_indexing_endpoint.format(card_id=card_id),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )

    @allure.step("PUT /Cards/{card_id}/indexing (without auth)")
    def update_card_indexing_without_auth(self, card_id: int, is_indexable: bool):
        payload = Payloads.build_card_indexing_payload(is_indexable)
        return self._call(
            "PUT",
            url=self.endpoints.update_card_indexing_endpoint.format(card_id=int(card_id)),
            headers=Headers.without_authorization_field_header(),
            json=payload,
        )
