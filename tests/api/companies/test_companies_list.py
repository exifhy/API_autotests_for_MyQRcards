import allure
import pytest
from http import HTTPStatus

from services.companies.companies_list.api_companies_list import CompaniesListAPI
from tests.api.companies.helpers import assert_companies_list_model


@allure.epic("API")
@allure.feature("Companies")
@pytest.mark.api
@pytest.mark.company
@allure.description(
    """
    /Companies
    """
)
class TestCompaniesList:
    @allure.title("GET /Companies returns companies list")
    @pytest.mark.smoke
    def test_companies_list_200_or_206(self):
        response, model = CompaniesListAPI().get_companies(range_header="items=0-199")

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get("Content-Range") or response.headers.get("content-range")
            assert content_range, "Expected Content-Range header for 206 response"

        assert_companies_list_model(model)

    @allure.title("GET /Companies supports searchText query")
    def test_companies_list_with_search_text(self):
        response, model = CompaniesListAPI().get_companies(search_text="test", fetch=50, offset=0)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, list)

    @allure.title("GET /Companies without auth")
    @pytest.mark.ng
    def test_companies_list_401_without_auth(self):
        response = CompaniesListAPI().get_companies_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
