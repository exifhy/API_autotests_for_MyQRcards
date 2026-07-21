from http import HTTPStatus

import allure

from config.headers import Headers
from services.fonts.fonts_list.endpoints import Endpoints
from services.fonts.fonts_list.models.fonts_list_model import FontItemModel, FontsListModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class FontsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /fonts")
    def get_fonts(self) -> FontsListModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_fonts_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        return FontsListModel(items=[FontItemModel(**item) for item in data])

    @allure.step("GET /fonts without auth")
    def get_fonts_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_fonts_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response
