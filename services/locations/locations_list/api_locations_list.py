from http import HTTPStatus

import allure

from config.headers import Headers
from services.locations.locations_list.endpoints import Endpoints
from services.locations.locations_list.models.locations_list_model import (
    LocationListItemModel,
    LocationsListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class LocationsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Locations?locationID={location_id}")
    def get_locations_by_query_id(self, location_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_locations_list_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            params={"locationID": str(location_id)},
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json()
        assert isinstance(data, dict), f"Expected dict, got: {type(data)} / {data}"
        items = {
            str(key): LocationListItemModel(**value)
            for key, value in data.items()
            if isinstance(value, dict)
        }
        return response, LocationsListModel(items=items)

    @allure.step("GET /Locations without auth")
    def get_locations_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_locations_list_endpoint,
            headers=Headers.without_authorization_field_header(),
            params={"locationID": "1"},
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
