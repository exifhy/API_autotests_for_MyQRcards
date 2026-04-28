import allure
import pytest
from http import HTTPStatus

from services.exports.exports_statistic.api_exports_statistic import ExportsStatisticAPI
from services.exports.exports_statistic.payloads import Payloads


@allure.epic("API")
@allure.feature("Exports")
@pytest.mark.api
@pytest.mark.export
@allure.description(
    """
    /Exports
    """
)
class TestExportsStatistic:
    @allure.title("GET /Exports returns 200")
    @pytest.mark.smoke
    def test_exports_statistic_200(self):
        params = Payloads.build_exports_statistic_params()
        response, model = ExportsStatisticAPI().get_exports_statistic(params)

        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert model.content_type
        assert (
            "spreadsheetml" in model.content_type.lower()
            or "octet-stream" in model.content_type.lower()
            or "application/json" in model.content_type.lower()
        ), f"Unexpected content-type: {model.content_type}"
        assert model.is_xlsx, "Expected XLSX content from /Exports"

    @allure.title("GET /Exports without auth")
    @pytest.mark.ng
    def test_exports_statistic_401_without_auth(self):
        params = Payloads.build_exports_statistic_params()
        response = ExportsStatisticAPI().get_exports_statistic_without_auth(params)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
