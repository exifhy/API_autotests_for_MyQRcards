from http import HTTPStatus

import allure
import requests

from services.cards.card_attributes_list_v2.models.card_attributes_list_v2_model import (
    CardAttributeNodeV2Model,
)
from services.cards.card_link_attributes_v2.endpoints import Endpoints
from src.support.helper import Helper


class CardLinkAttributesV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_link}/cardLink/attributes/V2 (public, no auth)")
    def get_cardlink_attributes_v2(self, card_link: str) -> tuple[requests.Response, list[CardAttributeNodeV2Model]]:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_link_attributes_v2_endpoint.format(token=card_link),
            headers={"Accept": "application/json"},
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, []
        roots = [CardAttributeNodeV2Model(**item) for item in response.json()]
        return response, roots
