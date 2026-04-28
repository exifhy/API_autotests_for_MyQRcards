from http import HTTPStatus

import allure

from config.headers import Headers
from services.locations.location_by_id.endpoints import Endpoints
from services.locations.location_by_id.models.location_by_id_model import LocationByIdModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class LocationByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Locations/{location_id}")
    def get_location_by_id(self, location_id: int) -> LocationByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_location_by_id_endpoint.format(location_id=location_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        assert int(data["id"]) == int(location_id), (
            f"Expected location id={location_id}, got {data.get('id')}"
        )
        return LocationByIdModel(**data)

    @allure.step("GET /Locations/{location_id} without auth")
    def get_location_by_id_without_auth(self, location_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_location_by_id_endpoint.format(location_id=location_id),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
