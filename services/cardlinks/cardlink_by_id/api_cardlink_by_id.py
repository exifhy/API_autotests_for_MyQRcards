from http import HTTPStatus

import allure

from config.headers import Headers
from services.cardlinks.cardlink_by_id.endpoints import Endpoints
from services.cardlinks.cardlink_by_id.models.cardlink_by_id_model import CardLinkByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLinkByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cardlinks/{card_link}")
    def get_cardlink_by_id(self, card_link: str) -> CardLinkByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_cardlink_by_id_endpoint.format(card_link=card_link),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return CardLinkByIdModel(**data)
