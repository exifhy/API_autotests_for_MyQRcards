import allure
import pytest
from http import HTTPStatus

from services.fonts.fonts_list.api_fonts_list import FontsListAPI


@allure.epic("API")
@allure.feature("Fonts")
@pytest.mark.api
@allure.description(
    """
    GET /fonts (401, REQUIREMENT 30986)
    Справочник шрифтов — используется для FontStyleID в Cards/DesignSetting/Merge.
    """
)
class TestFontsList:
    @allure.title("GET /fonts returns list")
    @pytest.mark.smoke
    def test_fonts_list_200(self):
        model = FontsListAPI().get_fonts()

        assert isinstance(model.items, list)
        assert model.items, "Expected non-empty fonts list"
        for item in model.items:
            assert item.id is not None
            assert item.displayName
            assert item.fontFamily
            assert item.url

    @allure.title("GET /fonts without auth")
    @pytest.mark.ng
    def test_fonts_list_401_without_auth(self):
        response = FontsListAPI().get_fonts_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
