import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "Enterprise structure service offers various methods for managing assets and their corresponding attributes."
)
class TestEsCompanyRegistrationTypes(BaseTest):

    @allure.title('Test get company registration types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24279")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24279)
    def test_get_company_registration_types(self):
        self.api_es_company_registration_types.get_company_registration_types()
