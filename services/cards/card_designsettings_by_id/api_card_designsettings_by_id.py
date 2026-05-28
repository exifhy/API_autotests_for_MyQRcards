from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_designsettings_by_id.endpoints import Endpoints
from services.cards.card_designsettings_by_id.models.card_designsettings_by_id_model import (
    CardDesignsettingsByIdModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardDesignsettingsByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}/designSettings")
    def get_card_designsettings_by_id(self, card_id: int) -> CardDesignsettingsByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_designsettings_by_id_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        assert int(data["cardID"]) == int(card_id), (
            f"Expected cardID={card_id}, got {data.get('cardID')}"
        )
        return CardDesignsettingsByIdModel(**data)

    @allure.step("GET /Cards/{card_id}/designSettings without auth")
    def get_card_designsettings_by_id_without_auth(self, card_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_card_designsettings_by_id_endpoint.format(card_id=int(card_id)),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response

