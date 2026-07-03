import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmCapabilities(BaseTest):

    @allure.title('Test get list capabilities.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25758")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25758)
    def test_get_list_capabilities(self):
        self.api_adm_capabilities.get_list_capabilities()
