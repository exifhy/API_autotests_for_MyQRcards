import allure
import pytest
from http import HTTPStatus

from services.cultures.cultures_list.api_cultures_list import CulturesListAPI


@allure.epic("API")
@allure.feature("Cultures")
@pytest.mark.api
@allure.description(
    """
    /Cultures
    """
)
class TestCulturesList:
    @allure.title("GET /Cultures returns cultures list")
    @pytest.mark.smoke
    def test_cultures_list_200_or_206(self):
        response, model = CulturesListAPI().get_cultures(range_header="items=0-199")

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "Expected Content-Range header for 206 response"

        assert isinstance(model.items, list)
        assert model.items, "Cultures list is empty"
        assert model.items[0].id is not None
        assert model.items[0].code is None or model.items[0].code != ""

    @allure.title("GET /Cultures supports offset/fetch query")
    def test_cultures_list_with_paging_query(self):
        response, model = CulturesListAPI().get_cultures(offset=0, fetch=50)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, list)

    @allure.title("GET /Cultures without auth")
    @pytest.mark.ng
    def test_cultures_list_401_without_auth(self):
        response = CulturesListAPI().get_cultures_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
