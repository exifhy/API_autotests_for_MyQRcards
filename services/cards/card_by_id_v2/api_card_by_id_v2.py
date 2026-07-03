from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_by_id_v2.endpoints import Endpoints
from services.cards.card_by_id_v2.models.card_by_id_v2_model import CardByIdV2Model
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardByIdV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}/V2")
    def get_card_by_id_v2(
        self, card_id: int, *, all_data: bool = False, token: str | None = None
    ) -> CardByIdV2Model:
        params = {"AllData": "true"} if all_data else {}
        response = self._call(
            "GET",
            url=self.endpoints.get_card_by_id_v2_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=token or get_token()),
            params=params,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return CardByIdV2Model(**response.json())
