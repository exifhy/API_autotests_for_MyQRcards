import allure
import pytest
from config.base_test import BaseTest


@allure.epic("Administration")
@allure.feature("Users management")
class TestAdmUsers(BaseTest):

    @allure.title('Test add new user customer.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23168")
    @pytest.mark.smoke
    def test_post_add_user_customer(self):
        self.api_adm_users.post_add_user_customer()

    @allure.title('Test add new user staff.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23169")
    @pytest.mark.smoke
    def test_post_add_user_staff(self):
        self.api_adm_users.post_add_user_staff()
