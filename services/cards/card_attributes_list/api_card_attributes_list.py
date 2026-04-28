from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cards.card_attributes_list.endpoints import Endpoints
from services.cards.card_attributes_list.models.card_attributes_list_model import (
    CardAttributeItemModel,
    CardAttributesListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardAttributesListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cards/{card_id}/attributes/")
    def get_card_attributes(
        self,
        card_id: int,
        *,
        attribute_id: int | None = None,
    ) -> tuple[requests.Response, CardAttributesListModel]:
        params = {"attributeID": str(attribute_id)} if attribute_id is not None else None
        response = self._call(
            "GET",
            url=self.endpoints.get_card_attributes_list_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            params=params,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, CardAttributesListModel(items=[])

        data = response.json()
        if isinstance(data, list):
            items = [CardAttributeItemModel(**item) for item in data if isinstance(item, dict)]
        else:
            items = []
        return response, CardAttributesListModel(items=items)

    @allure.step("GET /cards/{card_id}/attributes/ without auth")
    def get_card_attributes_without_auth(self, card_id: int) -> requests.Response:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_attributes_list_endpoint.format(card_id=int(card_id)),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
