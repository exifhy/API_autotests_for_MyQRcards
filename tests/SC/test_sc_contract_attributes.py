import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Service Contracts management service")
class TestScServiceContract(BaseTest):

    @allure.title('Test method of get the total number of service contracts.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23582")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23582)
    def test_head_method_total_count_of_contract(self):
        self.api_sc_service_contract.head_method_total_count_of_contract()
