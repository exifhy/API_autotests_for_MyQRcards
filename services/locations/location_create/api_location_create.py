from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.locations.location_create.endpoints import Endpoints
from services.locations.location_create.models.location_create_model import LocationCreateModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class LocationCreateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Locations")
    def create_location(self, payload: dict) -> tuple[requests.Response, LocationCreateModel]:
        response = self._call(
            "POST",
            url=self.endpoints.create_location_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        location_id = data.get("id") or data.get("locationID") or data.get("LocationID")
        assert location_id, f"No location id in response: {data}"
        return response, LocationCreateModel(id=int(location_id))

