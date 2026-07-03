import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmRolePermissionsUi(BaseTest):

    @allure.title('Test add role permissions Ui.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25900")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25900)
    def test_post_role_permissions_ui(self):
        model_permissions_ui = self.api_adm_permissions_ui.get_list_permissions_ui()
        model_capability = self.api_adm_capabilities.get_list_capabilities()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_permissions_ui.post_role_permissions_ui(
            model_role.results[0],
            next(iter(model_capability.root)),
            next(iter(model_permissions_ui.root))
        )
        self.api_adm_roles.delete_role_by_id(model_role.results[0])

    @allure.title('Test delete role permissions Ui.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25901")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25901)
    def test_delete_role_permissions_ui(self):
        model_permissions_ui = self.api_adm_permissions_ui.get_list_permissions_ui()
        model_capability = self.api_adm_capabilities.get_list_capabilities()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_permissions_ui.post_role_permissions_ui(
            model_role.results[0],
            next(iter(model_capability.root)),
            next(iter(model_permissions_ui.root))
        )
        self.api_adm_role_permissions_ui.delete_role_permissions_ui(
            model_role.results[0],
            next(iter(model_capability.root)),
            next(iter(model_permissions_ui.root))
        )
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
