import allure
import pytest
from http import HTTPStatus

from services.powerbi_reports.powerbi_reports_list.api_powerbi_reports_list import PowerBIReportsListAPI


@allure.epic("API")
@allure.feature("PowerBIReports")
@pytest.mark.api
@pytest.mark.smoke
@allure.description(
    """
    GET /powerbireports/
    """
)
class TestPowerBIReportsList:
    @allure.title("GET /powerbireports/ -> 200/204")
    def test_powerbi_reports_list_200(self):
        response, model = PowerBIReportsListAPI().get_powerbi_reports()

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        assert isinstance(model.items, list)

    @pytest.mark.ng
    @allure.title("GET /powerbireports/ without auth -> 401/403")
    def test_powerbi_reports_list_401_without_auth(self):
        response = PowerBIReportsListAPI().get_powerbi_reports_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
