from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cards.card_custom_message_templates.endpoints import Endpoints
from services.cards.card_custom_message_templates.models.card_custom_message_templates_model import CardCustomMessageTemplatesModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardCustomMessageTemplatesAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}/customMessageTemplates")
    def get_card_custom_message_templates(
        self,
        card_id: int,
        *,
        range_header: str | None = None,
        offset: int | None = None,
        fetch: int | None = None,
    ) -> tuple[requests.Response, CardCustomMessageTemplatesModel]:
        # Legacy card-scoped branch kept only for compatibility. Prefer
        # Accounts/CustomMessageTemplates for new work and new tests.
        params: dict[str, str] = {}
        if offset is not None:
            params['offset'] = str(offset)
        if fetch is not None:
            params['fetch'] = str(fetch)

        headers = Headers.auth_header(bearer_token=get_token())
        if range_header:
            headers['Range'] = range_header

        response = self._call(
            "GET",
            url=self.endpoints.get_card_custom_message_templates_endpoint.format(card_id=int(card_id)),
            headers=headers,
            params=params or None,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return response, CardCustomMessageTemplatesModel(**response.json())

    @allure.step("GET /Cards/{card_id}/customMessageTemplates without auth")
    def get_card_custom_message_templates_without_auth(self, card_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_card_custom_message_templates_endpoint.format(card_id=int(card_id)),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
