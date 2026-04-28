from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_custom_message_templates_update.endpoints import Endpoints
from services.cards.card_custom_message_templates_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardCustomMessageTemplatesUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/{card_id}/customMessageTemplates")
    def update_card_custom_message_templates(self, card_id: int):
        # Legacy card-scoped branch kept only for compatibility. Prefer
        # Accounts/CustomMessageTemplates for new work and new tests.
        payload = Payloads.build_card_custom_message_templates_update_payload()
        response = self._call(
            "PUT",
            url=self.endpoints.update_card_custom_message_templates_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, payload
