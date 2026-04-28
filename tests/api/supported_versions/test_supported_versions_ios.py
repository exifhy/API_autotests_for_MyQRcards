import allure
import pytest
from http import HTTPStatus

from services.supported_versions.ios_supported_versions.api_supported_versions_ios import (
    SupportedVersionsIosAPI,
)


@allure.epic("API")
@allure.feature("SupportedVersions")
@pytest.mark.api
@allure.description(
    """
    /SupportedVersions/ios
    """
)
class TestSupportedVersionsIos:
    @allure.title("GET /SupportedVersions/ios returns supported versions")
    @pytest.mark.smoke
    def test_supported_versions_ios_200(self):
        response, model = SupportedVersionsIosAPI().get_supported_versions_ios()

        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert model.supportedIosVersion != ""
