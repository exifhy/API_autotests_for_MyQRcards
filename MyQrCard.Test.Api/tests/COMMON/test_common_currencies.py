import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonCurrencies(BaseTest):

    @allure.title('Test get list currencies. Range: Items=1-5.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25689")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25689)
    def test_get_list_currencies_range_1_5(self):
        self.api_common_currencies.get_list_currencies_range_1_5()
