from http import HTTPStatus

import allure

from services.cardlinks.cardlink_designsettings.endpoints import Endpoints
from services.cardlinks.cardlink_designsettings.models.cardlink_designsettings_model import (
    CardLinkDesignsettingsModel,
)
from src.support.helper import Helper


class CardLinkDesignsettingsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cardLinks/{card_link}/designsettings")
    def get_cardlink_designsettings(self, card_link: str) -> CardLinkDesignsettingsModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_cardlink_designsettings_endpoint.format(card_link=card_link),
            headers={"Accept": "application/json"},
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return CardLinkDesignsettingsModel(**data)
