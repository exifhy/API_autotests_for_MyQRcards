import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmRoles(BaseTest):

    @allure.title('Test get list roles.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25776")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25776)
    def test_get_list_roles(self):
        self.api_adm_roles.get_list_roles()

    @allure.title('Test get list applications role by role ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25863")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25863)
    def test_get_list_applications_role_by_role_id(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_list_applications_role_by_role_id(model_role.results[0].id)

    # @allure.title('Test get list attachments role by role ID.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25864")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(25864)
    # @pytest.mark.skip(reason="Ручка отключена.")
    # def test_get_list_attachments_role_by_role_id(self):
    #     model_role = self.api_adm_roles.get_list_roles()
    #     self.api_adm_roles.get_list_attachments_role_by_role_id(model_role.results[0].id)

    @allure.title('Test get role by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25865")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25865)
    def test_get_role_by_id(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_role_by_id(model_role.results[0].id)

    @allure.title('Test delete role by ID.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25866")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25866)
    def test_delete_role_by_id(self):
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_roles.delete_role_by_id(model_role.results[0])

    # @allure.title('Test add role.')
    # @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25867")
    # @pytest.mark.regress
    # @pytest.mark.test_case_id(25867)
    # @pytest.mark.skip(reason="Тест на создание проходит в - test_delete_role_by_id")
    # def test_post_add_role(self):
    #     model_role = self.api_adm_roles.post_add_role()
    #     self.api_adm_roles.delete_roles_by_list(model_role.results[0])

    @allure.title('Test update role.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25869")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25869)
    def test_put_update_role(self):
        model_role = self.api_adm_roles.post_add_role()
        self.api_adm_roles.put_update_role(model_role.results[0])
        self.api_adm_roles.delete_roles_by_list(model_role.results[0])

    @allure.title('Test delete three roles by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25870")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25870)
    def test_delete_roles_by_list(self):
        model_role = self.api_adm_roles.post_add_three_roles()
        self.api_adm_roles.delete_roles_by_list(
            model_role.results[0],
            model_role.results[1],
            model_role.results[2]
        )

    @allure.title('Test copy role.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25871")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25871)
    def test_post_copy_role(self):
        model_role = self.api_adm_roles.get_list_roles()
        model_copy = self.api_adm_roles.post_copy_roles(model_role.results[0].id)
        self.api_adm_roles.delete_roles_by_list(model_copy.results[0])

    @allure.title('Test get list role permissions api')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25872")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25872)
    def test_get_role_permissions_api(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_role_permissions_api(model_role.results[0].id)

    @allure.title('Test get list role permissions ext')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25873")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25873)
    def test_get_role_permissions_ext(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_role_permissions_ext(model_role.results[0].id)

    @allure.title('Test get list role permissions UI')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/25874")
    @pytest.mark.regress
    @pytest.mark.test_case_id(25874)
    def test_get_role_permissions_ui(self):
        model_role = self.api_adm_roles.get_list_roles()
        self.api_adm_roles.get_role_permissions_ui(model_role.results[0].id)
