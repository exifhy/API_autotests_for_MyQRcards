from http import HTTPStatus

import allure

from config.headers import Headers
from services.locations.locations_delete.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class LocationsDeleteAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Locations")
    def delete_locations(self, location_ids: list[int]):
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_locations_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=[int(location_id) for location_id in location_ids],
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
            HTTPStatus.NOT_FOUND,
        ), f"Unexpected status: {response.status_code} {response.text}"
        return response

