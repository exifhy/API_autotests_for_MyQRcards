from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cards.card_attributes_list_v2.endpoints import Endpoints
from services.cards.card_attributes_list_v2.models.card_attributes_list_v2_model import (
    CardAttributeNodeV2Model,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardAttributesListV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}/attributes/V2")
    def get_card_attributes_v2(self, card_id: int) -> tuple[requests.Response, list[CardAttributeNodeV2Model]]:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_attributes_v2_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, []
        roots = [CardAttributeNodeV2Model(**item) for item in response.json()]
        return response, roots

    @allure.step("GET /Cards/{card_id}/attributes/V2 (raw, no assert — for negative cases)")
    def get_card_attributes_v2_raw(self, card_id) -> requests.Response:
        return self._call(
            "GET",
            url=self.endpoints.get_card_attributes_v2_endpoint.format(card_id=card_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )

    @allure.step("GET /Cards/{card_id}/attributes/V2 without auth")
    def get_card_attributes_v2_without_auth(self, card_id: int) -> requests.Response:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_attributes_v2_endpoint.format(card_id=int(card_id)),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
