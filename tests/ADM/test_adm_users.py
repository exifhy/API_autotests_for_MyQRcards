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
        self.api_adm_users.post_add_user_staff()

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
