import allure
import pytest
from http import HTTPStatus

from services.applications.applications_list.api_applications_list import ApplicationsListAPI


@allure.epic("API")
@allure.feature("Applications")
@pytest.mark.api
@allure.description(
    """
    /Applications
    """
)
class TestApplicationsList:
    @allure.title("GET /Applications returns applications list")
    @pytest.mark.smoke
    def test_applications_list_200_or_206(self):
        response, model = ApplicationsListAPI().get_applications(range_header="items=0-199")

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "Expected Content-Range header for 206 response"

        assert isinstance(model.items, list)
        assert model.items, "Applications list is empty"
        assert model.items[0].id is not None
        assert model.items[0].code is None or model.items[0].code != ""

    @allure.title("GET /Applications supports offset/fetch query")
    def test_applications_list_with_paging_query(self):
        response, model = ApplicationsListAPI().get_applications(offset=0, fetch=50)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, list)

    @allure.title("GET /Applications without auth")
    @pytest.mark.ng
    def test_applications_list_401_without_auth(self):
        response = ApplicationsListAPI().get_applications_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
