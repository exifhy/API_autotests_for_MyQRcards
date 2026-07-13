import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmPermissionApiTags(BaseTest):

    @allure.title('Test get list permission api tags.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25828")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25828)
    def test_get_list_permission_api_tags(self):
        self.api_adm_permission_api_tags.get_list_permission_api_tags()
