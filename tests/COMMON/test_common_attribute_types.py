import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Common service offers various methods for managing common and auxiliary dictionaries.")
class TestCommonAttributeTypes(BaseTest):

    @allure.title('Test get list attribute types.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25684")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25684)
    def test_get_list_attribute_types(self):
        self.api_common_attribute_types.get_list_attribute_types()

    @allure.title('Test get list attribute types V2.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25685")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25685)
    def test_get_list_attribute_types_v2(self):
        self.api_common_attribute_types.get_list_attribute_types_v2()
