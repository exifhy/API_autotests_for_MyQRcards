from http import HTTPStatus

import allure

from services.cardlinks.cardlink_card.endpoints import Endpoints
from services.cardlinks.cardlink_card.models.cardlink_card_model import CardLinkCardModel
from src.support.helper import Helper


class CardLinkCardAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cardLinks/{card_link}/card")
    def get_cardlink_card(self, card_link: str) -> CardLinkCardModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_cardlink_card_endpoint.format(card_link=card_link),
            headers={"Accept": "application/json"},
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return CardLinkCardModel(**response.json())
