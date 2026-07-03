import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmRolePermissionsExt(BaseTest):

    @allure.title('Test add role permissions Ext.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25897")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25897)
    def test_post_role_permissions_ext(self):
        model_permissions_ext = self.api_adm_permissions_ext.get_list_permissions_ext()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_permissions_ext.post_role_permissions_ext(
            model_role.results[0],
            next(iter(model_permissions_ext.root))
        )
        self.api_adm_roles.delete_role_by_id(model_role.results[0])

    @allure.title('Test delete role permissions Ext.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25898")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25898)
    def test_delete_role_permissions_ext(self):
        model_permissions_ext = self.api_adm_permissions_ext.get_list_permissions_ext()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_permissions_ext.post_role_permissions_ext(
            model_role.results[0],
            next(iter(model_permissions_ext.root))
        )
        self.api_adm_role_permissions_ext.delete_role_permissions_ext(
            model_role.results[0],
            next(iter(model_permissions_ext.root))
        )
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
