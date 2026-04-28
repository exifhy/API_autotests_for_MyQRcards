from http import HTTPStatus

import allure
import requests

from services.supported_versions.ios_supported_versions.endpoints import Endpoints
from services.supported_versions.ios_supported_versions.models.supported_versions_ios_model import (
    SupportedVersionsIosModel,
)
from src.support.helper import Helper


class SupportedVersionsIosAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /SupportedVersions/ios")
    def get_supported_versions_ios(self) -> tuple[requests.Response, SupportedVersionsIosModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_supported_versions_ios_endpoint,
            headers={"Accept": "application/json"},
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else ""
        assert isinstance(data, str), f"Expected string, got {type(data)} / {data}"
        return response, SupportedVersionsIosModel(supportedIosVersion=data)
