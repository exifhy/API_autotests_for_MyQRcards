import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmSystemPermissionUiTags(BaseTest):

    @allure.title('Test get system permission Ui tags.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25904")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25904)
    def test_get_system_permission_ui_tags(self):
        self.api_system_permission_ui_tags.get_list_system_permission_ui_tags()
