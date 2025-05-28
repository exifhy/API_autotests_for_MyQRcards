import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Users management")
class TestAdmUsers(BaseTest):

    @allure.title('Test add new user customer.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23168")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23168)
    def test_post_add_user_customer(self):
        self.api_adm_users.post_add_user_customer()

    @allure.title('Test add new user staff.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23169")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23169)
    def test_post_add_user_staff(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get list users info.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23272")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23272)
    def test_get_list_users_info(self):
        self.api_adm_users.get_list_users_info()

    @allure.title('Test get detail user info by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23185")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23185)
    def test_get_user_info_by_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.get_user_info_by_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test update user by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23286")
    @pytest.mark.smoke
    @pytest.mark.test_case_id(23286)
    def test_put_update_user_by_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_info_user = self.api_adm_users.get_user_info_by_id(model_user.userID)
        self.api_adm_users.put_update_user_by_id(
            user_id=model_user.userID,
            user_email=model_info_user.email,
            user_phone=model_info_user.mobilePhone
        )
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get users roles by id.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23554")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23554)
    def test_get_users_roles_by_id(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_roles = self.api_adm_roles.get_list_roles_undeleted()
        self.api_adm_user_roles.post_add_roles_to_user(model_user.userID, model_roles.results[0].id)
        self.api_adm_users.get_users_roles_by_id(model_user.userID)
        self.api_adm_users.delete_user_by_id(model_user.userID)

    @allure.title('Test get a list asset queries to the current user.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23883")
    @pytest.mark.regress
    @pytest.mark.test_case_id(23883)
    def test_get_list_asset_queries_to_current_user(self, bearer_token):
        self.api_adm_users.get_list_asset_queries_to_current_user(bearer_token)

    @allure.title('Test delete users by list.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/")
    @pytest.mark.regress
    @pytest.mark.test_case_id()
    def test_delete_users_by_list(self):
        model_user = self.api_adm_users.post_add_user_staff()
        model_user2 = self.api_adm_users.post_add_user_staff()
        model_user3 = self.api_adm_users.post_add_user_staff()
        self.api_adm_users.delete_users_by_list(
            model_user.userID,
            model_user2.userID,
            model_user3.userID,
        )
