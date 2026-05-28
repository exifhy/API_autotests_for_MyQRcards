from http import HTTPStatus

import allure

from services.cardlinks.cardlink_short_card.endpoints import Endpoints
from services.cardlinks.cardlink_short_card.models.cardlink_short_card_model import (
    CardLinkShortCardModel,
)
from src.support.helper import Helper


class CardLinkShortCardAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cardLinks/{card_link}/short/card")
    def get_cardlink_short_card(self, card_link: str) -> CardLinkShortCardModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_cardlink_short_card_endpoint.format(card_link=card_link),
            headers={"Accept": "application/json"},
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return CardLinkShortCardModel(**response.json())
