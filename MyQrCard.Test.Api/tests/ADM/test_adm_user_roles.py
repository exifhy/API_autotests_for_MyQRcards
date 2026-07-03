import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature(
    "The administration service provides methods for working with users, "
    "tenant, tenant creation requests, permissions, roles, etc."
)
class TestAdmUserRoles(BaseTest):

    @allure.title('Test add roles to a user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23170")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23170)
    def test_post_add_roles_to_user(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_roles = self.api_adm_roles.get_list_roles_undeleted()
        self.api_adm_user_roles.post_add_roles_to_user(
            model_user.userID,
            model_roles.results[0].id
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title("Test delete user's roles.")
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23171")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23171)
    def test_delete_users_roles(self):
        model_user = self.api_adm_users.post_add_user_customer()
        model_roles = self.api_adm_roles.get_list_roles_undeleted()
        self.api_adm_user_roles.post_add_roles_to_user(
            model_user.userID,
            model_roles.results[0].id
        )
        self.api_adm_user_roles.delete_users_roles(
            model_user.userID,
            model_roles.results[0].id
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)
