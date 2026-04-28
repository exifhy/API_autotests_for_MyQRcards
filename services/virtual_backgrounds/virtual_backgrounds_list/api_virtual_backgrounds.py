from http import HTTPStatus

import allure

from config.headers import Headers
from services.virtual_backgrounds.virtual_backgrounds_list.endpoints import Endpoints
from services.virtual_backgrounds.virtual_backgrounds_list.models.virtual_backgrounds_model import (
    VirtualBackgroundItemModel,
    VirtualBackgroundsModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class VirtualBackgroundsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /VirtualBackgrounds")
    def get_virtual_backgrounds(
        self,
        *,
        range_header: str = "items=0-199",
        offset: int | None = None,
        fetch: int | None = None,
    ):
        params: dict[str, str] = {}
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)

        response = self._call(
            "GET",
            url=self.endpoints.get_virtual_backgrounds_endpoint,
            headers=Headers.auth_header(bearer_token=get_token(), Range=range_header),
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [VirtualBackgroundItemModel(**item) for item in data if isinstance(item, dict)]
        return response, VirtualBackgroundsModel(items=items)

    @allure.step("GET /VirtualBackgrounds without auth")
    def get_virtual_backgrounds_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_virtual_backgrounds_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response

