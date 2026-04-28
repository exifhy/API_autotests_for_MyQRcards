import allure
import pytest
from http import HTTPStatus

from services.powerbi_reports.powerbi_report_by_id.api_powerbi_report_by_id import PowerBIReportByIdAPI
from services.powerbi_reports.powerbi_reports_list.api_powerbi_reports_list import PowerBIReportsListAPI


@allure.epic("API")
@allure.feature("PowerBIReports")
@pytest.mark.api
@allure.description(
    """
    GET /powerbireports/{id}
    """
)
class TestPowerBIReportById:
    @allure.title("GET /powerbireports/ -> GET /powerbireports/{id}")
    def test_powerbi_report_by_id_200(self):
        with allure.step("GET /powerbireports/ — get first report id"):
            _, reports = PowerBIReportsListAPI().get_powerbi_reports()

        if not reports.items:
            pytest.skip("No PowerBI reports available in this environment")

        report_id = reports.items[0].id
        assert report_id is not None, "First report has no id"

        with allure.step(f"GET /powerbireports/{report_id}"):
            response, model = PowerBIReportByIdAPI().get_powerbi_report_by_id(report_id)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
        if model is not None:
            assert model.id == report_id

    @pytest.mark.ng
    @allure.title("GET /powerbireports/{id} without auth -> 401/403")
    def test_powerbi_report_by_id_401_without_auth(self):
        response = PowerBIReportByIdAPI().get_powerbi_report_by_id_without_auth(1)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
