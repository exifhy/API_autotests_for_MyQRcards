import allure
import pytest
from http import HTTPStatus

from services.companies.company_designsettings_update.api_company_designsettings_update import (
    CompanyDesignsettingsUpdateAPI,
)
from services.companies.company_designsettings_update.payloads import Payloads
from tests.api.companies.helpers import (
    assert_company_designsettings_match,
    wait_company_designsettings_by_id,
)


@allure.epic("API")
@allure.feature("Companies")
@pytest.mark.api
@pytest.mark.company
@allure.description(
    """
    /Companies/{companyID}/designsettings
    """
)
class TestCompanyDesignsettingsFlow:
    @allure.title("POST /Companies -> PUT designsettings -> GET designsettings -> DELETE /Companies/{id}")
    @pytest.mark.smoke
    def test_company_designsettings_flow(self, created_company):
        created_company_id = created_company["id"]
        design_payload = Payloads.build_company_designsettings_payload()

        response = CompanyDesignsettingsUpdateAPI().update_company_designsettings(
            created_company_id,
            design_payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

        model = wait_company_designsettings_by_id(created_company_id)
        assert model is not None, (
            f"GET /Companies/{created_company_id}/designsettings did not return 200 in time"
        )
        assert_company_designsettings_match(model, design_payload, company_id=created_company_id)
