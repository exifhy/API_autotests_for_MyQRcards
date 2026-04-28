from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.exports.exports_statistic.endpoints import Endpoints
from services.exports.exports_statistic.models.exports_statistic_model import (
    ExportsStatisticModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class ExportsStatisticAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Exports")
    def get_exports_statistic(self, params: dict) -> tuple[requests.Response, ExportsStatisticModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_exports_statistic_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            params=params,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        content_type = response.headers.get("Content-Type") or response.headers.get("content-type") or ""
        content_disposition = response.headers.get("Content-Disposition") or response.headers.get("content-disposition") or ""
        is_xlsx = response.content.startswith(b"PK")
        return response, ExportsStatisticModel(
            content_type=content_type,
            content_disposition=content_disposition,
            is_xlsx=is_xlsx,
        )

    @allure.step("GET /Exports without auth")
    def get_exports_statistic_without_auth(self, params: dict):
        response = self._call(
            "GET",
            url=self.endpoints.get_exports_statistic_endpoint,
            headers=Headers.without_authorization_field_header(),
            params=params,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
