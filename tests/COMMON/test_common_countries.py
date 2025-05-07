import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonCountries(BaseTest):

    @allure.title('Test get list countries. Range: Items=1-5.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25687")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25687)
    def test_get_list_countries_range_1_5(self):
        self.api_common_countries.get_list_countries_range_1_5()
