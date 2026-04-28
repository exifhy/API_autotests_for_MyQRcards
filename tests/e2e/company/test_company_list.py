import allure
import pytest
from http import HTTPStatus

from services.companies.companies_list.api_companies_list import CompaniesListAPI


@allure.epic("LK")
@allure.feature("Company")
@allure.title("Companies list is available")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.company
@pytest.mark.e2e
def test_company_list_returns_200_and_list(lk_api):
    with allure.step("GET /companies"):
        response, model = CompaniesListAPI().get_companies()

    with allure.step("Check status code = 200"):
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"GET /companies failed: {response.status_code} {response.text}"
        )

    with allure.step("Check response body is a non-empty list"):
        assert isinstance(model.items, list)
        assert len(model.items) > 0, "Companies list is empty"
