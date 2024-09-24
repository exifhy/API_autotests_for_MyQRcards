from config.base_test import BaseTest
import allure
import pytest
from src.enums.params_enums import Params


@allure.epic("Administration")
@allure.feature("Authentication and authorization")
class TestAuthPasswords(BaseTest):

    @allure.title('Test changes the account password.')
    @allure.testcase("https://dev.azure.com/melston/HubEx/_workitems/edit/23411")
    @pytest.mark.regress
    @pytest.mark.parametrize('params_password', Params.params_auth_change_passwords.value)
    def test_post_change_password(self, params_password):
        self.api_auth_passwords.post_change_password(params=params_password)
        