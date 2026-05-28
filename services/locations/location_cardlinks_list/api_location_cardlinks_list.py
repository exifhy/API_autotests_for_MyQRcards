from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.locations.location_cardlinks_list.endpoints import Endpoints
from services.locations.location_cardlinks_list.models.location_cardlinks_list_model import (
    LocationCardLinkItemModel,
    LocationCardLinksListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class LocationCardLinksListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cards/attributes/locations/cardlink/{card_link_id}")
    def get_location_cardlinks_list(
        self,
        card_link_id: str,
    ) -> tuple[requests.Response, LocationCardLinksListModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_location_cardlinks_list_endpoint.format(card_link_id=card_link_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, LocationCardLinksListModel(items=[])

        data = response.json()
        if isinstance(data, list):
            items = [LocationCardLinkItemModel(**item) for item in data if isinstance(item, dict)]
        else:
            items = []
        return response, LocationCardLinksListModel(items=items)
