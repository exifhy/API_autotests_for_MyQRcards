import allure
import pytest
from http import HTTPStatus

from services.companies.company_update.api_company_update import CompanyUpdateAPI
from services.companies.company_update.payloads import Payloads
from tests.api.companies.helpers import assert_company_matches_payload, wait_company_matches


@allure.epic("API")
@allure.feature("Companies")
@pytest.mark.api
@pytest.mark.company
@allure.description(
    """
    /Companies
    """
)
class TestCompanyCreateUpdateGetDeleteFlow:
    @allure.title("POST /Companies -> PUT /Companies/{id} -> GET /Companies/{id} -> DELETE /Companies/{id}")
    @pytest.mark.smoke
    def test_company_create_update_get_delete_flow(self, created_company):
        created_company_id = created_company["id"]
        update_payload = Payloads.build_company_update_payload()

        update_response = CompanyUpdateAPI().update_company(created_company_id, update_payload)
        assert update_response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

        model = wait_company_matches(created_company_id, update_payload)
        assert model is not None, (
            f"GET /Companies/{created_company_id} did not return updated data in time"
        )
        assert_company_matches_payload(model, update_payload, company_id=created_company_id)
