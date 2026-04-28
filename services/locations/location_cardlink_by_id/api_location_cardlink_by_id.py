from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.locations.location_cardlink_by_id.endpoints import Endpoints
from services.locations.location_cardlink_by_id.models.location_cardlink_by_id_model import LocationCardLinkByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class LocationCardLinkByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cards/attributes/locations/{location_id}/cardlink/{card_link_id}")
    def get_location_cardlink_by_id(
        self,
        location_id: int,
        card_link_id: str,
    ) -> tuple[requests.Response, LocationCardLinkByIdModel | None]:
        response = self._call(
            "GET",
            url=self.endpoints.get_location_cardlink_by_id_endpoint.format(
                location_id=int(location_id),
                card_link_id=card_link_id,
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, None

        data = response.json()
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return response, LocationCardLinkByIdModel(**data)
