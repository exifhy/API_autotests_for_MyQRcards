from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_update_v2.endpoints import Endpoints
from services.cards.card_update_v2.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardUpdateV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/{card_id}/V2")
    def update_card_v2(self, card_id: int, *, company_id: int, gallery_attachment_ids: list[int] | None = None):
        payload = Payloads.build_card_update_v2_payload(
            company_id=company_id,
            gallery_attachment_ids=gallery_attachment_ids,
        )
        response = self._call(
            "PUT",
            url=self.endpoints.update_card_v2_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code in (HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )
        return response, payload
