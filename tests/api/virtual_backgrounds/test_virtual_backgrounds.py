import allure
import pytest
from http import HTTPStatus

from services.virtual_backgrounds.virtual_backgrounds_list.api_virtual_backgrounds import (
    VirtualBackgroundsAPI,
)


@allure.epic("API")
@allure.feature("VirtualBackgrounds")
@pytest.mark.api
@allure.description(
    """
    /VirtualBackgrounds
    """
)
class TestVirtualBackgrounds:
    @allure.title("GET /VirtualBackgrounds returns backgrounds list")
    @pytest.mark.smoke
    def test_virtual_backgrounds_200_or_206(self):
        response, model = VirtualBackgroundsAPI().get_virtual_backgrounds(range_header="items=0-199")

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "Expected Content-Range header for 206 response"

        assert isinstance(model.items, list)
        if model.items:
            assert model.items[0].id is not None
            assert model.items[0].name is None or model.items[0].name != ""

    @allure.title("GET /VirtualBackgrounds supports offset/fetch query")
    def test_virtual_backgrounds_with_paging_query(self):
        response, model = VirtualBackgroundsAPI().get_virtual_backgrounds(offset=0, fetch=50)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, list)

    @allure.title("GET /VirtualBackgrounds without auth")
    @pytest.mark.ng
    def test_virtual_backgrounds_401_without_auth(self):
        response = VirtualBackgroundsAPI().get_virtual_backgrounds_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
