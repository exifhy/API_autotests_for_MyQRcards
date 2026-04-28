from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cardlinks.cardlink_catalog_by_id.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardLinkCatalogByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cardlinks/{token}/catalog/{catalog_id}")
    def get_cardlink_catalog_by_id(self, token: str, catalog_id: int) -> requests.Response:
        response = self._call(
            "GET",
            url=self.endpoints.get_cardlink_catalog_by_id_endpoint.format(
                token=token,
                catalog_id=int(catalog_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND), (
            f"Expected 200/204/404, got {response.status_code}: {response.text}"
        )
        return response

    @allure.step("GET /cardlinks/{token}/catalog/{catalog_id} without auth")
    def get_cardlink_catalog_by_id_without_auth(self, token: str, catalog_id: int) -> requests.Response:
        response = self._call(
            "GET",
            url=self.endpoints.get_cardlink_catalog_by_id_endpoint.format(
                token=token,
                catalog_id=int(catalog_id),
            ),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN, HTTPStatus.CONFLICT), (
            f"Expected 401/403/409, got {response.status_code}: {response.text}"
        )
        return response
