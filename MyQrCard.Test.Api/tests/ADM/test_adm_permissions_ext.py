import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmPermissionsExtTags(BaseTest):

    @allure.title('Test get list permissions ext.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25833")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25833)
    def test_get_list_permissions_ext(self):
        self.api_adm_permissions_ext.get_list_permissions_ext()
