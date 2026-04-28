from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.exports.exports_employment.endpoints import Endpoints
from services.exports.exports_employment.models.exports_employment_model import (
    ExportsEmploymentModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class ExportsEmploymentAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @staticmethod
    def _headers() -> dict:
        headers = Headers.auth_header(bearer_token=get_token())
        headers.pop("Content-Type", None)
        headers["Accept"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        headers["Accept-Language"] = "ru-RU"
        headers["User-Agent"] = "PostmanRuntime/7.51.0"
        if headers.get("X-APPLICATION-ID"):
            headers["X-Aplication-ID"] = headers.pop("X-APPLICATION-ID")
        return headers

    @allure.step("GET /Exports/employment")
    def get_exports_employment(self, params: dict) -> tuple[requests.Response, ExportsEmploymentModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_exports_employment_endpoint,
            headers=self._headers(),
            params=params,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        content_type = response.headers.get("Content-Type") or response.headers.get("content-type") or ""
        content_disposition = response.headers.get("Content-Disposition") or response.headers.get("content-disposition") or ""
        is_xlsx = response.content.startswith(b"PK")
        return response, ExportsEmploymentModel(
            content_type=content_type,
            content_disposition=content_disposition,
            is_xlsx=is_xlsx,
        )

    @allure.step("GET /Exports/employment without auth")
    def get_exports_employment_without_auth(self, params: dict):
        headers = Headers.without_authorization_field_header()
        headers.pop("Content-Type", None)
        headers["Accept"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response = self._call(
            "GET",
            url=self.endpoints.get_exports_employment_endpoint,
            headers=headers,
            params=params,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response

