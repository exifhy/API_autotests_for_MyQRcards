import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmRolePermissionsAPI(BaseTest):

    @allure.title('Test add role permissions API.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25890")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25890)
    def test_post_role_permissions_api(self):
        model_permissions_api = self.api_adm_permissions_api.get_list_permissions_api()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_permissions_api.post_role_permissions_api(
            model_role.results[0],
            next(iter(model_permissions_api.root))
        )
        self.api_adm_roles.delete_role_by_id(model_role.results[0])

    @allure.title('Test delete role permissions API.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25891")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25891)
    def test_delete_role_permissions_api(self):
        model_permissions_api = self.api_adm_permissions_api.get_list_permissions_api()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_permissions_api.post_role_permissions_api(
            model_role.results[0],
            next(iter(model_permissions_api.root))
        )
        self.api_adm_role_permissions_api.delete_role_permissions_api(
            model_role.results[0],
            next(iter(model_permissions_api.root))
        )
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
