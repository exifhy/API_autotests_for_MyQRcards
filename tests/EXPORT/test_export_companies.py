import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Data Export Service")
@allure.feature("Export companies data")
class TestExportCompanies(BaseTest):

    @allure.title('Test exports the list of companies taking into account the specified filters.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23189")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23189)
    def test_get_export_list_companies(self):
        self.api_export_companies.get_export_list_companies()
