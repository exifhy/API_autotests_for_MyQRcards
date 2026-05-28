import allure
import pytest
from http import HTTPStatus

from services.supported_versions.android_supported_versions.api_supported_versions_android import (
    SupportedVersionsAndroidAPI,
)


@allure.epic("API")
@allure.feature("SupportedVersions")
@pytest.mark.api
@allure.description(
    """
    /SupportedVersions/android
    """
)
class TestSupportedVersionsAndroid:
    @allure.title("GET /SupportedVersions/android returns supported version")
    @pytest.mark.smoke
    def test_supported_versions_android_200(self):
        response, model = SupportedVersionsAndroidAPI().get_supported_versions_android()

        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert model.supportedAndroidVersion != ""
