from http import HTTPStatus

import allure
import requests

from services.cards.card_link_attributes.endpoints import Endpoints
from services.cards.card_link_attributes.models.card_link_attributes_model import (
    CardLinkAttributeItemModel,
    CardLinkAttributesModel,
)
from src.support.helper import Helper


class CardLinkAttributesAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cards/{token}/cardLink/attributes")
    def get_card_link_attributes(self, token: str) -> tuple[requests.Response, CardLinkAttributesModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_link_attributes_endpoint.format(token=token),
            headers={"Accept": "application/json"},
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, CardLinkAttributesModel(items=[])

        data = response.json()
        if isinstance(data, list):
            items = [CardLinkAttributeItemModel(**item) for item in data if isinstance(item, dict)]
        else:
            items = []
        return response, CardLinkAttributesModel(items=items)
