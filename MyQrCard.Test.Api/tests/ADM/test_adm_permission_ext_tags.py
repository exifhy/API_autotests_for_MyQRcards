import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmPermissionExtTags(BaseTest):

    @allure.title('Test get list permission ext tags.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25831")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25831)
    def test_get_list_permission_ext_tags(self):
        self.api_adm_permission_ext_tags.get_list_permission_ext_tags()
