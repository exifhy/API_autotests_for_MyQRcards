import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Service offers application programming interface for manipulation personnel and all connected entities."
)
class TestPaEmployment(BaseTest):

    @allure.title('Test add employment to user by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23178")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23178)
    def test_post_add_user_employment_by_id(self):
        user_model = self.api_adm_users.post_add_user_customer()
        created_company_id = self.api_es_companies.post_add_our_company()
        company_model = self.api_es_companies.get_detailed_information_on_company_by_id(created_company_id)
        self.api_pa_employment.post_add_user_employment_by_id(
            user_id=user_model.userID,
            customer_org_unit_id=company_model.customerOrgUnit.id
        )
        self.api_es_companies.delete_company_by_id(company_id=created_company_id)
        self.api_adm_users.delete_user_by_id(user_model.userID)
