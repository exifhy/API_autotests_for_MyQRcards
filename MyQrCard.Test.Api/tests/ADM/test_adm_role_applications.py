import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmRoleApplications(BaseTest):

    @allure.title('Test add role applications.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25887")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25887)
    def test_post_role_applications(self):
        model_app = self.api_common_applications.get_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_applications.post_role_applications(
            model_role.results[0],
            next(iter(model_app.root))
        )
        self.api_adm_roles.delete_role_by_id(model_role.results[0])

    @allure.title('Test delete role applications.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25888")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25888)
    def test_delete_role_applications(self):
        model_app = self.api_common_applications.get_list_applications()
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_role_applications.post_role_applications(
            model_role.results[0],
            next(iter(model_app.root))
        )
        self.api_adm_role_applications.delete_role_applications(
            model_role.results[0],
            next(iter(model_app.root))
        )
        self.api_adm_roles.delete_role_by_id(model_role.results[0])
