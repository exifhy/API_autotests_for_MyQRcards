from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_custom_message_templates_delete.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardCustomMessageTemplatesDeleteAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Cards/{card_id}/customMessageTemplates")
    def delete_card_custom_message_templates(self, card_id: int):
        # Legacy card-scoped branch kept only for compatibility. Prefer
        # Accounts/CustomMessageTemplates for new work and new tests.
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_card_custom_message_templates_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response
