from http import HTTPStatus

import allure
import requests

from services.supported_versions.android_supported_versions.endpoints import Endpoints
from services.supported_versions.android_supported_versions.models.supported_versions_android_model import (
    SupportedVersionsAndroidModel,
)
from src.support.helper import Helper


class SupportedVersionsAndroidAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /SupportedVersions/android")
    def get_supported_versions_android(self) -> tuple[requests.Response, SupportedVersionsAndroidModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_supported_versions_android_endpoint,
            headers={"Accept": "application/json"},
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else ""
        assert isinstance(data, str), f"Expected string, got {type(data)} / {data}"
        return response, SupportedVersionsAndroidModel(supportedAndroidVersion=data)

