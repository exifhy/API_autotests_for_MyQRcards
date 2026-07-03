import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmPermissionsUI(BaseTest):

    @allure.title('Test get list permissions UI.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25854")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25854)
    def test_get_list_permissions_ui(self):
        self.api_adm_permissions_ui.get_list_permissions_ui()

    @allure.title('Test delete permission UI by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25856")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25856)
    def test_delete_permissions_ui_by_id(self):
        model_permission = self.api_adm_permissions_ui.post_add_permission_ui()
        self.api_adm_permissions_ui.delete_permissions_ui_by_id(model_permission.results[0])

    @allure.title('Test get permission UI by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25857")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25857)
    def test_get_permission_ui_by_id(self):
        model_permission = self.api_adm_permissions_ui.post_add_permission_ui()
        self.api_adm_permissions_ui.get_permission_ui_by_id(model_permission.results[0])
        self.api_adm_permissions_ui.delete_permissions_ui_by_list(model_permission.results[0])

    @allure.title('Test add permission UI.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25858")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25858)
    def test_post_add_permission_ui(self):
        model_permission = self.api_adm_permissions_ui.post_add_permission_ui()
        self.api_adm_permissions_ui.delete_permissions_ui_by_list(model_permission.results[0])

    @allure.title('Test update permission UI.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25859")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25859)
    def test_put_update_permission_ui(self):
        model_permission = self.api_adm_permissions_ui.post_add_permission_ui()
        self.api_adm_permissions_ui.put_update_permission_ui(model_permission.results[0])
        self.api_adm_permissions_ui.delete_permissions_ui_by_id(model_permission.results[0])

    @allure.title('Test delete permissions UI by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25861")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25861)
    def test_delete_permissions_ui_by_list(self):
        model_permission = self.api_adm_permissions_ui.post_add_three_permissions_ui()
        self.api_adm_permissions_ui.delete_permissions_ui_by_list(
            model_permission.results[0],
            model_permission.results[1],
            model_permission.results[2]
        )

