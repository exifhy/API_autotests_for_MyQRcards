import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonBanks(BaseTest):

    @allure.title('Test get list banks.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24243")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24243)
    def test_get_list_banks(self):
        self.api_common_banks.get_list_banks()

    @allure.title('Test get info bank by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/24244")
    @pytest.mark.regress
    @pytest.mark.test_case_id(24244)
    def test_get_bank_by_id(self):
        bank_id = self.api_common_banks.get_list_banks_return_first_id()
        self.api_common_banks.get_info_bank_by_id(bank_id)
