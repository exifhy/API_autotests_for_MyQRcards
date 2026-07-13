from http import HTTPStatus
from typing import Optional

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
    def get_cardlink_by_id(self, card_link: str, is_skip_check: bool = False) -> Optional[CardLinkByIdModel]:
        params = {"IsSkipCheck": "true"} if is_skip_check else {}
        response = self._call(
            "GET",
            url=self.endpoints.get_cardlink_by_id_endpoint.format(card_link=card_link),
            headers=Headers.auth_header(bearer_token=get_token()),
            params=params,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200 or 204, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT:
            return None
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return CardLinkByIdModel(**data)
