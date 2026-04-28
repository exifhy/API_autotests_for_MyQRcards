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
    GET /VirtualBackgrounds
    """
)
class TestVirtualBackgroundsList:
    @allure.title("GET /VirtualBackgrounds returns list")
    def test_virtual_backgrounds_list_200(self):
        response, model = VirtualBackgroundsAPI().get_virtual_backgrounds(offset=0, fetch=20)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)

    @allure.title("GET /VirtualBackgrounds without auth")
    @pytest.mark.ng
    def test_virtual_backgrounds_list_401_without_auth(self):
        response = VirtualBackgroundsAPI().get_virtual_backgrounds_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
