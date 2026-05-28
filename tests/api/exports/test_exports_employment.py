import allure
import pytest
from http import HTTPStatus

from services.exports.exports_employment.api_exports_employment import ExportsEmploymentAPI
from services.exports.exports_employment.payloads import Payloads


@allure.epic("API")
@allure.feature("Exports")
@pytest.mark.api
@pytest.mark.export
@allure.description(
    """
    /Exports/employment
    """
)
class TestExportsEmployment:
    @allure.title("GET /Exports/employment returns XLSX for noData=true")
    @pytest.mark.smoke
    def test_exports_employment_no_data_true_200(self):
        params = Payloads.build_exports_employment_params(no_data=True)
        response, model = ExportsEmploymentAPI().get_exports_employment(params)

        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert model.content_type
        assert (
            "spreadsheetml" in model.content_type.lower()
            or "octet-stream" in model.content_type.lower()
        ), f"Unexpected content-type: {model.content_type}"
        assert model.is_xlsx, "Expected XLSX content from /Exports/employment"

    @allure.title("GET /Exports/employment without auth")
    @pytest.mark.ng
    def test_exports_employment_401_without_auth(self):
        params = Payloads.build_exports_employment_params(no_data=True)
        response = ExportsEmploymentAPI().get_exports_employment_without_auth(params)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
