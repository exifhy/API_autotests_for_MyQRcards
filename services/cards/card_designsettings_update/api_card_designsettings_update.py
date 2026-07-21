from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_designsettings_update.endpoints import Endpoints
from services.cards.card_designsettings_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardDesignsettingsUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/{card_id}/designsettings")
    def update_card_designsettings(self, card_id: int):
        payload = Payloads.build_card_designsettings_update_payload()
        response = self._call(
            "PUT",
            url=self.endpoints.update_card_designsettings_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, payload

    @allure.step("PUT /Cards/{card_id}/designsettings (raw payload, no assert — for font positive/negative cases)")
    def merge_card_designsettings_raw(self, card_id: int, payload: dict):
        return self._call(
            "PUT",
            url=self.endpoints.update_card_designsettings_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )

