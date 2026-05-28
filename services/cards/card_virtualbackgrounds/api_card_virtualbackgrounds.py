import allure
from http import HTTPStatus

from config.headers import Headers
from services.cards.card_virtualbackgrounds.endpoints import Endpoints
from services.virtual_backgrounds.virtual_backgrounds_list.models.virtual_backgrounds_model import (
    VirtualBackgroundItemModel,
    VirtualBackgroundsModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardVirtualBackgroundsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}/virtualbackground")
    def get_card_virtualbackgrounds(self, card_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.card_virtualbackgrounds_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"

        data = response.json()
        items = [VirtualBackgroundItemModel(**item) for item in data if isinstance(item, dict)]
        return response, VirtualBackgroundsModel(items=items)
