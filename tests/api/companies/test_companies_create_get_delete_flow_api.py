import allure
import pytest

from tests.api.companies.helpers import assert_company_matches_payload, wait_company_by_id


@allure.epic("API")
@allure.feature("Companies")
@pytest.mark.api
@pytest.mark.company
@allure.description(
    """
    /Companies
    """
)
class TestCompanyCreateGetDeleteFlow:
    @allure.title("POST /Companies -> GET /Companies/{id} -> DELETE /Companies/{id}")
    @pytest.mark.smoke
    def test_company_create_get_delete_flow(self, created_company):
        created_company_id = created_company["id"]
        payload = created_company["payload"]

        model = wait_company_by_id(created_company_id)
        assert model is not None, f"GET /Companies/{created_company_id} did not return 200 in time"
        assert_company_matches_payload(model, payload, company_id=created_company_id)
