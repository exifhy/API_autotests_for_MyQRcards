import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmPermissionsApi(BaseTest):

    @allure.title('Test get list permissions api.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25835")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25835)
    def test_get_list_permissions_api(self):
        self.api_adm_permissions_api.get_list_permissions_api()
