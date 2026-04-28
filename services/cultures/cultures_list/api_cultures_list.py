from http import HTTPStatus

import allure

from config.headers import Headers
from services.cultures.cultures_list.endpoints import Endpoints
from services.cultures.cultures_list.models.cultures_list_model import (
    CultureItemModel,
    CulturesListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class CulturesListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cultures")
    def get_cultures(
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
            url=self.endpoints.get_cultures_list_endpoint,
            headers=Headers.auth_header(bearer_token=get_token(), Range=range_header),
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CultureItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CulturesListModel(items=items)

    @allure.step("GET /Cultures without auth")
    def get_cultures_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_cultures_list_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response

